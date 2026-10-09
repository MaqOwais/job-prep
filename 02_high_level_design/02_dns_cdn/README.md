# 2. DNS & CDN

📖 Primer: [Domain name system](https://github.com/donnemartin/system-design-primer#domain-name-system) · [Content delivery network](https://github.com/donnemartin/system-design-primer#content-delivery-network) · [Push CDNs](https://github.com/donnemartin/system-design-primer#push-cdns) · [Pull CDNs](https://github.com/donnemartin/system-design-primer#pull-cdns)

---

## 2.1 DNS (Domain Name System)
Translates `www.example.com` → `93.184.216.34`. It's hierarchical, and results are cached at each layer (browser → OS → resolver → root → TLD → authoritative) according to **TTL**.

| Record | Purpose |
|---|---|
| **A / AAAA** | Name → IPv4 / IPv6 |
| **CNAME** | Name → another name (can't be used at the zone apex) |
| **NS** | Which nameservers are authoritative for a domain |
| **MX** | Mail servers |
| **TXT** | Verification, SPF/DKIM |
| Alias (Route 53) | CNAME-like, works at the apex, points to AWS resources |

**Traffic routing with DNS:** weighted round robin (canary releases, A/B tests), **latency-based**, **geolocation**, failover with health checks.

**Downsides:** slight lookup latency (mitigated by caching), changes propagate slowly (TTL), and DNS is a DDoS target.

## 2.2 CDN (Content Delivery Network)
A globally distributed network of edge proxy servers that serve content **close to users**.
- Serves static assets (images, JS, CSS, video) and increasingly dynamic content (edge compute).
- **Benefits:** lower latency for users, and less load on your origin servers.

| | Push CDN | Pull CDN |
|---|---|---|
| How | You upload content to the CDN when it changes | The CDN fetches from the origin on the first request, then caches it (TTL) |
| Good for | Low traffic, rarely changing content | High traffic, frequently accessed content |
| Downside | You manage uploads and storage | First request is slow; possible stale content until the TTL expires |

**Cache invalidation:** versioned filenames (`app.v123.js`) beat purging. Use `Cache-Control` headers.
**Examples:** CloudFront, Cloudflare, Akamai, Fastly.

**CDN downsides:** cost by traffic, stale content until TTL, and URLs must be changed to point to the CDN.

## 🗣️ Say it in an interview
> "Static assets and video segments are served from a pull CDN, so most reads never reach the origin. I'd version the filenames so I never have to purge."

## ✅ Self-check
- [ ] Walk through a DNS resolution end to end
- [ ] Push vs pull CDN: when would you use each?
- [ ] How do you invalidate CDN content?

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Walk through how DNS resolves a domain name.</b></summary>

Browser cache → OS cache → **recursive resolver** (ISP or 8.8.8.8). On a miss, the resolver asks a **root** server → the **TLD** server (.com) → the domain's **authoritative** nameserver, which returns the A/AAAA record. Each answer is cached according to its TTL.

</details>

<details>
<summary><b>Q2. CNAME vs A record vs alias record?</b></summary>

**A/AAAA** maps a name to an IP. **CNAME** maps a name to another name (it can't be used at the zone apex like example.com). An **alias** (Route 53) works like a CNAME but is allowed at the apex and points to AWS resources (ELB, CloudFront) with no extra lookup.

</details>

<details>
<summary><b>Q3. How can DNS be used for load balancing and failover?</b></summary>

Return different IPs per query using **weighted round robin** (canary releases), **latency-based** or **geolocation** routing, and **health-checked failover** records that stop returning unhealthy endpoints. The limit is client caching (TTL), so changes aren't instant.

</details>

<details>
<summary><b>Q4. How do you avoid serving stale assets from a CDN after a deploy?</b></summary>

Use **content-hashed filenames** (main.a1b2c3.js) with long TTLs, and short TTLs or no-cache on HTML. The new HTML references new URLs, so the CDN fetches the new assets. Purges are the fallback for mistakes.

</details>

<details>
<summary><b>Q5. Your origin gets hammered when CDN cache entries expire. What can you do?</b></summary>

Add an **origin shield** (a mid-tier cache in front of the origin), raise TTLs on stable assets, use stale-while-revalidate / serve-stale-on-error, collapse simultaneous requests for the same object at the edge, and pre-warm popular content before big launches.

</details>
