from __future__ import annotations

from urllib.parse import urlsplit, urlunsplit


def normalize_origin(url, *, allow_insecure=False):
    """Protocol section 1: discard path/query/fragment, normalize host and port."""
    p = urlsplit(url)
    if p.scheme not in ('https', 'http') or not p.hostname or p.username is not None or p.password is not None:
        raise ValueError('Use an HTTP(S) instance URL without credentials')
    if p.scheme != 'https' and not allow_insecure:
        raise ValueError('HTTPS required; allow_insecure is for local tests only')
    host = p.hostname.encode('idna').decode('ascii').lower()
    if ':' in host:
        host = '[' + host + ']'
    port = p.port
    if port is not None and port != (443 if p.scheme == 'https' else 80):
        host += ':' + str(port)
    return urlunsplit((p.scheme.lower(), host, '', '', ''))
