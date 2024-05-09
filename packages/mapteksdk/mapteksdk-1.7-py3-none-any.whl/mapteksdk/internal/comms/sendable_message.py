"""Base class for messages which define a full MCP message.

Warnings
--------
Vendors and clients should not develop scripts or applications against
this package. The contents may change at any time without warning.
"""
###############################################################################
#
# (C) Copyright 2024, Maptek Pty Ltd. All rights reserved.
#
###############################################################################

import logging
import typing

from ...capi import Mcpd
from .base_message import BaseMessage
from .repeating_fields import MessageWithRepeatingField
from .errors import FailedToCreateMessageError

if typing.TYPE_CHECKING:
  from .factory_protocol import Factory

LOGGER = logging.getLogger('mapteksdk.internal.comms')


class SendableMessage(MessageWithRepeatingField):
  """Base class for messages which define the entire message structure.

  Child classes of this can stand on their own and thus can be sent over the
  MCP.

  Parameters
  ----------
  factory
    Factory to use to construct the message before it can be sent.
  """
  def __init__(self, factory: "Factory") -> None:
    super().__init__()
    self.__factory = factory

  @classmethod
  def message_name(cls) -> str:
    """The name of the message.

    This must be implemented by derived types.
    This must not be empty and it must not contain any :: characters.
    This is used for sending and receiving the message over the communications
    system.
    """
    raise NotImplementedError

  @classmethod
  def receive(cls, received_handle, factory: "Factory") -> "typing.Self":
    """Receive this message from the communications system.

    Parameters
    ----------
    received_handle
      The message handle provided by the communications system.
    factory
      Factory to use to construct the received message.

    Returns
    -------
    Self
      The message received from the message system.
    """
    return factory.get(cls).extract(received_handle)

  @classmethod
  def logger(cls) -> logging.Logger:
    """Logger which should be used by child classes."""
    return LOGGER

  def _create_message(self, mcp: Mcpd, destination: str) -> typing.Any:
    """Create the message.

    Parameters
    ----------
    mcp
      MCP DLL to use to create the message.
    destination
      The name of the server to create the message to be sent to.

    Returns
    -------
    message_handle
      The handle for the newly created message.
    """
    raise NotImplementedError

  def _send_message(
    self,
    mcp: Mcpd,
    message_handle
  ) -> typing.Optional[BaseMessage]:
    """Send the message.

    Parameters
    ----------
    mcp
      MCP DLL to use to send the message. This must be the same as passed
      to _create_message().
    factory
      Factory to use to create the message.
    message_handle
      The message handle returned by _create_message().
    """
    raise NotImplementedError

  @property
  def _factory(self) -> "Factory":
    """The factory used to construct the message before sending."""
    return self.__factory

  def send(
      self,
      destination: str
    ) -> typing.Optional[BaseMessage]:
    """Send this message to the destination.

    Parameters
    ----------
    destination
      The name of the server to send this message to.
    factory
      Factory to use to construct the MCP message.

    Returns
    -------
    Optional[BaseMessage]
      The response to the message if this message expects a response.
      This will be None if this message does not expect a response.
    """
    mcp = Mcpd()

    message_name = self.message_name()
    assert message_name.strip(), 'The name of the message is required.'
    assert '::' not in message_name, 'The name may not contain ::'

    if not destination:
      raise ValueError('No destination specified.')

    self.logger().info('Sending %s to %s', message_name, destination)

    message_handle = self._create_message(mcp, destination)

    if not message_handle.value:
      raise FailedToCreateMessageError(
        "Failed to create the Message. The script may not be connected to the "
        "application or the application may not support messages."
      )

    try:
      sender = self._factory.get(type(self))
      sender.insert(message_handle, self)
    except:
      # Send message includes an implicit call to free message, so this only
      # needs to free the message if there is an error while building the
      # message.
      mcp.FreeMessage(message_handle)
      raise

    return self._send_message(mcp, message_handle)
