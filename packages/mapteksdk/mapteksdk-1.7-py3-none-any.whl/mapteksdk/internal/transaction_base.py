"""Base class for defining transactions for the TransactionManager.

Despite the similar names, this has no relation to anything in transaction.py.

Warnings
--------
Vendors and clients should not develop scripts or applications against
this package. The contents may change at any time without warning.
"""

###############################################################################
#
# (C) Copyright 2023, Maptek Pty Ltd. All rights reserved.
#
###############################################################################
from __future__ import annotations

from contextlib import AbstractContextManager
import dataclasses
import enum
import itertools
import logging
import time
import typing

from .comms import InlineMessage, Int64u, Factory

from .qualifiers import Qualifier, QualifierSet
from .serialisation import Context
from .transaction_errors import (
  TransactionSetUpError,
  TransactionTimeoutError,
  TransactionCancelledError
)
from .transaction_messages import (
  TransactionCreateHeader,
  CompoundTransactionCreateHeader,
  TransactionCreate,
  TransactionDestroy
)
from .transaction_request_data import (
  TransactionRequestData,
  TransactionRequestDataList,
)
from .transaction_state import TransactionState

if typing.TYPE_CHECKING:
  from .transaction_manager import TransactionManager

LOG = logging.getLogger("mapteksdk.internal.transaction_manager")

DATA_GROUP = "mdf::serC_DataGroup"
"""The name of a data group.

This is the default format for transaction data to be sent over the MCP.
"""

NEXT_OPERATION_ID = itertools.count(start=1)
"""Counter used to generate the operation IDs."""

TransactionKey: typing.TypeAlias = typing.Tuple[int, int]


class _CallbackTypes(enum.Enum):
  """Indicates the type of a callback."""
  CONFIRM = 0
  CANCEL = 1


@dataclasses.dataclass
class ServerInformation:
  """Information about server-side representation of a transaction."""
  server_name: str
  """The name of the server."""
  server_address: Int64u
  """The address of the transaction on the server."""


