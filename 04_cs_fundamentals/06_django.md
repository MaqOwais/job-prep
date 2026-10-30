# 6. Django (+ Django REST Framework)

📖 Related: [Databases & SQL](03_databases_sql.md) · [Concurrency](04_concurrency.md) · [Networking](02_networking.md) · [Caching (HLD)](../02_high_level_design/)

Django questions come up in backend SWE rounds when your resume mentions it. Expect **"how does it work under the hood"** questions (request lifecycle, ORM, middleware) and **"how would you fix this"** questions (N+1, slow endpoint, race condition). Every answer below is meant to be said out loud in 30–60 seconds.

---

## 🗺️ The request lifecycle (know this cold)

```
Client → Web server (Nginx) → WSGI/ASGI server (Gunicorn / Uvicorn)
       → Django: middleware (request phase, top → bottom)
       → URL resolver (urls.py) → view (FBV / CBV / DRF ViewSet)
       → ORM ↔ database, templates / serializers
       → middleware (response phase, bottom → top) → client
```

## Key pieces
| Piece | One-liner |
|---|---|
| **MVT** | Model (data + ORM), View (logic, ≈ controller), Template (presentation). Django itself is the "controller" via URL routing. |
| **ORM** | Python classes ↔ tables. QuerySets are **lazy**: nothing hits the DB until you iterate, slice with a step, `len()`, `list()`, `bool()`, or print. |
| **Migrations** | Versioned schema changes generated from model diffs (`makemigrations`), applied with `migrate`. |
| **Middleware** | Hooks wrapping every request/response: auth, sessions, CSRF, security headers, CORS, logging. |
| **Signals** | Decoupled event hooks (`post_save`, `pre_delete`). Synchronous, same transaction. Use sparingly. |
| **Admin** | Auto-generated CRUD UI from models. |
| **DRF** | Serializers (validation + JSON), ViewSets, Routers, authentication, permissions, throttling, pagination. |

---

## ⚡ Rapid-fire quiz
| # | Question | Short answer |
|---|---|---|
| 1 | Is a QuerySet evaluated when you create it? | No, it's lazy. It runs on iteration, `len()`, `list()`, `bool()`, `repr()`, or slicing with a step. Results are then cached on that QuerySet. |
| 2 | `select_related` vs `prefetch_related`? | `select_related`: SQL JOIN, for FK / one-to-one. `prefetch_related`: a second query + join in Python, for M2M / reverse FK. |
| 3 | `get()` vs `filter()`? | `get()` returns one object and raises `DoesNotExist` / `MultipleObjectsReturned`. `filter()` returns a QuerySet (possibly empty). |
| 4 | What is `F()`? | References a column value in the DB, so `F('stock') - 1` updates atomically in SQL without a read-modify-write race. |
| 5 | What is `Q()`? | Builds complex lookups with `\|` (OR), `&` (AND), `~` (NOT). |
| 6 | `null=True` vs `blank=True`? | `null` is the DB column allowing NULL. `blank` is form/serializer validation allowing empty input. |
| 7 | `on_delete` options? | `CASCADE`, `PROTECT`, `RESTRICT`, `SET_NULL`, `SET_DEFAULT`, `SET()`, `DO_NOTHING`. |
| 8 | `auto_now` vs `auto_now_add`? | `auto_now_add`: set once on create. `auto_now`: updated on every `save()` (not on `.update()`). |
| 9 | WSGI vs ASGI? | WSGI is synchronous, one request per worker thread. ASGI supports async, WebSockets, and long-lived connections. |
| 10 | How does CSRF protection work? | A secret token in a cookie + a matching token in the form/header. Cross-site requests can't read it, so they can't forge it. |
| 11 | `aggregate()` vs `annotate()`? | `aggregate()` returns one dict for the whole QuerySet. `annotate()` adds a computed value per row. |
| 12 | `values()` vs `values_list()`? | Dicts vs tuples (`flat=True` for a single field). Skips model instantiation, so it's faster. |
| 13 | Abstract model vs multi-table inheritance vs proxy? | Abstract: shared fields, no table of its own. Multi-table: one table per class, joined by an implicit one-to-one. Proxy: same table, different Python behavior. |
| 14 | `ATOMIC_REQUESTS`? | Wraps every view in a transaction. Simple but holds transactions open for the whole request. |
| 15 | Where should business logic live? | Not in views. In model methods, managers / QuerySets, or a service layer. ("Fat models, thin views" is the classic advice.) |

