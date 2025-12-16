import os
import shutil
import sqlite3
import subprocess
from datetime import datetime

# ==========================
# CONFIGURATION
# ==========================
PROJECT_ROOT = os.getcwd()
BACKUP_ROOT = os.path.join(PROJECT_ROOT, "backups")

SQLITE_DB = "school.db"
MONGO_DB = "school_analytics"

CODE_DIRS = ["app", "etl"]
OPTIONAL_DIRS = ["dashboards", "logs"]
CONFIG_FILES = [".env", "docker-compose.yml"]

TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
CURRENT_BACKUP = os.path.join(BACKUP_ROOT, TIMESTAMP)

# ==========================
# UTILITY
# ==========================
def safe_copy(src, dst):
    if os.path.exists(src):
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# ==========================
# CREATE STRUCTURE
# ==========================
log("Creating backup directories...")
os.makedirs(CURRENT_BACKUP, exist_ok=True)

# ==========================
# SQLITE BACKUP
# ==========================
def backup_sqlite():
    log("Backing up SQLite database...")
    sqlite_backup_dir = os.path.join(CURRENT_BACKUP, "sqlite")
    os.makedirs(sqlite_backup_dir, exist_ok=True)

    src = os.path.join(PROJECT_ROOT, SQLITE_DB)
    dst = os.path.join(sqlite_backup_dir, f"school_backup_{TIMESTAMP}.db")

    conn = sqlite3.connect(src)
    with sqlite3.connect(dst) as bck:
        conn.backup(bck)
    conn.close()

    # Verification
    conn = sqlite3.connect(dst)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()
    conn.close()

    log(f"SQLite backup OK — {len(tables)} tables verified.")

# ==========================
# MONGODB BACKUP
# ==========================
def backup_mongodb():
    log("Backing up MongoDB...")
    mongo_backup_dir = os.path.join(CURRENT_BACKUP, "mongo")

    subprocess.run([
        "mongodump",
        "--db", MONGO_DB,
        "--out", mongo_backup_dir
    ], check=True)

    log("MongoDB dump completed.")

# ==========================
# CODE + FILE BACKUP
# ==========================
def backup_files():
    log("Backing up source code...")
    code_backup = os.path.join(CURRENT_BACKUP, "code")
    os.makedirs(code_backup, exist_ok=True)

    for folder in CODE_DIRS:
        safe_copy(folder, os.path.join(code_backup, folder))

    log("Backing up optional directories...")
    for folder in OPTIONAL_DIRS:
        safe_copy(folder, os.path.join(CURRENT_BACKUP, folder))

    log("Backing up config files...")
    config_backup = os.path.join(CURRENT_BACKUP, "config")
    os.makedirs(config_backup, exist_ok=True)

    for file in CONFIG_FILES:
        safe_copy(file, os.path.join(config_backup, file))

# ==========================
# EXECUTION
# ==========================
if __name__ == "__main__":
    try:
        backup_sqlite()
        backup_mongodb()
        backup_files()
        log("✅ BACKUP COMPLETED SUCCESSFULLY")
    except Exception as e:
        log(f"❌ BACKUP FAILED: {e}")
