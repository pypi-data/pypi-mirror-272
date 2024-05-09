"""Common functions used by the SDK specifically for use with C API modules.

Warnings
--------
Vendors and clients should not develop scripts or applications against
this module. The contents may change at any time without warning.

"""
###############################################################################
#
# (C) Copyright 2020, Maptek Pty Ltd. All rights reserved.
#
###############################################################################
from __future__ import annotations

import ctypes
import enum
import logging
import os
import pathlib


class DllDirectoryState(enum.Enum):
  """Enum representing the state of the DLL directories."""
  NOT_SET = enum.auto()
  """The directories to load DLLs from have not been set.

  This is the state before the script has connected to an application
  via the Project() constructor.
  While in this state, it is an error to attempt to load a DLL
  because where to load the DLLs from has not been defined.
  """
  SET = enum.auto()
  """The directories to load DLLs from have been set.

  This is the state after the script has connected to an application
  via the Project() constructor, but before the Project's with block
  has ended.
  In this state it is valid to load DLLs.
  """
  CLEARED = enum.auto()
  """The application's DLL directory was set, but it has been cleared.

  This is the state after a script has connected to an application
  via the Project() constructor and after the associated with block has
  ended (i.e. After the script has disconnected from the application).

  In this state it is an error to load DLLs from the application.

  Notes
  -----
  In this state further DLL loading is disabled however all DLLs which were
  previously loaded are still loaded into the process. The SDK makes no
  effort to unload them because this cannot be done effectively.

  * The SDK could unload the "mdf_modelling.dll" and other explicitly loaded
    DLLs.
  * However the SDK cannot unload any DLLs loaded as dependencies of the
    explicitly loaded DLLs.
  * In practice, this includes at least 40 MDF DLLs and an unknown number
    of operating system DLLs.
  * Because most loaded DLLs cannot be unloaded, the SDK makes no effort
    to unload them.
  * This makes it impossible to disconnect from one application
    (e.g. PointStudio) and then connect to another application (e.g.
    GeologyCore or a different version of PointStudio) because
    it would attempt to use the DLLs loaded from the original application
    which are incompatible. (Even if the explicitly loaded DLLs were unloaded
    first, it still would not work because it would attempt to satisfy
    the dependencies of the explicitly loaded DLLs with the dependencies
    loaded for the original application, resulting in a mix of incompatible
    DLLs from both applications)
  * It is however possible to connect to the same application or a different
    instance of that application in one script. In this case the SDK reuses
    the DLLs which were loaded for the first connection (which are compatible
    because it is the same application).
  """

_DLL_DIRECTORIES: list[pathlib.Path] = []
"""List of paths to directories to load DLLs from.

The SDK will only explicitly load DLLs from these paths. Earlier paths in the
list will be searched first.
"""

_DEPENDENCY_DIRECTORIES: list | None = None
"""List of objects returned by os.add_dll_directories().

os.add_dll_directories() is called on each path in _DLL_DIRECTORIES and this
list contains these objects. These are closed when disconnecting from the
application, preventing further loading of DLLs from the directories in
_DLL_DIRECTORIES.
"""

_REMEMBERED_DLL_PATH: str | None = None
"""The path passed to register_dll_directory().

After disconnecting from one application, it is only valid for the script
to reconnect to the same application or a different instance of that application
because the SDK cannot effectively unload the DLLs from the first application
and thus would attempt to use the original applications DLLs to connect to the
second application, resulting in a crash.

This is used to detect attempts to connect to a different application and
to raise a useful error message.

"""

_DLL_STATUS: DllDirectoryState = DllDirectoryState.NOT_SET
"""The current state of this module."""

_HAS_ADDED_DLL_DIRECTORIES_TO_PATH: bool = False

logger = logging.getLogger("mapteksdk.capi.util")


class CApiError(Exception):
  """Base class for errors raised by the C API. This class should not be
  raised directly - raise a subclass instead.

  """


class CApiFunctionNotSupportedError(CApiError):
  """Error raised when a function in the C API is not supported by the current
  C API version.

  """


class CApiDllLoadFailureError(CApiError):
  """Error raised when one of the DLLs fails to load."""


