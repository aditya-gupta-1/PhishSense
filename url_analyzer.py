import re
import sqlite3
from datetime import datetime
from config import DB_PATH, BLOCKLIST_PATH

def analyze_url(url):
    verdict = "Benign"
    if is_suspicious(url):
        verdict = "Phishing"
        add_to_blocklist(url)

    log_to_db(url, verdict)
    if verdict == "Phishing":
        print(f"ALERT: Phishing URL detected! -> {url}")

def is_suspicious(url):
    bad_keywords = ["login", "secure", "verify", "reset"]
    bad_tlds = [".tk", ".xyz", ".gq", ".ml"]
    has_ip = bool(re.search(r"http[s]?://\d+\.\d+\.\d+\.\d+", url))

    keyword_match = any(k in url.lower() for k in bad_keywords)
    tld_match = any(url.endswith(tld) for tld in bad_tlds)

    return keyword_match or tld_match or has_ip

def log_to_db(url, verdict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS incidents (id INTEGER PRIMARY KEY AUTOINCREMENT, verdict TEXT, url TEXT, timestamp TEXT)")
    c.execute("INSERT INTO incidents (verdict, url, timestamp) VALUES (?, ?, ?)",
              (verdict, url, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def add_to_blocklist(url):
    domain = url.split("/")[2]
    with open(BLOCKLIST_PATH, "a") as f:
        f.write(domain + "\n")
