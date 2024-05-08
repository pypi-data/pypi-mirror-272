"""MSD Links."""

from . import (
    entity as _entity,
    env as _env,
    app as _app,
    _protocols,
)


ROOT_URL = "https://wfaac.crm.dynamics.com/main.aspx"

_SERVER_URLS = {
    _env.Env.PROD: _protocols.URL('wfaac.crm.dynamics.com'),
    _env.Env.STAGING: _protocols.URL('wfastg.crm.dynamics.com'),
}


def server_url(env: _env.Env) -> _protocols.URL:
    """Return server url."""
    return _SERVER_URLS[env]


def site_url(env: _env.Env) -> _protocols.URL:
    """Return website url."""
    url = f'https://{server_url(env)}/main.aspx'
    return _protocols.URL(url)


def to_record(
    entity: _entity.Entity,
    entity_id: str,
    env: _env.Env = _env.Env.PROD,
    app: _app.App = _app.App.AA,
) -> _protocols.URL:
    """Return link to entity record."""

    url = f"{site_url(env)}?appid={_app.guid(app)}&pagetype=entityrecord&etn={entity.value}&id={entity_id}"
    return _protocols.URL(url)
