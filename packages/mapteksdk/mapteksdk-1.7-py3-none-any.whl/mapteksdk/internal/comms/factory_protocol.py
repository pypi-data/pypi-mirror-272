"""Interface for factories which create message components.

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
from __future__ import annotations

import typing

from ..protocol import Protocol

if typing.TYPE_CHECKING:
  from .message_component_protocol import MessageComponent
  ComponentT = typing.TypeVar("ComponentT")

class Factory(Protocol):
  """Protocol for factories which can create message components.

  The `get()` function can be used to get a concrete implementation of
  `MessageComponent` which can be used to insert/extract values of
  the given type into/from a message. See default_factory() for a full list
  of the types supported by the SDK by default.

  The most common use case for factories is with the Message and Request
  classes. These classes hide the actual usage of the factory within the
  `send()` and `receive()` functions - see the Examples for those classes
  for more details.

  Notes
  -----
  Clients should always deal with factories through the class which implements
  this protocol returned by the `default_factory()` function. The concrete
  implementations of this protocol should be considered internal
  implementation details.
  """
  def supports_type(self, data_type: type) -> bool:
    """True if data_type is supported by this factory."""
    raise NotImplementedError

  def get(self, data_type: type[ComponentT]) -> MessageComponent[ComponentT]:
    """Get an MessageComponent which can handle `data_type`.

    Parameters
    ----------
    data_type
      The data type to return an MessageComponent concrete implementation
      which can insert or extract data of that type from a MCP message.

    Returns
    -------
    MessageComponent
      MessageComponent which can insert or extract data of type data_type
      from a MCP message.

    Raises
    ------
    DataTypeNotSupported
      If there is no MessageComponent class which can handle `data_type`.
    """
    raise NotImplementedError