class TransactionBase(AbstractContextManager):
  """Base class for Transactions.

  This contains the functionality shared by elemental and compound
  transactions. Classes should inherit from ElementalTransactionBase or
  CompoundTransactionBase.
  """
  def __init__(
      self,
      manager: "TransactionManager",
      factory: "Factory",
      parent: "typing.Optional[TransactionBase]"=None) -> None:
    self._manager = manager
    """The transaction manager which owns this transaction."""
    self._factory = factory
    """The factory to use to create MCP messages."""
    self._parent = parent
    """The parent transaction.

    If None, this transaction has no parent.
    """
    self._qualifiers: list[Qualifier] = list(self._default_qualifiers())
    """The qualifiers to send with this transaction."""
    self.__token = next(NEXT_OPERATION_ID)
    """The token which uniquely identifies this transaction."""
    self.__callbacks: typing.Dict[
      _CallbackTypes, typing.List[
        typing.Callable[[typing.Self], None]]] = {
          callback_type : [] for callback_type in _CallbackTypes
        }
    """Callbacks to call when a message arrives for this transaction.

    This is a dictionary where the key is the type of message which should
    cause the callbacks to be called and the value is a list of callback
    functions to call after that message is processed.

    Each callback is passed this object as a parameter.
    """
    self.__state: TransactionState = TransactionState.PENDING
    """The current state of the transaction."""
    self.__error: typing.Optional[Exception] = None
    """The error which has caused this to fail."""
    self.__server_information: typing.Optional[ServerInformation] = None
    """Information about the server-side representation of this transaction.

    This is None if the transaction does not have a server side
    representation. This is either because it has not been sent to
    the server or the server-side representation has been destroyed.
    """

  @staticmethod
  def name() -> str:
    """The name of the transaction this data is for.

    This includes the namespace.
    """
    raise NotImplementedError("Must be implemented in child classes.")

  @staticmethod
  def data_type_name() -> str:
    """The name of the data type this transaction accepts.

    This is "mdf::serC_DataGroup" by default, which is what most montages
    use, however child classes may overwrite this if they use a different type.
    """
    return DATA_GROUP

  @classmethod
  def _default_qualifiers(cls) -> typing.Sequence[Qualifier]:
    """The default qualifiers to apply to a newly created object.

    This can be overwritten by child classes to automatically apply
    qualifiers.
    """
    return []

  @staticmethod
  def _default_server_name() -> str:
    """The name of the server to send the transaction to.

    Can be overwritten by base classes. It is the ui server by default.
    """
    return "uiServer"

  @staticmethod
  def __assert_state(
      actual_state: TransactionState,
      expected_state: TransactionState):
    if actual_state != expected_state:
      raise RuntimeError(
        f"This function cannot be called in state: {actual_state}. "
        f"It requires state: {expected_state}"
      )

  @classmethod
  def body_type(cls) -> type[InlineMessage]:
    """The type used to parse / read the body of this message."""
    raise NotImplementedError

  def _generate_create_header(self) -> TransactionCreateHeader:
    """Generate the header for a Transaction create message."""
    raise NotImplementedError("Child classes must define the create header.")

  def _add_qualifier(self, qualifier: Qualifier):
    """Add a qualifier to the transaction.

    This qualifier will be sent with the data.
    """
    self._qualifiers.append(qualifier)

  def _add_qualifiers(self, qualifiers: typing.Iterable[Qualifier]):
    """Add many qualifiers to the Transaction."""
    self._qualifiers.extend(qualifiers)

  def _request_data(self) -> TransactionRequestData:
    data = TransactionRequestData()
    data.class_name = self.name()
    data.data_type_name = self.data_type_name()
    data.transaction_address = id(self)
    data.transaction_token = self.__token
    qualifiers = QualifierSet()
    qualifiers.values = self._qualifiers
    data.qualifiers = qualifiers
    return data

  def _generate_body(self) -> InlineMessage:
    """Generate the body of a message for this transaction.

    This is used to generate the body of TransactionCreate and
    TransactionCancel requests.
    """
    raise NotImplementedError("Must be implemented in child classes.")

  def _read_body(self, message_handle):
    """Read the body of a message for this transaction.

    This should set the classes state appropriately based on the contents
    of the body read from the message handle.
    """
    raise NotImplementedError("Must be implemented in child classes.")

  def key(self) -> TransactionKey:
    """Key which uniquely identifies this transaction (within this process).

    This is used by the transaction manager to determine which transaction
    an event is relevant to.

    Returns
    -------
    tuple
      A tuple containing the id of this Python object and the token
      assigned to this object.
    """
    return (id(self), self.__token)

  def register_confirm_callback(
      self, callback: typing.Callable[[typing.Self], None]):
    """Register a callback to be called when this transaction is confirmed.

    Parameters
    ----------
    callback
      Callback to be called after it is confirmed. This accepts this class.
      The callback will be called after _read_body() is called.
    """
    self.__callbacks[_CallbackTypes.CONFIRM].append(callback)

  def register_cancel_callback(
      self, callback: typing.Callable[[typing.Self], None]):
    """Register a callback to be called when this transaction is cancelled.

    Parameters
    ----------
    callback
      Callback to be called after this is cancelled.
    """
    self.__callbacks[_CallbackTypes.CANCEL].append(callback)

  def send(self, server_name: typing.Optional[str] = None):
    """Send the transaction to the relevant server.

    Parameters
    ----------
    server_name
      Name of the server to send the message to.
      If None, it will be sent to the default server.

    Raises
    ------
    TransactionSetUpError
      If the menu command could not be created on the relevant server.
    """
    if server_name is None:
      server_name = self._default_server_name()
    self.__assert_state(self.__state, TransactionState.PENDING)
    header = self._generate_create_header()
    body = self._generate_body()

    message = TransactionCreate(self._factory)
    message.header = header
    message.body = body

    response = message.send(server_name)
    # pylint: disable=no-member
    # Pylint can't figure out that response is of ResponseType.
    if not response.success:
      raise TransactionSetUpError(self.name())
    self.__server_information = ServerInformation(
      server_name,
      response.server_address
    )
    self.__state = TransactionState.ACTIVE

  def confirm(self, confirm_message_handle):
    """Handle an incoming confirm message.

    Parameters
    ----------
    Message handle for the confirm message. This assumes that the
      transaction address and token have already been extracted
      from the message.
    """
    # This doesn't currently use the context. Read it and discard it
    # so that the next part of the message can be read.
    context_reader = self._factory.get(Context)
    _ = context_reader.extract(confirm_message_handle)
    self._read_body(confirm_message_handle)

    self._confirm()

  def _confirm(self):
    """Internal confirm function.

    This causes the transaction to enter the final state without receiving
    a confirm message. This is primarily intended for child transactions which
    automatically confirm their parent when they are confirmed.
    """
    # Handle callbacks for the confirm.
    try:
      self._call_callbacks(_CallbackTypes.CONFIRM)
    # pylint: disable=broad-exception-caught
    # The error will be re-raised by wait().
    except Exception as error:
      self.__error = error
      self.__state = TransactionState.FAILED
      return

    self.__state = TransactionState.FINAL

  def cancel(self):
    """Cancel this transaction.

    This will destroy the server-side representation as if the user
    had cancelled the transaction in the user interface.
    """
    self.__state = TransactionState.CANCELLED
    self._delete_server_side()
    try:
      self._call_callbacks(_CallbackTypes.CANCEL)
    # pylint: disable=broad-exception-caught
    # The error will be re-raised by wait().
    except Exception as error:
      self.__error = error
      self.__state = TransactionState.FAILED
      return

  def wait(self, timeout: typing.Optional[float]=None):
    """Wait until the transaction is confirmed or cancelled.

    Parameters
    ----------
    timeout
      Time in seconds to wait for a value. If a value is not
      returned in this time, a TransactionTimeoutError will be raised.
    """
    if self._parent:
      raise RuntimeError(
        "Cannot wait for the child of a compound transaction. "
        "To confirm the parent when a child is confirmed, register a confirm "
        "callback on the child."
      )
    if timeout:
      start_time = time.perf_counter()
    try:
      while True:
        result = self._manager.service_events()
        if not result:
          raise TransactionCancelledError(self.name())
        if self.__state != TransactionState.ACTIVE:
          break
        if timeout:
          duration = time.perf_counter() - start_time
          if duration > timeout:
            raise TransactionTimeoutError(self.name(), timeout)
    except OSError as error:
      LOG.exception(error)
      raise
    if self.__state == TransactionState.CANCELLED:
      raise TransactionCancelledError(self.name())
    if self.__error:
      raise self.__error

  def _call_callbacks(self, callback_type: _CallbackTypes):
    """Call all callbacks with the given type."""
    for callback in self.__callbacks[callback_type]:
      callback(self)

  def _delete_server_side(self):
    """Delete the transactions server-side representation.

    This should be called immediately after receiving a response from
    the server to ensure that any UI the server created for the request
    is disposed of quickly.

    It is safe to call this function multiple times.
    """
    information = self.__server_information
    if information is None:
      return
    destroy_request = TransactionDestroy(self._factory)
    # We don't currently support parent transactions, so the parent
    # address is the same as the transaction address.
    destroy_request.parent_transaction_address = information.server_address
    destroy_request.transaction_address = information.server_address
    destroy_request.send(information.server_name)
    self.__server_information = None

  def __enter__(self):
    return self

  def __exit__(self, __exc_type, __exc_value, __traceback):
    self._manager._remove_transaction(self)
    self._delete_server_side()


