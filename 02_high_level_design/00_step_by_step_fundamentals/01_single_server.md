# Step 1 of 13: A Single Server (+ DNS)

[🏠 Overview](README.md) · **Next →** [Step 2: Separate database](02_separate_database.md)

## 📍 Where we are
Nothing yet. We have an idea for an app (say, a photo-sharing site) and a handful of users.

## 💡 The simplest thing that works
Put **everything on one machine**: the web server, the application code, the database, and the files.

```
   User (browser / mobile app)
        │ 1. "where is api.myapp.com?"
        ▼
      DNS ──── 2. "it's 203.0.113.10"
        │
        │ 3. HTTP request to 203.0.113.10
        ▼
┌──────────────────────────────┐
│        ONE SERVER            │
│  web server + app code       │
│  + database + uploaded files │
└──────────────────────────────┘
        │ 4. HTML page (web) or JSON (mobile API)
        ▼
      User
```

## ⚙️ How a request flows
1. The user types `www.myapp.com`. Computers talk to IP addresses, not names, so the browser asks **DNS** (Domain Name System) to translate the name into an IP address. DNS is usually a paid service (Route 53, Cloudflare) and isn't hosted on our server.
2. DNS returns the server's IP address (e.g. `203.0.113.10`). The answer is cached for a while (its TTL).
3. The browser sends an **HTTP request** to that IP.
4. The server runs our code, reads or writes the database, and returns:
   - **HTML** for web browsers, or
   - **JSON** for mobile apps through an API, e.g.
     ```
     GET /users/12  →  {"id": 12, "name": "Owais", "photos": 42}
     ```

## 🧩 Vocabulary introduced
| Term | Meaning |
|---|---|
| **Client** | Whatever sends requests: a browser, mobile app, or another service |
| **Server** | A machine (physical or virtual) that runs our code and answers requests |
| **DNS** | The internet's phone book: name → IP address |
| **IP address** | The numeric address of a machine on the network |
| **HTTP / HTTPS** | The request/response protocol of the web (HTTPS = encrypted with TLS) |
| **API** | The contract for how clients talk to the server (e.g. REST endpoints returning JSON) |

## ⚖️ Why this is fine (for now) and what's wrong with it
✅ Cheap, simple, fast to build. **This is genuinely the right architecture for an MVP** with a few hundred users.

❌ Problems that will appear as we grow:
- **Single point of failure (SPOF):** if this one machine dies, the whole app is down.
- **Everything competes** for the same CPU, memory, and disk. A heavy database query slows down page rendering.
- **No room to grow:** we can only make this one machine bigger.

## 🗣️ Say it in an interview
> "I'd start with the simplest version: one server behind DNS running the app and database. That's enough to validate the product. Then I'll scale it step by step as we hit bottlenecks."

## 🔗 Go deeper
- [DNS & CDN module](../02_dns_cdn/) · Primer: [Domain name system](https://github.com/donnemartin/system-design-primer#domain-name-system)
- [Communication protocols (HTTP, REST)](../08_communication_protocols/)
- [What happens when you type a URL](../../04_cs_fundamentals/02_networking.md#what-happens-when-you-type-googlecom)

## ✅ Self-check
- [ ] Draw the request flow from typing the URL to getting a response
- [ ] What does DNS do, and why isn't it on our server?
- [ ] Name 3 problems with the single-server setup

**Next →** [Step 2: Separate the database](02_separate_database.md)
