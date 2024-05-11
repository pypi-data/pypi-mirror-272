import ctypes
import subprocess
import sys


class ShutdownNotImplementedForPlatformError(NotImplementedError): ...


class CouldNotShutdownError(RuntimeError): ...


# NOTE: shutdown type
EWX_POWEROFF = 0x00000008
# NOTE: shutdown reason
SHTDN_REASON_MAJOR_OTHER = 0x00000000


def _windows_shutdown() -> None:
    # NOTE: we run mypy on linux so it thinks ctypes.WinDLL does not exist
    user32 = ctypes.WinDLL("user32")  # type: ignore[attr-defined]
    user32.ExitWindowsEx(EWX_POWEROFF, SHTDN_REASON_MAJOR_OTHER)


POSIX_PLATFORMS = {
    "linux",
    "linux2",
    "darwin",
    "freebsd7",
    "freebsd8",
    "freebsdN",
    "openbsd6",
}


def _posix_shutdown() -> None:
    subprocess.run(("shutdown", "-h", "now"), check=True)  # noqa: S603


def shutdown() -> None:
    """Shutdown the computer, supports multiple platforms.

    Raises:
        ShutdownNotImplementedForPlatformError:
            When current platform not supported.
        CouldNotShutdownError:
            When an error occured while shutting down computer.
    """
    if sys.platform == "win32":
        _windows_shutdown()
    elif sys.platform in POSIX_PLATFORMS:
        _posix_shutdown()
    else:
        raise ShutdownNotImplementedForPlatformError
