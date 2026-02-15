#!/usr/bin/env python3
"""
Fetches Blogger JSON feed and generates:
 - data/posts.json
 - data/posts.csv
 - sitemap.xml

Usage:
  python3 scripts/generate_blog_export.py --blog https://catfishheads.blogspot.com --out data
"""
from __future__ import annotations
import argparse
import csv
import json
import os
import re
import sys
from datetime import datetime
import requests
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

FEED_PATH = "/feeds/posts/default?alt=json&max-results=9999"

def fetch_feed(blog_url: str) -> dict:
    url = blog_url.rstrip("/") + FEED_PATH
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return r.json()

def extract_entries(feed_json: dict) -> list[dict]:
    entries = feed_json.get("feed", {}).get("entry", []) or []
    out = []
    for e in entries:
        # title
        title = e.get("title", {}).get("$t", "")
        # url: find alternate link
        url = ""
        for link in e.get("link", []):
            if link.get("rel") == "alternate":
                url = link.get("href")
                break
        # published
        published = e.get("published", {}).get("$t", "")
        # labels
        labels = [c.get("term") for c in e.get("category", []) if c.get("term")]
        # summary/excerpt
        summary = e.get("summary", {}).get("$t") or e.get("content", {}).get("$t", "")
        # find first image src
        image = None
        m = re.search(r'<img[^>]+src="([^"]+)"', summary)
        if m:
            image = m.group(1)
        out.append({
            "title": title,
            "url": url,
            "published": published,
            "labels": labels,
            "excerpt": re.sub(r"<[^>]+>", "", (summary or "") )[:500],
            "image": image,
        })
    return out

def write_json(out_dir: str, entries: list[dict]):
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "posts.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(entries, fh, ensure_ascii=False, indent=2)
    print("Wrote", path)

def write_csv(out_dir: str, entries: list[dict]):
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "posts.csv")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["title", "url", "published", "labels", "image", "excerpt"])
        for e in entries:
            writer.writerow([
                e.get("title",""),
                e.get("url",""),
                e.get("published",""),
                ";".join(e.get("labels",[])),
                e.get("image",""),
                e.get("excerpt",""),
            ])
    print("Wrote", path)

def write_sitemap(root_url: str, out_dir: str, entries: list[dict]):
    urlset = Element("urlset")
    urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
    for e in entries:
        if not e.get("url"):
            continue
        url = SubElement(urlset, "url")
        loc = SubElement(url, "loc")
        loc.text = e["url"]
        if e.get("published"):
            try:
                dt = datetime.fromisoformat(e["published"].replace("Z","+00:00"))
                lastmod = SubElement(url, "lastmod")
                lastmod.text = dt.date().isoformat()
            except Exception:
                pass
    raw = tostring(urlset, "utf-8")
    pretty = minidom.parseString(raw).toprettyxml(indent="  ")
    path = os.path.join(out_dir, "sitemap.xml")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(pretty)
    print("Wrote", path)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--blog", required=True, help="Blog base URL, e.g. https://catfishheads.blogspot.com")
    p.add_argument("--out", default="data", help="Output directory")
    args = p.parse_args()
    feed = fetch_feed(args.blog)
    entries = extract_entries(feed)
    write_json(args.out, entries)
    write_csv(args.out, entries)
    write_sitemap(args.blog, args.out, entries)

if __name__ == "__main__":
    main()