# AWS Associate Startup Solutions Architect: Interview Prep Plan

**Role:** Associate Startup Solution Architect, AWS Startups (Job ID 10528615)
**Location:** San Francisco, CA | **Base pay:** $122.6K–$185K, plus sign-on and RSUs
**Prepared for:** Muhammed Abdul Quadir Owais | **Created:** 2026-10-08

---

## 0. How to use this plan

1. Read Part 1 (the role) and Part 2 (where you stand) once.
2. Use the **4-week schedule (Part 9)** as your day-to-day guide. If the interview is sooner, use the **7-day crash plan** at the end of Part 9.
3. Parts 3–7 are your study material, starting from the basics.
4. Part 8 (Leadership Principles stories) is **at least half of the interview**. Don't leave it for the end.

---

# PART 1 — Understanding the Role

## 1.1 What an Associate Startup SA actually does

A Solutions Architect (SA) is a **technical advisor**. You don't write the customer's production code. You help startup founders and CTOs **choose the right architecture on AWS**, then help them build it well. "Associate" means early career: you're hired for potential, fundamentals and learning speed, not for 10 years of experience.

Here's how the job description breaks down:

| JD line | What it means day to day | What they'll test |
|---|---|---|
| "Help startups choose suitable architecture at each stage of their lifecycle" | A 3-person pre-seed team needs a cheap, simple serverless MVP. A Series B company needs multi-AZ, multi-account setup, compliance and cost control. | Architecture whiteboarding: "Design X for a startup" |
| "Scalable, reliable, and secure solutions" | Well-Architected reviews: HA, DR, IAM, encryption | Networking, security and database fundamentals |
| "Drive adoption of a broad range of AWS services" | Know the service catalog well enough to recommend the *right* one, which isn't always the most expensive one | AWS service breadth and tradeoffs |
| "Connect engineering teams with customers to inform the roadmap" | Write up customer feature requests and pass them to AWS service teams | Customer Obsession, Earn Trust |
| "Build relationships with accelerators, incubators, VCs" | Office hours at Y Combinator or Techstars-style programs, VC portfolio days | Communication, presence |
| "Create startup-focused technical content" | Blog posts, sample GitHub repos, talks at meetups and AWS Summits | Do you write, teach or present? |

**Basic qualifications (you clearly meet both):**
- One of Python, Ruby, Node.js, C#, C++ → **you have Python and C#** ✅
- Two or more of networking, security, storage/databases, operating systems → **you have databases (MongoDB, Redis, PostgreSQL). Networking and security are your weaker areas, so this plan strengthens them.**

**Preferred qualifications:**
- Implemented a cloud-based solution → **your Django + EC2 + S3 + Lambda + CodeDeploy thesis app** ✅
- Cloud architecture, system design, software dev, data engineering or DevOps → **SWE II at ThoughtSpot, CI/CD, MLOps** ✅

## 1.2 Why AWS Startups cares so much about GenAI right now

Most early-stage startups coming to AWS today are building **AI products**: LLM apps, RAG, agents, fine-tuning. AWS Startups heavily pushes **Amazon Bedrock**, **Bedrock AgentCore / Agents**, **SageMaker AI**, and the **AWS Generative AI Accelerator**. **Your agentic AI work (orchestrator/router agents, LangChain, LLMs) is your biggest differentiator.** Lead with it.

## 1.3 The Amazon interview process (what to expect)

The posting doesn't describe the process, but SA hiring at AWS usually follows this pattern. Confirm details with your recruiter.

1. **Recruiter screen** (~20–30 min): background, why AWS, logistics, work authorization.
2. **Phone screen** (~45–60 min) with an SA or manager: **2 Leadership Principle questions + technical fundamentals** (networking, security, DBs, AWS basics). It might include a small architecture question.
3. **Virtual "Loop"** (4–5 interviews, ~55 min each, often on the same day):
   - Every interviewer is assigned **2–3 Leadership Principles**. Expect roughly **2 behavioral questions per round**.
   - **Technical depth rounds:** fundamentals (networking, security, storage/DB, OS) and AWS services.
   - **Architecture whiteboard / customer role-play:** "I'm a startup CTO building X. Help me." You ask clarifying questions, design, and discuss tradeoffs and cost.
   - Sometimes a **presentation** or "teach me something technical" round, which tests the content-creation side of the job.
   - Possibly light **coding** (Python): usually easy/medium, sometimes "write a Lambda handler" or "parse this JSON".
   - One interviewer is the **Bar Raiser**: someone from outside the team with veto power who focuses on LPs and long-term hiring quality.
4. **Debrief → offer.** Usually within about 5 business days.

**Key fact:** Amazon interviewers write down your answers nearly word for word and score them against LPs. **Vague answers with "we" score poorly. Specific "I" answers with numbers score well.**

---

# PART 2 — Where You Stand (Gap Analysis From Your Resume)

## 2.1 Strengths you should use

| Strength | Evidence on your resume | How to use it |
|---|---|---|
| Real industry SWE experience | SWE II @ ThoughtSpot, GraphQL, microservices, 15% latency improvement, mentoring | Deliver Results and Ownership stories, plus system design credibility |
| Hands-on AWS | EC2, S3, Lambda, SQS, CodeDeploy, CI/CD; AWS AI cert | "Implemented cloud-based solution" ✅ |
| **GenAI / agentic AI** | Multi-agent orchestrator/router, LangChain, OpenAI/HF | **Biggest differentiator.** Startups are building exactly this. |
| Research mindset | VAEs, KDE, manifolds, papers in progress | Learn & Be Curious, Dive Deep, Invent & Simplify |
| Customer impact with real users | VR therapy for brain-injury patients, 60% setup time saved | Customer Obsession: patients and clinicians were your "customers" |
| Open source | SymPy PRs, code reviews | Earn Trust, collaboration |
| Problem-solving | 570+ LeetCode | You won't struggle in any coding round |

## 2.2 Gaps to close (in priority order)

| # | Gap | Why it matters | Fix (Part of this plan) |
|---|---|---|---|
| 1 | **Networking fundamentals** (TCP/IP, DNS, subnetting, VPC) | Named in basic quals and asked in nearly every SA loop | Part 3.1 + Part 4.3 + VPC lab |
| 2 | **Security** (IAM, encryption, KMS, shared responsibility) | Named in basic quals and is "job zero" at AWS | Part 3.2 + Part 4.5 |
| 3 | **AWS breadth** beyond EC2/S3/Lambda (VPC, RDS/Aurora, DynamoDB, ECS/Fargate, CloudFront, Bedrock) | You need to recommend services across the whole catalog | Part 4 + SAA certification |
| 4 | **Architecture whiteboarding** in a customer conversation | Core of the loop | Part 5 + mock practice |
| 5 | **Customer-facing / communication evidence** | SA is a customer-facing role | Frame research, mentoring and SymPy work as customer and stakeholder stories (Part 8) |
| 6 | **Linux / OS basics** | One of the four basic-qual areas | Part 3.4 |
| 7 | **IaC (CDK/CloudFormation), containers, cost optimization** | Startups ask about these constantly | Part 4 + labs |
| 8 | **Startup ecosystem knowledge** (funding stages, Activate, VCs) | Specific to this team | Part 6 |
| 9 | **Technical content portfolio** | JD explicitly asks for blog posts and sample code | Write 1 blog post + 1 GitHub sample (Part 9, Week 3) |

