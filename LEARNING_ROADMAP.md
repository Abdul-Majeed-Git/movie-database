# 🎯 Database Learning Roadmap - Track Your Progress

**Created:** May 23, 2026  
**Author:** Abdul-Majeed-Git  
**Current Status:** SQLite Basics Completed (45 hours)  
**Next Goal:** PostgreSQL + Advanced SQL

---

## 📊 Progress Overview

| Phase | Duration | Hours | Status | Start Date | End Date |
|-------|----------|-------|--------|-----------|----------|
| Phase 1: SQLite Basics | 1.5 months | 45 | ✅ COMPLETED | Apr 8 | May 23 |
| Phase 2: Advanced SQL (JOINs, GROUP BY) | 1 week | 7 | ⏳ TODO | May 24 | May 31 |
| Phase 3: PostgreSQL + psycopg2 | 3 weeks | 15 | ⏳ TODO | Jun 1 | Jun 21 |
| Phase 4: SQLAlchemy ORM | 2 weeks | 10 | ⏳ TODO | Jun 22 | Jul 5 |
| Phase 5: FastAPI Integration | 2 weeks | 10 | ⏳ TODO | Jul 6 | Jul 19 |
| **TOTAL** | **9 weeks** | **87 hours** | | |

---

## 🔥 Phase 2: Advanced SQL Challenges (Next 1 Week)

**Objective:** Master JOINs, GROUP BY, Aggregations before moving to PostgreSQL

### Challenge 2.1: Add Relationships to Your Movie DB

**Create these new tables:**

```sql
-- Users table
CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Reviews table (links movies to users - Foreign Key)
CREATE TABLE Reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    rating REAL NOT NULL CHECK(rating >= 1 AND rating <= 10),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(movie_id) REFERENCES Movies(id) ON DELETE CASCADE,
    FOREIGN KEY(user_id) REFERENCES Users(id) ON DELETE CASCADE
);

-- Favorites table (users can favorite movies)
CREATE TABLE Favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(movie_id) REFERENCES Movies(id) ON DELETE CASCADE,
    FOREIGN KEY(user_id) REFERENCES Users(id) ON DELETE CASCADE,
    UNIQUE(movie_id, user_id)
);
```

**✓ Completion Checklist:**
- [ ] Created Users table
- [ ] Created Reviews table with FOREIGN KEYs
- [ ] Created Favorites table
- [ ] Added 5+ sample users
- [ ] Added 20+ sample reviews
- [ ] Added 10+ favorites

**Time:** 2 hours

---

### Challenge 2.2: INNER JOIN Queries

**Write these queries and save results to a file:**

```sql
-- Q1: Get all reviews with movie title and username
SELECT 
    m.title,
    u.username,
    r.rating,
    r.comment,
    r.created_at
FROM Reviews r
INNER JOIN Movies m ON r.movie_id = m.id
INNER JOIN Users u ON r.user_id = u.id
ORDER BY r.created_at DESC;
```

**What you're learning:** How to connect data across 3 tables

```sql
-- Q2: Find movies that have been reviewed
SELECT DISTINCT 
    m.id,
    m.title,
    m.genre,
    COUNT(r.id) as review_count
FROM Movies m
INNER JOIN Reviews r ON m.id = r.movie_id
GROUP BY m.id, m.title, m.genre
ORDER BY review_count DESC;
```

**What you're learning:** INNER JOIN + COUNT aggregation

```sql
-- Q3: Get reviews for a specific movie (e.g., "Inception")
SELECT 
    u.username,
    r.rating,
    r.comment,
    r.created_at
FROM Reviews r
INNER JOIN Users u ON r.user_id = u.id
WHERE r.movie_id = (SELECT id FROM Movies WHERE title = 'Inception')
ORDER BY r.created_at DESC;
```

**What you're learning:** Subqueries inside WHERE clause

**✓ Completion Checklist:**
- [ ] Query Q1 works (3-table join)
- [ ] Query Q2 works (COUNT aggregation)
- [ ] Query Q3 works (subquery)
- [ ] All queries return correct results
- [ ] Saved queries to `sql_queries.txt`

**Time:** 3 hours

---

### Challenge 2.3: LEFT JOIN + GROUP BY Queries

**The tricky ones - master these:**

```sql
-- Q4: Show all movies WITH their review counts (even if no reviews)
SELECT 
    m.id,
    m.title,
    m.genre,
    m.rate,
    COUNT(r.id) as user_reviews_count,
    CASE 
        WHEN COUNT(r.id) = 0 THEN 'No reviews yet'
        WHEN AVG(r.rating) >= 8 THEN 'Highly rated'
        WHEN AVG(r.rating) >= 6 THEN 'Good'
        ELSE 'Mixed reviews'
    END as review_status
FROM Movies m
LEFT JOIN Reviews r ON m.id = r.movie_id
GROUP BY m.id, m.title, m.genre, m.rate
ORDER BY COUNT(r.id) DESC;
```

**What you're learning:** LEFT JOIN keeps all movies even without reviews, CASE for logic