---

## 🧪 Interview questions

### Easy

<details>
<summary><b>Q1. Walk me through what happens when a request hits a Django app.</b></summary>

Nginx forwards to **Gunicorn** (WSGI) or **Uvicorn** (ASGI), which calls Django's handler. The request goes through **middleware** top-to-bottom (security, sessions, CSRF, auth sets `request.user`). The **URL resolver** matches `urls.py` patterns and calls the **view**. The view uses the **ORM** and returns an `HttpResponse` (rendered template or DRF serializer output). The response passes back through middleware **bottom-to-top** and returns to the client.

</details>

<details>
<summary><b>Q2. Explain MVT and how it differs from MVC.</b></summary>

**Model** = data and the ORM. **View** = request handling and business logic (what MVC calls the controller). **Template** = presentation (what MVC calls the view). The framework itself plays the "controller" role through URL dispatching. It's mostly naming; the separation of concerns is the same.

</details>

<details>
<summary><b>Q3. What are migrations, and what happens if two developers create conflicting migrations?</b></summary>

Migrations are versioned Python files describing schema changes, generated from model diffs with `makemigrations` and applied with `migrate`. Django tracks applied ones in the `django_migrations` table. Two branches both adding `0005_*` produce a **conflict**. Fix with `makemigrations --merge` (creates a merge migration), or rebase and renumber if neither has been deployed. Always review generated migrations and test them against a production-like DB.

</details>

<details>
<summary><b>Q4. Function-based views vs class-based views. Which do you prefer?</b></summary>

**FBVs** are explicit and easy to read. Good for one-off logic. **CBVs** (`ListView`, `DetailView`, DRF `APIView`/`ViewSet`) give reuse through inheritance and mixins and cut boilerplate for CRUD. The cost is hidden control flow (you need to know which method to override). My take: CBVs/ViewSets for standard CRUD APIs, FBVs when the flow is unusual.

</details>

<details>
<summary><b>Q5. What is middleware? Give an example of a custom one.</b></summary>

A callable wrapping every request/response, configured as an ordered list in `MIDDLEWARE`.

```python
import time, logging
log = logging.getLogger(__name__)

class TimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response      # called once at startup

    def __call__(self, request):
        start = time.perf_counter()
        response = self.get_response(request)  # rest of the chain + view
        ms = (time.perf_counter() - start) * 1000
        response["X-Response-Time-ms"] = f"{ms:.1f}"
        log.info("%s %s %d %.1fms", request.method, request.path, response.status_code, ms)
        return response
```
Other hooks: `process_view`, `process_exception`, `process_template_response`. Order matters: auth must run after sessions.

</details>

<details>
<summary><b>Q6. How does Django's authentication work? Sessions vs tokens/JWT?</b></summary>

Default: **session auth**. On login, Django stores the user id in a server-side session and sends a `sessionid` cookie. `AuthenticationMiddleware` loads `request.user` on each request. Passwords are hashed with **PBKDF2** (Argon2/bcrypt configurable). For APIs/mobile, DRF supports **token auth** or **JWT** (e.g. `simplejwt`): stateless, scales horizontally, but revocation is harder (short-lived access token + refresh token, or a deny list). Sessions are easier to revoke and are the safer default for browser apps.

</details>

### Medium

<details>
<summary><b>Q7. What is the N+1 query problem and how do you fix it in Django?</b></summary>

