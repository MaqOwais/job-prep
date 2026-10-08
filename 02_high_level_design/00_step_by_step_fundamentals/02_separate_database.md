# Step 2 of 13: Separate the Database (and choose SQL vs NoSQL)

[🏠 Overview](README.md) · **← Prev** [Step 1](01_single_server.md) · **Next →** [Step 3: Scaling](03_vertical_vs_horizontal_scaling.md)

## 📍 Where we are
One server runs everything.

## 🚨 The problem
Traffic grows. The app code (CPU-heavy: rendering, business logic) and the database (memory- and disk-heavy: queries, indexes) **compete for the same machine**. We also can't scale them independently: maybe we need more app power but the DB is fine, or the reverse.

## 💡 The fix: split into two tiers
```
User ──▶ DNS
  │
  ▼
┌───────────────────┐        ┌──────────────────┐
│ Web/App server     │──SQL──▶│ Database server   │
│ (web tier)         │◀──────│ (data tier)       │
└───────────────────┘        └──────────────────┘
```
- **Web tier:** handles requests and runs the code.
- **Data tier:** stores the data.
Now each tier can be sized, tuned, and scaled **independently**. In the cloud, the DB often becomes a **managed service** (e.g., Amazon RDS) that handles backups and patching for you.

## 🔀 Options: which database?
### Relational (SQL): Postgres, MySQL, Aurora
- Data in **tables with rows and columns**, a fixed schema, relationships via foreign keys, **JOINs**.
- **ACID transactions**: e.g., "debit A and credit B" either both happen or neither does.
- Decades of maturity and tooling.

### Non-relational (NoSQL): four main families
| Family | Data looks like | Examples | Good for |
|---|---|---|---|
| Key-value | `key → value` | Redis, DynamoDB | Sessions, carts, lookups by ID |
| Document | JSON documents | MongoDB, DynamoDB | Flexible or changing schemas, catalogs |
| Wide-column | Rows with dynamic columns, optimized for writes | Cassandra, HBase | Huge write volume: messages, logs, time series |
| Graph | Nodes + edges | Neo4j, Neptune | Relationships: social graphs, recommendations |

### How to choose
| Pick SQL (the default) when… | Consider NoSQL when… |
|---|---|
| Data is structured and relational | You need **very low latency** at huge scale |
| You need transactions and joins | Data is unstructured or semi-structured, or the schema changes often |
| You're not sure yet (the safe default) | You only need simple access by key (serialize/deserialize JSON) |
| | You must store **massive amounts** of data with very high write throughput |

> Rule of thumb: **start with a relational DB.** Move specific data to NoSQL when an access pattern demands it.

## ⚖️ Tradeoffs and pitfalls
- Now there's a **network hop** between app and DB (~0.5 ms in the same data center). Fine, but avoid making 100 queries per page (the N+1 problem).
- We still have **two single points of failure**: one app server and one DB server.

## 🗣️ Say it in an interview
> "I'll separate the web tier from the data tier so they scale independently. I'd use Postgres for users and orders because we need transactions. If we later have a write-heavy feature like activity logs, I'd put that one in Cassandra or DynamoDB."

## 🔗 Go deeper
- [Databases module](../05_databases/) · [Databases & SQL fundamentals](../../04_cs_fundamentals/03_databases_sql.md)
- Primer: [RDBMS](https://github.com/donnemartin/system-design-primer#relational-database-management-system-rdbms) · [NoSQL](https://github.com/donnemartin/system-design-primer#nosql) · [SQL or NoSQL](https://github.com/donnemartin/system-design-primer#sql-or-nosql)

## ✅ Self-check
- [ ] Why separate the web and data tiers?
- [ ] Name the 4 NoSQL families with one use case each
- [ ] Give 2 reasons to choose SQL and 2 reasons to choose NoSQL

**Next →** [Step 3: Vertical vs horizontal scaling](03_vertical_vs_horizontal_scaling.md)
