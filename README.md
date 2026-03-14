# COROS Running App

A personal CLI running dashboard built on your own `.fit` file exports from COROS. Your data, your way — no subscriptions, no third-party dashboards.

---

## Requirements

- Python 3.12+
- PostgreSQL 14+
- A COROS watch with `.fit` file exports

---

## 1. PostgreSQL Setup

### Install PostgreSQL (if not already installed)
```bash
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql   # start on boot
```

### Create the database and user
```bash
sudo -i -u postgres psql
```

Inside psql:
```sql
CREATE DATABASE running;
CREATE USER running_user WITH PASSWORD 'running';
GRANT ALL PRIVILEGES ON DATABASE running TO running_user;
\c running
GRANT ALL ON SCHEMA public TO running_user;
\q
```

---

## 2. Project Setup

### Clone / navigate to the project
```bash
cd ~/Projects/cheeseboard
```

### Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Configure the database connection
Edit `db.py` and update the connection string if needed:
```python
DB_URL = "postgresql+psycopg2://running_user:running@localhost/running"
```

### Initialize the database (creates all tables)
```bash
python app.py init
```

---

## 3. Exporting .fit Files from COROS

1. Open the COROS app on your phone
2. Tap the activity you want to export
3. Tap the share icon → Export → `.fit` file
4. Transfer the file to your machine (AirDrop, email, USB, etc.)
5. Place it anywhere accessible — you'll pass the path to the import command

---

## 4. Usage

### Import a run
```bash
python app.py import ~/Downloads/my_run.fit
```

### List recent runs
```bash
python app.py runs                  # last 10 runs
python app.py runs --limit 20       # last 20 runs
```

### View a single run in detail
Shows splits, HR zones, elevation, and pace breakdown.
```bash
python app.py run 1                 # run with ID 1
```

### Weekly trends
```bash
python app.py trends                # last 8 weeks
python app.py trends --weeks 16     # last 16 weeks
```

### Personal records
```bash
python app.py pr
```
Shows your best pace across standard distances: 1 Mile, 5K, 10K, Half Marathon, Marathon.

### Generate an AI training plan
Requires an Anthropic API key (see below).
```bash
python app.py plan --race "Detroit Half Marathon" --date 2025-10-19
python app.py plan --race "Detroit Marathon" --date 2025-10-19 --goal "3:30:00"
```

---

## 5. AI Training Plans (Optional)

The `plan` command uses the Anthropic API to generate a week-by-week training plan based on your recent run history.

### Get an API key
Sign up at [console.anthropic.com](https://console.anthropic.com) and create an API key.

### Set the environment variable
```bash
export ANTHROPIC_API_KEY=your_key_here
```

To persist it across sessions, add that line to your `~/.bashrc` or `~/.zshrc`.

---

## 6. Project Structure

```
app.py                  # CLI entry point
db.py                   # DB connection and init
parser.py               # .fit file parser — core of the import pipeline
requirements.txt

models/
  runner.py             # Runner profile (you)
  run.py                # One row per activity
  fit_data.py           # imported data points from .fit files

commands/
  import_run.py         # `python app.py import`
  runs.py               # `python app.py runs` and `python app.py run <id>`
  trends.py             # `python app.py trends`
  pr.py                 # `python app.py pr`
  plan.py               # `python app.py plan`
```

---

## 7. Useful PostgreSQL Commands

```bash
# Connect to the running database
sudo -u postgres psql -d running

# Or as running_user
psql -U running_user -d running -h localhost
```

Inside psql:
```sql
\dt                          -- list all tables
\d runs                      -- describe the runs table
SELECT * FROM runs;          -- view all runs
SELECT * FROM runners;       -- view runner profiles

-- Weekly mileage summary
SELECT date_trunc('week', date) AS week,
       COUNT(*) AS runs,
       ROUND(SUM(distance_m) / 1609.34, 1) AS miles
FROM runs
GROUP BY week
ORDER BY week DESC;
```

---

## 8. Re-initializing the Database

This will **delete all data** — use with caution:
```bash
# In psql as postgres:
\c running
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO running_user;
\q

# Then recreate tables:
python app.py init
```

## 9. Draeam goal 

I'd like this to eventually turn into a visual GUI for users to interact with other than 
command line. 

PyQt6 is something to look into for that, as well as PySide6