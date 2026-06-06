use std::env;
use std::io::{Read, Write};
use std::net::TcpStream;

fn parse_base_url(base_url: &str) -> (&str, u16) {
    let stripped = base_url.strip_prefix("http://").unwrap_or(base_url);
    let mut parts = stripped.split(':');
    let host = parts.next().unwrap_or("127.0.0.1");
    let port = parts
        .next()
        .and_then(|v| v.parse::<u16>().ok())
        .unwrap_or(9000);
    (host, port)
}

fn main() {
    let base_url = env::args()
        .nth(1)
        .unwrap_or_else(|| "http://127.0.0.1:9000".to_string());
    let endpoint = env::args().nth(2).unwrap_or_else(|| "/about".to_string());

    let (host, port) = parse_base_url(&base_url);
    let mut stream = TcpStream::connect((host, port)).expect("connect failed");
    let request = format!(
        "GET {} HTTP/1.1\r\nHost: {}\r\nConnection: close\r\n\r\n",
        endpoint, host
    );
    stream
        .write_all(request.as_bytes())
        .expect("write request failed");

    let mut response = String::new();
    stream.read_to_string(&mut response).expect("read failed");
    if let Some(body) = response.split("\r\n\r\n").nth(1) {
        println!("{}", body.trim());
    } else {
        println!("{}", response.trim());
    }
}
