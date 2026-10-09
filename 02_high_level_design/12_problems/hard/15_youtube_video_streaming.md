# 🔴 15. YouTube / Netflix: Video Upload & Streaming

📖 Related: primer [CDN](https://github.com/donnemartin/system-design-primer#content-delivery-network) · [Netflix tech blog](https://netflixtechblog.com/) · primer [Real-world architectures: YouTube, Netflix](https://github.com/donnemartin/system-design-primer#real-world-architectures)
⏱️ Try it yourself first: 45 minutes.

## 1. Requirements
**Functional:** upload video; transcode to multiple resolutions; stream with **adaptive bitrate**; view counts, likes, comments; search; recommendations (out of scope).
**Non-functional:** smooth playback (low start time, little rebuffering), global scale, huge storage, cost efficiency (CDN egress is the biggest cost).

## 2. Estimates
~500 hours of video uploaded per minute (public YouTube figure) ≈ 30K min/min. Reads ≫ writes (~1000:1).
1 minute of video in all renditions ≈ 300 MB → petabytes per day. **CDN bandwidth dominates the cost.**

## 3. High-level design
```
UPLOAD:
Client → API: request upload → pre-signed URL → upload directly to object storage (S3), multipart/resumable
   S3 "raw" event → Kafka → Transcoding orchestrator (DAG):
       split into GOP chunks → parallel workers: encode 240p…4K (H.264/VP9/AV1)
       → thumbnails, audio, captions → safety/copyright checks (Content ID)
       → package HLS/DASH (segments + manifest) → S3 "processed"
       → update Video metadata DB (status=ready) → notify uploader

STREAM:
Client → API: GET /videos/{id} → metadata + manifest URL
Client player → CDN edge (segments cached) → origin shield → S3
Player picks the bitrate per segment based on measured bandwidth (ABR)
```

## 4. Deep dives
- **Adaptive bitrate streaming (HLS/DASH):** the video is split into 2–10 s segments at multiple bitrates. The manifest lists them, and the player switches quality between segments.
- **Transcoding at scale:** chunk-level parallelism (a DAG of tasks), Spot instances or GPUs, priority queues (popular creators first), retries per chunk.
- **CDN strategy:** popular videos are pushed or pre-warmed to edges; long-tail videos are pulled from origin. Netflix uses Open Connect appliances inside ISPs.
- **Metadata:** MySQL (sharded, Vitess at YouTube) for videos and users. Cassandra for views and comments.
- **View counts:** don't write the DB per view. Use Kafka → stream aggregation → batched counter updates (approximate is fine).
- **Resumable uploads:** chunks with offsets, so an upload can resume after a network drop.
- **Cost:** cheaper storage tiers for old renditions, and transcode rare videos lazily into fewer renditions.

## ✅ Takeaways
Pre-signed direct upload → async **chunked transcoding DAG** → **HLS/DASH segments** → CDN with ABR. Async view counting.

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Walk through the video upload pipeline.</b></summary>

Pre-signed **direct upload to S3** (resumable/multipart) → event → a transcoding orchestrator splits the video into **chunks (GOPs)** → parallel workers encode several resolutions and codecs → thumbnails and captions → content checks → package as **HLS/DASH** segments + manifests → metadata status = ready → notify the uploader.

</details>

<details>
<summary><b>Q2. What is adaptive bitrate streaming?</b></summary>

The video is encoded at several bitrates and cut into **2–10 s segments**. A manifest lists them. The player measures bandwidth and buffer health and **switches quality between segments**, giving a smooth playback with no stalls on varying networks.

</details>

<details>
<summary><b>Q3. Why is the CDN the most important (and expensive) component?</b></summary>

Reads vastly outnumber uploads, and video bytes dominate bandwidth. Serving from **edges near users** cuts latency and origin load. Popular content is pre-positioned (Netflix even places appliances inside ISPs). Egress is the largest cost line.

</details>

<details>
<summary><b>Q4. How do you count views without overloading the database?</b></summary>

Clients send view events → **Kafka** → stream aggregation (per video per minute) → **batched counter updates**. Deduplicate and filter bots before counting, and show approximate real-time counts.

</details>

<details>
<summary><b>Q5. How do you reduce transcoding cost?</b></summary>

Use **Spot instances** and GPU or hardware encoders, transcode popular videos into all renditions immediately but **long-tail videos lazily** (fewer renditions until they're watched), use efficient codecs (AV1) where clients support them, and move old renditions to cheaper storage tiers.

</details>
