import logging

from collections import UserDict

logger = logging.getLogger(__name__)

# os.environ.get

DONT_UNLOAD_MODULES = [
  "warnings", "builtins", "sys", "_pytest", "flask", "hosted_flasks", "eventlet"
]

class Environment(UserDict):
  def __init__(self, scope, current_environ=None, debug=False):
    self._scope = scope.upper()
    self._debug = debug
    super().__init__(current_environ)

  @classmethod
  def scope(cls, scope, debug=False):
    logger.info(f"🔧 creating fresh os.environ, for {scope}")
    import os
    current_environ = os.environ.copy()
    import sys
    # remove modules, with some exceptions ;-)
    for mod_name in list(sys.modules.keys()):
      keep = False
      for exception in DONT_UNLOAD_MODULES:
        if mod_name[:len(exception)] == exception:
          keep = True
          break
      if not keep:
        sys.modules.pop(mod_name, None) 
    import os
    patched_environ = cls(scope, current_environ, debug=debug)
    os.environ = patched_environ
    return patched_environ

  def _get_raw(self, key):
    # utility to access env var without looking up the calling app
    return super().__getitem__(key)  # pragma: no cover

  def _log(self, msg):
    if self._debug:
      logger.info(msg) # pragma: no cover
  
  def __setitem__(self, key, value):
    # add the scope prefix
    scoped_key = f"{self._scope}_{key}"
    self._log(f"remapping {key} -> {scoped_key}")
    super().__setitem__(scoped_key, value)

  def __getitem__(self, key):
    # try a prefix first
    app_key = f"{self._scope}_{key}"
    self._log(f"  trying to get {app_key} for {key}")
    try:
      value = super().__getitem__(app_key)
      self._log(f"  SUCCESS {app_key} = {value}")
      return value
    except KeyError:
      pass

    # fall back to the non-prefixed variable
    self._log(f"  FAIL: trying {key}")
    try:
      value = super().__getitem__(key)
      self._log(f"  SUCCESS: found {key}={value}")
    except KeyError:
      raise KeyError
    return value
