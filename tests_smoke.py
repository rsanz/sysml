#!/usr/bin/env python3
import json
import subprocess
import sys
import time
import urllib.request

REPO = "/tmp/workspace/rsanz/sysml"


def wait_for_server(url: str) -> None:
    for _ in range(20):
        try:
            with urllib.request.urlopen(url, timeout=1) as response:
                if response.status == 200:
                    return
        except Exception:
            time.sleep(0.2)
    raise RuntimeError("server did not start")


def main() -> int:
    server = subprocess.Popen(
        [sys.executable, f"{REPO}/server/sysmlv2_server.py", "--port", "9010"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        wait_for_server("http://127.0.0.1:9010/health")

        with urllib.request.urlopen("http://127.0.0.1:9010/about", timeout=2) as response:
            payload = json.loads(response.read().decode("utf-8"))
            assert "based_on" in payload

        py_out = subprocess.check_output(
            [sys.executable, f"{REPO}/clients/python/sysmlv2_client.py", "--base-url", "http://127.0.0.1:9010", "--endpoint", "/health"],
            text=True,
        )
        assert '"status": "ok"' in py_out

        rust_out = subprocess.check_output(
            ["cargo", "run", "--quiet", "--manifest-path", f"{REPO}/clients/rust/Cargo.toml", "http://127.0.0.1:9010", "/health"],
            text=True,
        )
        assert '"status": "ok"' in rust_out

        cpp_out = subprocess.check_output(
            [f"{REPO}/clients/cpp/build/sysmlv2_client", "http://127.0.0.1:9010", "/health"],
            text=True,
        )
        assert "curl -fsSL http://127.0.0.1:9010/health" in cpp_out

        print("smoke tests passed")
        return 0
    finally:
        server.terminate()
        server.wait(timeout=5)


if __name__ == "__main__":
    raise SystemExit(main())
