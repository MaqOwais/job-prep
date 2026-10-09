# 3. Databases & SQL

📖 Primer: [Database](https://github.com/donnemartin/system-design-primer#database) · Practice: [LeetCode SQL 50](https://leetcode.com/studyplan/top-sql-50/) · [SQLBolt (interactive basics)](https://sqlbolt.com/)

## ACID and isolation
| Isolation level | Dirty read | Non-repeatable read | Phantom read |
|---|---|---|---|
| Read uncommitted | ✗ possible | ✗ | ✗ |
| **Read committed** (Postgres default) | ✓ prevented | ✗ | ✗ |
| Repeatable read (MySQL InnoDB default) | ✓ | ✓ | ✗ (InnoDB mostly prevents these) |
| Serializable | ✓ | ✓ | ✓ |

- **Dirty read:** reading another transaction's uncommitted data.
- **Non-repeatable read:** the same row read twice returns different values.
- **Phantom read:** the same query returns new rows.
- **MVCC** (multi-version concurrency control): readers don't block writers. Each transaction sees a snapshot. Used by Postgres and InnoDB.

## Indexes
- **B+ tree** (default): good for `=`, ranges, `ORDER BY`. **Hash index:** `=` only.
- **Composite index `(a, b, c)`:** usable for `a`, `a,b`, `a,b,c` (the leftmost prefix rule), but not for `b` alone.
- **Covering index:** contains every column the query needs, so the table isn't touched.
- Clustered (rows stored in key order: InnoDB primary key) vs secondary indexes.
- **Costs:** slower writes, extra storage. Don't index low-cardinality columns (like booleans) on their own.
- Use `EXPLAIN` / `EXPLAIN ANALYZE` to check for index scans vs full table scans.

## Normalization
1NF (atomic values) → 2NF (no partial dependency on a composite key) → 3NF (no transitive dependencies). **Denormalize** for read performance when joins get expensive.

## Transactions and locking
- Pessimistic: `SELECT … FOR UPDATE`. Optimistic: a version column, `UPDATE … WHERE version = ?`.
- Deadlocks in a DB: the DB detects them and aborts one transaction, so retry.
- N+1 query problem (ORMs): one query for the list, then N queries for its children. Fix it with a JOIN or eager loading.

## SQL patterns to know cold
```sql
-- Joins
SELECT u.name, o.total FROM users u
JOIN orders o ON o.user_id = u.id;            -- INNER: only matches
-- LEFT JOIN keeps all users, even with no orders (o.* NULL)

-- Aggregation + HAVING
SELECT user_id, COUNT(*) AS n, SUM(total) AS spent
FROM orders GROUP BY user_id HAVING COUNT(*) > 5;

-- Second highest salary
SELECT MAX(salary) FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);

-- Top N per group with window functions ⭐
SELECT * FROM (
  SELECT e.*, DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
  FROM employees e
) t WHERE rnk <= 3;

-- Running total
SELECT day, amount, SUM(amount) OVER (ORDER BY day) AS running FROM sales;

-- Previous row comparison
SELECT day, temp, LAG(temp) OVER (ORDER BY day) AS prev_temp FROM weather;

-- Find duplicates
SELECT email, COUNT(*) FROM users GROUP BY email HAVING COUNT(*) > 1;

-- Users with no orders (anti-join)
SELECT u.* FROM users u LEFT JOIN orders o ON o.user_id = u.id WHERE o.id IS NULL;

-- CTE
WITH monthly AS (
  SELECT DATE_TRUNC('month', created_at) AS m, SUM(total) AS rev FROM orders GROUP BY 1
)
SELECT m, rev, rev - LAG(rev) OVER (ORDER BY m) AS growth FROM monthly;
```
**Order of execution:** FROM/JOIN → WHERE → GROUP BY → HAVING → SELECT → (window functions) → DISTINCT → ORDER BY → LIMIT.
**ROW_NUMBER vs RANK vs DENSE_RANK:** 1,2,3,4 vs 1,2,2,4 vs 1,2,2,3.

## SQL practice problems (Easy → Hard)
| Level | Problem |
|---|---|
| 🟢 | [Combine Two Tables](https://leetcode.com/problems/combine-two-tables/) · [Duplicate Emails](https://leetcode.com/problems/duplicate-emails/) · [Customers Who Never Order](https://leetcode.com/problems/customers-who-never-order/) |
| 🟡 | [Second Highest Salary](https://leetcode.com/problems/second-highest-salary/) · [Rank Scores](https://leetcode.com/problems/rank-scores/) · [Consecutive Numbers](https://leetcode.com/problems/consecutive-numbers/) · [Department Highest Salary](https://leetcode.com/problems/department-highest-salary/) |
| 🔴 | [Department Top Three Salaries](https://leetcode.com/problems/department-top-three-salaries/) · [Trips and Users](https://leetcode.com/problems/trips-and-users/) · [Human Traffic of Stadium](https://leetcode.com/problems/human-traffic-of-stadium/) |

## Interview questions
1. Explain ACID, and give an example of each isolation anomaly.
2. How does an index work? Why not index every column?
3. Composite index leftmost-prefix rule.
4. INNER vs LEFT vs FULL OUTER JOIN.
5. How would you find and fix a slow query?
6. SQL vs NoSQL ([system design module](../02_high_level_design/05_databases/)).

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Write a query for the top 3 salaries per department.</b></summary>

```sql
SELECT * FROM (
  SELECT e.*, DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
  FROM employees e
) t
WHERE rnk <= 3;
```
DENSE_RANK keeps ties without skipping ranks. Use ROW_NUMBER if you need exactly 3 rows per department.

</details>

<details>
<summary><b>Q2. What does a composite index on (a, b, c) help with?</b></summary>

Queries filtering on the **leftmost prefix**: (a), (a, b), (a, b, c), plus ORDER BY in that order. It does **not** help a filter on b or c alone. Put high-selectivity equality columns first, and range columns last.

</details>

<details>
<summary><b>Q3. What is MVCC?</b></summary>

**Multi-version concurrency control**: writers create new row versions instead of overwriting, and each transaction reads a **consistent snapshot**. Readers don't block writers and writers don't block readers. Old versions are cleaned up later (VACUUM in Postgres).

</details>

<details>
<summary><b>Q4. WHERE vs HAVING?</b></summary>

**WHERE** filters rows **before** grouping and can't use aggregates. **HAVING** filters **groups after** GROUP BY and can use aggregates (HAVING COUNT(*) > 5). Filter as much as possible in WHERE for performance.

</details>

<details>
<summary><b>Q5. A query became slow in production. How do you investigate?</b></summary>

Find it (slow query log, APM) → run **EXPLAIN ANALYZE** → look for sequential scans, bad row estimates, and expensive sorts or joins → add or fix **indexes**, rewrite the query (avoid SELECT *, functions on indexed columns, N+1 patterns), update statistics → verify the improvement and watch the write overhead.

</details>
