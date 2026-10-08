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
