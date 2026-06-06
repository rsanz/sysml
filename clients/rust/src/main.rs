use std::env;
use std::io::{Read, Write};
use std::net::TcpStream;

fn parse_base_url(base_url: &str) -> (&str, u16) {
    let stripped = base_url
        .strip_prefix("http://")
        .or_else(|| base_url.strip_prefix("https://"))
        .unwrap_or(base_url);
    let authority = stripped.split('/').next().unwrap_or(stripped);
    let mut host_port = authority.rsplitn(2, ':');
    let port_candidate = host_port.next().unwrap_or("");
    let host = host_port.next().unwrap_or(authority);
    let port = port_candidate.parse::<u16>().unwrap_or(9000);
    (host, port)
}

fn main() {
    let base_url = env::args()
        .nth(1)
        .unwrap_or_else(|| "http://127.0.0.1:9000".to_string());
    let endpoint = env::args().nth(2).unwrap_or_else(|| "/about".to_string());

    let (host, port) = parse_base_url(&base_url);
    let mut stream = TcpStream::connect((host, port))
        .unwrap_or_else(|err| panic!("connect failed to {}:{}: {}", host, port, err));
    let request = format!(
        "GET {} HTTP/1.1\r\nHost: {}\r\nConnection: close\r\n\r\n",
        endpoint, host
    );
    stream
        .write_all(request.as_bytes())
        .expect("write request failed");

    let mut response = String::new();
    stream.read_to_string(&mut response).expect("read failed");
    if let Some(body) = response
        .split("\r\n\r\n")
        .nth(1)
        .or_else(|| response.split("\n\n").nth(1))
    {
        println!("{}", body.trim());
    } else {
        println!("{}", response.trim());
    }
}
