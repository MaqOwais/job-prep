# 🟡 13. Personal Finance App (Mint.com)

📖 Primer solution: [Design Mint.com](https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/mint/README.md)
⏱️ Try it yourself first: 35 minutes.

## 1. Requirements
**Functional:** connect bank accounts; pull transactions daily; **auto-categorize** them; per-category budgets with alerts; monthly spending analysis.
**Non-functional:** write-heavy ingestion (many transactions, few reads), security (financial data!), and analytics can be eventually consistent.

## 2. Estimates
10M users, 30 transactions/user/month → 300M transactions/month (~100 writes/s), ~250 GB/month. Reads are much lower.

## 3. High-level design
```
User → LB → Web/API → Accounts API → SQL (users, accounts)
                     │
Scheduler (daily per account) → Queue → Transaction extraction workers
                                          → bank APIs / aggregator (Plaid)
                                          → categorizer (seller → category map, ML model)
                                          → SQL/NoSQL transactions store
                                          → budget updater → alert if over budget → notification service
Monthly analysis: MapReduce/Spark over transaction logs → monthly_spending table → cache
```

## 4. Deep dives
- **Async ingestion:** a queue decouples slow and flaky bank APIs. Retries with backoff, idempotent on `(account_id, bank_txn_id)`.
- **Inactive users:** only refresh accounts for users active in the last 30 days, which saves a lot of work.
- **Categorization:** start with a seller → category lookup, use an ML classifier for unknowns, and let users correct it (feedback loop).
- **Budgets:** derived aggregates per (user, month, category), updated incrementally by the worker.
- **Security:** encrypt credentials and tokens (KMS), use OAuth-based bank connections instead of stored passwords, audit logs, PCI/SOC2 posture.
- **Scaling:** shard transactions by user_id; analytics in a warehouse (Redshift).

## ✅ Takeaways
Scheduled async ingestion pipeline + categorization + incremental budget aggregates + strong security.