Looping over objects and touching a relation triggers one query per row:

```python
for book in Book.objects.all():        # 1 query
    print(book.author.name)            # +N queries
```
Fix:
```python
Book.objects.select_related("author")              # FK/1-1 → one JOIN
Author.objects.prefetch_related("books")           # reverse FK/M2M → 2 queries
Author.objects.prefetch_related(
    Prefetch("books", queryset=Book.objects.filter(published=True))
)
```
Detect it with **django-debug-toolbar**, `connection.queries`, `assertNumQueries` in tests, or APM tracing. In DRF, nested serializers are the classic N+1 source, so override `get_queryset()` with the right `select_related`/`prefetch_related`.

</details>

<details>
<summary><b>Q8. Two users buy the last item at the same time. How do you prevent overselling?</b></summary>

The bug is read-modify-write in Python. Options:

```python
# 1. Atomic conditional update (best: one SQL statement, no lock held in Python)
updated = Product.objects.filter(id=pid, stock__gt=0).update(stock=F("stock") - 1)
if not updated:
    raise OutOfStock

# 2. Pessimistic lock
with transaction.atomic():
    p = Product.objects.select_for_update().get(id=pid)   # SELECT ... FOR UPDATE
    if p.stock < 1: raise OutOfStock
    p.stock -= 1; p.save(update_fields=["stock"])

# 3. Optimistic locking: version column, UPDATE ... WHERE version = old, retry on 0 rows
```
Plus a DB **CheckConstraint** (`stock >= 0`) as the last line of defense.

</details>

<details>
<summary><b>Q9. How do transactions work in Django? What does transaction.atomic do?</b></summary>

Django runs in **autocommit** by default (each query commits on its own). `transaction.atomic()` opens a transaction; nested `atomic` blocks create **savepoints**. If an exception escapes the block, it rolls back. Gotchas:
- Catching an exception **inside** the atomic block without a nested atomic leaves the transaction broken.
- Side effects (emails, Celery tasks) should use `transaction.on_commit(lambda: send.delay(...))` so they don't fire for rolled-back data, or before the row is visible to the worker.

</details>

<details>
<summary><b>Q10. Signals: when would you use them and when would you avoid them?</b></summary>

Signals (`post_save`, `pre_delete`, `m2m_changed`, custom) decouple a sender from receivers, e.g. a third-party app reacting to your models. Avoid them for core business logic: they're **implicit** (hard to trace), **synchronous**, run in the same transaction, and **don't fire on `bulk_create` / `.update()` / `.delete()` on QuerySets**. Prefer an explicit service function (`create_order()` calls `send_receipt()`).

</details>

<details>
<summary><b>Q11. How would you speed up a slow Django endpoint?</b></summary>

Measure first (APM, debug toolbar, `EXPLAIN ANALYZE`). Then in order of usual payoff:
1. **Query count**: `select_related` / `prefetch_related`; kill N+1.
2. **Query cost**: add **indexes** (`Meta.indexes`, `db_index=True`) on filter/order columns; avoid `OFFSET` pagination on large tables (use cursor/keyset pagination).
3. **Fetch less**: `only()`, `defer()`, `values()`; paginate.
4. **Cache**: per-view (`cache_page`), low-level (`cache.get_or_set`) in **Redis**, template fragments; invalidate on write.
5. **Move work off the request path**: Celery + Redis/SQS for emails, reports, image processing.
6. **Infra**: DB connection pooling (`CONN_MAX_AGE` / PgBouncer), read replicas with a DB router, more Gunicorn workers, CDN for static.

</details>

<details>
<summary><b>Q12. Explain DRF serializers. Serializer vs ModelSerializer? Where does validation go?</b></summary>

