# 🟡 21. Instagram (photo sharing + feed)

📖 Related: [Twitter / news feed](06_twitter_news_feed.md) · primer [Real-world architectures: Instagram](https://github.com/donnemartin/system-design-primer#real-world-architectures) · [Instagram engineering: sharding IDs](https://instagram-engineering.com/sharding-ids-at-instagram-1cf5a71e5a5c)
⏱️ Try it yourself first: 40 minutes.

## 1. Requirements
**Functional:** upload photos/videos with captions; follow users; home feed; likes and comments; user profile grid; (stretch: stories, search, explore).
**Non-functional:** 500M daily active users, read-heavy (~100:1), feed loads < 300 ms, uploads are durable, eventual consistency is fine for feeds and likes.

## 2. Estimates
- 100M uploads/day → ~1,200/s. 2 MB average (plus resized versions) → **~200 TB/day** of raw media. Object storage + CDN are mandatory.
- Feed reads: 500M × 10/day = 5B/day → **~60K QPS**.

## 3. API
```
POST /v1/media/upload-url           → pre-signed S3 URL(s)
POST /v1/posts {media_ids, caption} → post_id
GET  /v1/feed?cursor=               → posts[]
POST /v1/posts/{id}/like · POST /v1/posts/{id}/comments · POST /v1/users/{id}/follow
```

## 4. Data model
- `users` (SQL), `follows(follower_id, followee_id)` (sharded SQL or a graph store, with both directions indexed)
- `posts(post_id [Snowflake], user_id, caption, media_keys[], created_at)`: sharded by user_id (Instagram famously sharded Postgres)
- `likes(post_id, user_id)` + **like counters** in Redis, flushed to the DB in batches
- Feed cache: Redis list of post_ids per user

## 5. High-level design
```
UPLOAD: client → API → pre-signed URL → upload to S3 directly
        S3 event → queue → media workers: resize (thumbnail/small/large), transcode video, strip EXIF, moderation
        → write post row → Kafka "post_created" → feed fan-out workers → followers' feed caches (hybrid for celebrities)
READ:   client → CDN (images) ; client → LB → Feed service → Redis feed (post_ids) → hydrate posts + users (caches) → ranked feed
Likes/comments → Like service → Redis counters + Kafka → async persist; notifications service
```

## 6. Deep dives
- **Media path:** never stream bytes through app servers. Pre-signed upload → async processing → CDN delivery. Multiple resolutions; WebP/AVIF formats.
- **Feed generation:** same push/pull/hybrid tradeoff as [Twitter](06_twitter_news_feed.md). Modern feeds are **ranked** (ML), not chronological: candidate posts → ranking model.
- **Counters:** a celebrity post gets 1M likes. Don't update a single DB row per like: Redis INCR + batched writes, or sharded counters.
- **Profile grid:** query posts by user_id (same shard), cached.
- **Search and explore:** Elasticsearch for users and hashtags; explore = recommendation system ([AI folder](../../../08_ai_system_design/problems/medium/07_recommendation_system.md)).

## ✅ Takeaways
**Pre-signed direct uploads + async media pipeline + CDN**, hybrid fan-out feed with ranking, Redis counters for likes, sharding by user_id.

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. How should photo uploads work?</b></summary>

The client asks the API for a **pre-signed URL** and uploads **directly to S3** (multipart for large files), so the bytes never pass through app servers. An S3 event triggers async workers to resize, transcode, strip EXIF, and moderate. Then the post is published and fanned out.

</details>

<details>
<summary><b>Q2. How are images served fast worldwide?</b></summary>

From a **CDN**, with multiple pre-generated sizes and modern formats (WebP/AVIF), immutable versioned URLs with long TTLs, and lazy loading in the client.

</details>

<details>
<summary><b>Q3. How do you handle a post getting a million likes in an hour?</b></summary>

Don't update one DB row per like. Use **Redis INCR or sharded counters**, batch flush to the DB, record like edges asynchronously via Kafka, and show approximate counts.

</details>

<details>
<summary><b>Q4. How is the home feed generated?</b></summary>

A **hybrid fan-out** like Twitter: push post IDs to followers' feed caches for normal accounts, pull for celebrities at read time. Then **rank** the candidates with an ML model (engagement prediction) rather than sorting by time.

</details>

<details>
<summary><b>Q5. How would you shard the posts data?</b></summary>

By **user_id** (Instagram's famous approach on Postgres with logical shards), so a user's posts live together and the profile grid query hits one shard. IDs embed the shard and time (Snowflake-like), so they're sortable and routable.

</details>
