# 🟡 06. Twitter Timeline / News Feed

📖 Primer solution: [Design the Twitter timeline and search](https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/twitter/README.md) · Related: [Facebook news feed](https://github.com/donnemartin/system-design-primer#additional-system-design-interview-questions)
⏱️ Try it yourself first: 40 minutes.

## 1. Requirements
**Functional:** post a tweet; view your **home timeline** (tweets from people you follow); view a **user timeline**; follow/unfollow; search (stretch goal).
**Non-functional:** read-heavy, low-latency timeline (< 200 ms), eventual consistency is fine (a few seconds of delay), highly available.

## 2. Estimates
- 100M daily active users, 500M tweets/day → ~6K tweets/s.
- Timeline reads: 100M × 10/day ≈ 1B/day → **~12K QPS** (peak more).
- **Fan-out:** an average of 10 deliveries per tweet → 5B timeline inserts/day → ~60K/s.

## 3. API
```
POST /v1/tweets              {text, media_ids}
GET  /v1/timeline/home?cursor=&limit=20
GET  /v1/users/{id}/tweets?cursor=
POST /v1/users/{id}/follow
```

## 4. Data model
- `tweets(tweet_id [Snowflake], user_id, text, media_url, created_at)`: sharded by tweet_id or user_id (Cassandra/MySQL shards).
- `follows(follower_id, followee_id)`: graph store or a sharded SQL table (with both directions indexed).
- **Home timeline cache:** Redis list per user of `[tweet_id…]` (keep the last ~800).

## 5. High-level design
```
POST tweet → LB → Tweet service → Tweets DB
                          └→ Kafka "tweet_created" → Fan-out workers
                                   → get followers (Graph service)
                                   → LPUSH tweet_id into each follower's Redis timeline
GET timeline → LB → Timeline service → Redis list (tweet_ids)
                                    → hydrate via Tweet cache / User cache → response
Media → S3 + CDN       Search → Kafka → Elasticsearch indexer
```

## 6. Deep dive: fan-out strategy (**the core question**)
| | Fan-out on write (push) | Fan-out on read (pull) |
|---|---|---|
| How | When a tweet is posted, insert it into every follower's timeline | When a user reads, merge the recent tweets of everyone they follow |
| Read | ⚡ Fast (precomputed) | Slow (merge N lists; a k-way merge with a [heap](../../../01_coding/09_heap_priority_queue/)) |
| Write | Expensive for celebrities (100M followers!) | Cheap |
| Wasted work | Fans out to inactive users | None |

**Hybrid (what Twitter actually does):** push for normal users. **Pull for celebrities** (> ~10K followers) at read time and merge their tweets in. Skip fan-out to inactive users.

## 7. Other deep dives
- **Hydration:** the timeline stores only IDs. Tweet and user objects come from caches (multi-get).
- **Search:** inverted index (Elasticsearch), sharded; scatter-gather queries.
- **Counters (likes/retweets):** Redis counters, flushed to the DB in batches.
- **Ranking:** a modern feed is ranked by an ML model (candidate generation → ranking), not purely by time.

## 8. Bottlenecks
Celebrity fan-out → hybrid. Hot tweets → cache replication. Redis memory → keep only N items and only for active users. Search index lag → acceptable.

## ✅ Takeaways
**Push vs pull vs hybrid fan-out** is what this interview is about. Store IDs in timelines and hydrate from caches.
Related coding problem: [Design Twitter (LeetCode 355)](https://leetcode.com/problems/design-twitter/).

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Fan-out on write vs fan-out on read?</b></summary>

**On write (push):** when someone tweets, insert the tweet ID into every follower's timeline cache. Reads are fast; writes are expensive for accounts with huge followings. **On read (pull):** build the timeline at read time by merging the recent tweets of everyone you follow. Cheap writes, slow reads. Twitter-scale systems use a **hybrid**.

</details>

<details>
<summary><b>Q2. How do you handle celebrities with 100M followers?</b></summary>

Don't fan out their tweets. At read time, **merge the celebrity tweets** (fetched from their user timelines, heavily cached) into the user's precomputed timeline. Also skip fan-out to inactive users.

</details>

<details>
<summary><b>Q3. What exactly is stored in the timeline cache?</b></summary>

Only **tweet IDs** (and maybe author IDs) in a Redis list per user, capped at ~800 entries. On read, the IDs are **hydrated** via multi-get from the tweet and user caches. Storing IDs keeps memory small and avoids updating copies when a tweet is edited or deleted.

</details>

<details>
<summary><b>Q4. How would you design tweet search?</b></summary>

Stream new tweets (via Kafka) into an **inverted index** (Elasticsearch / custom Earlybird-style), sharded by time or document, with replicas. Queries **scatter-gather** across shards, merge the top-k, and rank by relevance + recency + engagement.

</details>

<details>
<summary><b>Q5. How do you store and display like counts at scale?</b></summary>

Increment counters in **Redis** (or sharded counters) and flush them to the DB in batches; record the like edge (user, tweet) for "did I like this". Show approximate counts; exact real-time accuracy isn't required.

</details>
