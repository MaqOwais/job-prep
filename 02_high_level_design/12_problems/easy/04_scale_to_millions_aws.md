# 🟢 04. Design a System That Scales to Millions of Users on AWS

📖 Primer solution: [Design a system that scales to millions of users on AWS](https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/scaling_aws/README.md)
⏱️ This is **the most important easy problem** for any cloud or AWS role. It's about *iterating*: find the bottleneck, fix it, repeat.

## The iterative approach
**Benchmark/load test → profile → find the bottleneck → evaluate alternatives and tradeoffs → apply → repeat.**

### Stage 1: One user to a few hundred
```
Route 53 → single EC2 (web + app + MySQL) + Elastic IP
```
Vertical scaling only. Restrict open ports with a security group. Monitor CPU, memory, and disk with CloudWatch.

### Stage 2: Thousands of users. Separate the parts.
- Move the **DB to RDS** (managed backups, Multi-AZ).
- Move **static content to S3 + CloudFront CDN**.
- Put the app inside a VPC: public subnet for web, private subnets for the DB.

### Stage 3: Tens of thousands. Scale horizontally.
```
Route 53 → CloudFront/S3 (static)
        → ALB → Auto Scaling Group of web/app servers (multiple AZs)
                 → ElastiCache (Redis): sessions + hot data
                 → RDS primary (Multi-AZ) + read replicas
```
- **Stateless app servers** (sessions in Redis).
- Read replicas for read-heavy traffic.
- Split web servers from app servers (API servers can scale on their own).

### Stage 4: Hundreds of thousands to millions. Autoscale, decouple, automate.
- **Auto Scaling** on CPU, latency, or queue depth.
- **Async workers** behind SQS for slow jobs (thumbnails, emails).
- **Infrastructure as code** (CloudFormation/Terraform/CDK) and CI/CD.
- Centralized logging and metrics (CloudWatch, X-Ray); alerting.

### Stage 5: Millions+. Data tier scaling.
- **Federation** (split DBs by function), **sharding**, denormalization.
- Move suitable data to **NoSQL (DynamoDB)**: high-write, key-value access patterns.
- Data warehouse for analytics (Redshift), with ETL out of the OLTP DB.
- Multi-region for latency and disaster recovery.

## Key ideas to say out loud
- "I'll start simple and scale only when metrics show a bottleneck."
- "Every tier becomes redundant across AZs to remove SPOFs."
- "Cache before you shard. Sharding is the last resort because of its complexity."

## ✅ Takeaways
Know the **5 stages** and the AWS service for each layer. This maps directly onto the [AWS SA prep plan](../../../06_company_specific/aws_startup_sa/AWS_Associate_Startup_SA_Prep_Plan.md).