## 2.3 Resume claims you MUST be ready to defend (Dive Deep follow-ups)

Interviewers *will* probe these. Prepare a precise 2-minute explanation for each:

- **"Synthetic data … up to 99% accuracy"**: Accuracy of *what*? Define the metric (e.g., a classifier trained on synthetic data and tested on real data? statistical similarity? cluster agreement via K-means/GMM?). If you can't define it clearly, it hurts your credibility.
- **"80% of patients got better with VR therapy"**: Sample size? How was "better" measured? (Be honest. The case report is about one patient. Know exactly what the manuscript claims.)
- **"Saved 60% setup time"**: What was the baseline, what did you change, and how did you measure it?
- **"15% response time improvement / 10% feature adoption"** at ThoughtSpot: Which metric (p50/p95 latency)? How did you measure it? What did you change in GraphQL (batching, DataLoader, caching, fewer round trips)?
- **"19% reduced learning time, 9% data fidelity"** (AIENs): 9% relative to what baseline?
- **"Contributing to multi-million-dollar revenue"** in your summary: Be ready to explain the connection, or soften the wording.
- **"5+ years of programming"**: Be ready to explain the timeline (college + SymPy from 2019 + industry).
- **The 13-month ThoughtSpot tenure**: Have a clean, positive reason ready (you left to do your MS in the US).

## 2.4 Quick resume fixes before you apply or interview

- Add a **"Cloud/AWS"** skills line: EC2, S3, Lambda, SQS, CodeDeploy, IAM, CloudWatch, plus **Bedrock** once you've done the lab.
- Remove duplicates ("Agentic AI" appears twice in one tech line; "Django" appears twice in skills).
- Fix the typo "Micheal" → "Michael" (unless that's the professor's actual spelling).
- "applying your Core Java" → "applying Core Java".
- Update the education dates. Dec '25 is past, so mark the degree as completed.
- Move AWS certifications into their own **Certifications** line, with the exact name (e.g., "AWS Certified AI Practitioner") and year.
- Consider a one-line headline for the target role: *"Software Engineer → Cloud Solutions Architect | AWS | GenAI/Agentic AI"*.

---

# PART 3 — Technical Fundamentals From the Basics

These four areas are the **basic qualifications**. Know each topic well enough to explain it to a founder on a whiteboard.

## 3.1 Networking fundamentals

### OSI / TCP-IP model
| Layer | Name | Examples | AWS relevance |
|---|---|---|---|
| 7 | Application | HTTP, HTTPS, DNS, gRPC, WebSocket | ALB, API Gateway, CloudFront, WAF |
| 6 | Presentation | TLS encryption, encoding | ACM certificates |
| 5 | Session | Session setup | — |
| 4 | Transport | **TCP** (reliable, ordered, 3-way handshake), **UDP** (fast, no guarantees) | NLB, Security Groups (ports) |
| 3 | Network | **IP**, routing, ICMP | VPC, route tables, subnets |
| 2 | Data link | MAC, Ethernet, ARP | ENIs |
| 1 | Physical | Cables, signals | AWS handles this |

**Be able to explain:** "What happens when you type `www.example.com` into a browser?"
1. Browser cache, then OS cache, then a **DNS resolver** query (recursive: root → TLD `.com` → authoritative nameserver, e.g. Route 53) → IP address
2. **TCP 3-way handshake** (SYN, SYN-ACK, ACK) on port 443
3. **TLS handshake**: certificate check, key exchange, session keys (symmetric)
4. HTTP request → CDN (CloudFront) → load balancer → app server → DB
5. Response, browser renders the page, then fetches additional assets

### IP addressing and CIDR (practice until it's automatic)
- IPv4 = 32 bits, e.g. `10.0.1.25`.
- **CIDR** `/n` = the first n bits are the network. Number of addresses = 2^(32−n).
  - `/16` = 65,536 | `/20` = 4,096 | `/24` = 256 | `/28` = 16
- **AWS reserves 5 IPs per subnet** (network address, VPC router, DNS, future use, broadcast). So a `/24` gives **251** usable addresses.
- **Private ranges (RFC 1918):** `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`.
- Typical VPC: `10.0.0.0/16`, split into `/24` or `/20` subnets per AZ.

