#!/usr/bin/env python3
import argparse
import json
import urllib.request


def get_json(base_url: str, endpoint: str) -> dict:
    with urllib.request.urlopen(f"{base_url}{endpoint}", timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Python SysMLv2 API client")
    parser.add_argument("--base-url", default="http://127.0.0.1:9000")
    parser.add_argument("--endpoint", default="/about")
    args = parser.parse_args()

    print(json.dumps(get_json(args.base_url, args.endpoint), indent=2))


if __name__ == "__main__":
    main()
