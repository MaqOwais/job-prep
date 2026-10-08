# 🔴 18. Google Docs: Real-Time Collaborative Editing

📖 Related: [Figma: how multiplayer works](https://www.figma.com/blog/how-figmas-multiplayer-technology-works/) · [CRDTs (crdt.tech)](https://crdt.tech/) · primer [Communication](https://github.com/donnemartin/system-design-primer#communication)
⏱️ Try it yourself first: 45 minutes.

## 1. Requirements
**Functional:** many users edit the same document at once; everyone sees changes in < 1 s; cursors and presence; version history and restore; comments; offline editing (stretch goal).
**Non-functional:** **convergence** (all replicas end up identical), low latency, never losing edits, permissions.

## 2. The core problem: concurrent edits
Alice inserts "X" at position 5 while Bob deletes position 3. If both apply raw positions, their documents **diverge**.

| Approach | How | Used by |
|---|---|---|
| **Operational Transformation (OT)** | A central server orders operations and **transforms** each incoming op against concurrent ones (shifting positions) | Google Docs |
| **CRDT** | Each character gets a unique, ordered ID, so operations commute and every replica converges without a central server | Figma (CRDT-inspired), Notion-like apps, Yjs/Automerge |
| Locking sections | Simple | Bad user experience |

## 3. High-level design
```
Client (local doc + pending ops queue)
  ⇄ WebSocket → Collaboration service (one "session owner" per doc, via consistent hashing on doc_id)
                   - assigns revision numbers, transforms ops (OT), broadcasts to the other clients
                   - appends ops to the Operation log (Kafka/DB)
                   ↓ periodic
                Snapshot service → document snapshots (S3/DB) every N ops
Doc metadata + ACLs (SQL)   ·   Presence/cursor service (Redis, ephemeral)   ·   Comments service
```

## 4. Deep dives
- **Client protocol (OT):** send op with base revision → server transforms against newer ops → acknowledges with the new revision → broadcasts. The client transforms its own pending ops against incoming ones.
- **One owner per document** keeps ordering simple. That server holds the document in memory, and the doc_id → server mapping lives in a registry.
- **Persistence:** append-only op log (never lose edits) + periodic snapshots for fast loading: load a snapshot + replay the remaining ops.
- **Version history:** derived from snapshots and the op log.
- **Offline:** CRDTs handle offline merges naturally. OT needs the queued ops replayed and transformed on reconnect.
- **Scaling:** the number of documents scales horizontally; a single document is limited to one owner server, which is fine since a doc has at most ~100 concurrent editors.

## ✅ Takeaways
Explain **OT vs CRDT** clearly, a per-document session owner, an op log + snapshots, WebSockets, ephemeral presence.
