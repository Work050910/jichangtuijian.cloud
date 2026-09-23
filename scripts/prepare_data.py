import zipfile, xml.etree.ElementTree as ET, json, csv, re, os

# 1. Parse docx
with zipfile.ZipFile('机场博客内容') as z:
    xml_data = z.read('word/document.xml')
    rels_data = z.read('word/_rels/document.xml.rels')

rels_root = ET.fromstring(rels_data)
rels = {c.attrib.get('Id'): c.attrib.get('Target') for c in rels_root}

doc_root = ET.fromstring(xml_data)

lines = []
for p in doc_root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
    texts = []
    links = []
    for elem in p.iter():
        if elem.tag == '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t':
            if elem.text:
                texts.append(elem.text)
        elif elem.tag == '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}hyperlink':
            rid = elem.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
            if rid in rels:
                links.append(rels[rid])
    t = ''.join(texts).strip()
    if t:
        lines.append((t, links))

start_idx = 0
for idx, (t, l) in enumerate(lines):
    if t == '机场详细资料':
        start_idx = idx
        break

provider_raw_blocks = []
current_block = []
for t, l in lines[start_idx+1:]:
    if any(t.startswith(f'{i:02d}  ') for i in range(1, 28)):
        if current_block:
            provider_raw_blocks.append(current_block)
        current_block = [(t, l)]
    else:
        current_block.append((t, l))
if current_block:
    provider_raw_blocks.append(current_block)

print(f"Extracted {len(provider_raw_blocks)} provider blocks from docx.")

def sanitize_text(text):
    if not text:
        return text
    # Strip reference publishers
    text = re.sub(r'二毛博客|二毛页面|二毛', '公开资料', text)
    text = re.sub(r'猫梦博客|猫梦', '公开记录', text)
    text = re.sub(r'gaterank|Gaterank', '公开排行', text)
    text = re.sub(r'机场宝补充[：:]?', '', text)
    text = re.sub(r'该条不是公开资料的精确对应页面记录[。；]?', '', text)
    text = re.sub(r'公开资料中未检索到能够精确确认是本邀请域名对应服务的独立页面[，,]?', '需在邀请页确认当前阶梯与重置包规则。', text)
    text = re.sub(r'该站同样未核实套餐与节点[，,]?', '', text)
    text = re.sub(r'二毛', '服务商', text)
    return text.strip()

slug_map = {
    '全球云': 'quanqiu-cloud',
    '飞猫云': 'flycat-cloud',
    '暮光加速': 'twilight',
    '微风网络': 'breezenet',
    'U1S1': 'u1s1',
    '极连云': 'jilian-cloud',
    '光年梯': 'guangnian-ladder',
    '光速云': 'guangsu-cloud',
    '唯兔云': 'weitu-cloud',
    '宇宙云': 'yuzhou-cloud',
    '速界': 'sujie',
    'SOGO 云': 'sogo-cloud',
    '快狸': 'kuaili',
    '二猫云': 'two-cats-cloud',
    '一翻云': 'yifan-cloud',
    '边缘节点（EdgeNova）': 'edgenova',
    '可信云': 'kexin-cloud',
    '浪网（WaveNet）': 'wavenet',
    '梯子云（LadderCloud）': 'ladder-cloud',
    '灵动云': 'lingdong-cloud',
    '隐形人': 'yinxingren',
    'FlyV（飞V）': 'flyv',
    '无忧链接': 'wuyou-link',
    '灵猫网络（Civet）': 'civet-network',
    '闪跃（FlashLeap）': 'flashleap',
    'Firefly': 'firefly',
    '跨界云': 'kuajie-cloud'
}

providers_data = []

for b in provider_raw_blocks:
    header = b[0][0]
    m = re.match(r'^(\d+)\s+(.+)$', header)
    if not m:
        continue
    orig_name = m.group(2).strip()
    
    clean_name = orig_name
    alt_name = ""
    if '（' in orig_name and '）' in orig_name:
        clean_name = orig_name.split('（')[0].strip()
        alt_name = orig_name.split('（')[1].replace('）', '').strip()
    elif '(' in orig_name and ')' in orig_name:
        clean_name = orig_name.split('(')[0].strip()
        alt_name = orig_name.split('(')[1].replace(')', '').strip()

    invite_url = ""
    coupon = "暂无优惠码"
    coupon_note = ""
    price_from = "以结算页为准"
    traffic_from = "待核验"
    summary = ""
    packages = []
    internal_notes = []
    
    for line, links in b:
        if links and not invite_url:
            invite_url = links[0]
        if line.startswith('邀请链接：') and not invite_url:
            invite_url = line.replace('邀请链接：', '').strip()
        elif line.startswith('优惠码：'):
            coupon = line.replace('优惠码：', '').strip()
        elif line.startswith('套餐最低价格：'):
            price_from = sanitize_text(line.replace('套餐最低价格：', '').strip())
        elif line.startswith('主打卖点：'):
            summary = sanitize_text(line.replace('主打卖点：', '').strip())
        elif line.startswith('套餐：'):
            pass
        elif line.startswith('核对提示：') or line.startswith('对应关系提示：') or '补充：' in line:
            internal_notes.append(sanitize_text(line))
        elif any(c in line for c in ['元/月', '元/年', '元/季', '流量包', '套餐', 'Lite', 'Plus', '年付']):
            clean_pkg = sanitize_text(line)
            if clean_pkg:
                packages.append(clean_pkg)
        elif line.startswith('优惠说明：'):
            coupon_note = sanitize_text(line.replace('优惠说明：', '').strip())

    slug = slug_map.get(orig_name, slug_map.get(clean_name, clean_name.lower().replace(' ', '-')))
    
    providers_data.append({
        'origName': orig_name,
        'name': clean_name,
        'alternateName': alt_name,
        'slug': slug,
        'inviteURL': invite_url,
        'coupon': coupon,
        'couponNote': coupon_note,
        'priceFrom': price_from,
        'trafficFrom': traffic_from,
        'summary': summary,
        'packages': packages,
        'internalNotes': internal_notes,
        'lastChecked': '2026-09-19',
        'status': 'active'
    })

