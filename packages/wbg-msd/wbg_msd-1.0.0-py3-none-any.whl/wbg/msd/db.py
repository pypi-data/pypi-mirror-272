"""Database operations."""
import enum
import pyodbc

from . import env as _env, link


class Database(enum.StrEnum):
    """MSD databases."""

    WFAAC = enum.auto()
    WFASTG = enum.auto()


_DATABASES = {_env.Env.PROD: Database.WFAAC, _env.Env.STAGING: Database.WFASTG}


def get(env: _env.Env) -> Database:
    """Return database for environment."""
    return _DATABASES[env]


def connect(
    env: _env.Env = _env.Env.PROD, user: str = 'ssrinivasan13@worldbank.org'
) -> pyodbc.Connection:
    """Return connection to server."""
    server = link.server_url(env)
    db = get(env)

    con = _get_connection(server, db, user)
    # seems to always require a retry to connect successfully
    con = _get_connection(server, db, user)
    return con


def _get_connection(server: str, database: str, user: str) -> pyodbc.Connection:
    connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={user};Authentication=ActiveDirectoryInteractive;'
    conn = pyodbc.connect(connectionString)
    return conn
