# 9. Security

📖 Primer: [Security](https://github.com/donnemartin/system-design-primer#security) (+ [OWASP Top 10](https://owasp.org/www-project-top-ten/), [Security guide for developers](https://github.com/FallibleInc/security-guide-for-developers))

---

## 9.1 Fundamentals
- **Encrypt in transit** (TLS everywhere, including between internal services: mTLS) and **at rest** (AES-256, KMS-managed keys).
- **Sanitize all user input** and use parameterized queries to prevent XSS and SQL injection.
- **Principle of least privilege** for users, services, and DB accounts.
- **Authentication (authN)** = who you are. **Authorization (authZ)** = what you can do (RBAC/ABAC).

## 9.2 Auth patterns in system design
| Pattern | Notes |
|---|---|
| **Session cookie** | Server stores the session (in Redis); cookie set with `HttpOnly`, `Secure`, `SameSite` |
| **JWT** | Stateless signed token (header.payload.signature). Short expiry + refresh token. Hard to revoke. |
| **OAuth 2.0** | Delegated authorization ("Log in with Google"). Authorization code flow + PKCE. |
| **OpenID Connect** | Identity layer on top of OAuth (ID token) |
| **API keys** | Server-to-server. Rotate them, scope them, never commit them. |
| **mTLS** | Service-to-service identity |

## 9.3 Common attacks and defenses
| Attack | Defense |
|---|---|
| SQL injection | Parameterized queries, ORM |
| XSS | Output encoding, Content Security Policy |
| CSRF | SameSite cookies, CSRF tokens |
| DDoS | CDN/WAF, rate limiting, autoscaling, Shield/Cloudflare |
| Credential stuffing | Rate limiting, MFA, breached-password checks |
| SSRF | Allow-list outbound URLs; block the metadata IP |
| Secrets leakage | Secrets manager, scanning in CI |
| Prompt injection (LLM apps) | Input/output guardrails, least-privilege tools, human in the loop |

## 9.4 Passwords
Never store plaintext or reversible encryption. Use **bcrypt / scrypt / argon2** with a per-user salt (these are slow on purpose).

## 9.5 In a design interview, mention
TLS + an auth service/gateway + rate limiting + encryption at rest + audit logs + PII handling (GDPR/HIPAA) + least-privilege IAM. It takes 30 seconds and shows maturity.

## ✅ Self-check
- [ ] Session vs JWT tradeoffs
- [ ] How does OAuth "Log in with Google" work, step by step?
- [ ] Name 5 attacks and their defenses

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Authentication vs authorization?</b></summary>

**Authentication** verifies **who** you are (password + MFA, SSO, OAuth/OIDC login). **Authorization** decides **what** you may do (RBAC roles, ABAC attributes, resource ACLs). A 401 means not authenticated; a 403 means authenticated but not allowed.

</details>

<details>
<summary><b>Q2. How does 'Log in with Google' (OAuth 2.0 + OIDC) work?</b></summary>

The app redirects the user to Google with its client_id, scopes, and a redirect URI (+ PKCE). The user logs in and consents. Google redirects back with an **authorization code**. The app's backend exchanges the code for an **access token** and **ID token** (OIDC, a JWT with the user's identity). The app then creates its own session.

</details>

<details>
<summary><b>Q3. How should passwords be stored?</b></summary>

Never in plaintext or with reversible encryption. Hash them with a **slow, salted, adaptive** algorithm (**argon2id, bcrypt, scrypt**) with a unique salt per user and a tuned cost factor. Add rate limiting, MFA, and breached-password checks.

</details>

<details>
<summary><b>Q4. How do you prevent SQL injection and XSS?</b></summary>

**SQL injection:** use **parameterized queries / prepared statements** or an ORM; never build SQL by concatenating strings; use a least-privilege DB user. **XSS:** **escape output** for its context, use templating that escapes automatically, a Content-Security-Policy, HttpOnly cookies, and sanitize any HTML users can submit.

</details>

<details>
<summary><b>Q5. What security items should you mention in any system design answer?</b></summary>

TLS everywhere (mTLS internally), authentication at the gateway, authorization checks in services, rate limiting / WAF / DDoS protection, encryption at rest with managed keys, secrets in a secrets manager, least-privilege IAM, audit logs, and PII handling and compliance (GDPR/HIPAA).

</details>
