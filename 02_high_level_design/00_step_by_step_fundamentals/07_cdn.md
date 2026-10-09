# Step 7 of 13: CDN (Content Delivery Network)

[🏠 Overview](README.md) · **← Prev** [Step 6](06_cache.md) · **Next →** [Step 8: Stateless web tier](08_stateless_web_tier.md)

## 📍 Where we are
```
User ──▶ LB ──▶ [web servers] ──▶ [cache] ──▶ [DB primary + replicas]
```

## 🚨 The problem
Our servers are in Virginia (USA). A user in Mumbai loads the site: every image, video, CSS, and JavaScript file travels ~13,000 km. That's **~200+ ms per round trip**, and a page needs dozens of files. The app feels slow, and our web servers waste effort serving **static files** that never change.

## 💡 The fix: a CDN
A CDN is a **network of servers spread around the world** (edge locations or points of presence) that keep **copies of static content close to users**.
```
User in Mumbai ──▶ CDN edge in Mumbai ──(cache hit)──▶ image returned in ~20 ms
                         │ cache miss (first request only)
                         ▼
                   Origin: our S3 bucket / web servers in Virginia
```

## ⚙️ How it works (pull CDN, the most common type)
1. The HTML references assets via a CDN URL: `https://cdn.myapp.com/img/logo.png`.
2. DNS routes the user to the **nearest edge server**.
3. **Cache miss:** the edge fetches the file from our **origin** (S3 or web server) and stores it with a **TTL** (from `Cache-Control` headers).
4. **Later users** nearby get it straight from the edge, so it's fast and the origin isn't touched.

Static files now live in **object storage (S3)** with the CDN in front, so web servers only handle dynamic requests.

## 🔀 Options
| | Pull CDN | Push CDN |
|---|---|---|
| How | Edge fetches from the origin on the first request | You upload content to the CDN in advance |
| Good for | Most sites, high traffic | Rarely changing content, big files you want pre-positioned |

Providers: CloudFront, Cloudflare, Akamai, Fastly. Modern CDNs can also cache some dynamic responses and run code at the edge.

## ⚖️ Considerations and pitfalls
- **Cost:** CDNs charge for data transfer. Don't send rarely accessed files through them.
- **TTL:** too long → users see stale files; too short → more origin fetches.
- **Invalidation:** to update a file, either purge it from the CDN (slow, sometimes costly) or **version the filename** (`app.v2.js`, `logo.8f3a.png`). Versioning is better.
- **CDN outage:** the app should fall back to fetching from the origin.

## 🗣️ Say it in an interview
> "All static assets and media go into S3 behind CloudFront. Users get them from the nearest edge, which cuts latency and takes that load off our servers. Filenames are content-hashed, so we never need purges."

## 🔗 Go deeper
- [DNS & CDN module](../02_dns_cdn/) · Primer: [Content delivery network](https://github.com/donnemartin/system-design-primer#content-delivery-network)
- Where CDNs matter most: [YouTube](../12_problems/hard/15_youtube_video_streaming.md) · [Instagram](../12_problems/medium/21_instagram.md)

## ✅ Self-check
- [ ] Walk through a CDN cache miss and then a hit
- [ ] Pull vs push CDN
- [ ] How do you update a file that's cached for a year? (Version the filename)

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. How does a pull CDN serve a file, from the first request onward?</b></summary>

DNS routes the user to the nearest edge. On the **first request** (miss), the edge fetches the file from the origin (S3 or web server), caches it according to Cache-Control/TTL, and returns it. **Later requests** in that region are served directly from the edge, which is fast and keeps load off the origin.

</details>

<details>
<summary><b>Q2. Push vs pull CDN: when would you choose each?</b></summary>

**Pull** (the default): low effort, good for high-traffic sites. Content is fetched on demand. **Push**: you upload content proactively. Good for large files or launches where you want content pre-positioned and full control over what's on the edge, but you manage the uploads.

</details>

<details>
<summary><b>Q3. How do you update a file that's cached on the CDN with a long TTL?</b></summary>

**Version the filename** (content hash, e.g., app.3f9a.js, or ?v=2) so the new file is a new URL and the old cache entries are simply unused. Purging/invalidation also works but is slower, rate-limited, and sometimes costs money. Keep HTML short-lived and assets long-lived.

</details>

<details>
<summary><b>Q4. What are the main downsides or risks of using a CDN?</b></summary>

**Cost** (data transfer charges), **stale content** if the TTL is too long, more complexity in cache invalidation, and dependence on a third party. Mitigate with a sensible TTL strategy, versioned assets, and an origin fallback if the CDN has problems.

</details>

<details>
<summary><b>Q5. Can a CDN help with dynamic content and security, not just static files?</b></summary>

Yes. Modern CDNs keep TLS connections warm to the origin, cache short-lived API responses, run **edge compute** (auth checks, redirects, A/B tests), and provide **DDoS protection and a WAF** at the edge. Video streaming relies on CDNs for segments.

</details>

**Next →** [Step 8: Stateless web tier](08_stateless_web_tier.md)