class CApiUnknownError(CApiError):
  """Error raised when an unknown error occurs in the CAPI."""


class NoConnectedApplicationError(CApiError):
  """Error raised when not connected to an application"""


class MultipleApplicationConnectionsError(CApiError):
  """Error raised when attempting to connect to two different applications.

  Connecting to two different applications within the same script is impossible
  because Python cannot effectively unload every DLL required to connect
  an application (It can't unload DLLs implicitly loaded as dependencies of
  the explicitly loaded DLLs). Thus, attempting to connect to a second
  application results in a mix of incompatible DLLs from the two
  applications.

  """


class CApiWarning(Warning):
  """Base class for warnings emitted from the C APIs."""


class CApiUnknownWarning(CApiWarning):
  """A C API function returned an unknown error, but it was not fatal.

  This is emitted in place of CApiUnknownError when the error is non-fatal.
  """


def _ensure_dlls_available():
  """Raises an error if the application's DLLs are not available.

  This will raise an error if the script has yet to connect to an application,
  or if the script has disconnected from an application.

  Raises
  ------
  NoConnectedApplicationError
    If the application DLLs are not available.
  """
  if _DLL_STATUS is DllDirectoryState.NOT_SET:
    raise NoConnectedApplicationError(
      "This function cannot be accessed because the script has not connected "
      "to an application. Use the Project() constructor to connect to an "
      "application.")

  if _DLL_STATUS is DllDirectoryState.CLEARED:
    raise NoConnectedApplicationError(
      "This function cannot be accessed because the script has disconnected "
      "from the application. Ensure all functions which require a "
      "connected application are inside of the Project's `with` block.")

  if _DLL_STATUS is not DllDirectoryState.SET:
    raise Exception(
      "Unreachable code reached. Please use Workbench's report bug feature "
      "to provide Maptek with steps to replicate this error.")

def load_dll(dll_name: str):
  """Load a dll using the dll_path configured by connecting to an application.

  Parameters
  ----------
  dll_name : str
    The name of the dll to load.

  Raises
  ------
  NoConnectedApplicationError
    If the script has not connected to an application.
  """
  _ensure_dlls_available()

  last_error = None

  # Try to load the DLL from all of the configured paths.
  for path in _DLL_DIRECTORIES:
    try:
      path = path / dll_name
      path = path.resolve()
      return ctypes.CDLL(str(path))
    except OSError as error:
      last_error = error

  # If all possible paths to the DLL were attempted, but none resulted in
  # a successful load, raise the last error.
  if last_error:
    raise last_error

  # This would mean that _IS_CONNECTED is True, but the SDK failed to
  # set the DLL directory. This should not be possible, but just in case.
  raise NoConnectedApplicationError(
    f"An application seems to be connected, but failed to load {dll_name}.")

def register_dll_directory(base_path: str):
  """Registers a DLL directory.

  This handles the differences between installed applications versus
  applications compiled from source.
  """
  # pylint: disable=global-statement
  global _DEPENDENCY_DIRECTORIES
  global _REMEMBERED_DLL_PATH
  global _DLL_STATUS

  # Disallow connecting to multiple applications at once.
  if _DLL_STATUS is DllDirectoryState.SET:
    raise MultipleApplicationConnectionsError(
      "Cannot connect to an application because the script is already "
      "connected to an application.")

  # The SDK cannot disconnect from one application (e.g. PointStudio) and
  # then connect to another application (e.g. GeologyCore).
  if (_DLL_STATUS is DllDirectoryState.CLEARED
        and _REMEMBERED_DLL_PATH != base_path):
    raise MultipleApplicationConnectionsError(
      "Cannot connect to multiple different applications in one script")

  logger.debug("Loading dlls from %s", base_path)

  base = pathlib.Path(base_path)
  shlib_path = base.parent / "shlib"

  if shlib_path.is_dir():
    # The application is compiled from source because the DLLs are in the shlib
    # folder instead of the bin folder.
    _DLL_DIRECTORIES.append(shlib_path)

    # Also add the eureka shlib folder to the search path. This is needed
    # to be able to find the drillhole model C API.
    eureka_path = shlib_path / ".." / ".." / "eureka" / "shlib"
    if eureka_path.is_dir():
      _DLL_DIRECTORIES.append(eureka_path)
  elif base.is_dir():
    # The application is installed. The base path can be added without
    # modification.
    _DLL_DIRECTORIES.append(base)
  else:
    error = FileNotFoundError(
      "Failed to locate folder containing required DLLs. "
      f"Searched:\n{shlib_path}\nand\n{base}")
    error.searched_paths = [base, shlib_path]
    raise error

  _DEPENDENCY_DIRECTORIES = [
    os.add_dll_directory(str(path)) for path in _DLL_DIRECTORIES
  ]

  _REMEMBERED_DLL_PATH = base_path
  _DLL_STATUS = DllDirectoryState.SET

