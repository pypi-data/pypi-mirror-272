import logging
from .logger import Logger, Formatter

class StdHandler(logging.Handler):
  """A `logging.Handler` from a `dslog.Logger`"""
  def __init__(self, logger: Logger[logging.LogRecord]):
    super().__init__()
    self.logger = logger

  def emit(self, record):
    self.logger(record, level=record.levelname) # type: ignore (level)

class StdFormatter(Formatter[logging.LogRecord]):

  def __init__(self, formatter: logging.Formatter):
    self._formatter = formatter
  
  def __call__(self, record: logging.LogRecord, /, *, level):
    return self._formatter.format(record),