```sql
-- Q5: Top reviewers (users who reviewed most movies)
SELECT 
    u.username,
    COUNT(DISTINCT r.movie_id) as movies_reviewed,
    AVG(r.rating) as avg_rating_given,
    MIN(r.rating) as lowest_rating,
    MAX(r.rating) as highest_rating
FROM Users u
LEFT JOIN Reviews r ON u.id = r.user_id
GROUP BY u.id, u.username
HAVING COUNT(r.id) > 0
ORDER BY movies_reviewed DESC;
```

**What you're learning:** GROUP BY multiple columns, HAVING clause, DISTINCT count

```sql
-- Q6: Genre performance (which genre has highest avg user ratings)
SELECT 
    m.genre,
    COUNT(DISTINCT m.id) as movie_count,
    COUNT(DISTINCT r.id) as total_reviews,
    AVG(r.rating) as avg_user_rating,
    MIN(r.rating) as worst_rating,
    MAX(r.rating) as best_rating
FROM Movies m
LEFT JOIN Reviews r ON m.id = r.movie_id
GROUP BY m.genre
ORDER BY avg_user_rating DESC;
```

**What you're learning:** Complex GROUP BY with multiple aggregates

**✓ Completion Checklist:**
- [ ] Query Q4 works (LEFT JOIN + CASE)
- [ ] Query Q5 works (TOP reviewers)
- [ ] Query Q6 works (Genre analysis)
- [ ] Understand difference between INNER vs LEFT JOIN
- [ ] Understand HAVING vs WHERE clause
- [ ] Saved all queries

**Time:** 2 hours

---

### Challenge 2.4: Advanced Queries (OPTIONAL but Recommended)

```sql
-- Q7: Movies favorited by most users
SELECT 
    m.title,
    m.genre,
    COUNT(DISTINCT f.user_id) as favorite_count,
    COUNT(DISTINCT r.id) as review_count,
    AVG(r.rating) as avg_rating
FROM Movies m
LEFT JOIN Favorites f ON m.id = f.movie_id
LEFT JOIN Reviews r ON m.id = r.movie_id
GROUP BY m.id, m.title, m.genre
ORDER BY favorite_count DESC;
```

```sql
-- Q8: Users who favorited but didn't review movies
SELECT 
    u.username,
    m.title,
    f.added_at,
    CASE WHEN r.id IS NULL THEN 'No review' ELSE 'Has review' END as status
FROM Favorites f
INNER JOIN Users u ON f.user_id = u.id
INNER JOIN Movies m ON f.movie_id = m.id
LEFT JOIN Reviews r ON f.movie_id = r.movie_id AND f.user_id = r.user_id
ORDER BY f.added_at DESC;
```

**What you're learning:** Multiple JOINs with NULL detection

**✓ Completion Checklist:**
- [ ] Query Q7 works
- [ ] Query Q8 works
- [ ] Can explain what each JOIN does

**Time:** 1 hour

---

## 📝 Phase 2 Deliverables

After completing Phase 2, you should have:

1. **Updated `movies.py`** with new methods:
   ```python
   class MovieDatabase:
       def add_user(self, username, email) -> bool
       def add_review(self, movie_id, user_id, rating, comment) -> bool
       def get_reviews_for_movie(self, movie_id) -> list
       def get_top_reviewers(self) -> list
       def get_genre_stats(self) -> list
       def add_favorite(self, movie_id, user_id) -> bool
   ```

2. **`sql_queries.txt`** containing all 8 queries with explanations

3. **GitHub commit** with message: `feat: add advanced SQL queries (JOINs, GROUP BY, aggregations)`

---

## ⚠️ Common Mistakes to Avoid in Phase 2

| Mistake | Why It's Wrong | How to Fix |
|---------|---|---|
| Using WHERE instead of HAVING | WHERE filters before GROUP, HAVING filters after | Use `HAVING COUNT(*) > 0` not `WHERE COUNT(*) > 0` |
| Forgetting to GROUP BY all non-aggregated columns | SQL will give wrong results | Add all SELECT columns (except aggregates) to GROUP BY |
| Using INNER JOIN when you need LEFT JOIN | Data disappears if no match | Use LEFT JOIN to keep all rows from first table |
| Not handling NULL values | Wrong calculations | Use `COUNT(DISTINCT r.id)` instead of `COUNT(*)` |

---

## 🎯 Phase 3: PostgreSQL + psycopg2 (Weeks 2-4)

**Prerequisites:** Complete Phase 2 ✅

### Tasks:

1. **Install PostgreSQL** (Week 1 of Phase 3)
   - [ ] Download & install PostgreSQL 15+
   - [ ] Create database: `movie_db`
   - [ ] Migrate all tables from SQLite

2. **Learn psycopg2** (Week 2 of Phase 3)
   - [ ] Connection basics
   - [ ] Connection pooling
   - [ ] Error handling
   - [ ] Transaction management

3. **Rewrite Movie App** (Week 3 of Phase 3)
   - [ ] Replace sqlite3 with psycopg2
   - [ ] Implement connection pool
   - [ ] Add proper error logging
   - [ ] Commit to GitHub

**Estimated Time:** 15 hours

---