A serializer converts model instances ↔ primitive types (JSON) and **validates input**. `ModelSerializer` generates fields and `create`/`update` from a model. Validation layers: field-level `validate_<field>()`, object-level `validate()` (cross-field), field `validators=[...]`, and DB constraints as the final guarantee. Use `read_only_fields` to stop clients writing fields like `owner` or `created_at`, and set those in `perform_create(serializer.save(owner=request.user))`.

</details>

<details>
<summary><b>Q13. Authentication vs permissions vs throttling in DRF?</b></summary>

**Authentication** answers "who are you?" (Session, Token, JWT) and sets `request.user`. **Permissions** answer "may you do this?": global (`IsAuthenticated`, `IsAdminUser`) and **object-level** (`has_object_permission`, e.g. `IsOwnerOrReadOnly`). **Throttling** answers "how often?": `AnonRateThrottle`, `UserRateThrottle`, `ScopedRateThrottle`, backed by the cache. Note: object permissions only run when you call `get_object()`, so a custom list endpoint must filter the queryset itself (`filter(owner=request.user)`).

</details>

<details>
<summary><b>Q14. How do you run background or scheduled tasks with Django?</b></summary>

**Celery** with a broker (Redis, RabbitMQ, or **SQS** on AWS) and workers; **Celery Beat** for cron-like schedules. Lighter options: Django-Q, RQ, Huey, or Django 5's built-in tasks framework / plain cron + management commands. Design tasks to be **idempotent** (they may retry), pass IDs not model instances, set retries with backoff, and enqueue with `transaction.on_commit`.

</details>

<details>
<summary><b>Q15. Custom managers and QuerySets: why and how?</b></summary>

To put reusable query logic on the model instead of repeating filters in views.

```python
class OrderQuerySet(models.QuerySet):
    def paid(self):        return self.filter(status="paid")
    def for_user(self, u): return self.filter(user=u)

class Order(models.Model):
    ...
    objects = OrderQuerySet.as_manager()

Order.objects.paid().for_user(request.user)   # chainable
```

</details>

<details>
<summary><b>Q16. How do you design a custom User model, and why do it at project start?</b></summary>

