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

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Why separate the web tier and the data tier?</b></summary>

They have **different resource profiles** (app = CPU, DB = memory and disk I/O) and **different scaling strategies** (web servers scale horizontally easily; databases don't). Separating them lets you size, tune, secure, and scale each one independently, and use a managed DB with automated backups.

</details>

<details>
<summary><b>Q2. You're starting a new product. SQL or NoSQL? Justify your answer.</b></summary>

**Default to SQL** (e.g., Postgres): the data is usually relational, transactions matter, the schema can evolve with migrations, and it handles a lot of scale with indexes and replicas. Pick NoSQL for a **specific access pattern** that needs it: massive write throughput, simple key lookups at huge scale, flexible documents, or graph traversal.

</details>

<details>
<summary><b>Q3. Name the four NoSQL families and give one use case for each.</b></summary>

- **Key-value** (Redis, DynamoDB): sessions, carts, feature flags.
- **Document** (MongoDB): product catalog with varied attributes, CMS content.
- **Wide-column** (Cassandra, HBase): chat messages, time series, activity logs (write-heavy).
- **Graph** (Neo4j, Neptune): social graphs, fraud rings, recommendations.

</details>

<details>
<summary><b>Q4. What does ACID mean, and why does it matter for a payments feature?</b></summary>

**Atomicity** (all or nothing), **Consistency** (constraints always hold), **Isolation** (concurrent transactions don't see each other's partial work), **Durability** (once committed, it survives crashes). For payments, a debit and its matching credit must both happen or neither does, and two concurrent withdrawals must not overdraw the account.

</details>

<details>
<summary><b>Q5. What new problem does a separate DB server introduce, and how do you mitigate it?</b></summary>

A **network hop** for every query (~0.5 ms in the same data center), plus a second machine that can fail. Mitigate the latency by avoiding chatty access (N+1 queries): batch queries, use joins, use connection pooling. The availability risk is addressed later with replication and failover.

</details>

**Next →** [Step 3: Vertical vs horizontal scaling](03_vertical_vs_horizontal_scaling.md)