class ElementalTransactionBase(TransactionBase):
  """Base class for elemental transactions."""
  def __init__(
      self,
      manager: TransactionManager,
      factory: "Factory",
      parent: "typing.Optional[TransactionBase]"=None) -> None:
    super().__init__(manager, factory, parent)
    self._body: InlineMessage = self.body_type()()
    """Backing field for the body of the transaction.

    Child transactions should store the current values in this object rather
    than their own backing field to prevent duplication of values.
    """
    self._initialise_body(self._body)

  @classmethod
  def body_type(cls) -> typing.Type[InlineMessage]:
    raise NotImplementedError("Child classes must define the body type.")

  def _initialise_body(self, body: InlineMessage):
    """Initialise the body of this transaction.

    This will be passed an instance of the type returned by body_type().
    """
    raise NotImplementedError("Child classes must initialise the body.")

  def _generate_create_header(self) -> TransactionCreateHeader:
    """Generate the header for a Transaction create message."""
    header = TransactionCreateHeader()
    header.manager_address = id(self._manager)
    header.request_data = self._request_data()
    return header

  def _read_body(self, message_handle: InlineMessage):
    body_reader = self._factory.get(self.body_type())
    self._body = body_reader.extract(message_handle)

  def _generate_body(self) -> InlineMessage:
    return self._body