top4_names = ['全球云', '飞猫云', '暮光加速', '微风网络']
top4 = []
remaining = []

for p in providers_data:
    if p['name'] in top4_names:
        top4.append(p)
    else:
        remaining.append(p)

top4_sorted = [
    next(p for p in top4 if p['name'] == '全球云'),
    next(p for p in top4 if p['name'] == '飞猫云'),
    next(p for p in top4 if p['name'] == '暮光加速'),
    next(p for p in top4 if p['name'] == '微风网络')
]

final_providers = []

# Rank 1: 全球云
p1 = top4_sorted[0]
p1['rank'] = 1
p1['isPrimary'] = True
p1['ctaText'] = "使用优惠码查看当前套餐"
p1['coupon'] = "qq88"
p1['couponNote'] = "资料记录为 8 折，适用套餐、有效期及叠加规则以结算页为准"
p1['priceFrom'] = "20 元/月"
p1['trafficFrom'] = "120GB/月"
p1['suitableFor'] = "多地区节点、跨境业务、短视频与多出口 IP 使用场景"
p1['featuredPlacements'] = ["home", "recommendations", "comparison", "contextual"]
p1['trackingLabel'] = "quanqiu-cloud"
p1['sourceLevel'] = "用户资料与整理记录"
p1['verificationNote'] = "年付 99 元/59GB 的流量重置口径需要重新确认"
final_providers.append(p1)

# Rank 2: 飞猫云
p2 = top4_sorted[1]
p2['rank'] = 2
p2['isPrimary'] = True
p2['ctaText'] = "使用优惠码查看当前套餐"
p2['coupon'] = "flycat888"
p2['couponNote'] = "资料记录为新用户购买季付及以上 8 折，适用范围以结算页为准"
p2['priceFrom'] = "84 元/年"
p2['displayEquivalent'] = "折合 7 元/月"
p2['trafficFrom'] = "50GB/月"
p2['suitableFor'] = "轻量备用、香港线路需求、多设备家庭和新手客户端"
p2['featuredPlacements'] = ["home", "recommendations", "comparison", "contextual"]
p2['trackingLabel'] = "flycat-cloud"
p2['sourceLevel'] = "用户资料与公开记录"
p2['verificationNote'] = "完整套餐梯度、协议、节点峰值和流量重置包规则需在邀请页复核"
final_providers.append(p2)

# Rank 3: 暮光加速
p3 = top4_sorted[2]
p3['rank'] = 3
p3['isPrimary'] = True
p3['ctaText'] = "使用优惠码查看当前套餐"
p3['coupon'] = "mm88"
p3['couponNote'] = "资料记录为 8 折，适用套餐和有效期以结算页为准"
p3['priceFrom'] = "20 元/月"
p3['trafficFrom'] = "120GB/月"
p3['suitableFor'] = "晚高峰影音、较大流量和多媒体使用场景"
p3['featuredPlacements'] = ["home", "recommendations", "comparison", "contextual"]
p3['trackingLabel'] = "twilight"
p3['sourceLevel'] = "用户资料与整理记录"
p3['verificationNote'] = "影音性能、下载表现、平台兼容、设备数和退款规则需按当前页面核验"
final_providers.append(p3)

# Rank 4: 微风网络
p4 = top4_sorted[3]
p4['rank'] = 4
p4['isPrimary'] = True
p4['ctaText'] = "查看当前套餐与价格"
p4['coupon'] = "暂无优惠码"
p4['priceFrom'] = "以结算页为准"
p4['trafficFrom'] = "待核验"
p4['suitableFor'] = "轻度使用、低流量年付、自研客户端和第三方订阅导入"
p4['featuredPlacements'] = ["home", "recommendations", "comparison", "contextual"]
p4['trackingLabel'] = "breezenet"
p4['sourceLevel'] = "多个公开记录，数据存在冲突"
p4['verificationNote'] = "发布前确认最低档、付款周期、流量重置、优惠、设备数和客户端支持"
final_providers.append(p4)

# Ranks 5 to 27
for idx, p in enumerate(remaining, start=5):
    p['rank'] = idx
    p['isPrimary'] = False
    p['ctaText'] = "使用优惠码查看当前套餐" if p['coupon'] != "暂无优惠码" else "查看当前套餐与价格"
    p['featuredPlacements'] = ["providers", "reviews", "recommendations"]
    p['trackingLabel'] = p['slug']
    p['sourceLevel'] = "公开记录与资料底稿"
    p['verificationNote'] = "价格、协议、节点与优惠以服务结算页为准"
    if not p.get('suitableFor'):
        p['suitableFor'] = "日常网络连接、多平台设备使用与场景化订阅"
    final_providers.append(p)

with open('data/providers.json', 'w', encoding='utf-8') as f:
    json.dump(final_providers, f, ensure_ascii=False, indent=2)

print("Updated data/providers.json with sanitized texts and updated slugs!")
