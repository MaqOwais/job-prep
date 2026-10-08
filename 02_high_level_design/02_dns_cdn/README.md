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
