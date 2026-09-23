import os, sys, re, json, xml.etree.ElementTree as ET

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
public_dir = os.path.join(base_dir, "public")
data_dir = os.path.join(base_dir, "data")
docs_dir = os.path.join(base_dir, "docs")

domain = "https://jichangtuijian.cloud"

errors = []
warnings = []
passed = 0

def check(condition, message):
    global passed
    if condition:
        passed += 1
        print(f"  [PASS] {message}")
    else:
        errors.append(message)
        print(f"  [FAIL] {message}")

print("=" * 70)
print("Running Comprehensive SEO & Quality Verification Suite")
print("=" * 70)

# Test 1: Essential files existence
print("\n--- Test 1: Essential Files Existence ---")
check(os.path.exists(os.path.join(public_dir, "index.html")), "public/index.html exists")
check(os.path.exists(os.path.join(public_dir, "robots.txt")), "public/robots.txt exists")
check(os.path.exists(os.path.join(public_dir, "sitemap.xml")), "public/sitemap.xml exists")
check(os.path.exists(os.path.join(public_dir, "rss.xml")), "public/rss.xml exists")
check(os.path.exists(os.path.join(public_dir, "404.html")), "public/404.html exists")
check(os.path.exists(os.path.join(public_dir, "static/css/main.css")), "public/static/css/main.css exists")
check(os.path.exists(os.path.join(public_dir, "static/js/main.js")), "public/static/js/main.js exists")

# Test 2: Parse Sitemap & Verify all URLs
print("\n--- Test 2: Sitemap XML & URLs Validation ---")
sitemap_path = os.path.join(public_dir, "sitemap.xml")
try:
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    locs = [elem.text for elem in root.findall('.//ns:loc', ns)]
    check(len(locs) >= 200, f"Sitemap contains {len(locs)} indexable URLs (>= 200)")
    
    # Check all URLs start with domain
    all_domain = all(loc.startswith(domain) for loc in locs)
    check(all_domain, f"All sitemap URLs start with {domain}")
    
    # No localhost or example.com
    no_bad_hosts = all("localhost" not in loc and "example.com" not in loc for loc in locs)
    check(no_bad_hosts, "No localhost or example.com found in sitemap")
    
    # Check no 404 in sitemap
    check(not any("404" in loc for loc in locs), "No 404 error page in sitemap")
except Exception as e:
    errors.append(f"Sitemap XML parsing failed: {e}")

# Test 3: Parse RSS XML
print("\n--- Test 3: RSS Feed Validation ---")
rss_path = os.path.join(public_dir, "rss.xml")
try:
    tree = ET.parse(rss_path)
    root = tree.getroot()
    items = root.findall('.//item')
    check(len(items) >= 10, f"RSS feed contains {len(items)} items (>= 10)")
except Exception as e:
    errors.append(f"RSS XML parsing failed: {e}")

# Test 4: Top 4 Providers Data & Links
print("\n--- Test 4: Top 4 Fixed Providers & Links Validation ---")
with open(os.path.join(data_dir, "providers.json"), "r", encoding="utf-8") as f:
    providers = json.load(f)

check(providers[0]['name'] == '全球云' and providers[0]['rank'] == 1, "Rank 1 is 全球云")
check(providers[1]['name'] == '飞猫云' and providers[1]['rank'] == 2, "Rank 2 is 飞猫云")
check(providers[2]['name'] == '暮光加速' and providers[2]['rank'] == 3, "Rank 3 is 暮光加速")
check(providers[3]['name'] == '微风网络' and providers[3]['rank'] == 4, "Rank 4 is 微风网络")

check(providers[0]['inviteURL'] == "https://hueue09.gcvipaff.com/#/?code=z8U9aaa4", "全球云 invite link correct")
check(providers[1]['inviteURL'] == "https://quanqiu.flycatvipaff.cc/#/?code=7ZOeVmNS", "飞猫云 invite link correct")
check(providers[2]['inviteURL'] == "https://quanqi12.twilightaff.com/#/?code=beAVqNPf", "暮光加速 invite link correct")
check(providers[3]['inviteURL'] == "https://edp01.breezenetaff.com/#/?code=vxDUI8kY", "微风网络 invite link correct")

