#!/usr/bin/env python3
"""
This is the simplest version of an HTTP server that responds dynamically
to a GET request that I could come up with. Surprisingly, I couldn't find a
similar example already in the wild.

A lot of the code is stolen/adapted from Python's http.server module.

Use should be pretty self-explanatory: just override `MyReqHandler.get_content()`.
"""
import sys
import shutil
import contextlib
import socket
from io import BytesIO

from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """Simple HTTP request handler with GET commands."""
    server_version = "SimpleHTTP/1.0"

    def do_GET(self):
        """Serve a GET request."""
        content: str = self.get_content()
        f = BytesIO()
        f.write(content.encode('utf-8'))
        f.seek(0)

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", 'text')
        self.send_header("Content-Length", str(len(f.getbuffer())))
        self.end_headers()

        shutil.copyfileobj(f, self.wfile)

    def get_content(self) -> str:
        raise NotImplementedError


class Server(ThreadingHTTPServer):

    def server_bind(self):
        # suppress exception when protocol is IPv4
        with contextlib.suppress(Exception):
            self.socket.setsockopt(
                socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        return super().server_bind()

    def finish_request(self, request, client_address):
        self.RequestHandlerClass(request, client_address, self)


def run_server(
        bind='127.0.0.1', port=8000,
        HandlerClass=BaseHTTPRequestHandler,
        protocol="HTTP/1.0"
):
    infos = socket.getaddrinfo(
        bind, port,
        type=socket.SOCK_STREAM,
        flags=socket.AI_PASSIVE,
    )
    Server.address_family, _, _, _, addr = next(iter(infos))
    HandlerClass.protocol_version = protocol

    with Server(addr, HandlerClass) as httpd:
        host, port = httpd.socket.getsockname()[:2]
        url_host = f'[{host}]' if ':' in host else host
        print(
            f"Serving HTTP on {host} port {port} "
            f"(http://{url_host}:{port}/) ..."
        )
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            sys.exit(0)


class MyReqHandler(SimpleHTTPRequestHandler):

    def get_content(self):
        # Do your stuff here!
        return f"hello world\n(path: {self.path}"


if __name__ == "__main__":
    run_server('0.0.0.0', HandlerClass=MyReqHandler)
