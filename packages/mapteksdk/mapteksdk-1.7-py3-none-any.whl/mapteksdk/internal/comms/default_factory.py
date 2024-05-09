"""Default factory for MCP messages.

This combines all of the concrete factories defined by the SDK.

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

from ._factories.any_factory import AnyFactory
from ._factories.compound_factory import CompoundFactory
from ._factories.message_factory import MessageFactory
from ._factories.primitive_factory import PrimitiveFactory
from ._factories.repeating_field_factory import RepeatingFieldFactory
from ._factories.serialisable_factory import SerialisableFactory
from ._factories.sequence_factory import SequenceFactory
from ._factories.union_factory import UnionFactory

if typing.TYPE_CHECKING:
  from ...capi import Mcpd
  from .factory_protocol import Factory


def default_factory(mcp: Mcpd) -> Factory:
  """Get the default implementation of the `Factory` protocol.

  The `get()` function of this factory supports:

  * `Message`
  * `Request`
  * `Response`
  * `SubMessage`
  * `InlineMessage`
  * `str`
  * `bool`
  * `SerialisedText`
  * `ReceivedSerialisedText`
  * The integer and float types defined in types.py.
  * The structure types defined in base_message.py.
  * `typing.Any` (Only when inserting into a message).

  Passing any other type will result in a DataTypeNotSupportedError.
  Typically, users of this factory would pass only `Message` and `Request`
  concrete implementations to `get()` to avoid needing to deal with the
  complexities of creating or extracting messages in a piecemeal fashion.
  """
  factory =  CompoundFactory(
    [
      PrimitiveFactory(mcp)
    ]
  )

  # These factories must be added after construction because they
  # require a reference to the factory to use for their contents.
  factory.add_factory(SerialisableFactory(factory))
  factory.add_factory(SequenceFactory(factory, mcp))
  factory.add_factory(RepeatingFieldFactory(factory, mcp))
  factory.add_factory(MessageFactory(factory, mcp))
  factory.add_factory(UnionFactory(factory))
  factory.add_factory(AnyFactory(factory))
  return factory
