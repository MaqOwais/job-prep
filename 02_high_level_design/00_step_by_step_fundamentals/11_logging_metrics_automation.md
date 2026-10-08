# Step 11 of 13: Logging, Metrics & Automation

[🏠 Overview](README.md) · **← Prev** [Step 10](10_message_queue.md) · **Next →** [Step 12: Sharding](12_database_sharding.md)

## 📍 Where we are
Dozens of servers, several data stores, queues, and workers across data centers.

## 🚨 The problem
- A user reports "checkout failed". **Which** of 50 servers handled it? What happened?
- Is the system healthy right now? Is latency rising? Is a queue backing up?
- Deploying by hand to 50 servers in 2 regions is slow and error-prone. One mistake causes an outage.

**At this size, you can't run what you can't see, and you can't change it safely by hand.**

## 💡 The fix: observability + automation
### 1. Logging
- Every service writes **structured logs** (JSON with timestamp, level, service, request_id, user_id, message).
- **Ship them to a central system** (ELK/OpenSearch, CloudWatch Logs, Datadog) so you can search across all servers.
- A **correlation / trace ID** generated at the edge and passed through every call lets you follow one request across services.

### 2. Metrics
| Level | Examples |
|---|---|
| Host | CPU, memory, disk, network |
| Aggregated / service | Request rate, **error rate**, **latency p50/p95/p99**, cache hit rate, DB connections, queue depth |
| **Business** | Daily active users, signups, orders/minute, revenue, retention |
- Dashboards (Grafana, CloudWatch) + **alerts** on symptoms users feel (error rate > 1%, p99 > 1 s), routed to on-call.
- The **4 golden signals:** latency, traffic, errors, saturation.

### 3. Tracing
**Distributed tracing** (OpenTelemetry, X-Ray, Jaeger) shows the time spent in each service for a request, so you can find the slow hop.

### 4. Automation
- **CI/CD:** every commit → build → automated tests → deploy through staging → production.
- **Infrastructure as code** (Terraform, CloudFormation, CDK): servers, networks, and databases defined in version-controlled code, so every region is identical and reproducible.
- **Safe deploys:** rolling, **blue/green**, **canary** (1% → 10% → 100%) with automatic rollback on alarms; feature flags.
- **Autoscaling** policies and **self-healing** (replace unhealthy instances automatically).

```
Code ──▶ CI (build, test) ──▶ CD (canary → full) ──▶ Servers ──logs/metrics/traces──▶ Observability ──alerts──▶ On-call
                                       ▲                                                   │
                                       └────────── auto-rollback on bad metrics ◀──────────┘
```

## ⚖️ Pitfalls
- **Too many alerts:** if people learn to ignore pages, they'll miss the real one. Alert on symptoms, not every CPU blip.
- **High-cardinality metrics** (user_id as a label) blow up metrics storage.
- Logs cost money: sample debug logs, set retention policies, never log secrets or PII.

## 🗣️ Say it in an interview
> "For operations: structured logs with a request ID shipped centrally, metrics on the golden signals plus business KPIs, distributed tracing, and alerts on SLO breaches. Everything is deployed through CI/CD with canary releases and infrastructure as code, so regions stay identical."

## 🔗 Go deeper
- Design problem: [metrics & monitoring system](../12_problems/hard/27_metrics_monitoring.md) · [Microservices: deployment strategies](../04_application_layer_microservices/)
- [AI systems: LLM observability](../../08_ai_system_design/concepts/05_evaluation_observability.md)

## ✅ Self-check
- [ ] How do you follow one user request across 10 services?
- [ ] Name the 4 golden signals
- [ ] Explain a canary deployment with auto-rollback
- [ ] Why use infrastructure as code with multiple data centers?

**Next →** [Step 12: Database sharding](12_database_sharding.md)
