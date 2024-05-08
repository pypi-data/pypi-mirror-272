"""MSD app definitions."""
import enum


class App(enum.Enum):
    """MSD App."""

    AA = enum.auto()


_APP_ID = {App.AA: '0ba02a6d-031e-ea11-a811-000d3a3be43c'}


def guid(app: App) -> str:
    """Return GUID of app."""
    return _APP_ID[app]
