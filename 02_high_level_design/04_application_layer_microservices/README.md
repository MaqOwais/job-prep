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
