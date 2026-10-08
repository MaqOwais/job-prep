# 2. Networking

📖 Primer: [Communication](https://github.com/donnemartin/system-design-primer#communication) · Deeper: [High Performance Browser Networking (free)](https://hpbn.co/)

## OSI vs TCP/IP
| OSI layer | Examples | TCP/IP layer |
|---|---|---|
| 7 Application | HTTP, DNS, SMTP, gRPC | Application |
| 6 Presentation | TLS, encoding | Application |
| 5 Session | Sessions | Application |
| 4 Transport | **TCP, UDP** | Transport |
| 3 Network | **IP**, ICMP, routing | Internet |
| 2 Data link | Ethernet, MAC, ARP | Link |
| 1 Physical | Cables, radio | Link |

## TCP essentials
- **3-way handshake:** SYN → SYN-ACK → ACK. **Teardown:** FIN/ACK (4-way); TIME_WAIT state.
- Reliability: sequence numbers, ACKs, retransmission.
- **Flow control** (receiver window: don't overwhelm the receiver) vs **congestion control** (slow start, AIMD: don't overwhelm the network).
- Head-of-line blocking: one lost packet stalls everything behind it, which is why HTTP/3 moved to QUIC.

## IP addressing
- IPv4 is 32-bit, IPv6 is 128-bit. **CIDR** `/24` = 256 addresses.
- Private ranges: `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`. **NAT** maps private addresses to a public IP.
- Ports: 80 HTTP, 443 HTTPS, 22 SSH, 53 DNS, 5432 Postgres, 3306 MySQL, 6379 Redis.

## What happens when you type google.com
1. **URL parsing**. The browser checks HSTS (forcing HTTPS).
2. **DNS:** browser cache → OS cache → resolver → root → `.com` TLD → Google's authoritative nameserver → IP. Cached with a TTL.
3. **TCP handshake** to IP:443.
4. **TLS handshake:** ClientHello (supported ciphers) → ServerHello + **certificate** → client verifies the chain of trust → key exchange (ECDHE) → symmetric session keys. TLS 1.3 needs 1 round trip.
5. **HTTP request** `GET /` with headers and cookies.
6. On the server side: **GeoDNS/anycast → CDN edge → load balancer → web servers → services → cache/DB**.
7. **Response:** status + headers + HTML. Compressed (gzip/brotli), with caching headers.
8. **Browser renders:** parse HTML → DOM, CSS → CSSOM, run JS, fetch sub-resources (in parallel over HTTP/2), layout, paint.

## DNS
Record types: A, AAAA, CNAME, MX, NS, TXT. Resolution is recursive (the resolver does all the work) vs iterative (each server refers you onward). DNS uses UDP on port 53 (TCP for large responses).

## HTTP
- Methods and idempotency: GET, PUT, and DELETE are idempotent. POST isn't.
- Status codes: 200, 201, 204 · 301, 302, 304 (not modified) · 400, 401, 403, 404, 409, 429 · 500, 502, 503, 504.
- **Versions:** HTTP/1.1 (keep-alive, text) → HTTP/2 (binary, multiplexed, header compression, server push) → HTTP/3 (QUIC over UDP, faster handshakes, no TCP head-of-line blocking).
- Caching headers: `Cache-Control`, `ETag`, `Last-Modified`.
- Cookies: `HttpOnly`, `Secure`, `SameSite`. **CORS:** the browser enforces cross-origin rules; the server opts in with `Access-Control-Allow-Origin`.

## TLS / HTTPS
- Asymmetric crypto (RSA/ECDHE) for **key exchange and authentication**; symmetric crypto (AES-GCM) for **bulk data**.
- Certificates are signed by CAs, forming a chain of trust up to a root stored in the OS/browser.
- **mTLS:** both sides present certificates (service-to-service).

## Load balancing and proxies
See [system design: load balancing](../02_high_level_design/03_load_balancing_reverse_proxy/).

## Interview questions
1. What happens when you type a URL? (Above. Practice saying it in 2 minutes.)
2. TCP vs UDP, with examples.
3. How does TLS work?
4. What is a socket? (An endpoint: IP + port + protocol.)
5. How does traceroute work? (Increasing TTL values + ICMP "time exceeded" replies.)
6. Why is HTTP stateless, and how do we keep sessions? (Cookies + a server-side session store, or a JWT.)
