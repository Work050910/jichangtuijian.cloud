import json, os

with open('data/navigation_articles.json', 'r', encoding='utf-8') as f:
    nav_articles = json.load(f)

with open('data/provider_reviews.json', 'r', encoding='utf-8') as f:
    provider_reviews = json.load(f)

with open('data/faq100.json', 'r', encoding='utf-8') as f:
    faq100 = json.load(f)

search_items = []

# 1. Main landing pages
main_pages = [
    {"title": "机场推荐总榜：按预算与场景科学选型", "url": "/recommendations/", "type": "推荐榜", "keywords": "机场推荐 性价比机场 稳定机场"},
    {"title": "性价比机场推荐：按预算与流量选择指南", "url": "/recommendations/value/", "type": "性价比", "keywords": "便宜机场 低价机场 性价比"},
    {"title": "Clash 机场推荐：兼容性、套餐与节点选择", "url": "/recommendations/clash/", "type": "Clash", "keywords": "Clash 订阅 客户端"},
    {"title": "AI 机场推荐：ChatGPT、Claude、Gemini 工具选型", "url": "/recommendations/ai/", "type": "AI工具", "keywords": "AI 机场 ChatGPT Claude"},
    {"title": "新手开始指南：从核心术语到客户端导入", "url": "/start-here/", "type": "新手", "keywords": "新手 怎么开始 基础"},
    {"title": "方案对比：主流机场入门与大流量套餐对比", "url": "/compare/", "type": "对比", "keywords": "套餐对比 价格 流量"},
    {"title": "设备入口：Windows/Mac/iOS/Android 配置教程", "url": "/devices/", "type": "设备", "keywords": "Windows Mac iPhone Android"},
    {"title": "使用须知：购买机场前 8 项避坑核验清单", "url": "/before-you-buy/", "type": "须知", "keywords": "购买前须知 退款 账号安全"},
    {"title": "常见问题解答中心 (FAQ 100 问)", "url": "/faq/", "type": "问答", "keywords": "FAQ 常见问题 答疑"},
    {"title": "机场优惠码汇总与核验", "url": "/coupons/", "type": "优惠", "keywords": "优惠码 折扣 券"}
]

for p in main_pages:
    search_items.append(p)

# 2. 27 Providers
for p in provider_reviews:
    search_items.append({
        "title": f"{p['name']} 机场测评：价格、套餐与适合人群",
        "url": p['url'],
        "type": "服务商测评",
        "keywords": f"{p['name']} {p['primaryKeyword']} {p['priceFrom']} {p['suitableFor']}"
    })

# 3. 60 Navigation Articles
for a in nav_articles:
    search_items.append({
        "title": a['h1'],
        "url": a['url'],
        "type": a['sectionName'],
        "keywords": f"{a['primaryKeyword']} {a['searchIntent']} {' '.join(a['secondaryKeywords'])}"
    })

# 4. Top 20 FAQs
for faq in faq100[:30]:
    search_items.append({
        "title": faq['questionTitle'],
        "url": f"/faq/{faq['slug']}/",
        "type": "FAQ 问答",
        "keywords": f"{faq['primaryKeyword']} {faq['cluster']} {' '.join(faq['supportingKeywords'])}"
    })

print(f"Total search index items: {len(search_items)}")

js_content = f"window.SITE_SEARCH_INDEX = {json.dumps(search_items, ensure_ascii=False, indent=2)};\n"

with open('src/static/js/search-data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Saved src/static/js/search-data.js.")
