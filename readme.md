# 🎬 Movie Collection Manager

A lightweight, CLI-based movie library app built with Python and SQLite. Add, search, filter, and delete movies — all from your terminal, with data that actually sticks around between sessions.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Getting Started](#getting-started)
- [How to Use](#how-to-use)
- [Project Structure](#project-structure)
- [Code Architecture](#code-architecture)
- [Database Schema](#database-schema)
- [Known Limitations](#known-limitations)
- [Future Ideas](#future-ideas)

---

## Overview

| Field     | Details              |
|-----------|----------------------|
| Author    | Abdul-Majeed         |
| Language  | Python 3.x           |
| Libraries | `sqlite3`, `tabulate`|
| Database  | SQLite (`movies.db`) |
| Interface | Command-Line (CLI)   |
| Version   | 1.0                  |

---

## Features

- ✅ **Add Movies** — Enter a title, genre, and a rating from 1–10. Input is validated before anything gets saved.
- ✅ **View All Movies** — See your full collection in a clean table, sorted by rating (highest first).
- ✅ **Search by Title** — Partial keyword search. Type `dark` and it'll find `The Dark Knight`.
- ✅ **Filter by Minimum Rating** — Only want 8.5+ movies? Done.
- ✅ **Delete by ID** — View movies with their IDs, pick the one to remove.
- ✅ **Wipe Database** — Drops and recreates the table (asks for confirmation first).
- ✅ **Load 40 Sample Movies** — Instantly populate the database for testing.
- ✅ **Persistent Storage** — Data is saved in `movies.db` — nothing disappears on exit.

---

## Getting Started

### Prerequisites

- Python 3.x
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Abdul-Majeed-Git/movie-database.git

# 2. Navigate into the project folder
cd movie-collection-manager

# 3. Install the only external dependency
pip install tabulate

# 4. Run the app
python movie_manager.py
```

> The `movies.db` file is created automatically on first run. No manual setup needed.

---

## How to Use

When you run the script, you'll see this menu:

```
--- Movie Collection Management ---
1. Add Movie
2. View All Movies
3. Search Movie
4. Search Movie by minimum rating
5. Delete Movie by ID
6. Delete Entire Database Table
7. Add 40 sample movies to DB
8. Exit
```

| Option | Action | Notes |
|--------|--------|-------|
| 1 | Add Movie | Validates title, genre, and rating before saving |
| 2 | View All Movies | Sorted by rating, descending |
| 3 | Search by Title | Case-insensitive partial match |
| 4 | Filter by Rating | Enter a minimum rating (1–10) |
| 5 | Delete a Movie | Shows IDs first, then asks which to remove |
| 6 | Wipe Database | Drops the table — confirmation required |
| 7 | Load Sample Data | Adds 40 popular movies instantly |
| 8 | Exit | Exits cleanly |

---

## Project Structure

```
movie-collection-manager/
│
├── movie_manager.py   # All application logic
├── movies.db          # SQLite database (auto-generated)
└── README.md          # This file
```

---

## Code Architecture

The code is split into two classes and a main loop:

### `Movie` — Data Model
A simple container that holds a movie's `id`, `title`, `genre`, and `rating`. It doesn't touch the database — it just carries data from the user to the database layer.

### `MovieDatabase` — Data Access Layer
Handles everything database-related. Opens and closes its own SQLite connection per method (safe, no connection leaks). Exposes clean methods for every operation.

| Method | Description |
|--------|-------------|
| `__init__(db_name)` | Connects to the DB and creates the table if it doesn't exist |
| `add_movie(movie_obj)` | Inserts a new movie record |
| `view_movies_list()` | Prints all movies sorted by rating |
| `view_movies_with_id()` | Same, but includes the ID column |
| `search_movie(search_item)` | Partial title search |
| `search_movie_by_rating(min_rate)` | Filter by minimum rating |
| `delete_movie(id)` | Deletes by ID, returns `True`/`False` |
| `delete_movie_database()` | Drops the entire Movies table |

### Main Loop — UI Layer
A `while True` loop that drives the menu, reads input, validates it, and calls the right method. `KeyboardInterrupt` (Ctrl+C) is caught so the app exits gracefully.

---

## Database Schema

**Table: `Movies`**

| Column | Type    | Constraint               |
|--------|---------|--------------------------|
| ID     | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| title  | TEXT    | —                        |
| genre  | TEXT    | —                        |
| rate   | REAL    | —                        |

---

## Known Limitations

- **No duplicate detection** — You can add the same movie twice without a warning.
- **No edit/update function** — Can't modify an existing entry; have to delete and re-add.
- **Single-user, local only** — No network access or multi-user support.
- **No export** — Can't export your collection to CSV or JSON yet.

---

## Future Ideas

- [ ] Edit/update existing movie entries
- [ ] Duplicate detection on insert
- [ ] Export collection to CSV or JSON
- [ ] Filter by genre
- [ ] Sort by title alphabetically
- [ ] Simple web UI with Flask or FastAPI
- [ ] Mark movies as favourites

---

## License

This project is open source and free to use.