### Other networking concepts
- **DNS record types:** A (IPv4), AAAA (IPv6), CNAME (alias to another name; can't be used at the zone apex), **Alias** (Route 53-specific; works at the apex and points to AWS resources), MX, TXT, NS.
- **TTL** and caching. Lowering TTL before a migration makes cutover faster.
- **NAT:** lets private IPs reach the internet through one public IP, outbound only.
- **Load balancing:** L4 (TCP/UDP, very fast, static IP → NLB) vs L7 (HTTP-aware, path/host routing → ALB). Algorithms: round robin, least connections. Health checks.
- **Proxy vs reverse proxy.** CDN = cache at the edge, closer to users.
- **Stateful vs stateless firewall** (this maps directly to Security Group vs NACL; see Part 4).
- **Latency vs bandwidth vs throughput.**
- **HTTP:** methods (GET/POST/PUT/PATCH/DELETE), status codes (2xx success, 3xx redirect, 4xx client error such as 401/403/404/429, 5xx server error such as 500/502/503/504), idempotency, REST vs GraphQL vs gRPC, WebSockets.
- **VPN vs dedicated link** (Site-to-Site VPN vs Direct Connect).

## 3.2 Security fundamentals

- **CIA triad:** Confidentiality, Integrity, Availability.
- **Authentication (who are you?) vs Authorization (what can you do?).**
- **Least privilege**, **defense in depth**, **zero trust**.
- **Encryption:**
  - *Symmetric* (AES-256): one key, fast, used for bulk data.
  - *Asymmetric* (RSA/ECC): public/private key pair, used for key exchange and signatures.
  - **At rest** (disk/S3/DB → KMS) vs **in transit** (TLS).
  - **Envelope encryption:** a data key encrypts the data, and a master key (KMS) encrypts the data key. This is how KMS works.
- **Hashing** (SHA-256: one-way) vs encryption (reversible). Store passwords with **bcrypt/argon2 plus a salt**.
- **TLS/HTTPS:** certificates, Certificate Authorities, chain of trust.
- **Identity standards:** OAuth 2.0 (authorization delegation), OpenID Connect (authentication on top of OAuth), **JWT** (signed token: header.payload.signature), SAML (enterprise SSO), MFA.
- **Common attacks:** SQL injection, XSS, CSRF, DDoS, credential leaks (keys committed to GitHub!), SSRF. Know the OWASP Top 10 at a headline level.
- **AWS Shared Responsibility Model:** AWS is responsible for security **OF** the cloud (hardware, facilities, hypervisor, managed-service infrastructure). The customer is responsible for security **IN** the cloud (data, IAM, OS patching on EC2, security groups, encryption choices). The split shifts with the service: with EC2 you do more; with Lambda, S3 and DynamoDB, AWS does more.

## 3.3 Storage and databases

### Storage types
| Type | What it is | AWS |
|---|---|---|
| **Block** | Raw disk volumes, attached to one machine | EBS (gp3, io2), instance store |
| **File** | Shared filesystem (NFS/SMB) | EFS, FSx |
| **Object** | Files + metadata in a flat namespace, accessed over HTTP | S3 |

### Database concepts
- **ACID:** Atomicity, Consistency, Isolation, Durability. These are relational transaction guarantees.
- **CAP theorem:** during a network Partition, choose Consistency or Availability. **BASE** = eventual consistency.
- **SQL (relational)** vs **NoSQL** (key-value, document, wide-column, graph):
  - SQL → structured data, joins, transactions, complex queries (Postgres/MySQL → **RDS / Aurora**)
  - Key-value at massive scale with known access patterns → **DynamoDB**
  - Document → **DocumentDB** (MongoDB-compatible) or DynamoDB
  - Cache → **ElastiCache (Redis/Valkey/Memcached)**
  - Graph → **Neptune** | Search → **OpenSearch** | Time-series → **Timestream**
  - Vectors (for RAG) → **OpenSearch Serverless, Aurora pgvector, S3 Vectors**, or third-party (Pinecone etc.)
- **Indexes:** B-tree, why they speed up reads but slow down writes.
- **Normalization vs denormalization.**
- **Scaling:** vertical (bigger machine) vs horizontal. **Read replicas** (scale reads, asynchronous) vs **Multi-AZ** (HA standby, synchronous, *not* for scaling reads). **Sharding/partitioning.**
- **Caching patterns:** cache-aside (lazy loading), write-through, TTL, cache invalidation. You did this in QEATS with Redis, so use that example.
- **OLTP vs OLAP** (transactions vs analytics → Redshift/Athena).
- **Backups:** point-in-time recovery, snapshots. **RPO** (how much data loss is acceptable) vs **RTO** (how long recovery can take).

## 3.4 Operating systems / Linux basics

- **Process vs thread**; context switching; concurrency vs parallelism (you used multithreading in QEATS/QMoney).
- **Memory:** stack vs heap, virtual memory, paging, swap, OOM killer.
- **File systems, inodes, permissions:** `chmod 755` (rwx = 4+2+1), `chown`, users/groups, `sudo`.
- **Essential commands:** `ls, cd, cat, less, grep, find, ps, top/htop, kill, df -h, du -sh, free -m, netstat/ss, curl, dig/nslookup, ping, traceroute, ssh, scp, tail -f, systemctl, journalctl, crontab`.
- **Boot and services:** systemd units, logs in `/var/log`.
- **Troubleshooting story:** "An EC2 web server is slow. How do you debug it?" → check CPU/memory/disk with CloudWatch and `top`/`df`, check the app logs, check DB connections, check network (SGs, latency), check recent deploys. **Be methodical.**
- **Containers vs VMs:** containers share the host kernel (namespaces + cgroups), are lighter and start faster. Docker image vs container; Dockerfile basics.

---

# PART 4 — AWS Services: What to Know and When to Recommend Each

Goal: for each service, know **what it is, when to use it, when NOT to use it, and roughly what it costs**.

## 4.1 Global infrastructure
- **Region** (geographic area, e.g. us-west-2) → **Availability Zones** (≥3 per region; isolated data centers with low-latency links) → **Edge locations** (CloudFront/Route 53).
- **High availability = spread across multiple AZs.** DR = multiple regions.
- Choose a region based on latency to users, data residency/compliance, service availability and price.

## 4.2 Compute: the startup decision tree
| Service | Use when | Startup angle |
|---|---|---|
| **Lambda** | Event-driven, spiky or low traffic, short tasks (≤15 min) | Pay per request, scales to zero. **Ideal for MVPs.** Watch for cold starts. |
| **ECS on Fargate** | Containerized apps, no servers to manage | The most common "grown-up" default for startups |
| **EKS** | Team already knows Kubernetes or needs portability | Powerful, but significant operational overhead. Don't push it on a 3-person team. |
| **App Runner / Elastic Beanstalk / Amplify Hosting** | Simplest path from code or container to URL | Great for very early stage |
| **EC2** | Full control, special hardware (GPU), legacy apps | Use Auto Scaling Groups + ALB. Graviton (ARM) is ~20–40% better price-performance. |
| **Lightsail** | Simple VPS, fixed monthly price | Hobby or very small projects |
| **Batch** | Batch jobs at scale | ML preprocessing, simulations |

**EC2 pricing models:** On-Demand → **Savings Plans / Reserved Instances** (1–3 year commitment, up to ~72% off) → **Spot** (up to ~90% off, can be interrupted; good for batch jobs, CI, training) → Dedicated Hosts.
**Instance families:** t (burstable), m (general purpose), c (compute), r (memory), g/p (GPU), inf/trn (AWS Inferentia/Trainium AI chips).

## 4.3 Networking (VPC): draw this from memory
```
Region
└── VPC 10.0.0.0/16
    ├── AZ-a: Public subnet 10.0.1.0/24  (ALB, NAT GW)  ── route 0.0.0.0/0 → Internet Gateway
    │         Private subnet 10.0.11.0/24 (app/ECS)     ── route 0.0.0.0/0 → NAT Gateway
    │         Private DB subnet 10.0.21.0/24 (RDS)      ── no internet route
    └── AZ-b: (same three tiers, mirrored)
```
- **Internet Gateway (IGW):** gives the VPC internet access. A subnet is "public" only because its route table points to the IGW.
- **NAT Gateway:** outbound-only internet for private subnets. **It's expensive** (hourly + per-GB). Startups often get surprised by this. Use one per AZ for HA, or one total to save money in dev environments.
- **Security Group** vs **NACL** (classic question):

| | Security Group | NACL |
|---|---|---|
| Level | Instance/ENI | Subnet |
| State | **Stateful** (return traffic automatically allowed) | **Stateless** (must allow both directions) |
| Rules | Allow only | Allow and Deny |
| Evaluation | All rules evaluated | Numbered order, first match wins |

- **VPC Endpoints:** *Gateway* (S3, DynamoDB; free) and *Interface* (PrivateLink; for most other services). These keep traffic off the internet and reduce NAT cost.
- **VPC Peering** (1:1, non-transitive) vs **Transit Gateway** (hub-and-spoke for many VPCs).
- **Route 53:** DNS + routing policies (simple, weighted, latency, failover, geolocation) + health checks.
- **CloudFront:** CDN, edge caching, TLS, works with S3 (Origin Access Control) and WAF.
- **ALB** (L7, path/host routing, HTTP/2, WebSockets) vs **NLB** (L4, static IP, extreme performance) vs **Gateway LB** (for security appliances).
- **API Gateway:** REST/HTTP/WebSocket APIs, throttling, auth (Cognito/JWT/Lambda authorizer). It pairs naturally with Lambda.
- **Hybrid connectivity:** Site-to-Site VPN, Direct Connect.

## 4.4 Storage
- **S3:** 11 nines (99.999999999%) durability. Storage classes: Standard → Intelligent-Tiering → Standard-IA → One Zone-IA → Glacier Instant/Flexible/Deep Archive. **Lifecycle policies**, versioning, replication (CRR/SRR), presigned URLs, static website hosting, event notifications → Lambda. Block Public Access is on by default.
- **EBS:** block storage for EC2, tied to one AZ, snapshots stored in S3. gp3 is the default; io2 for high IOPS.
- **EFS:** shared NFS across many instances and AZs, scales automatically.
- **FSx:** Windows file shares, Lustre (HPC/ML).

## 4.5 Security, identity and governance
- **IAM:** users, groups, **roles** (preferred: temporary credentials), **policies** (JSON: Effect, Action, Resource, Condition). Explicit Deny always wins. **Never use root**; enable MFA. Use roles for EC2/Lambda instead of access keys.
- **IAM Identity Center (SSO)** for human access across accounts.
- **AWS Organizations + SCPs + Control Tower**: multi-account setup (separate prod/dev/security accounts). Recommend this at Series A and later.
- **Cognito:** user sign-up/sign-in for the startup's *own* app users (user pools), social login, JWTs.
- **KMS** (encryption keys, envelope encryption), **Secrets Manager** (rotating DB credentials, API keys), **SSM Parameter Store** (config, cheaper).
- **ACM** (free TLS certificates for ALB/CloudFront).
- **WAF** (L7 rules: SQLi/XSS, rate limiting, bot control), **Shield** (DDoS; Standard is free, Advanced is paid).
- **GuardDuty** (threat detection), **Security Hub** (posture dashboard), **Inspector** (vulnerability scans), **Macie** (finds PII in S3), **CloudTrail** (API audit log: "who did what"), **Config** (resource configuration history and compliance).
- **Compliance:** AWS Artifact (reports for SOC 2, HIPAA, PCI). Startups selling to enterprises need SOC 2, so this comes up often.

## 4.6 Databases (when to recommend which)
| Need | Recommend | Why |
|---|---|---|
| Standard relational app | **Aurora PostgreSQL/MySQL** or **RDS** | Managed, Multi-AZ, read replicas |
| Spiky or unpredictable relational load | **Aurora Serverless v2** | Scales capacity automatically |
| Massive scale, simple key access, serverless | **DynamoDB** | Single-digit-ms latency, on-demand pricing, Streams, global tables |
| Caching / sessions / leaderboards | **ElastiCache (Valkey/Redis)** | Sub-ms latency |
| Search / log analytics / vector search | **OpenSearch** | Full-text + vector search |
| Analytics / data warehouse | **Redshift (Serverless)** / **Athena** on S3 | OLAP |
| Graph relationships | **Neptune** | Fraud detection, social graphs |

**DynamoDB basics:** partition key (+ optional sort key), GSI/LSI, design for your access patterns first, single-table design, avoiding hot partitions, on-demand vs provisioned capacity, TTL, Streams → Lambda.

## 4.7 Application integration (decoupling)
- **SQS:** queue, one consumer group, buffering/decoupling, retries, **DLQ** (dead-letter queue), Standard (at-least-once, best-effort ordering) vs FIFO (exactly-once processing, ordered).
- **SNS:** pub/sub fan-out to many subscribers. **SNS → multiple SQS queues** is the classic fan-out pattern.
- **EventBridge:** event bus with content-based routing rules, SaaS integrations, scheduler. A good default for event-driven startups.
- **Step Functions:** orchestrate multi-step workflows with retries and branching (also useful for orchestrating AI agent pipelines).
- **Kinesis Data Streams / Firehose** (or **MSK** for Kafka): real-time streaming.

## 4.8 Observability and operations
- **CloudWatch:** metrics, logs, alarms, dashboards. **X-Ray / CloudWatch Application Signals:** distributed tracing. **CloudTrail:** audit.
- **Systems Manager:** Session Manager (SSH without opening port 22), Patch Manager, Parameter Store.

## 4.9 DevOps and Infrastructure as Code (startups love this)
- **IaC:** **AWS CDK** (write infra in Python/TypeScript → CloudFormation), **CloudFormation** (YAML/JSON), **SAM** (serverless shorthand), **Terraform** (multi-cloud, very common among startups).
- **CI/CD:** CodePipeline, CodeBuild, CodeDeploy (which you've used!), and GitHub Actions with OIDC to AWS (no stored keys). Deployment strategies: rolling, **blue/green**, **canary**.
- **ECR** (container registry).

## 4.10 AI/ML (your strongest card, so go deep)
- **Amazon Bedrock:** fully managed access to foundation models through one API (Anthropic Claude, Amazon Nova, Meta Llama, Mistral, Cohere, etc.). Covers:
  - **Knowledge Bases** (managed RAG: chunking, embeddings, vector store)
  - **Agents / AgentCore** (building, deploying and operating AI agents at scale: runtime, memory, gateway/tools, identity, observability)
  - **Guardrails** (content filtering, PII redaction, grounding checks)
  - **Model evaluation**, **fine-tuning / model customization**, **Provisioned Throughput**, **batch inference**, **prompt caching**, **model distillation**
- **SageMaker AI:** build, train and deploy your own models (training jobs, endpoints, HyperPod for large-scale training, JumpStart). **Inferentia / Trainium** chips for lower inference and training cost.
- **Amazon Q Developer / Kiro:** AI coding assistant and agentic IDE.
- **Pre-built AI services:** Rekognition (vision), Transcribe (speech-to-text), Polly (text-to-speech), Comprehend (NLP), Textract (document extraction), Translate.
- **Know these tradeoffs cold:**
  - **Prompting vs RAG vs fine-tuning vs training from scratch.** Start with prompting, then RAG for private or fresh data, then fine-tune for style/format/domain behavior. Pretraining is almost never right for a startup.
  - **Bedrock (managed, API) vs SageMaker (full control) vs self-hosting on EC2 GPUs.**
  - LLM cost levers: smaller models for simple tasks (routing), prompt caching, batch inference, token limits, response caching.
  - Evaluation, hallucination mitigation, latency (streaming), security (prompt injection, data privacy: Bedrock doesn't use customer data to train models).

> ⚠️ AWS launches and renames services often. Before the interview, spend 30 minutes on "What's New with AWS" and the AWS Startups blog to check current names and features, especially for Bedrock/AgentCore, and skim the latest re:Invent announcements.

## 4.11 Frameworks every SA must know

### AWS Well-Architected Framework: 6 pillars (memorize)
1. **Operational Excellence:** IaC, small reversible changes, observability, learning from failures
2. **Security:** identity foundation, traceability, security at every layer, encryption, automation
3. **Reliability:** automatic recovery, horizontal scaling, stop guessing capacity, multi-AZ
4. **Performance Efficiency:** right resource types, serverless, global reach, experimentation
5. **Cost Optimization:** pay for what you use, measure, Savings Plans, Spot, right-sizing
6. **Sustainability:** maximize utilization, managed services, efficient hardware (Graviton)

There's also a **Well-Architected Tool** and **Lenses** (Serverless, SaaS, GenAI, ML).

### Disaster recovery strategies (cheapest/slowest → most expensive/fastest)
| Strategy | RTO/RPO | Description |
|---|---|---|
| Backup & Restore | Hours | Backups in another region |
| Pilot Light | 10s of minutes | Core (DB) replicated, everything else off |
| Warm Standby | Minutes | Scaled-down full copy running |
| Multi-site Active/Active | Near zero | Full production in 2+ regions |

### Migration "7 Rs"
Retire, Retain, Rehost (lift-and-shift), Relocate, Replatform (lift-tinker-shift, e.g., move to RDS), Repurchase (move to SaaS), Refactor/Re-architect (cloud-native).

### Cost optimization checklist (a startup's favorite topic)
AWS Activate credits · Cost Explorer + **Budgets + alerts** · tagging · right-sizing (Compute Optimizer) · Graviton · Spot for fault-tolerant workloads · Savings Plans once usage is stable · serverless or scale-to-zero for dev · S3 lifecycle/Intelligent-Tiering · watch NAT Gateway and data-transfer costs · shut down dev environments at night · CloudFront to reduce egress · Trusted Advisor.

---

# PART 5 — Architecture Whiteboarding (the Core SA Skill)

## 5.1 A framework to use in every design question

**1. Clarify (spend 5–8 minutes here; interviewers score this heavily, because it's Customer Obsession)**
- What does the product do? Who are the users? How many now, and in 12 months?
- Traffic pattern: steady or spiky? Global or regional? Read-heavy or write-heavy?
- **Startup context:** funding stage, **team size and skills** (Python? containers? Kubernetes?), **budget / credits**, time to market.
- Data: type, volume, sensitivity (PII/PHI → HIPAA? payments → PCI?), retention.
- Requirements: latency, availability target (99.9%?), RTO/RPO.
- What exists already? (Greenfield, or migrating from Heroku, a VPS or another cloud?)

**2. State assumptions and requirements** (functional + non-functional). Write them on the board.

**3. High-level design.** Draw the boxes: users → DNS → CDN → API layer → compute → data → async → observability.

**4. Deep dive** on 1–2 components (data model, scaling, the AI pipeline).

**5. Tradeoffs:** "I'd pick X over Y because of your team size and budget. When you reach Z scale, migrate to Y." **Always explain why.**

**6. Cover the pillars:** security (IAM, encryption, WAF), reliability (multi-AZ, backups), cost (rough monthly estimate, credits), operations (IaC, CI/CD, monitoring).

**7. Evolution path:** what changes at 10× and 100× scale.

**8. Summarize** and ask: "Does this fit what you had in mind? What concerns you most?"

**Golden rule for startups:** *Simple, managed and serverless first. Avoid over-engineering. Optimize for team velocity and cost, and design so that scaling later doesn't require a rewrite.*

## 5.2 Reference architectures to practice drawing (do each one at least twice)

**A. Serverless MVP web/mobile app (pre-seed)**
Route 53 → CloudFront → S3 (React SPA) | API Gateway (HTTP API) → Lambda (Python) → DynamoDB | Cognito for auth | S3 for uploads via presigned URLs | CloudWatch | deploy with CDK/SAM + GitHub Actions. Cost: close to $0 at low traffic, and covered by credits.

**B. Containerized SaaS at Series A**
Route 53 → CloudFront + WAF → ALB → ECS Fargate services in private subnets across 2–3 AZs → Aurora PostgreSQL (Multi-AZ + read replica) + ElastiCache → SQS/EventBridge for async workers → S3 → Secrets Manager → CloudWatch/X-Ray → multi-account setup with Control Tower, CI/CD with blue/green deploys.

**C. Multi-tenant SaaS**
Tenant isolation models: **Silo** (separate stack/account per tenant: strongest isolation, highest cost), **Pool** (shared infra, tenant_id on every row, enforced by IAM/row-level security), **Bridge** (a mix: e.g., shared app tier, separate DB per tenant). Cover tenant onboarding, per-tenant metering and cost, and noisy-neighbor problems.

**D. GenAI RAG chatbot startup** (your sweet spot)
Ingestion: S3 (documents) → EventBridge/S3 event → Lambda/Step Functions → chunk → embed (Titan/Cohere embeddings via Bedrock) → vector store (OpenSearch Serverless / Aurora pgvector / S3 Vectors) **or simply Bedrock Knowledge Bases**.
Query: user → CloudFront → API Gateway (WebSocket for streaming) → Lambda/ECS → retrieve top-k → Bedrock LLM (Claude) with Guardrails → response, with citations.
Plus: DynamoDB for chat history, Cognito, CloudWatch + evaluation, caching for repeated queries, a cost-control plan (model routing, prompt caching, smaller models for classification), and privacy (data stays in the customer's account, VPC endpoints/PrivateLink to Bedrock).

**E. Multi-agent AI system** (connect to your research work)
Orchestrator/router agent → specialized agents (tools via Lambda, data fetch via APIs) → Bedrock AgentCore or Step Functions for orchestration, DynamoDB for memory/state, observability with tracing, guardrails, human-in-the-loop for risky actions.

**F. Data and analytics pipeline**
Ingestion (Kinesis Firehose / app events) → S3 data lake (raw → curated, Parquet) → Glue (catalog + ETL) → Athena (ad-hoc SQL) / Redshift Serverless → QuickSight dashboards. You can mention ThoughtSpot here as BI experience.

**G. ML training + inference (your thesis)**
S3 dataset → SageMaker training (Spot for cost) → model registry → SageMaker endpoint (or serverless/async inference) → API → monitoring for drift. Alternative: a container on ECS with GPU.

**H. Real-time features** (chat, notifications, live dashboards)
API Gateway WebSocket / AppSync (GraphQL subscriptions, which ties to your GraphQL experience) → Lambda → DynamoDB Streams → fan-out via SNS/EventBridge.

**I. High availability and DR for a growing fintech/healthtech**
Multi-AZ everything, Aurora Global Database, Route 53 failover, DynamoDB global tables, AWS Backup, an explicit RTO/RPO choice. Add compliance: HIPAA eligible services + BAA, encryption, CloudTrail, Config.

**J. Migration from Heroku / another cloud / a single VPS**
Assess → choose a migration "R" → set up landing zone (multi-account) → migrate DB with DMS → containerize the app onto ECS → DNS cutover with low TTL → optimize afterwards.

## 5.3 Classic technical questions (practice answering out loud in 1–2 minutes each)

1. Security Group vs NACL?
2. What makes a subnet public vs private?
3. How does a private instance reach the internet? How would you reduce NAT cost?
4. SQS vs SNS vs EventBridge vs Kinesis?
5. RDS Multi-AZ vs Read Replica?
6. DynamoDB vs Aurora: when would you pick each?
7. Lambda vs Fargate vs EC2?
8. How would you secure an S3 bucket that serves private user files?
9. IAM role vs IAM user? How do you avoid hard-coded keys?
10. What's in the shared responsibility model for EC2 vs Lambda?
11. What happens when you type a URL into a browser?
12. TCP vs UDP?
13. How does TLS work?
14. Explain encryption at rest vs in transit, and how KMS envelope encryption works.
15. How do you make an app highly available? Fault tolerant?
16. Explain RTO/RPO and the 4 DR strategies.
17. Vertical vs horizontal scaling; stateless application design (sessions → ElastiCache/DynamoDB).
18. How would you reduce a startup's AWS bill by 30%?
19. CAP theorem; eventual consistency example.
20. How does caching work, and what are the invalidation challenges?
21. A Lambda function is timing out. How do you debug it?
22. Users report slow page loads globally. What do you do?
23. RAG vs fine-tuning? How do you reduce hallucinations? How do you evaluate an LLM app?
24. Bedrock vs SageMaker vs self-hosting an open-source model?
25. How would you explain an API / the cloud / a container / Kubernetes to a non-technical founder?
26. How would you design a CI/CD pipeline for a startup?
27. What is Infrastructure as Code, and why does it matter for a startup?
28. Monolith vs microservices for a 5-person startup? (Answer: usually a modular monolith first. You can draw on ThoughtSpot experience to discuss microservices tradeoffs.)
29. What is a VPC endpoint and why use it?
30. How do you protect against DDoS and SQL injection on AWS?

## 5.4 Customer role-play tips
- **Listen more than you talk** at first. Repeat their problem back to them.
- **Ask about constraints before naming a service.**
- **It's fine to say "I don't know, but here's how I'd find out / here's my reasoning."** Amazon values intellectual honesty (Earn Trust) much more than bluffing.
- Translate everything into business terms: cost, time to market, risk.
- If the "customer" pushes back ("I want Kubernetes because it's cool"), respond respectfully with data: Have Backbone, then Disagree and Commit.
- Close with next steps: "I'll send you a reference architecture and a link to Activate credits, and set up a follow-up with a Bedrock specialist."

---

# PART 6 — Startup Ecosystem Knowledge (Team-Specific)

- **Funding stages:** Pre-seed (idea, founders, friends & family) → Seed (MVP, early traction; ~$1–4M) → Series A (product-market fit, scaling; ~$10–20M) → Series B/C+ (expansion, enterprise, compliance) → IPO/acquisition.
- **What a startup cares about at each stage:**
  - Pre-seed/Seed: **speed, cost, credits**, small team → serverless, managed services, simplicity
  - Series A: **scale, reliability, security basics**, hiring → containers, IaC, CI/CD, multi-AZ, SOC 2 prep
  - Series B+: **multi-account governance, compliance, cost optimization, global expansion, enterprise features** (SSO, tenant isolation)
- **AWS Activate:** a program that gives startups **AWS credits** (tiers run from a few thousand dollars up to six figures through approved VC/accelerator partners), technical support, and training. Check the current amounts on aws.amazon.com/activate before the interview.
- Also: the **AWS Generative AI Accelerator**, **AWS Marketplace** (startups sell through it to reach enterprise buyers), **AWS Partner Network (APN)**, the **AWS Startups blog**, and AWS Startup Loft events in SF.
- **Accelerators and VCs:** Y Combinator, Techstars, 500 Global; know names like Sequoia, a16z, Accel, Lightspeed. AWS SAs partner with them to support their portfolio companies.
- **Why startups pick (or don't pick) AWS:** breadth of services, credits, Bedrock model choice, security/compliance credibility, co-selling through Marketplace. The competition is GCP and Azure (credits, AI offerings). Speak about it respectfully, focused on customer benefits.
- **Read before the interview:** 3–5 AWS Startups blog posts, 2–3 recent case studies of AI startups on AWS. Mention one in the interview: "I read how [startup] used Bedrock to…"

---

# PART 7 — Coding Round (Light, but Be Ready)

You have 570+ LeetCode problems solved, so the DS&A itself won't be the problem. Focus on:
- **Python fluency without an IDE:** dicts, lists, sets, string manipulation, `collections.Counter/defaultdict`, sorting with keys, list comprehensions, exceptions.
- **Practical cloud-style tasks:**
  - Write a Lambda handler that reads an S3 event and writes to DynamoDB (using `boto3`)
  - Parse a JSON/CSV log file and compute counts or top-k
  - Call a REST API with retries and exponential backoff
  - Implement a simple rate limiter or LRU cache
- **Talk while you code.** Explain your approach and complexity, and test with edge cases.
- Do ~15 easy/medium problems (arrays, hashmaps, strings, intervals, BFS) over the 4 weeks just to stay sharp.

---

# PART 8 — Amazon Leadership Principles (≈50% of Your Score)

## 8.1 The 16 Leadership Principles (know each in one line)
1. **Customer Obsession:** Start with the customer and work backwards.
2. **Ownership:** Act on behalf of the whole company; never say "that's not my job."
3. **Invent and Simplify:** Find new, simpler ways of doing things.
4. **Are Right, A Lot:** Good judgment, seek diverse perspectives.
5. **Learn and Be Curious:** Never stop learning.
6. **Hire and Develop the Best:** Raise the bar, coach others.
7. **Insist on the Highest Standards:** Don't accept defects; raise the bar.
8. **Think Big:** Bold direction that inspires results.
9. **Bias for Action:** Speed matters; many decisions are reversible.
10. **Frugality:** Accomplish more with less.
11. **Earn Trust:** Listen, be candid, admit mistakes.
12. **Dive Deep:** Stay connected to details, audit frequently, be skeptical when metrics and anecdotes differ.
13. **Have Backbone; Disagree and Commit:** Challenge respectfully, then commit fully.
14. **Deliver Results:** Deliver on key inputs, with quality and on time, despite setbacks.
15. **Strive to be Earth's Best Employer:** Create a safe, productive, empathetic environment.
16. **Success and Scale Bring Broad Responsibility:** Consider the wider impact of your actions.

**Most important for SA roles:** Customer Obsession, Earn Trust, Learn and Be Curious, Dive Deep, Ownership, Bias for Action, Deliver Results, Invent and Simplify, Have Backbone, Are Right A Lot.

## 8.2 The STAR(+L) answer format
- **S**ituation (~15%): context, briefly
- **T**ask (~10%): *your* responsibility
- **A**ction (~50–60%): what **I** did, step by step, with technical detail and the decisions you made
- **R**esult (~15–20%): **numbers**, impact, and what the customer got
- **L**earning: what you'd do differently next time (Bar Raisers love this)

Rules:
- Say **"I"**, not "we". Target 2–3 minutes per answer.
- Use real, specific examples from the last few years, not hypotheticals.
- Expect 2–4 follow-ups: "What data did you use?" "What would you do differently?" "What did your manager say?" "What was the hardest part?"
- Have **at least 2 stories per key LP**, and make sure each story can cover 2–3 LPs. Don't reuse the same story with the same interviewer, and try not to repeat stories across the loop.
- Include **failure/mistake stories**. They will ask for them.

## 8.3 Your story bank: draft mapping from your resume

Fill in the details yourself using the template in 8.4. These are starting points.

| # | Story (from your resume) | Primary LPs | Notes / angle |
|---|---|---|---|
| 1 | **ThoughtSpot: new Homepage & Navigation with GraphQL** (15% faster, 10% adoption) | Deliver Results, Customer Obsession, Invent & Simplify | How did you know users struggled? What did the data say? Which GraphQL optimizations? |
| 2 | **ThoughtSpot: A/B testing components** | Dive Deep, Are Right A Lot, Customer Obsession | A case where the data contradicted what someone assumed? |
| 3 | **ThoughtSpot: Adding test pipelines for Teams edition** | Insist on Highest Standards, Ownership | Was it your idea, outside your assigned scope? Bugs caught? |
| 4 | **ThoughtSpot: Mentoring junior engineers** | Hire & Develop the Best, Earn Trust | A specific mentee, the specific growth, and the outcome |
| 5 | **VR project Phase 1: cross-platform HTC → Meta port, 60% setup time saved** | Customer Obsession (patients and clinicians), Ownership, Bias for Action, Deliver Results | **Your best customer story.** Real patients and clinicians with a real pain point. |
| 6 | **VR Phase 2: Designing the multi-agent architecture** (orchestrator/router) | Invent & Simplify, Think Big, Learn & Be Curious | Why multi-agent? Which tradeoffs did you consider? What failed first? |
| 7 | **Thesis: AWS deployment pipeline** (Django + EC2 + S3 + Lambda + CodeDeploy) | Ownership, Frugality, Bias for Action | Why these services? Cost? What would you change now? (Natural lead-in to the technical rounds.) |
| 8 | **Thesis research: KDE/VAE/manifolds; AIENs 19% less training time** | Dive Deep, Learn & Be Curious, Invent & Simplify | An experiment that failed → how you debugged it → what you changed |
| 9 | **Disagreement with an advisor/teammate on approach** (e.g., GAN vs VAE, or an architecture choice) | Have Backbone, Earn Trust | Find a real one. This question is almost guaranteed. |
| 10 | **QEATS: Redis caching + multithreading + JMeter load testing** | Dive Deep, Insist on Highest Standards | Scientific debugging of a performance issue |
| 11 | **SymPy open source: picking up abandoned work, code reviews** | Ownership, Earn Trust, Learn & Be Curious | Taking over someone else's unfinished PR; handling reviewer feedback |
| 12 | **Learning a new stack fast** (Unity/C# for VR, or AWS for thesis) | Learn & Be Curious, Bias for Action | Show how quickly you got productive |
| 13 | **Moving countries / doing MS while doing research** | Deliver Results under pressure | Use carefully, and keep it professional |
| 14 | **A mistake or failure** (a production bug you shipped, a missed deadline, a wrong experiment) | Earn Trust, Ownership | Be honest about the mistake, then show what you fixed and what you learned |
| 15 | **Explaining something technical to a non-technical person** (clinicians, professors from other fields, patients) | Earn Trust, Customer Obsession | **Very relevant for an SA role.** Prepare this one carefully. |
| 16 | **Making a decision with incomplete data / tight deadline** | Bias for Action, Are Right A Lot | Possibly from ThoughtSpot releases or the VR study timeline |

## 8.4 Story template (copy this for each story)
```
Title:
LPs:
Situation (2 lines):
Task — my specific responsibility:
Actions — what I did (4–6 bullets with technical detail):
  1.
  2.
  3.
Result — numbers + customer impact:
Learning / what I'd do differently:
Likely follow-ups + my answers:
```

## 8.5 Common LP questions (practice all of them)

**Customer Obsession**
- Tell me about a time you went above and beyond for a customer.
- A time you had to understand a customer's need that they couldn't express clearly.
- A time you said no to a customer or balanced their request against what was best for them.

**Ownership**
- A time you took on something outside your area of responsibility.
- A time you made a decision with long-term impact versus a short-term win.

**Invent and Simplify**
- Describe the most innovative thing you've done.
- A time you simplified a complex process.

**Are Right, A Lot**
- A time you made a decision without enough data.
- A time you were wrong.

**Learn and Be Curious**
- How do you stay current with technology? (Mention specifics: AWS What's New, re:Invent, papers, Kaggle.)
- A time you learned a new technology quickly to solve a problem.

**Insist on the Highest Standards**
- A time you refused to compromise on quality.
- A time you raised the bar for your team.

**Bias for Action**
- A time you made a quick decision with limited information.
- A time you took a calculated risk.

**Frugality**
- A time you delivered with limited resources or budget.

**Earn Trust**
- A time you received critical feedback. What did you do?
- A time you had to deliver bad news.
- A time you made a mistake.

**Dive Deep**
- A time you found the root cause of a difficult problem.
- A time the data contradicted your intuition.

**Have Backbone; Disagree and Commit**
- A time you disagreed with your manager or a senior person.
- A time you committed to a decision you didn't agree with.

**Deliver Results**
- Your most significant accomplishment.
- A time you missed a deadline, or nearly did.
- A time you faced a major obstacle on a project.

**Hire and Develop the Best**
- A time you mentored or helped someone grow.

**Think Big**
- A time you proposed a bold idea.

## 8.6 "Why" questions (have polished 60–90 second answers)
- **Tell me about yourself.** Use present → past → future: "I'm a software engineer and ML researcher who just finished an MS in CS… At ThoughtSpot I… In my research I built AWS pipelines and multi-agent GenAI systems… I want to help startups make the same architecture decisions I've had to make myself, at the speed they need."
- **Why AWS?** Breadth and leadership in cloud and GenAI (Bedrock), the LP culture, the learning opportunities, and working on the platform you already build on.
- **Why Solutions Architect, not SWE?** You enjoy the *decision* layer (choosing architectures and tradeoffs), explaining tech to others (mentoring, research communication), and variety across many customers. You still keep your hands technical.
- **Why startups?** Fast pace, real impact, early architecture decisions matter most, and the GenAI startup wave matches your skills. Mention your own experience building things from scratch.
- **Where do you see yourself in 3–5 years?** Becoming a specialist SA in GenAI/ML for startups, publishing technical content, speaking at AWS Summits.

## 8.7 Questions to ask your interviewers (pick 2 per round)
- What does a typical week look like for an Associate SA on the Startups team? How is time split between customers, learning, and content?
- How are associates onboarded and mentored? Is there a specialty track (e.g., GenAI)?
- What are the most common architecture challenges you see with early-stage startups right now?
- How do you measure success for an SA in the first 6–12 months?
- Can you share an example of a customer request that turned into an AWS roadmap change?
- What separates SAs who thrive on this team?

---

# PART 9 — The Schedule

Assumes roughly **3–4 hours/day on weekdays and 5–6 hours on weekends**. Adjust if your interview date is set.

## Week 1: Foundations (networking, security, core AWS)
| Day | Focus | Tasks |
|---|---|---|
| 1 | Setup + role | Read this plan. Read the JD 3 times. Read amazon.jobs "How We Hire" + the LP page. Create an AWS Free Tier account with **billing alarms + MFA on root**. Start the story bank document. |
| 2 | Networking I | OSI/TCP-IP, TCP vs UDP, DNS walkthrough, HTTP. Practice: "What happens when you type a URL?" out loud. |
| 3 | Networking II | CIDR/subnetting drills (do 20 problems), NAT, load balancers. |
| 4 | AWS VPC | Study 4.3. **Lab:** build a VPC by hand: 2 AZs, public + private subnets, IGW, NAT GW, route tables, SGs, EC2 in a private subnet reached via SSM Session Manager. **Delete the NAT GW afterwards (cost!).** |
| 5 | Security I | CIA, encryption, TLS, OAuth/JWT, OWASP headline list, shared responsibility model. |
| 6 | IAM + KMS | Write 3 IAM policies by hand (S3 read-only on one bucket, Lambda execution role, a deny-based policy). Envelope encryption. **LP:** write 3 stories (5, 1, 14). |
| 7 | Review + mock | Explain 10 questions from 5.3 out loud and record yourself. Write 3 more LP stories (9, 15, 7). |

## Week 2: AWS breadth + databases + OS
| Day | Focus | Tasks |
|---|---|---|
| 8 | Compute | EC2 families/pricing, ASG, Lambda, ECS/Fargate, EKS, App Runner. Build the "which compute?" decision tree from memory. |
| 9 | Storage + DB concepts | S3 deep dive, EBS/EFS, ACID/CAP, indexing, replication vs Multi-AZ. |
| 10 | Databases on AWS | RDS/Aurora, DynamoDB data modeling (design 2 tables by access pattern), ElastiCache. **Lab:** API Gateway + Lambda + DynamoDB CRUD API. |
| 11 | Integration | SQS/SNS/EventBridge/Step Functions/Kinesis. **Lab:** S3 upload → Lambda → SQS → Lambda worker with a DLQ. |
| 12 | Linux/OS | Processes, memory, permissions, 30 commands, troubleshooting flow, containers vs VMs. Write a Dockerfile and push the image to ECR. |
| 13 | Well-Architected + DR + cost | Memorize the 6 pillars, 4 DR strategies, 7 Rs, cost checklist. Read the Well-Architected Framework overview whitepaper. |
| 14 | Mock #1 | Full mock: 2 LP questions + 15 minutes of fundamentals + 1 design (Architecture A). Ask a friend, use Pramp, or record yourself. Write 4 more stories (2, 3, 4, 10). |

**Optional but strongly recommended:** register for **AWS Certified Solutions Architect – Associate (SAA-C03)** around the end of Week 4. Even if you only *study* for it, it covers about 70% of the technical content in this plan. Use Adrian Cantrill's or Stephane Maarek's course and Tutorials Dojo practice exams.

## Week 3: Architecture + GenAI + startup context + content
| Day | Focus | Tasks |
|---|---|---|
| 15 | Design framework | Study Part 5.1. Practice architectures A and B on paper or Excalidraw, timed at 35 minutes each. |
| 16 | GenAI on AWS | Bedrock, Knowledge Bases, Agents/AgentCore, Guardrails, RAG vs fine-tuning. **Lab:** a small Bedrock RAG app (S3 docs → Knowledge Base → Lambda API → Claude). |
| 17 | GenAI architectures | Practice architectures D and E. Prepare to explain your multi-agent research with an AWS mapping. |
| 18 | SaaS + data | Architectures C and F. Multi-tenancy patterns. |
| 19 | Startup ecosystem | Part 6. Read 5 AWS Startups blog posts and 2 AI startup case studies. Learn Activate details. |
| 20 | **Content creation** | Turn the Day 16 RAG lab into a **public GitHub repo with a CDK deploy + README**, and write a **short blog post** (Medium/Dev.to/LinkedIn): "Building a RAG app on Amazon Bedrock in an afternoon: an architect's notes." Put the link on your resume and LinkedIn. **This directly proves the "create technical content" part of the JD.** |
| 21 | Mock #2 | Full 60-minute mock with a customer role-play ("I'm a seed-stage healthtech founder…"). Finish your story bank (16 stories). |

## Week 4: Polish + mocks + final review
| Day | Focus | Tasks |
|---|---|---|
| 22 | IaC + CI/CD | CDK basics (deploy the Day 10 API with CDK), GitHub Actions with OIDC to AWS, blue/green/canary. |
| 23 | Architectures G, H, I, J | Timed practice. Put DR/HA and cost optimization into every design. |
| 24 | Dive Deep on your resume | Prepare 2-minute deep explanations for every claim in 2.3. Practice "explain my thesis to a 10-year-old / to a founder / to an ML expert." |
| 25 | Mock #3 (LP-heavy, Bar Raiser style) | 4 LP questions with aggressive follow-ups. Fix weak stories. |
| 26 | Coding refresh | 5 Python problems + the boto3 Lambda-handler exercise + a retry/backoff function. |
| 27 | Rapid review | Re-do the 30 questions in 5.3. Check AWS What's New for the latest Bedrock/AgentCore updates. Prepare questions for interviewers. |
| 28 | Rest + logistics | Light review only. Test your camera/mic, whiteboard tool (often Amazon Chime/Zoom + a shared whiteboard or paper), and lighting. Sleep well. |

## If you only have 7 days (crash plan)
1. **Day 1:** Networking (3.1) + VPC (4.3). Draw a VPC 3 times.
2. **Day 2:** Security (3.2) + IAM/KMS (4.5) + shared responsibility.
3. **Day 3:** Compute + DB + integration (4.2, 4.6, 4.7) + Well-Architected / DR / cost.
4. **Day 4:** Design framework (5.1) + architectures A, B, D. Run the Bedrock RAG lab if time allows.
5. **Day 5:** Write 10 STAR stories (priority: 5, 1, 9, 14, 15, 6, 7, 3, 4, 8).
6. **Day 6:** Two full mocks (LP + design), and fix the weakest areas.
7. **Day 7:** Review the 30 questions, resume deep-dives (2.3), "why" answers, questions to ask. Rest.

---

# PART 10 — Interview Day Checklist

- [ ] Quiet room, stable internet, camera at eye level, a pen and paper or whiteboard tool ready
- [ ] Your story bank open on a second screen (key words only; don't read from it)
- [ ] Water nearby. Join 5 minutes early.
- [ ] For every design question: **clarify first**, think out loud, state tradeoffs, mention cost and security
- [ ] For every LP question: **STAR, "I", numbers, a learning**. Pause for 5 seconds to pick the best story, which is fine.
- [ ] If stuck: "Let me think through this from first principles…" Never bluff. Say what you'd verify.
- [ ] Ask 2 good questions at the end of every round
- [ ] Send a thank-you email to your recruiter afterwards

---

# PART 11 — Resources

**Official AWS (free)**
- amazon.jobs → "How We Hire," "Leadership Principles," "Interviewing at Amazon" (the STAR guide)
- AWS Skill Builder (free courses): *Cloud Practitioner Essentials*, *Architecting on AWS*, *Generative AI Learning Plan*
- AWS Well-Architected Framework whitepaper + Serverless, SaaS and Generative AI Lenses
- AWS Architecture Center (reference architectures) and "This Is My Architecture" videos (YouTube)
- AWS Startups blog + aws.amazon.com/startups + AWS Activate page
- "What's New with AWS" + the latest re:Invent keynote summaries
- AWS Workshops (workshops.aws): Bedrock workshop, Serverless workshop, VPC workshop

**Courses and practice**
- Adrian Cantrill (SAA-C03): best for deep networking fundamentals
- Stephane Maarek (Udemy, SAA-C03) + Tutorials Dojo practice exams
- *System Design Interview* by Alex Xu (Vol. 1) for general design thinking
- Pramp / interviewing.io / a friend for mock interviews

**Your own portfolio (build these)**
- [ ] GitHub repo: Bedrock RAG app with CDK + architecture diagram in the README
- [ ] Blog post about it (LinkedIn/Medium)
- [ ] Optional: a second blog post explaining your AKDE-VAE synthetic data idea for practitioners
- [ ] Updated resume + LinkedIn headline

---

### Final note
You're a strong fit on paper: real SWE experience, hands-on AWS, an AWS AI certification, and GenAI/agentic work that matches what AWS startups are building right now. The difference between a pass and an offer will come from three things:
1. **Crisp networking and security fundamentals.** This is your biggest gap, so close it in Week 1.
2. **A structured, customer-first architecture conversation.** Clarify, design, explain tradeoffs and cost.
3. **16 rehearsed, numbers-backed STAR stories.**

Good luck! 🚀
