# sysml

Starter project that includes:

1. A SysMLv2 API server scaffold based on the SysML v2 pilot implementation reference repository: https://github.com/Systems-Modeling/SysML-v2-Pilot-Implementation
2. SysMLv2 API clients in C++, Python, and Rust

## Project layout

- `/server/sysmlv2_server.py` - lightweight API server scaffold (`/health`, `/about`)
- `/clients/python/sysmlv2_client.py` - Python client
- `/clients/rust` - Rust client (`cargo run`)
- `/clients/cpp` - C++ client (`cmake`)
- `/tests_smoke.py` - smoke test across server + all clients

## Run server

```bash
python server/sysmlv2_server.py --port 9000
```

## Run clients

### Python

```bash
python clients/python/sysmlv2_client.py --base-url http://127.0.0.1:9000 --endpoint /about
```

### Rust

```bash
cargo run --manifest-path clients/rust/Cargo.toml -- http://127.0.0.1:9000 /about
```

### C++

```bash
cmake -S clients/cpp -B clients/cpp/build
cmake --build clients/cpp/build
./clients/cpp/build/sysmlv2_client http://127.0.0.1:9000 /about
```

## Smoke test

```bash
cmake -S clients/cpp -B clients/cpp/build
cmake --build clients/cpp/build
python tests_smoke.py
```
