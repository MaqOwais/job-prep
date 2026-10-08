# 🟡 22. Dropbox / Google Drive (file storage + sync)

📖 Related: primer [Additional questions: Dropbox](https://github.com/donnemartin/system-design-primer#additional-system-design-interview-questions) · [Dropbox tech blog](https://dropbox.tech/)
⏱️ Try it yourself first: 40 minutes.

## 1. Requirements
**Functional:** upload and download files; **sync** changes across a user's devices automatically; share files and folders; version history; offline edits that sync later.
**Non-functional:** files up to 50 GB, highly durable (never lose data), bandwidth-efficient sync, 100M users.

## 2. Key idea: chunking + deduplication
Split each file into **~4 MB blocks**, hash each one (SHA-256), and store blocks in object storage keyed by hash.
- Editing 1 byte in a 1 GB file → re-upload **only the changed block(s)**.
- Identical blocks (across versions or users) are stored **once** (dedup).
- A file = an ordered list of block hashes (stored in metadata).

## 3. High-level design
```
Desktop/mobile client:
  watcher (file system events) → chunker + hasher → local DB of indexed state
  upload: ask "which of these block hashes do you NOT have?" → upload only missing blocks (parallel, resumable)
  then commit: new file version = [hash1, hash2, …]
           ↓
Block service → S3 (blocks by hash, encrypted)       Metadata service → SQL (sharded by namespace/user):
                                                        files, versions, block lists, sharing ACLs, journal
Notification service: long-poll / WebSocket → "namespace X changed at cursor N" → other devices pull the changes
```

## 4. Deep dives
- **Sync protocol:** each namespace has an append-only **journal** with a cursor. Devices ask "changes since cursor N?" and apply them. A notification only says *something changed*; the client then pulls the actual changes.
- **Conflicts:** two devices edit offline → the server accepts the first commit; the second becomes a **"conflicted copy"** file (Dropbox's approach), rather than an automatic merge.
- **Metadata consistency:** strongly consistent SQL (the source of truth for what a file contains). Blocks are immutable, so they're trivially cacheable.
- **Bandwidth:** delta sync (only changed blocks), compression, LAN sync between devices.
- **Durability:** object storage (11 nines), cross-region replication, and garbage collection of unreferenced blocks (reference counting, plus a grace period).
- **Large files:** multipart, resumable uploads with block-level retries.
- **Sharing:** ACLs on namespaces; a shared folder = a namespace mounted into several users' trees.

## ✅ Takeaways
**Block-level chunking + content-hash dedup**, metadata DB as the source of truth, a journal/cursor sync protocol, notify-then-pull, conflicted copies.
