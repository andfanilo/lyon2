#! /usr/bin/env python3
"""Generate fake HTTP access logs (Apache combined format) on stdout.

Without arguments, writes one line per second forever (used by start_logs.sh).
With --count N, writes N lines immediately and exits.
"""

from datetime import datetime
from pathlib import Path
from urllib.parse import quote
import argparse
import json
import random
import sys
import time

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


class IPGenerator:
    def __init__(self, session_count, session_length):
        self.session_count = session_count
        self.session_length = session_length
        self.sessions = {}

    def get_ip(self):
        self.session_gc()
        self.session_create()
        ip = random.choice(list(self.sessions))
        self.sessions[ip] += 1
        return ip

    def session_create(self):
        while len(self.sessions) < self.session_count:
            self.sessions[self.random_ip()] = 0

    def session_gc(self):
        self.sessions = {ip: n for ip, n in self.sessions.items() if n < self.session_length}

    def random_ip(self):
        octets = [str(random.randrange(223) + 1)]
        octets += [str(random.randrange(255)) for _ in range(3)]
        return ".".join(octets)


class LogGenerator:
    REQUESTS = {
        "/departments": 40,
        "/department/*DEPARTMENT*/categories": 20,
        "/department/*DEPARTMENT*/products": 10,
        "/categories/*CATEGORY*/products": 5,
        "/product/*PRODUCT*": 10,
        "/add_to_cart/*PRODUCT*": 5,
        "/login": 5,
        "/logout": 2,
        "/checkout": 3,
        "/support": 1
    }

    RESPONSE_CODES = {
        200: 92,
        404: 5,
        503: 3,
    }

    USER_AGENTS = {
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36": 11,
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0": 6,
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36": 5,
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36": 4,
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.77.4 (KHTML, like Gecko) Version/7.0.5 Safari/537.77.4": 4,
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36": 3,
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:30.0) Gecko/20100101 Firefox/30.0": 3,
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.76.4 (KHTML, like Gecko) Version/7.0.4 Safari/537.76.4": 3,
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36": 2,
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36": 2,
        "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0": 2,
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36": 2,
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko": 2,
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36": 2,
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:30.0) Gecko/20100101 Firefox/30.0": 1,
        "Mozilla/5.0 (Windows NT 6.1; rv:30.0) Gecko/20100101 Firefox/30.0": 1
    }

    def __init__(self, ipgen):
        self.ipgen = ipgen
        products = load_json("products.json")
        depts = load_json("departments.json")
        cats = load_json("categories.json")
        # Cheaper products are requested more often.
        self.products = {p["product_id"]: int(5000 / p["product_price"]) for p in products}
        self.departments = {d["department_name"]: 1 for d in depts}
        self.categories = {c["category_name"]: 1 for c in cats}

    def write_qps(self, dest, qps):
        sleep = 1.0 / qps
        while True:
            self.write(dest, 1)
            time.sleep(sleep)

    def write(self, dest, count):
        for _ in range(count):
            request = (
                pick_weighted_key(self.REQUESTS)
                .replace("*PRODUCT*", str(pick_weighted_key(self.products)))
                .replace("*DEPARTMENT*", pick_weighted_key(self.departments))
                .replace("*CATEGORY*", pick_weighted_key(self.categories))
                .lower()
            )
            dest.write('%s - - [%s] "GET %s HTTP/1.1" %s %s "-" "%s"\n' % (
                self.ipgen.get_ip(),
                datetime.now().astimezone().strftime("%d/%b/%Y:%H:%M:%S %z"),
                quote(request),
                pick_weighted_key(self.RESPONSE_CODES),
                random.randrange(2 * 1024) + 192,
                pick_weighted_key(self.USER_AGENTS),
            ))
            dest.flush()


def load_json(name):
    return json.loads((DATA_DIR / name).read_text(encoding="utf-8"))


def pick_weighted_key(weights):
    # Zero weights (e.g. products priced above 5000) are never picked.
    keys = [k for k, w in weights.items() if w > 0]
    return random.choices(keys, weights=[weights[k] for k in keys])[0]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--count", type=int, help="write COUNT lines and exit instead of streaming")
    args = parser.parse_args()

    generator = LogGenerator(IPGenerator(100, 10))
    if args.count:
        generator.write(sys.stdout, args.count)
    else:
        generator.write_qps(sys.stdout, 1)
