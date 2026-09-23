import csv, json, re

# Read KeywordStats_9_19_2026.csv
keywords_raw = []
with open('KeywordStats_9_19_2026.csv', 'r', encoding='utf-8-sig') as f:
    r = csv.reader(f)
    header = next(r)
    for row in r:
        if row:
            keywords_raw.append({
                'keyword': row[0].strip(),
                'trend': row[1].strip(),
                'impressions': int(row[2].strip()) if row[2].strip().isdigit() else 0
            })

print(f"Loaded {len(keywords_raw)} keywords from CSV.")

# Reference publisher blocklist
blocklist_terms = [
    '二毛博客', 'ermao.net', 'ermao',
    '猫梦博客', '猫梦',
    'gaterank', 'Gaterank',
    '星维机场',
    '三毛机场', '一毛机场', '一份机场',
    '机场宝'
]

with open('docs/reference-publisher-blocklist.md', 'w', encoding='utf-8') as f:
    f.write("# 内部参考发布者与敏感来源隔离黑名单\n\n")
    f.write("> **警告**：本项目内部参考整理资料可能包含第三方博主、评测站或竞品站点的标识。本文件所列词汇严禁出现在公开站点的任何可见 HTML、标题、Meta、正文、JSON-LD、URL、RSS 或 Sitemap 中。\n\n")
    f.write("## 隔离发布者与域名列表\n\n")
    for t in blocklist_terms:
        f.write(f"- `{t}`\n")
    f.write("\n## 隔离来源表达句式\n\n")
    f.write("- `根据某某博客`\n")
    f.write("- `某评测站称`\n")
    f.write("- `资料来自某博客`\n")
    f.write("- `在某站未检索到`\n")
    f.write("- `二毛页面`\n")
    f.write("- `参考资料` / `出处` 栏目\n")

print("Created docs/reference-publisher-blocklist.md.")

# Keyword clustering and coverage
# Clusters:
# 1. 商业推荐与选型 (recommendations, value, clash, rankings, nodes, coupons)
# 2. 客户端与协议知识 (clash, ss, trojan, vpn, client)
# 3. 新手指南与购买决策 (guides, start-here, before-you-buy, service)
# 4. 常见问题 (faq)
# 5. 内部研究/隔离词 (blocklist, non-compliant)

coverage_rows = []

# High-priority user project keywords
project_core_keywords = [
    ("机场推荐", "user_core", "商业推荐与选型", "commercial", "/recommendations/"),
    ("机场服务", "user_core", "新手指南与购买决策", "informational", "/service/"),
    ("机场套餐", "user_core", "新手指南与购买决策", "commercial", "/compare/"),
    ("机场订阅", "user_core", "客户端与协议知识", "informational", "/start-here/"),
    ("机场新手教程", "user_core", "新手指南与购买决策", "informational", "/start-here/"),
    ("机场推荐云", "user_core", "品牌总入口", "brand", "/"),
    ("AI 机场推荐", "user_seed", "商业推荐与选型", "commercial", "/recommendations/ai/"),
    ("AI 工具使用场景怎么选机场", "user_seed", "商业推荐与选型", "informational", "/recommendations/ai-tools/"),
    ("AI 办公机场推荐", "user_seed", "商业推荐与选型", "commercial", "/recommendations/ai-office/")
]

for kw, src, cluster, intent, primary_url in project_core_keywords:
    coverage_rows.append({
        'keyword': kw,
        'normalized_keyword': kw.lower().replace(' ', ''),
        'impressions': 99999,
        'trend': '[user_priority]',
        'cluster': cluster,
        'intent': intent,
        'public_status': '公开使用',
        'primary_url': primary_url,
        'supporting_urls': '/ /recommendations/ /service/ /compare/',
        'placement_plan': 'Hero / H1 / 导航 / 核心推荐落地页',
        'notes': '用户填报核心或指定种子词'
    })

