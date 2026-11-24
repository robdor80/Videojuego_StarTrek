#!/usr/bin/env python3
"""Local-only preview server for the F07 final UI (no F06 writes)."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from webbrowser import open_new_tab


def main():
    directory = Path(__file__).resolve().parent
    handler = partial(SimpleHTTPRequestHandler, directory=str(directory))
    with ThreadingHTTPServer(("127.0.0.1", 0), handler) as server:
        url = "http://127.0.0.1:{}/index.html".format(server.server_port)
        print("F07 en modo DEMOSTRACIÓN:", url, flush=True)
        print("Ctrl+C cierra el servidor. No escribe en CoreRPG.", flush=True)
        open_new_tab(url)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