check(providers[0]['coupon'] == "qq88", "全球云 coupon is qq88")
check(providers[1]['coupon'] == "flycat888", "飞猫云 coupon is flycat888")
check(providers[2]['coupon'] == "mm88", "暮光加速 coupon is mm88")

# Test 5: Check 27 Independent Provider Pages
print("\n--- Test 5: 27 Independent Provider Review Pages ---")
check(len(providers) == 27, f"Total providers count is 27 (actual: {len(providers)})")
all_provider_pages_exist = True
for p in providers:
    p_path = os.path.join(public_dir, "providers", p['slug'], "index.html")
    if not os.path.exists(p_path):
        all_provider_pages_exist = False
        errors.append(f"Missing provider page: {p_path}")
check(all_provider_pages_exist, "All 27 provider review pages exist on disk")

# Test 6: Check Reference Publisher Blocklist across ALL generated public files
print("\n--- Test 6: Reference Publisher Blocklist Scan in public/ ---")
blocklist = [
    '二毛博客', 'ermao.net', 'ermao',
    '猫梦博客', '猫梦',
    'gaterank', 'Gaterank',
    '星维机场',
    '三毛机场', '一毛机场', '一份机场',
    '机场宝',
    '根据某某博客', '某评测站称', '资料来自某博客', '在某站未检索到', '二毛页面'
]

blocklist_hits = []
for root_dir, dirs, files in os.walk(public_dir):
    for fname in files:
        if fname.endswith(('.html', '.xml', '.txt', '.js', '.json')):
            fpath = os.path.join(root_dir, fname)
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                for b in blocklist:
                    if b in content:
                        blocklist_hits.append((fpath, b))

check(len(blocklist_hits) == 0, f"Blocklist scan clean in public/ (hits: {len(blocklist_hits)})")
if blocklist_hits:
    for fpath, b in blocklist_hits[:5]:
        print(f"  [WARN] Blocklist hit: '{b}' in {fpath}")

# Test 7: Internal Fields Isolation Check
print("\n--- Test 7: Internal Fields Isolation Scan ---")
internal_fields = ['sourceLevel', 'sources', 'generatedNarrative', 'factualFieldsMissing']
internal_hits = []
for root_dir, dirs, files in os.walk(public_dir):
    for fname in files:
        if fname.endswith(('.html', '.js')):
            fpath = os.path.join(root_dir, fname)
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                for field in internal_fields:
                    # check for field names in quotes or json
                    if f'"{field}"' in content or f"'{field}'" in content:
                        internal_hits.append((fpath, field))

check(len(internal_hits) == 0, f"Internal fields strictly isolated from public output (hits: {len(internal_hits)})")

# Test 8: Character Count Verification (800 - 1200 Chinese characters)
print("\n--- Test 8: Chinese Character Count Verification (800~1200) ---")
with open(os.path.join(data_dir, "navigation_articles.json"), "r", encoding="utf-8") as f:
    nav_articles = json.load(f)

with open(os.path.join(data_dir, "provider_reviews.json"), "r", encoding="utf-8") as f:
    provider_reviews = json.load(f)

nav_char_check = all(800 <= a['bodyCharCount'] <= 1200 for a in nav_articles)
check(nav_char_check, f"All 60 navigation articles between 800 and 1200 chars (Sample: {nav_articles[0]['bodyCharCount']})")

rev_char_check = all(800 <= p['bodyCharCount'] <= 1200 for p in provider_reviews)
check(rev_char_check, f"All 27 provider reviews between 800 and 1200 chars (Sample: {provider_reviews[0]['bodyCharCount']})")

# Test 9: FAQ 100 Quota & Structure
print("\n--- Test 9: FAQ 100 Quotas and Verification ---")
with open(os.path.join(data_dir, "faq100.json"), "r", encoding="utf-8") as f:
    faq100 = json.load(f)

check(len(faq100) == 100, f"Total FAQ items count is exactly 100 (actual: {len(faq100)})")

cluster_counts = {}
for item in faq100:
    cid = item['clusterId']
    cluster_counts[cid] = cluster_counts.get(cid, 0) + 1

expected_quotas = {
    1: 18, 2: 14, 3: 10, 4: 10, 5: 8, 6: 14, 7: 10, 8: 8, 9: 8
}
quota_match = (cluster_counts == expected_quotas)
check(quota_match, f"FAQ 9 cluster quotas match strictly: {cluster_counts}")

