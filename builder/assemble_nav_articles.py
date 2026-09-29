# -*- coding: utf-8 -*-
"""
Assemble all 66 navigation articles from builder/sections/*.py into data/navigation_articles.json
"""

import os, sys, json, re

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_dir)

from builder.sections import start_here, service, compare, devices, before_you_buy, recommendations

modules = [
    start_here,
    service,
    compare,
    devices,
    before_you_buy,
    recommendations
]

all_articles = []
for m in modules:
    arts = m.get_articles()
    for a in arts:
        # Ensure all required fields exist
        section = a["section"]
        slug = a["slug"]
        url = f"/{section}/{slug}/"
        body = a["body"].strip()
        body_char_count = len(re.findall(r'[\u4e00-\u9fa5]', body))
        
        entry = {
            "section": section,
            "sectionName": a["sectionName"],
            "title": a["title"],
            "h1": a["h1"],
            "slug": slug,
            "url": url,
            "primaryKeyword": a["primaryKeyword"],
            "secondaryKeywords": a["secondaryKeywords"],
            "metaDescription": a["metaDescription"],
            "searchIntent": a["searchIntent"],
            "body": body,
            "bodyCharCount": body_char_count,
            "lastChecked": a.get("lastChecked", "2026-09-28")
        }
        all_articles.append(entry)

assert len(all_articles) == 66, f"Expected 66 articles, got {len(all_articles)}"

# Verify uniqueness of slugs, urls, and primaryKeywords
slugs = set()
urls = set()
keywords = set()
for a in all_articles:
    assert a["slug"] not in slugs, f"Duplicate slug: {a['slug']}"
    assert a["url"] not in urls, f"Duplicate url: {a['url']}"
    assert a["primaryKeyword"] not in keywords, f"Duplicate keyword: {a['primaryKeyword']}"
    slugs.add(a["slug"])
    urls.add(a["url"])
    keywords.add(a["primaryKeyword"])

output_path = os.path.join(base_dir, "data", "navigation_articles.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(all_articles, f, ensure_ascii=False, indent=2)

print(f"Successfully assembled {len(all_articles)} unique articles to {output_path}")
print(f"All 66 slugs unique, all 66 primary keywords unique.")
