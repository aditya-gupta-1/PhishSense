import time
from url_analyzer import analyze_url

LOG_FILE = "data/sample_log.log"
SEEN_LINES = set()

def tail_file():
    while True:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
            for line in lines:
                if line not in SEEN_LINES:
                    SEEN_LINES.add(line)
                    url = extract_url(line)
                    if url:
                        analyze_url(url)
        time.sleep(5)

def extract_url(line):
    parts = line.strip().split(" ")
    for part in parts:
        if part.startswith("http://") or part.startswith("https://"):
            return part
    return None

if __name__ == "__main__":
    tail_file()