Subclass `AbstractUser` (keep Django's fields, add yours) or `AbstractBaseUser + PermissionsMixin` (full control, e.g. email as the login). Set `AUTH_USER_MODEL = "accounts.User"` and always reference it with `settings.AUTH_USER_MODEL` / `get_user_model()`. Do it **before the first migration**: switching later means rewriting FKs across every table, which is painful. Profile data you don't need on every request can go in a one-to-one `Profile` model.

</details>

### Hard

<details>
<summary><b>Q17. How does the ORM actually build and execute a query?</b></summary>

A `QuerySet` holds a `Query` object (a tree of filters, joins, annotations). Chaining (`filter`, `exclude`, `order_by`) **clones** the QuerySet and mutates the clone's `Query`, which is why QuerySets are immutable and reusable. On evaluation, the `SQLCompiler` for the DB backend turns `Query` into SQL + params (parameterized, so injection-safe), runs it through the DB connection, and the iterator builds model instances. Results are cached in `_result_cache`. `str(qs.query)` shows the SQL; `.explain()` shows the plan.

</details>

<details>
<summary><b>Q18. Async Django: what's actually async, and when is it worth it?</b></summary>

Under ASGI, `async def` views run on the event loop. The ORM has async methods (`aget`, `acreate`, `async for`), but database drivers are still mostly sync under the hood (run in a thread pool), so DB-heavy views gain little. Async pays off for **I/O fan-out** (calling several external APIs concurrently with `httpx` + `asyncio.gather`), **WebSockets / SSE / streaming** (Django Channels, LLM token streaming), and long-polling. Use `sync_to_async` / `async_to_sync` at the boundaries; never call blocking code directly in an async view.

</details>

<details>
<summary><b>Q19. How would you scale a Django app to millions of users?</b></summary>

Django is stateless per request, so **scale horizontally**: many app containers (ECS/EKS/EC2 ASG) behind a load balancer, sessions in Redis/DB not memory, static/media on **S3 + CloudFront**. Database: connection pooling (PgBouncer / RDS Proxy), indexes, **read replicas** via a DB router, caching hot reads in Redis, and eventually partitioning/sharding. Move slow work to **Celery + SQS**. Observability: structured logs, APM, slow query log. Rate limit at the edge. (Same path as [1 server → millions](../02_high_level_design/00_step_by_step_fundamentals/README.md).)

</details>

<details>
<summary><b>Q20. How do you ship a migration on a big table with zero downtime?</b></summary>

Avoid operations that lock or rewrite large tables during deploy. Use **expand → migrate → contract**:
1. **Expand:** add the new column as **nullable** (or with a DB-side default in Postgres 11+, which is metadata-only). Deploy code that writes both old and new.
2. **Backfill** in batches in a background job, not inside the migration.
3. Switch reads to the new column; then add `NOT NULL` / constraints (Postgres: add the constraint `NOT VALID`, then `VALIDATE`).
4. **Contract:** remove the old column in a later release.

Create indexes with `AddIndexConcurrently` (Postgres; needs `atomic = False` on the migration). Never rename a column in one step while old code still runs. Use `SeparateDatabaseAndState` when the DB and model state must diverge temporarily.

</details>

<details>
<summary><b>Q21. Name Django's main security protections and the common ways people break them.</b></summary>

| Threat | Django protection | How it gets broken |
|---|---|---|
| SQL injection | ORM parameterizes queries | f-strings in `raw()` / `extra()` / `cursor.execute` |
| XSS | Templates auto-escape | `mark_safe`, `\|safe` on user input |
| CSRF | `CsrfViewMiddleware` + token | `@csrf_exempt` on cookie-authenticated endpoints |
| Clickjacking | `X-Frame-Options` middleware | Disabling it |
| Host header attacks | `ALLOWED_HOSTS` | `ALLOWED_HOSTS = ["*"]` |
| Data leaks | — | `DEBUG=True` in prod, secrets in settings committed to git |
| IDOR | — | Fetching `Order.objects.get(id=pk)` without scoping to `request.user` |

Run `manage.py check --deploy` before shipping. Set `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, HSTS.

</details>

<details>
<summary><b>Q22. How do you test a Django app?</b></summary>

`TestCase` wraps each test in a transaction and rolls back (fast). `TransactionTestCase` when you need real commits (e.g. testing `on_commit`). `APIClient`/`APITestCase` for DRF. Use **factory_boy** for fixtures, **pytest-django** for ergonomics, `assertNumQueries` to lock in query counts (prevents N+1 regressions), `override_settings`, and mock external calls (`responses`, `unittest.mock`). Pyramid: lots of model/service unit tests, fewer API tests, a few end-to-end.

</details>

<details>
<summary><b>Q23. Design question: build a URL shortener API in Django. Models and key decisions?</b></summary>

```python
class ShortURL(models.Model):
    code = models.CharField(max_length=10, unique=True)   # indexed by unique
    target = models.URLField(max_length=2048)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
```
- Code generation: base62 of an auto-increment id (no collisions) or random 7 chars with retry on `IntegrityError`.
- `GET /<code>` → cache lookup in Redis → fall back to DB → `HttpResponseRedirect` (302 if you want analytics, 301 if not).
- Click counts: don't `UPDATE` on every hit. Increment in Redis (`INCR`) or push to a queue and flush to the DB in batches.
- DRF `CreateAPIView` with URL validation + `UserRateThrottle` to stop abuse.

</details>

---

## 🎯 Tie it to your resume
For each Django project you list, be ready to answer:
1. What did the data model look like, and why those relationships?
2. What was the slowest endpoint and how did you find / fix it? (N+1, index, cache: give a number.)
3. How did you handle auth and permissions?
4. What ran in the background, and how did you make it safe to retry?
5. What would break first at 100× traffic?
