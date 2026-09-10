import ipaddress
import socket
from urllib.parse import urlparse


BLOCKED_HOSTS = {
    'localhost',
    'localhost.localdomain',
    'metadata.google.internal',
}


def assert_public_http_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in ('http', 'https'):
        raise ValueError('Only http and https URLs are allowed')
    host = (parsed.hostname or '').strip().lower()
    if not host:
        raise ValueError('URL is missing a host')
    if host in BLOCKED_HOSTS or host.endswith('.localhost'):
        raise ValueError('Private or reserved hosts are not allowed')
    try:
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror as exc:
        raise ValueError(f'Could not resolve host: {host}') from exc
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_reserved
            or ip.is_multicast
            or ip.is_unspecified
        ):
            raise ValueError('URL resolves to a non-public address')
