"""Errors raised by the comms module.

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

class FailedToCreateMessageError(Exception):
  """A Message to send to an application could not be created.

  This is raised if the C API returns a null message handle.
  """


class DataTypeNotSupported(Exception):
  """A MCP message included a data type which is not supported."""


class MalformedMessageError(Exception):
  """Exception raised when a message is malformed."""