## 📚 Phase 4: SQLAlchemy ORM (Weeks 5-6)

**Prerequisites:** Complete Phase 3 ✅

### Key Topics:
- [ ] Declarative base and models
- [ ] Relationships (one-to-many, many-to-many)
- [ ] Session management
- [ ] Query API
- [ ] Lazy vs eager loading
- [ ] Migrations with Alembic

**Project:** Rewrite Movie app using SQLAlchemy ORM

**Estimated Time:** 10 hours

---

## 🚀 Phase 5: FastAPI Integration (Weeks 7-8)

**Prerequisites:** Complete Phase 4 ✅

### API Endpoints to Build:
- [ ] GET `/movies` - List all movies
- [ ] GET `/movies/{id}` - Get single movie
- [ ] POST `/movies` - Add new movie
- [ ] GET `/movies/{id}/reviews` - Get reviews for movie
- [ ] POST `/reviews` - Add review
- [ ] GET `/users/{id}/favorites` - Get user favorites

**Estimated Time:** 10 hours

---

## ✅ Weekly Checklist

### Week 1 (May 24-31) - Phase 2
- [ ] Monday: Setup new tables (Users, Reviews, Favorites)
- [ ] Tuesday-Wednesday: INNER JOIN challenges (Q1-Q3)
- [ ] Thursday-Friday: LEFT JOIN challenges (Q4-Q6)
- [ ] Saturday: Advanced queries (Q7-Q8)
- [ ] Sunday: Review & commit to GitHub

### Week 2 (Jun 1-7) - Phase 3 Part 1
- [ ] Monday-Tuesday: Install PostgreSQL, migrate data
- [ ] Wednesday-Thursday: Learn psycopg2 basics
- [ ] Friday: Connection pooling
- [ ] Weekend: Start rewriting Movie app

---

## 📞 Resources to Bookmark

**SQL Learning:**
- SQLZoo (http://sqlzoo.net/) - Interactive SQL problems
- LeetCode Database Problems - Real interview questions
- Mode Analytics SQL Tutorial - Excellent guide

**PostgreSQL:**
- Official Docs: https://www.postgresql.org/docs/
- psycopg2 Docs: https://www.psycopg.org/

**SQLAlchemy:**
- Official Docs: https://docs.sqlalchemy.org/
- Miguel Grinberg's Flask-SQLAlchemy Tutorial

**FastAPI:**
- Official Docs: https://fastapi.tiangolo.com/
- Full Stack Python + React + FastAPI

---

## 📊 Success Metrics

By end of Phase 2 (1 week):
- ✅ Can write INNER JOINs from memory
- ✅ Can write GROUP BY with aggregations
- ✅ Can explain difference between LEFT & INNER JOIN
- ✅ Can debug SQL errors quickly
- ✅ Have 3+ GitHub commits

By end of Phase 3 (4 weeks total):
- ✅ PostgreSQL database running locally
- ✅ psycopg2 app working
- ✅ Can use connection pooling
- ✅ Movie app fully migrated

By end of Phase 4 (6 weeks total):
- ✅ SQLAlchemy models created
- ✅ Complex queries written using ORM
- ✅ Understand relationships (1-to-many, many-to-many)
- ✅ Migrations working

By end of Phase 5 (9 weeks total):
- ✅ FastAPI with PostgreSQL working
- ✅ Full CRUD API endpoints
- ✅ Error handling & validation
- ✅ Ready for FastAPI projects

---

## 🎓 Final Notes

**Why this roadmap?**
1. **Progressive complexity** - Not jumping too fast
2. **Real-world skills** - PostgreSQL is industry standard
3. **Problem solving** - Each phase builds on previous
4. **Portfolio building** - GitHub shows growth

**Don't:**
- ❌ Skip advanced SQL challenges
- ❌ Use SQLite tricks in PostgreSQL (different!)
- ❌ Jump to FastAPI without ORM understanding
- ❌ Copy-paste code without understanding it

**Do:**
- ✅ Type out all queries yourself
- ✅ Test each query in SQLite first
- ✅ Commit to GitHub frequently
- ✅ Ask questions when stuck (use Stack Overflow/GitHub Discussions)

---

## 📈 Track Daily Progress

Use this template daily in `PROGRESS.md`:

```markdown
## Week 1 - May 24-30

### May 24 (Monday)
- ⏱️ Time spent: 1.5 hours
- ✅ Completed: Created Users, Reviews, Favorites tables
- 📝 Notes: Learned FOREIGN KEY constraints with CASCADE
- 🔗 Commit: [link to commit]

### May 25 (Tuesday)  
- ⏱️ Time spent: 1 hour
- ✅ Completed: Query Q1 (3-table INNER JOIN)
- 📝 Notes: Tricky part was ordering by created_at
- 🔗 Commit: [link to commit]
```

---

## 🎯 Remember

You've already spent 45 hours learning SQLite basics. The next 9 weeks will:
- Make you job-ready
- Give you production skills
- Build a strong GitHub portfolio
- Prepare you for FastAPI/Django jobs

**Stay consistent. 1 hour/day compounds.**

Good luck! 🚀
