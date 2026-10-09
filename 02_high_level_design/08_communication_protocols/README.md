# 8. Communication Protocols

📖 Primer: [Communication](https://github.com/donnemartin/system-design-primer#communication) · [HTTP](https://github.com/donnemartin/system-design-primer#hypertext-transfer-protocol-http) · [TCP](https://github.com/donnemartin/system-design-primer#transmission-control-protocol-tcp) · [UDP](https://github.com/donnemartin/system-design-primer#user-datagram-protocol-udp) · [RPC](https://github.com/donnemartin/system-design-primer#remote-procedure-call-rpc) · [REST](https://github.com/donnemartin/system-design-primer#representational-state-transfer-rest) · [RPC vs REST](https://github.com/donnemartin/system-design-primer#rpc-and-rest-calls-comparison)

---

## 8.1 OSI model (the 4 layers that matter)
L7 Application (HTTP, DNS, gRPC) · L4 Transport (TCP/UDP) · L3 Network (IP) · L2 Data link (Ethernet). More detail in [CS fundamentals: networking](../../04_cs_fundamentals/02_networking.md).

## 8.2 TCP vs UDP
| TCP | UDP |
|---|---|
| Connection-oriented (3-way handshake) | Connectionless |
| Reliable, ordered, retransmits, flow and congestion control | Best effort, can lose or reorder packets |
| Higher latency | Lower latency |
| Web, APIs, DBs, file transfer, email | Video calls, gaming, DNS, live streaming, QUIC/HTTP3 base |

## 8.3 HTTP
- A request/response protocol on top of TCP (HTTP/3 runs on QUIC over UDP).
- Methods: **GET** (safe, idempotent), **PUT** (idempotent), **DELETE** (idempotent), **POST** (not idempotent), **PATCH**.
- Status codes: 2xx ok · 3xx redirect (301 permanent, 302 temporary) · 4xx client error (400, 401, 403, 404, **429 too many requests**) · 5xx server error (500, 502, **503**, 504).
- HTTP/1.1 keep-alive → HTTP/2 multiplexing + header compression → HTTP/3 (QUIC: no head-of-line blocking).

## 8.4 API styles
| Style | Good for | Notes |
|---|---|---|
| **REST** | Public APIs, CRUD on resources | Resource URLs, HTTP verbs, stateless, cacheable |
| **RPC / gRPC** | Internal service-to-service calls, low latency | Protobuf (binary), HTTP/2, streaming, strong typing, generated clients |
| **GraphQL** | Many clients needing different data shapes; avoiding over- and under-fetching | Single endpoint; N+1 risk (use DataLoader); caching is harder |

## 8.5 Real-time options (frequently asked)
| Technique | How | Use |
|---|---|---|
| Short polling | Client asks every N seconds | Simple, wasteful |
| **Long polling** | Server holds the request until there's data | Fallback when WebSockets aren't available |
| **Server-Sent Events (SSE)** | Server pushes over one HTTP connection (one direction) | Notifications, live feeds, **LLM token streaming** |
| **WebSockets** | Full-duplex persistent TCP connection | **Chat, multiplayer games, collaborative editing** |
| Webhooks | Server → your server via HTTP callback | Payment status (Stripe), integrations |

## 8.6 API design checklist
- Nouns for resources (`/users/{id}/orders`), plural, versioned (`/v1/`)
- **Pagination:** cursor-based (`?cursor=abc&limit=20`) beats offset for large or changing datasets
- **Idempotency keys** for POST requests that create payments or orders
- Rate limiting (429 + `Retry-After`), auth (OAuth2/JWT), consistent error format
- Filtering, sorting, field selection

## ✅ Self-check
- [ ] TCP vs UDP with 2 examples each
- [ ] REST vs gRPC vs GraphQL: when would you use each?
- [ ] WebSockets vs SSE vs long polling
- [ ] Why is cursor pagination better than offset?

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. REST vs gRPC vs GraphQL: when would you use each?</b></summary>

**REST:** public APIs, simple CRUD over HTTP, cacheable, universal. **gRPC:** internal service-to-service calls, low latency, binary Protobuf, streaming, typed generated clients. **GraphQL:** many client types needing different data shapes, avoiding over- and under-fetching (watch for N+1 queries and harder caching).

</details>

<details>
<summary><b>Q2. WebSockets vs Server-Sent Events vs long polling?</b></summary>

**WebSockets:** full-duplex persistent connection, for chat, games, and collaborative editing. **SSE:** server → client one-way stream over HTTP, auto-reconnects, for notifications, live feeds, and LLM token streaming. **Long polling:** the request is held until there's data. A fallback when neither is available; higher overhead.

</details>

<details>
<summary><b>Q3. Which HTTP methods are idempotent, and why does it matter?</b></summary>

**GET, PUT, DELETE, HEAD, OPTIONS** are idempotent: repeating them has the same effect. **POST** isn't (and PATCH may not be). This matters for **retries**: clients and proxies can safely retry idempotent calls. For POSTs that create payments or orders, use an **Idempotency-Key** header.

</details>

<details>
<summary><b>Q4. Why is cursor-based pagination better than offset-based?</b></summary>

OFFSET 1,000,000 makes the DB scan and skip a million rows (slow), and inserts or deletes during paging cause skipped or duplicated items. A **cursor** (e.g., the last seen ID or timestamp) uses an index seek (WHERE id < cursor LIMIT 20), so it's fast and stable.

</details>

<details>
<summary><b>Q5. What did HTTP/2 and HTTP/3 improve?</b></summary>

**HTTP/2:** binary framing, **multiplexing** many requests over one TCP connection, header compression (HPACK). **HTTP/3:** runs over **QUIC (UDP)**, which removes TCP head-of-line blocking, gives faster handshakes (0/1-RTT), and keeps connections alive across network changes (Wi-Fi to cellular).

</details>