def disable_dll_loading():
  """Disable loading DLLs from the application.

  This should be called when disconnecting from an application.
  """
  # pylint: disable=global-statement
  global _DLL_DIRECTORIES
  global _DEPENDENCY_DIRECTORIES
  global _DLL_STATUS
  _DLL_DIRECTORIES = []
  if _DEPENDENCY_DIRECTORIES is not None:
    for directory in _DEPENDENCY_DIRECTORIES:
      directory.close()
    _DEPENDENCY_DIRECTORIES = None
  _DLL_STATUS = DllDirectoryState.CLEARED

def add_dll_directories_to_path():
  """Add the DLL directories to the PATH environment variable.

  This is used used to work around bugs in DLLs where they do not
  use the DLL search directories to load DLLs.

  This will only add the DLL directories to PATH once.
  """
  # pylint: disable=global-statement
  global _HAS_ADDED_DLL_DIRECTORIES_TO_PATH
  if _HAS_ADDED_DLL_DIRECTORIES_TO_PATH:
    return
  _HAS_ADDED_DLL_DIRECTORIES_TO_PATH = True
  new_path = [str(dll_path) for dll_path in _DLL_DIRECTORIES]
  new_path.append(os.environ["PATH"])
  os.environ["PATH"] = os.pathsep.join(new_path)

def singleton(class_reference):
  """Provides an implementation of the singleton pattern.

  This should only be used for the C API singletons. It includes additional
  functionality to disable accessing the DLLs after disconnecting from
  the application.

  Notes
  -----
  Usage: @singleton above class

  """
  instances = {}
  def get_instance():
    """Gets (or creates) the only instance of a singleton class."""
    # Disallow accessing the DLLs if there is no connected application.
    _ensure_dlls_available()
    if class_reference not in instances:
      instances[class_reference] = class_reference()
    return instances[class_reference]
  return get_instance

def get_string(target_handle, dll_function):
  """Read a string from a C API function.

  This works for C API functions which return a string
  and have a function signature of the form: Tint32u (handle, *buffer, size).

  Parameters
  ----------
  target_handle : c_uint64, T_ObjectHandle, T_NodePathHandle, etc
    Suitable type of native handle (), supporting
    a *.value property.
  dll_function : function
    A function of Tint32u (handle, *buffer, size).

  Returns
  -------
  str
    Result as string or None on failure (e.g. not supported by dll).

  """
  try:
    value_size = 64
    while value_size > 0:
      value_buffer = ctypes.create_string_buffer(value_size)
      result_size = dll_function(target_handle, value_buffer, value_size)
      if result_size is None:
        # probably not supported by dll version
        return None
      value_size = -1 if result_size <= value_size else result_size
    return value_buffer.value.decode("utf-8")
  except OSError:
    result = None
  return result

def raise_if_version_too_old(feature, current_version, required_version):
  """Raises a CapiVersionNotSupportedError if current_version is less
  than required_version.

  Parameters
  ----------
  feature : str
    The feature name to include in the error message.
  current_version : tuple
    The current version of the C Api.
  required_version : tuple
    The version of the C Api required to access the new feature.

  Raises
  ------
  CApiVersionNotSupportedError
    If current_version < required_version. The text of the error is:
    f"{feature} is not supported in C Api version: {current_version}. "
    f"Requires version: {required_version}."

  """
  if current_version < required_version:
    raise CApiFunctionNotSupportedError(
      f"{feature} is not supported in C Api version: {current_version}. "
      f"Requires version: {required_version}")
