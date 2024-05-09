"""The Request class for the comms module.

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

import typing

from .repeating_fields import MessageWithRepeatingField
from .sendable_message import SendableMessage
from ..mcp import McpCallback
from ..util import default_type_error_message


if typing.TYPE_CHECKING:
  from .factory_protocol import Factory
  from ...capi import Mcpd


class Response(MessageWithRepeatingField):
  """Base class for responses to requests."""


class Request(SendableMessage):
  """A MCP message which forms a request that expects a response back.

  This provides special case handling for this scenario. It is often
  possible to mimic this behaviour by listening for a message that forms
  the reply and then sending an message which will elicit the message
  being sent back.

  Warnings
  --------
  If a thread calls `send()` on a `Request` subclass then that thread will
  block until the `Response` to the request arrives. If the `Response` never
  arrives, the thread will block forever. There is currently no mechanism for
  placing a timeout on receiving the response.

  Examples
  --------
  `Request` subclasses are structured the same as message subclasses, except
  that they have an extra `classproperty` which indicates the response type.
  The following example demonstrates a `Request` which sends the
  server a number and receives a `Response` which contains a different number.

  >>> class DoubleMessage(Request):
  ...     class DoubleResponse(Response):
  ...         result: Int64s
  ...
  ...     @classmethod
  ...     def message_name(cls) -> str:
  ...         return "double"
  ...
  ...     @classmethod
  ...     def response_type(cls) -> "type[DoubleResponse]":
  ...         return cls.DoubleResponse
  ...     value: Int64s

  The request can be sent by calling the `send()` function on an instance of
  the `Request` subclass. This will return an instance of the response type:

  >>> message = DoubleMessage(default_factory(Mcpd()))
  >>> message.value = 42
  >>> response = message.send("doubleServer")
  >>> print(response.result)
  84

  To receive a `Request` subclass on a thread, it is best to use the
  `callback_on_receive()` classmethod. This handles sending the response
  returned by the callback and disposing of any message handles. The following
  example demonstrates a thread which will receive and send a response to a
  single `DoubleMessage` request.

  >>> finished = threading.Event()
  >>> def callback(message: DoubleMessage) -> DoubleMessage.DoubleResponse:
  ...     response = DoubleMessage.Response()
  ...     response.result = message.value * 2
  ...     finished.set()
  ...     return response
  >>> with DoubleMessage.callback_on_receive(
  ...     Mcpd(),
  ...     callback,
  ...     default_factory(Mcpd())
  >>> ):
  ...     while not finished.is_set():
  ...         Mcpd().ServicePendingEvents()
  """
  @classmethod
  def message_name(cls) -> str:
    raise NotImplementedError

  @classmethod
  def response_type(cls) -> typing.Type[Response]:
    """The type of the response expected for this Request.

    This must be implemented by child classes.
    """
    raise NotImplementedError

  @classmethod
  def send_response(
      cls,
      mcp: "Mcpd",
      factory: "Factory",
      message_handle,
      response: Response
    ):
    """Send a reply to this message.

    Typically, this will not be called on the thread which sent the message.
    Rather than call this directly, it is best to use callback_on_receive()
    instead.

    Parameters
    ----------
    message_handle
      The handle of the message to send the reply for.
    response
      The response to send.

    Raises
    ------
    TypeError
      If the response does not match the response type of this class.
    """
    response_type = cls.response_type()
    if not isinstance(response, response_type):
      raise TypeError(
        default_type_error_message(
          "response",
          response,
          response_type
        )
      )
    reply = mcp.BeginReply(message_handle)
    factory.get(response_type).insert(reply, response)
    mcp.Send(reply)

  @classmethod
  def callback_on_receive(
    cls,
    mcp: "Mcpd",
    callback: typing.Callable[["typing.Self"], Response],
    factory: "Factory"
  ) -> McpCallback:
    """Call a callback when a message of this type is received.

    This returns a MCPCallback and is best used in a with block.
    The callback should return the response to the message. This will handle
    sending that response.

    Parameters
    ----------
    mcp
      MCP DLL to use to receive the message.
    callback
      Callback to call when a message of this type is received. The callback
      is passed the received message as its only parameter. The callback
      should return an appropriate response to this message. This function
      will handle sending this response.
    factory
      Factory to use to receive the message.
    """
    def receive_message_and_call_callback(message_handle):
      try:
        received_message = cls.receive(message_handle, factory)
        response = callback(received_message)
        cls.send_response(
          mcp,
          factory,
          message_handle,
          response
        )
      finally:
        mcp.FreeMessage(message_handle)
    return McpCallback(
      cls.message_name(),
      receive_message_and_call_callback
    )

  def _create_message(self, mcp: "Mcpd", destination: str):
    return mcp.NewMessage(
      destination.encode('utf-8'),
      self.message_name().encode('utf-8'),
      True # This is a Request.
    )

  def _send_message(
      self,
      mcp: "Mcpd",
      message_handle
    ) -> Response:
    response = mcp.SendAndGetResponseBlocking(message_handle)
    try:
      self.logger().info('Received response back for %s from %s',
                  self.message_name(), "server")
      decoded_response = self._factory.get(
        self.response_type()).extract(response)
      return decoded_response
    finally:
      mcp.FreeMessage(response)

  def send(self, destination: str,) -> Response:
    # The implementation of _send_message() ensures this will return a
    # Response object.
    return super().send(destination) # type: ignore