class CompoundTransactionBase(TransactionBase):
  """Base class for compound transactions.

  These are transactions which contain other transactions.
  """
  def __init__(
      self,
      manager: "TransactionManager",
      factory: "Factory",
      parent: "typing.Optional[TransactionBase]") -> None:
    self._child_transactions: typing.Dict[
      str, "TransactionBase"] = self.create_child_transactions(manager)
    super().__init__(manager, factory, parent)
    self.initialise_child_transactions()

  @staticmethod
  def child_transaction_types() -> typing.Dict[
      str, typing.Type[TransactionBase]]:
    """Return a dictionary of the types of the child transactions."""
    raise NotImplementedError

  @classmethod
  def body_type(cls) -> "type[InlineMessage]":
    """Body of the MCP message."""
    child_transaction_types = cls.child_transaction_types()
    annotations = {
      name : child.body_type()
      for name, child in child_transaction_types.items()
    }

    return type(f"{cls.__name__}Body", (InlineMessage,), {
      "__annotations__" : annotations
    })

  def initialise_child_transactions(self):
    """Initialise the child transactions.

    This is called at the end of __init__().
    Child classes can implement this to allow for extra setup to be performed
    on their child transactions. By default, this does nothing.
    """

  def create_child_transactions(self, manager: "TransactionManager"
      ) -> typing.Dict[str, "TransactionBase"]:
    """Create the child transactions for a newly created object."""
    def create_child(
        parent: "TransactionBase",
        child_type: "type[TransactionBase]") -> "TransactionBase":
      child = manager.create_transaction(child_type, parent_transaction=parent)
      # When the child is cancelled, also cancel the parent.
      child.register_cancel_callback(lambda _: parent.cancel())
      return child

    return {
      name : create_child(self, child_type)
      for name, child_type in self.child_transaction_types().items()
    }

  def _generate_create_header(self):
    header = CompoundTransactionCreateHeader()
    header.manager_address = id(self._manager)
    header.request_data = self._request_data()
    child_request_data = TransactionRequestDataList()
    # pylint: disable=protected-access
    child_request_data.request_list = [
      child._request_data() for child in self._child_transactions.values()]
    header.child_requests = child_request_data
    return header

  def _read_body(self, message_handle):
    for child in self._child_transactions.values():
      # pylint: disable=protected-access
      child._read_body(message_handle)

  def _generate_body(self) -> InlineMessage:
    body = self.body_type()()
    for name, child in self._child_transactions.items():
      # pylint: disable=protected-access
      setattr(body, name, child._generate_body())
    return body

  def __exit__(self, __exc_type, __exc_value, __traceback):
    for child in self._child_transactions.values():
      self._manager._remove_transaction(child)
      child._delete_server_side()
    self._child_transactions = {}
    super().__exit__(__exc_type, __exc_value, __traceback)