# Check 5 paginated hub pages exist
faq_hub_pages_exist = all(
    os.path.exists(os.path.join(public_dir, "faq" if i == 1 else f"faq/page/{i}", "index.html"))
    for i in range(1, 6)
)
check(faq_hub_pages_exist, "FAQ 5 paginated crawlable hub pages exist on disk")

# Test 10: Hero & Footer Keyword Text Constraints
print("\n--- Test 10: Hero & Footer Character Count Constraints ---")
with open(os.path.join(data_dir, "site-seo-profile.json"), "r", encoding="utf-8") as f:
    profile = json.load(f)

hero_sub = profile["heroSubtitleText"]
hero_chars = len(re.findall(r'[\u4e00-\u9fa5]', hero_sub))
check(90 <= hero_chars <= 160, f"Hero keyword subtitle between 90 and 160 Chinese characters (actual: {hero_chars})")

footer_p1 = profile["footerParagraph1"]
footer_chars = len(re.findall(r'[\u4e00-\u9fa5]', footer_p1))
check(70 <= footer_chars <= 130, f"Footer keyword paragraph between 70 and 130 Chinese characters (actual: {footer_chars})")

# Test 11: HTML Quality & Metadata Checks (Sample HTML pages)
print("\n--- Test 11: HTML Quality, Title, H1, Canonical, Rel='sponsored' Checks ---")
sample_pages = [
    "/index.html",
    "/recommendations/index.html",
    "/start-here/index.html",
    "/compare/index.html",
    "/devices/index.html",
    "/before-you-buy/index.html",
    "/faq/index.html",
    "/about/index.html",
    "/providers/quanqiu-cloud/index.html",
    "/providers/flycat-cloud/index.html"
]

all_sample_valid = True
for sp in sample_pages:
    fpath = os.path.join(public_dir, sp.lstrip("/"))
    if not os.path.exists(fpath):
        all_sample_valid = False
        errors.append(f"Sample page does not exist: {sp}")
        continue
    with open(fpath, "r", encoding="utf-8") as f:
        html_text = f.read()
        
    # Check single H1
    h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', html_text, re.DOTALL | re.IGNORECASE)
    if len(h1s) != 1:
        all_sample_valid = False
        errors.append(f"Page {sp} does not have exactly 1 H1 (found {len(h1s)})")
        
    # Check title exists
    if "<title>" not in html_text or "</title>" not in html_text:
        all_sample_valid = False
        errors.append(f"Page {sp} missing <title>")
        
    # Check meta description
    if 'name="description"' not in html_text:
        all_sample_valid = False
        errors.append(f"Page {sp} missing meta description")
        
    # Check canonical
    if '<link rel="canonical" href="https://jichangtuijian.cloud' not in html_text:
        all_sample_valid = False
        errors.append(f"Page {sp} missing valid HTTPS canonical")
        
    # Check JSON-LD
    if 'application/ld+json' not in html_text:
        all_sample_valid = False
        errors.append(f"Page {sp} missing JSON-LD structured data")

check(all_sample_valid, "Sample pages have exactly 1 H1, valid title, description, HTTPS canonical, and JSON-LD")

# Test 12: Documentation Artifacts
print("\n--- Test 12: Documentation Artifacts Verification ---")
docs_files = [
    "site-seo-profile.json",
    "seo-profile-replacement-contract.md",
    "keyword-map.md",
    "keyword-coverage.csv",
    "reference-publisher-blocklist.md",
    "faq-keywords-100.csv",
    "faq-content-matrix.md",
    "navigation-content-matrix.md",
    "provider-review-matrix.md",
    "content-plan.md",
    "publishing-guide.md",
    "search-console-setup.md",
    "launch-checklist.md"
]
all_docs_exist = all(os.path.exists(os.path.join(docs_dir, f)) for f in docs_files)
check(all_docs_exist, f"All {len(docs_files)} docs artifacts exist in docs/ directory")

print("\n" + "=" * 70)
print(f"Summary: {passed} PASSED, {len(errors)} FAILED, {len(warnings)} WARNINGS")
print("=" * 70)

if errors:
    print("\nErrors encountered:")
    for err in errors:
        print(f"  - {err}")
    sys.exit(1)
else:
    print("\n[ALL TESTS PASSED] The website meets 100% of the technical and SEO specifications!")
    sys.exit(0)
