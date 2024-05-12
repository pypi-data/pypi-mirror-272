import logging
from contextlib import contextmanager
from logging.handlers import QueueHandler, QueueListener
from multiprocessing import Queue
from timeit import default_timer as timer

from spellbound.utils.ensure import ensure_list

logger = logging.getLogger(__name__)


def ensure_logger(maybe_logger):
    """
    Ensure that the given logger is a Logger instance.

    Args:
        logger (str|Logger): logger name (str) or logger (Logger)

    Returns:
        Logger: logger instance
    """
    if isinstance(maybe_logger, str):
        return logging.getLogger(maybe_logger)
    if isinstance(maybe_logger, logging.Logger):
        return maybe_logger
    raise TypeError(f"{maybe_logger} is not a Logger.")


def ensure_loggers(loggers):
    """
    Ensure that the given loggers are Logger instances.

    Args:
        loggers (str|Logger|List[str|Logger]): logger name (str) or logger (Logger) or list of loggers

    Returns:
        List[Logger]: list of logger instances
    """
    return [ensure_logger(l) for l in ensure_list(loggers)]


class PipeHandler(logging.Handler):
    """
    Logging handler that pipes log records to another logger.
    """

    def __init__(self, logger, **kwargs):
        super().__init__(**kwargs)
        self.logger = ensure_logger(logger)

    def emit(self, record):
        self.logger.handle(record)


@contextmanager
def pipe_logs(input_loggers, output_logger):
    """
    Create context to pipe logs from input logger(s) to output logger.

    Example usage

    ```
    with pipe_logs("input.logger", "output.logger"):
        # do something that uses input.logger
    ```

    Args:
        input_loggers (str|Logger|List[str|Logger]): input logger(s)
        output_logger (str|Logger): output logger

    Yields:
        None
    """
    in_loggers = ensure_loggers(input_loggers)
    out_logger = ensure_logger(output_logger)

    # This will also support multiprocessing
    queue = Queue(-1)
    queue_handler = QueueHandler(queue)
    queue_handler.setLevel(out_logger.level)
    pipe_handler = PipeHandler(out_logger)
    pipe_handler.setLevel(out_logger.level)
    queue_listener = QueueListener(queue, pipe_handler)

    old_levels = [l.level for l in in_loggers]

    for l in in_loggers:
        l.level = out_logger.level
        l.addHandler(queue_handler)

    queue_listener.start()
    yield
    queue_listener.stop()

    for l, level in zip(in_loggers, old_levels):
        l.removeHandler(queue_handler)
        l.level = level


@contextmanager
def log_duration(log_fn=None, name="Code block"):
    log_fn = log_fn or logger.debug
    start = timer()
    yield
    log_fn("%s took %.3fs", name, timer() - start)
