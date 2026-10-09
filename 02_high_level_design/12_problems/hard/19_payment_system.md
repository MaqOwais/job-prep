# 🔴 19. Payment System (Stripe / Amazon Pay checkout)

📖 Related: [Stripe: designing robust APIs with idempotency](https://stripe.com/blog/idempotency) · primer [Consistency patterns](https://github.com/donnemartin/system-design-primer#consistency-patterns) · [Microservices / saga](../../04_application_layer_microservices/)
⏱️ Try it yourself first: 45 minutes.

## 1. Requirements
**Functional:** customer pays for an order (card or wallet) through an external payment service provider (PSP: Stripe/Adyen); refunds; merchant payouts; transaction history.
**Non-functional:** **correctness above everything**: never charge twice, never lose money. Auditable, secure (PCI DSS), highly available. Latency is secondary.

## 2. High-level design
```
Checkout → Payment service (API + idempotency check)
              │ 1. create payment record (status=PENDING) in SQL
              │ 2. call PSP with idempotency key  ──→ PSP (hosted card page/tokenization: we never store PAN)
              │ 3. PSP result (sync) or webhook (async) → update status SUCCESS/FAILED
              ▼
           Ledger service (double-entry, append-only)   Wallet/balance service
              ▼
           Outbox → Kafka → Order service, Notification, Analytics
Reconciliation job (daily): compare our ledger with PSP settlement files → flag mismatches
```

## 3. Deep dives
- **Idempotency (the #1 topic):** the client sends an `Idempotency-Key`. The server stores (key → result) with a unique constraint. Retries return the stored result, so a double click or network retry **never charges twice**. Pass the same key to the PSP.
- **Exactly-once effect = at-least-once delivery + idempotent processing.**
- **Double-entry ledger:** every transaction = a debit row + a credit row that sum to zero. Append-only (never UPDATE amounts; corrections are new entries). This gives an audit trail.
- **State machine:** `CREATED → PENDING → SUCCEEDED | FAILED → REFUNDED`. Transitions use conditional updates (optimistic locking with a version column).
- **Distributed consistency:** order + payment + inventory → **saga** with compensations (refund, release stock) + **outbox** for reliable events.
- **Timeouts and unknown states:** if the PSP times out, mark the payment UNKNOWN. Query the PSP status or wait for the webhook. **Never blindly retry with a new key.**
- **Reconciliation:** the daily diff against PSP and bank reports is the final safety net.
- **Security:** tokenization (never store card numbers; use PSP tokens), PCI scope minimization, encryption, fraud checks (risk scoring), audit logs.
- **Database:** relational (Postgres/Aurora), ACID, strongly consistent, sharded by merchant or user if needed.

## ✅ Takeaways
**Idempotency keys**, a double-entry append-only ledger, a payment state machine, saga + outbox, reconciliation, and never storing card data.

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. How do you guarantee a customer is never charged twice?</b></summary>

**Idempotency keys**: the client sends a unique key per payment attempt. The server stores key → result under a unique constraint, so a retried request returns the original result. Pass the same key to the payment provider so its side is idempotent too.

</details>

<details>
<summary><b>Q2. What is a double-entry ledger, and why use it?</b></summary>

Every money movement is recorded as **balanced debit and credit entries** summing to zero, in an **append-only** table. Corrections are new entries, never updates. This gives an audit trail, makes errors detectable (balances must reconcile), and is standard accounting practice.

</details>

<details>
<summary><b>Q3. The payment provider call timed out. Did the charge happen?</b></summary>

Unknown. Mark the payment **PENDING/UNKNOWN**, then **query the provider** with the same idempotency key or wait for its webhook to learn the real status. Never retry with a new key, which could double-charge.

</details>

<details>
<summary><b>Q4. What is reconciliation?</b></summary>

A periodic job (e.g., daily) that compares **your ledger** with the provider's and bank's **settlement reports**, flags mismatches (missing, duplicated, or amount differences), and triggers investigation or corrections. It's the final safety net.

</details>

<details>
<summary><b>Q5. How do you keep card data out of your PCI scope?</b></summary>

**Tokenization**: card details are collected by the provider's hosted fields or SDK, and you only store a **token**. Your servers never see the raw card number, which drastically reduces PCI DSS requirements.

</details>
