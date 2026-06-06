#!/usr/bin/env python3
"""Submit ErgoWorkspace sitemap URLs to Bing via IndexNow."""
import urllib.request
import urllib.parse
import json
import xml.etree.ElementTree as ET
import os
import sys

SITEMAP_URL = "https://www.gadgethumans.com/ergo-workspace/sitemap.xml"
INDEXNOW_URL = "https://api.indexnow.org/indexnow"
API_KEY = "c1830cb07b6b45d9a97f5d6b302e8be0"
KEY_LOCATION = f"https://www.gadgethumans.com/{API_KEY}.txt"

# Check key file exists on site
key_check = urllib.request.urlopen(f"https://www.gadgethumans.com/{API_KEY}.txt")
if key_check.status != 200:
    print(f"Key file check failed: {key_check.status}")
    sys.exit(1)

# Fetch sitemap
resp = urllib.request.urlopen(SITEMAP_URL)
tree = ET.fromstring(resp.read())
ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
urls = [loc.text for loc in tree.findall("ns:url/ns:loc", ns)]
print(f"Found {len(urls)} URLs in sitemap")

# Submit in batches of 10
for i in range(0, len(urls), 10):
    batch = urls[i:i+10]
    payload = {
        "host": "www.gadgethumans.com",
        "key": API_KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": batch
    }
    data = json.dumps(payload).encode()
    req = urllib.request.Request(INDEXNOW_URL, data=data, 
        headers={"Content-Type": "application/json"})
    try:
        resp = urllib.request.urlopen(req)
        print(f"Batch {i//10+1}: {resp.status} ({len(batch)} URLs)")
    except urllib.error.HTTPError as e:
        print(f"Batch {i//10+1}: HTTP {e.code} - {e.read().decode()[:200]}")

print("Done")
