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

**Next →** [Step 8: Stateless web tier](08_stateless_web_tier.md)
