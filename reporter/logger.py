"""Logging helpers."""
from datetime import datetime
from pathlib import Path
from typing import Literal, TypeAlias

import coloredlogs
from verboselogs import VerboseLogger

LogLevel: TypeAlias = Literal["error", "warning"]

programLogger: VerboseLogger = VerboseLogger("reporter")


def set_logger(debug: bool) -> None:
    """Set the program's logger.

    Parameters
    ----------
    debug : bool
        If True, set log verbosity level to debug.

    """
    level: str = "DEBUG" if debug else "INFO"

    coloredlogs.install(
        logger=programLogger,
        level=level,
        fmt="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    )


def log_to_file(message: str, level: LogLevel = "error") -> None:
    """Write logs to local file.

    Parameters
    ----------
    message : str
        The text to write to file.
    level : 'error' or 'warning', default='error'
        The log level.

    """
    if level == "error":
        programLogger.error(message)
    else:
        programLogger.warning(message)

    logfile: Path = Path("logs/reporter.log")

    try:
        if not logfile.parent.exists():
            logfile.parent.mkdir(parents=True)

        timestamp: str = datetime.now().isoformat()

        with logfile.open(mode="a") as file_handle:
            file_handle.write(f"{timestamp} - {message}\n")

    except (FileNotFoundError, OSError, PermissionError, ValueError) as err:
        programLogger.error(f"Failed to write logs to '{str(logfile)}': {err}")