# Process the 100 CSV keywords
for item in keywords_raw:
    kw = item['keyword']
    norm_kw = kw.lower().replace(' ', '')
    impr = item['impressions']
    trend = item['trend']
    
    # Check blocklist
    is_blocked = False
    for b in blocklist_terms:
        if b.lower() in norm_kw:
            is_blocked = True
            break
            
    # Check non-compliant / sensitive terms
    sensitive_words = ['翻墙', '科学上网', '牛逼']
    is_sensitive = any(s in kw for s in sensitive_words)
    
    if is_blocked:
        public_status = '内部隔离（不用于公开页面）'
        cluster = '内部参考研究'
        intent = 'competitor_reference'
        primary_url = 'N/A'
        placement = '不公开展示，仅作内部竞品及研究隔离'
        notes = '命中参考发布者黑名单，禁止出现于公开产物'
    elif is_sensitive:
        public_status = '内部研究（不用于公开页面）'
        cluster = '合规隔离'
        intent = 'non_compliant'
        primary_url = 'N/A'
        placement = '不用于公开页面'
        notes = '不符合网络服务合规表达边界'
    elif '梯子' in kw:
        # User explicitly requested neutral conversational context
        public_status = '公开使用（中立口语解释语境）'
        cluster = '网络工具与常识说明'
        intent = 'informational'
        primary_url = '/faq/'
        placement = 'FAQ 与新手术语解释，中立网络服务语境'
        notes = '中立解释口语搜索词与使用注意事项'
    elif any(k in kw for k in ['clash', 'Clash']):
        public_status = '公开使用'
        cluster = '客户端与协议'
        intent = 'commercial_informational'
        primary_url = '/recommendations/clash/'
        placement = 'Clash 落地页与教程'
        notes = '高展现客户端意图词'
    elif any(k in kw for k in ['性价比', '便宜', '低价', '划算']):
        public_status = '公开使用'
        cluster = '商业推荐与选型'
        intent = 'commercial'
        primary_url = '/recommendations/value/'
        placement = '性价比机场与方案对比落地页'
        notes = '核心转化意图词'
    elif any(k in kw for k in ['排行', '排行榜']):
        public_status = '公开使用'
        cluster = '商业推荐与选型'
        intent = 'commercial'
        primary_url = '/rankings/'
        placement = '排行榜落地页（说明排序逻辑）'
        notes = '高意图候选词'
    elif any(k in kw for k in ['测评', '评测', '测速']):
        public_status = '公开使用'
        cluster = '服务评测与分析'
        intent = 'informational_commercial'
        primary_url = '/reviews/'
        placement = '评测汇总与独立测评页'
        notes = '高展现评测词'
    elif any(k in kw for k in ['节点']):
        public_status = '公开使用'
        cluster = '节点与线路说明'
        intent = 'informational'
        primary_url = '/nodes/'
        placement = '节点推荐与地区选择指南'
        notes = '网络节点选型'
    elif any(k in kw for k in ['ssr', 'trojan', 'ss', 'vpn', '协议']):
        public_status = '公开使用'
        cluster = '客户端与协议知识'
        intent = 'informational'
        primary_url = '/devices/'
        placement = '设备与协议知识库'
        notes = '协议中立知识词'
    elif any(k in kw for k in ['优惠', '优惠码', '折扣']):
        public_status = '公开使用'
        cluster = '商业推荐与选型'
        intent = 'commercial'
        primary_url = '/coupons/'
        placement = '优惠码核验与汇总页'
        notes = '强转化意图词'
    else:
        public_status = '公开使用'
        cluster = '综合推荐与教程'
        intent = 'commercial_informational'
        primary_url = '/recommendations/'
        placement = '综合推荐文章与栏目页'
        notes = '通用机场推荐意图'

    coverage_rows.append({
        'keyword': kw,
        'normalized_keyword': norm_kw,
        'impressions': impr,
        'trend': trend,
        'cluster': cluster,
        'intent': intent,
        'public_status': public_status,
        'primary_url': primary_url,
        'supporting_urls': '/recommendations/ /compare/ /start-here/',
        'placement_plan': placement,
        'notes': notes
    })

# Write docs/keyword-coverage.csv
with open('docs/keyword-coverage.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'keyword', 'normalized_keyword', 'impressions', 'trend', 'cluster',
        'intent', 'public_status', 'primary_url', 'supporting_urls',
        'placement_plan', 'notes'
    ])
    writer.writeheader()
    for row in coverage_rows:
        writer.writerow(row)

print("Generated docs/keyword-coverage.csv successfully.")

# Write docs/keyword-map.md
with open('docs/keyword-map.md', 'w', encoding='utf-8') as f:
    f.write("# 关键词战略与搜索意图页面映射说明 (Keyword Map)\n\n")
    f.write("本文档系统阐述本项目在 Google / Bing 自然搜索中的关键词聚类、意图映射、合规隔离与落地页规划。\n\n")
    f.write("## 1. 核心商业与推荐意图集群\n\n")
    f.write("- **主推落地页**：`/recommendations/`（综合推荐）、`/recommendations/value/`（性价比）、`/recommendations/clash/`（Clash推荐）、`/rankings/`（排序说明）\n")
    f.write("- **核心词群**：性价比机场、机场推荐 clash、便宜机场、低价机场、稳定机场、专线机场、顶级机场（指标化解读）\n")
    f.write("- **转化路径**：解决选型焦虑 -> 展示前四名固定服务（全球云、飞猫云、暮光加速、微风网络）对比卡片 -> 引导查看当前套餐与结算页\n\n")
    f.write("## 2. 节点与线路选型集群\n\n")
    f.write("- **主推落地页**：`/nodes/`、`/service/`\n")
    f.write("- **核心词群**：机场节点、节点推荐、vpn 节点、香港/日本/新加坡/美国节点选择、倍率与延迟\n\n")
    f.write("## 3. 客户端与协议知识集群\n\n")
    f.write("- **主推落地页**：`/devices/`、`/start-here/`\n")
    f.write("- **核心词群**：Clash 订阅、Trojan 协议、SSR、SS 协议、Shadowrocket、sing-box\n")
    f.write("- **定位**：中立技术概念科普、兼容性与隐私配置指南，不写规避或滥用教程\n\n")
    f.write("## 4. 常见问题与口语长尾词集群 (FAQ 100)\n\n")
    f.write("- **主推落地页**：`/faq/`\n")
    f.write("- **核心词群**：网络梯子服务选择、“梯子”中立术语解析、连接失败排查、退款规则、多设备并发、流量用尽处理\n\n")
    f.write("## 5. 合规与参考源隔离规则\n\n")
    f.write("- 严禁将参考博客（如二毛博客、猫梦博客等）名称或外链公开写入页面。\n")
    f.write("- 严禁使用“翻墙”“100%保证可用”“全网第一”等违规表达。\n")

print("Generated docs/keyword-map.md successfully.")
