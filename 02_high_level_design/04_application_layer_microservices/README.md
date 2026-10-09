# 4. Application Layer & Microservices

📖 Primer: [Application layer](https://github.com/donnemartin/system-design-primer#application-layer) · [Microservices](https://github.com/donnemartin/system-design-primer#microservices) · [Service discovery](https://github.com/donnemartin/system-design-primer#service-discovery)

---

## 4.1 Separate the web layer from the application layer
The web tier (serving requests) and the app/worker tier (business logic, async jobs) scale independently. Adding a new API means adding app servers, not necessarily web servers. This follows the **single responsibility principle**: small, autonomous services.

## 4.2 Monolith vs microservices
| | Monolith | Microservices |
|---|---|---|
| Deploy | One unit | Independent per service |
| Scaling | All or nothing | Per service |
| Team fit | Small team, early product | Many teams, clear domain boundaries |
| Complexity | Low | High: network calls, distributed tracing, data consistency |
| Failure | One bug can take everything down | Isolated failures (if designed well) |

> **Interview answer:** "Start with a **modular monolith**. Split out services when a domain needs independent scaling, deployment, or team ownership."

## 4.3 Microservices patterns to know
- **Service discovery:** Consul, etcd, ZooKeeper, Kubernetes DNS. Services register with health checks, and clients look them up.
- **API gateway / backend-for-frontend (BFF).**
- **Database per service:** no shared DB, so cross-service data access goes through events and APIs.
- **Saga pattern:** a distributed transaction as a sequence of local transactions + **compensating actions** (choreography via events, or orchestration via a coordinator).
- **Circuit breaker:** stop calling a failing dependency, fail fast, retry after a cooldown.
- **Bulkhead:** isolate resources (thread pools) per dependency.
- **Retries with exponential backoff + jitter**, plus **timeouts** on every network call.
- **Outbox pattern:** write the DB row and the "event to publish" in one transaction. A relay publishes it to the queue, so you never get a DB write without its event.
- **CQRS:** separate write model and read model (often with event sourcing).
- **Observability:** logs, metrics, distributed tracing (OpenTelemetry, Jaeger, X-Ray), correlation IDs.
- **Sidecar / service mesh** (Envoy, Istio): mTLS, retries, and traffic shifting outside the app code.

## 4.4 Deployment strategies
Rolling · **Blue/green** (switch traffic between two stacks) · **Canary** (1% → 10% → 100%) · Feature flags · Shadow traffic.

## 🗣️ Say it in an interview
> "Order and payment are separate services, each with its own database. Placing an order runs a saga: reserve inventory → charge payment → confirm. If payment fails, a compensating action releases the inventory. I'd use the outbox pattern so events are never lost."

## ✅ Self-check
- [ ] When would you NOT use microservices?
- [ ] Explain the saga + compensating action pattern
- [ ] Circuit breaker states: closed → open → half-open
- [ ] What problem does the outbox pattern solve?

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Monolith or microservices for a five-engineer startup?</b></summary>

A **modular monolith**: one deployable unit with clear internal module boundaries. It's faster to build, debug, and deploy, and you avoid distributed-systems overhead. Extract a service only when a module needs independent scaling, deployment cadence, or team ownership.

</details>

<details>
<summary><b>Q2. Explain the saga pattern with an example.</b></summary>

A distributed transaction made of **local transactions**, each with a **compensating action**. Order: reserve inventory → charge payment → create shipment. If payment fails, compensate by releasing the inventory. Sagas are either **choreographed** (services react to events) or **orchestrated** (a coordinator drives the steps).

</details>

<details>
<summary><b>Q3. What problem does the outbox pattern solve?</b></summary>

The **dual-write problem**: updating the DB and publishing an event are two systems, so one can succeed while the other fails. With an outbox, you write the business row **and** an outbox row in the same DB transaction, and a relay (or CDC) publishes the outbox rows to the broker. Events are never lost or invented.

</details>

<details>
<summary><b>Q4. How does a circuit breaker work?</b></summary>

**Closed**: calls flow normally while failures are counted. Past a threshold it goes **open**: calls fail fast (or use a fallback) without hitting the sick dependency. After a cooldown it goes **half-open** and lets a few trial calls through. Success closes it; failure reopens it. This prevents cascading failures and thread exhaustion.

</details>

<details>
<summary><b>Q5. Why should each microservice own its database?</b></summary>

Loose coupling: services can change their schemas, scale, and choose storage technology independently, and one service's heavy queries can't take down another's. Data is shared through **APIs and events**, not shared tables. The cost: no cross-service joins and eventual consistency between services.

</details>
