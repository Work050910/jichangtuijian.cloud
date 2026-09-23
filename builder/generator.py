import os, json, re, shutil, html
from datetime import datetime

def clean_item_text(text):
    return re.sub(r'^\d+\.\s*', '', text)

class SiteGenerator:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.output_dir = os.path.join(base_dir, "public")
        self.data_dir = os.path.join(base_dir, "data")
        
        # Load datasets
        with open(os.path.join(self.data_dir, "site-seo-profile.json"), "r", encoding="utf-8") as f:
            self.profile = json.load(f)
            
        with open(os.path.join(self.data_dir, "providers.json"), "r", encoding="utf-8") as f:
            self.providers = json.load(f)
            
        with open(os.path.join(self.data_dir, "provider_reviews.json"), "r", encoding="utf-8") as f:
            self.provider_reviews = json.load(f)
            
        with open(os.path.join(self.data_dir, "navigation_articles.json"), "r", encoding="utf-8") as f:
            self.nav_articles = json.load(f)
            
        with open(os.path.join(self.data_dir, "faq100.json"), "r", encoding="utf-8") as f:
            self.faq100 = json.load(f)

        self.domain = self.profile["domain"] # https://jichangtuijian.cloud
        self.brand_name = self.profile["brandName"]
        self.tg_channel = self.profile.get("telegramChannel", "https://t.me/+U77JVhkbnhgzM2Q9")
        self.current_year = "2026"
        self.today_iso = "2026-09-23"

        # Indexable URLs for sitemap
        self.sitemap_urls = []

    def clean_output_dir(self):
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Copy static assets
        static_src = os.path.join(self.base_dir, "src", "static")
        static_dest = os.path.join(self.output_dir, "static")
        if os.path.exists(static_src):
            shutil.copytree(static_src, static_dest)

    def render_header(self, current_url="/"):
        nav_items_html = ""
        for item in self.profile["navigationItems"]:
            is_current = ' aria-current="page"' if item["url"] == current_url else ''
            nav_items_html += f'<li><a href="{item["url"]}" class="nav-link"{is_current}>{html.escape(item["label"])}</a></li>\n'
            
        return f"""
<header class="site-header">
  <div class="container header-top-row">
    <div class="header-brand">
      <a href="/" class="brand-logo" aria-label="{self.brand_name} 首页">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--primary)"><path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"/></svg>
        <span>{self.brand_name}</span>
      </a>
      <div class="brand-tagline">高性价比机场推荐 · Clash 机场测评 · 稳定专线节点指南</div>
    </div>
    
    <div class="header-top-actions">
      <!-- 搜索栏 -->
      <div class="header-search-container">
        <svg class="search-icon-svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <input type="search" id="header-search-input" class="header-search-input" placeholder="搜索文章/机场/教程..." aria-label="搜索全站文章">
        <div id="header-search-results" class="search-results-dropdown"></div>
      </div>

      <!-- Telegram 官方交流群 -->
      <a href="{self.tg_channel}" class="header-tg-btn" target="_blank" rel="sponsored nofollow noopener" aria-label="加入 Telegram 官方交流群">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/></svg>
        <span>TG 交流群</span>
      </a>

      <a href="/recommendations/" class="header-cta-btn">查看机场推荐</a>
      <button class="mobile-menu-toggle" aria-label="切换主导航菜单" aria-expanded="false" aria-controls="main-nav">☰</button>
    </div>
  </div>
  <div class="header-nav-row" id="main-nav">
    <div class="container">
      <nav aria-label="站点主导航">
        <ul class="nav-list">
          {nav_items_html}
        </ul>
      </nav>
    </div>
  </div>
</header>
"""

    def render_footer(self):
        p1 = self.profile["footerParagraph1"]
        p2 = self.profile["footerParagraph2"]
        
        return f"""
<footer class="site-footer">
  <div class="container footer-top">
    <div class="footer-brand-desc">
      <div style="font-size:18px;font-weight:700;margin-bottom:8px;color:var(--text-main);">{self.brand_name}</div>
      <p>{p1}</p>
      <p>{p2}</p>
      <div style="margin-top:12px;">
        <a href="{self.tg_channel}" target="_blank" rel="sponsored nofollow noopener" style="display:inline-flex;align-items:center;gap:6px;font-size:13px;font-weight:600;color:#0088cc;">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/></svg>
          <span>加入官方 Telegram 交流群</span>
        </a>
      </div>
    </div>
    <div>
      <div class="footer-col-title">热门导航</div>
      <ul class="footer-links">
        <li><a href="/recommendations/">机场推荐榜单</a></li>
        <li><a href="/recommendations/value/">性价比机场推荐</a></li>
        <li><a href="/recommendations/clash/">Clash 机场推荐</a></li>
        <li><a href="/recommendations/ai/">AI 机场推荐</a></li>
        <li><a href="/rankings/">机场排行榜说明</a></li>
        <li><a href="/nodes/">节点推荐与选择</a></li>
        <li><a href="/coupons/">机场优惠码核验</a></li>
        <li><a href="/reviews/">机场测评汇总</a></li>
        <li><a href="/faq/">常见问题中心</a></li>
      </ul>
    </div>
    <div>
      <div class="footer-col-title">信任与说明</div>
      <ul class="footer-links">
        <li><a href="/about/">关于本站</a></li>
        <li><a href="/contact/">联系我们</a></li>
        <li><a href="/editorial-policy/">编辑原则</a></li>
        <li><a href="/methodology/">评测方法</a></li>
        <li><a href="/corrections/">纠错政策</a></li>
        <li><a href="/affiliate-disclosure/">邀请链接披露</a></li>
        <li><a href="/privacy/">隐私政策</a></li>
        <li><a href="/terms/">服务条款</a></li>
        <li><a href="/disclaimer/">免责声明</a></li>
        <li><a href="/sitemap.xml">站点地图</a></li>
        <li><a href="/rss.xml">RSS 订阅</a></li>
      </ul>
    </div>
  </div>
  <div class="container footer-bottom">
    <div>© {self.current_year} {self.brand_name} (jichangtuijian.cloud) · 保留所有权利</div>
    <div>第三方商标与品牌归原所有者所有，本站不暗示任何官方隶属关系。</div>
  </div>
</footer>
"""

    def render_page(self, title, description, canonical_path, content_html, schema_json=None, page_type="website"):
        canonical_url = f"{self.domain}{canonical_path}"
        if not canonical_url.endswith("/") and not canonical_url.endswith(".html"):
            canonical_url += "/"
            
        if not canonical_path.endswith("404.html"):
            self.sitemap_urls.append(canonical_url)

        schema_script = ""
        if schema_json:
            schema_script = f'<script type="application/ld+json">\n{json.dumps(schema_json, ensure_ascii=False, indent=2)}\n</script>'
        else:
            default_schema = {
                "@context": "https://schema.org",
                "@type": "WebSite" if canonical_path == "/" else "WebPage",
                "name": title,
                "url": canonical_url,
                "description": description,
                "inLanguage": "zh-CN"
            }
            schema_script = f'<script type="application/ld+json">\n{json.dumps(default_schema, ensure_ascii=False, indent=2)}\n</script>'

        header_html = self.render_header(canonical_path)
        footer_html = self.render_footer()

        full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <link rel="canonical" href="{canonical_url}">
  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
  <meta property="og:type" content="{page_type}">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:site_name" content="{self.brand_name}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title)}">
  <meta name="twitter:description" content="{html.escape(description)}">
  <link rel="stylesheet" href="/static/css/main.css">
  <link rel="alternate" type="application/rss+xml" title="{self.brand_name} RSS Feed" href="{self.domain}/rss.xml">
  {schema_script}
</head>
<body>
  {header_html}
  <main id="main-content">
    {content_html}
  </main>
  {footer_html}
  <script src="/static/js/search-data.js" defer></script>
  <script src="/static/js/main.js" defer></script>
</body>
</html>
"""
        rel_path = canonical_path.strip("/")
        if not rel_path:
            out_file = os.path.join(self.output_dir, "index.html")
        elif rel_path.endswith(".html"):
            out_file = os.path.join(self.output_dir, rel_path)
        else:
            out_dir = os.path.join(self.output_dir, rel_path)
            os.makedirs(out_dir, exist_ok=True)
            out_file = os.path.join(out_dir, "index.html")

        with open(out_file, "w", encoding="utf-8") as f:
            f.write(full_html)

    def generate_home_page(self):
        hero_sub = self.profile["heroSubtitleText"]
        
        cards_html = ""
        for p in self.providers[:12]:
            rank = p['rank']
            coupon_html = f'<div class="provider-coupon-box"><span>优惠码：<span class="coupon-code">{p["coupon"]}</span></span><button class="btn-copy" data-coupon="{p["coupon"]}" data-provider="{p["slug"]}">复制</button></div>' if p['coupon'] != '暂无优惠码' else '<div class="provider-coupon-box"><span style="color:var(--text-light)">暂无优惠码</span></div>'
            
            cards_html += f"""
<div class="provider-card">
  <span class="provider-card-rank">TOP {rank}</span>
  <h3 class="provider-card-title"><a href="/providers/{p['slug']}/">{p['name']}</a></h3>
  <div class="provider-card-price">{p['priceFrom']}</div>
  <div class="provider-card-summary">{p['summary']}</div>
  {coupon_html}
  <div class="provider-card-actions">
    <a href="/providers/{p['slug']}/" class="btn-provider-review">查看 {p['name']} 测评</a>
    <a href="{p['inviteURL']}" class="btn-register-prominent" rel="sponsored nofollow noopener" target="_blank" data-provider="{p['slug']}" data-rank="{rank}" data-placement="home_featured">👉 前往 {p['name']} 官网注册体验</a>
  </div>
</div>
"""

        table_rows = ""
        for p in self.providers[:8]:
            table_rows += f"""
<tr>
  <td><strong>{p['rank']}</strong></td>
  <td><a href="/providers/{p['slug']}/"><strong>{p['name']}</strong></a></td>
  <td>{p['priceFrom']}</td>
  <td>{p['trafficFrom']}</td>
  <td><code>{p['coupon']}</code></td>
  <td>{p['suitableFor']}</td>
  <td><span style="font-size:12px;color:var(--text-light)">{p['lastChecked']}</span></td>
  <td><a href="{p['inviteURL']}" rel="sponsored nofollow noopener" target="_blank" class="btn-register-prominent" style="padding:6px 12px;font-size:12px;min-height:auto;" data-provider="{p['slug']}" data-rank="{p['rank']}" data-placement="home_table">官网注册</a></td>
</tr>
"""

        # Fully expanded FAQ items (No accordion collapsing!)
        faq_preview_html = ""
        for faq in self.faq100[:6]:
            faq_preview_html += f"""
<div class="faq-item-expanded">
  <span class="hero-badge" style="font-size:11px;padding:2px 8px;margin-bottom:8px;">{faq['cluster']}</span>
  <h3>{faq['questionTitle']}</h3>
  <p>{faq['summary']}</p>
  <div><a href="/faq/{faq['slug']}/" style="font-size:13px;font-weight:600;">阅读全文详细解答 →</a></div>
</div>
"""

        content_html = f"""
<section class="hero-section">
  <div class="container">
    <div class="hero-badge">{self.current_year} 高性价比机场推荐 · Clash 机场测评 · 稳定专线节点选型</div>
    <h1 class="hero-title">{self.brand_name}：从了解方案到配置订阅，清楚开始每一步</h1>
    <p class="hero-subtitle">{hero_sub}</p>
    <div class="hero-ctas">
      <a href="/recommendations/" class="btn-primary">查看机场推荐榜单</a>
      <a href="/providers/quanqiu-cloud/" class="btn-secondary">了解第一名全球云测评</a>
      <a href="{self.tg_channel}" target="_blank" rel="sponsored nofollow noopener" class="header-tg-btn" style="padding:12px 18px;font-size:14px;border-radius:var(--radius-md);">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/></svg>
        <span>加入 TG 官方交流群</span>
      </a>
    </div>
    <div class="hero-disclaimer">信息核验声明：本站所有价格、流量与优惠码均包含最后核验日期，下单前请以服务商当前结算页为准。本站部分外链包含带有 rel="sponsored nofollow noopener" 属性的邀请链接。</div>
  </div>
</section>

<!-- Universal 首页四个主要信息入口卡片 -->
<section class="section" style="padding-top:20px;">
  <div class="container">
    <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(240px, 1fr));gap:16px;">
      <div style="background:var(--bg-surface);border:1px solid var(--border-color);border-radius:var(--radius-md);padding:20px;">
        <h2 style="font-size:18px;font-weight:700;margin-bottom:8px;"><a href="/start-here/">新手开始指南</a></h2>
        <p style="font-size:14px;color:var(--text-muted);margin-bottom:12px;">面向初次接触机场的新手，梳理核心概念、订阅导入步骤、防踩坑建议与首轮排错清单。</p>
        <a href="/start-here/" style="font-size:13px;font-weight:600;">查看新手入门文章 →</a>
      </div>
      <div style="background:var(--bg-surface);border:1px solid var(--border-color);border-radius:var(--radius-md);padding:20px;">
        <h2 style="font-size:18px;font-weight:700;margin-bottom:8px;"><a href="/compare/">方案横向对比</a></h2>
        <p style="font-size:14px;color:var(--text-muted);margin-bottom:12px;">按每月 20 元预算、低价年付、大流量影音、单人多端与专线中转进行清晰透明的横向比对。</p>
        <a href="/compare/" style="font-size:13px;font-weight:600;">查阅套餐对比报告 →</a>
      </div>
      <div style="background:var(--bg-surface);border:1px solid var(--border-color);border-radius:var(--radius-md);padding:20px;">
        <h2 style="font-size:18px;font-weight:700;margin-bottom:8px;"><a href="/devices/">跨设备教程入口</a></h2>
        <p style="font-size:14px;color:var(--text-muted);margin-bottom:12px;">覆盖 Windows、macOS、iPhone、iPad、Android 及软路由等平台的一键导入与分流配置实操。</p>
        <a href="/devices/" style="font-size:13px;font-weight:600;">按设备查看客户端教程 →</a>
      </div>
      <div style="background:var(--bg-surface);border:1px solid var(--border-color);border-radius:var(--radius-md);padding:20px;">
        <h2 style="font-size:18px;font-weight:700;margin-bottom:8px;"><a href="/service/">服务资料与说明</a></h2>
        <p style="font-size:14px;color:var(--text-muted);margin-bottom:12px;">提供 27 家服务商的基础资料、协议支持（SS/Trojan）、节点分布与工单支持边界解析。</p>
        <a href="/service/" style="font-size:13px;font-weight:600;">浏览服务商资料库 →</a>
      </div>
    </div>
  </div>
</section>

<!-- 精选机场推荐榜 -->
<section class="section" id="recommendations-list">
  <div class="container">
    <div class="section-header">
      <div>
        <h2 class="section-title">机场推荐榜：高性价比稳定机场精选</h2>
        <div class="section-subtitle">严格固定前四名展示排序，清晰区分定位，提供站内测评解读与醒目官网注册入口</div>
      </div>
      <a href="/recommendations/" style="font-size:14px;font-weight:600;">查看全部 27 家服务测评 →</a>
    </div>
    <div class="providers-grid">
      {cards_html}
    </div>
  </div>
</section>

<!-- 快速对比表 -->
<section class="section" style="background-color:var(--bg-subtle);">
  <div class="container">
    <div class="section-header">
      <div>
        <h2 class="section-title">主流机场方案多维快速对比表</h2>
        <div class="section-subtitle">前四名固定排在表格前列，数据带最后核验日期，所有外链严格添加 rel="sponsored nofollow noopener"</div>
      </div>
      <a href="/compare/" style="font-size:14px;font-weight:600;">查看完整对比指南 →</a>
    </div>
    <div class="table-responsive">
      <table class="data-table">
        <thead>
          <tr>
            <th>排名</th>
            <th>服务商名称</th>
            <th>参考起步价</th>
            <th>参考流量</th>
            <th>优惠码</th>
            <th>适用场景与人群</th>
            <th>核验时间</th>
            <th>官网直达</th>
          </tr>
        </thead>
        <tbody>
          {table_rows}
        </tbody>
      </table>
    </div>
  </div>
</section>

<!-- 常见问题全部展开 (No Collapse!) -->
<section class="section">
  <div class="container">
    <div class="section-header">
      <div>
        <h2 class="section-title">高频常见问题解答中心 (FAQ 全部展开呈现)</h2>
        <div class="section-subtitle">直接呈现核心要点与排错逻辑，无需点击折叠展开，快速获取解答</div>
      </div>
      <a href="/faq/" style="font-size:14px;font-weight:600;">查阅全量 100 题 FAQ 知识库 →</a>
    </div>
    <div style="max-width:880px;">
      {faq_preview_html}
    </div>
  </div>
</section>
"""
        title = self.profile["titlePatterns"]["home"]
        desc = self.profile["descriptionPatterns"]["home"]
        self.render_page(title, desc, "/", content_html, page_type="website")
        print("Generated updated Home page.")

    def generate_all_provider_pages(self):
        for p in self.provider_reviews:
            name = p['name']
            slug = p['slug']
            rank = p['rank']
            coupon = p['coupon']
            price = p['priceFrom']
            invite = p['inviteURL']
            body_html = ""
            for line in p['body'].split("\n\n"):
                if line.startswith("### "):
                    body_html += f"<h2>{html.escape(line.replace('### ', ''))}</h2>\n"
                elif line.startswith("## "):
                    body_html += f"<h2>{html.escape(line.replace('## ', ''))}</h2>\n"
                elif line.startswith("- "):
                    items = line.split("\n")
                    body_html += "<ul>" + "".join([f"<li>{html.escape(item.replace('- ', ''))}</li>" for item in items if item.strip()]) + "</ul>\n"
                elif line.startswith("1. "):
                    items = line.split("\n")
                    cleaned_items = [clean_item_text(item) for item in items if item.strip()]
                    body_html += "<ol>" + "".join([f"<li>{html.escape(it)}</li>" for it in cleaned_items]) + "</ol>\n"
                else:
                    body_html += f"<p>{html.escape(line)}</p>\n"

            coupon_box = f'<div class="provider-coupon-box" style="margin:20px 0;"><span>专属优惠码：<strong class="coupon-code">{coupon}</strong></span><button class="btn-copy" data-coupon="{coupon}" data-provider="{slug}">点击复制优惠码</button></div>' if coupon != '暂无优惠码' else ''

            content_html = f"""
<div class="container">
  <div class="breadcrumbs">
    <a href="/">首页</a> <span>/</span> <a href="/reviews/">机场测评</a> <span>/</span> <span>{name}</span>
  </div>
  <div class="article-layout" data-page-type="provider-detail" data-provider-name="{name}">
    <article class="article-main">
      <header class="article-header">
        <h1 class="article-title">{name} 机场测评与全方位选型指南</h1>
        <div class="article-meta">
          <span>发布日期：2026-09-19</span>
          <span>最后核验：{p['lastChecked']}</span>
          <span>净中文约 {p['bodyCharCount']} 字</span>
          <span>阅读时间：约 4 分钟</span>
        </div>
      </header>
      
      <div style="background:var(--bg-subtle);border:1px solid var(--border-color);border-radius:var(--radius-md);padding:20px;margin-bottom:24px;">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;">
          <div>
            <div style="font-size:14px;color:var(--text-light)">本站推荐排名：TOP {rank}</div>
            <div style="font-size:22px;font-weight:800;color:var(--primary);">{price}</div>
          </div>
          <a href="{invite}" rel="sponsored nofollow noopener" target="_blank" class="btn-register-prominent" data-provider="{slug}" data-rank="{rank}" data-placement="review_top_cta">👉 前往 {name} 官网注册查看当前套餐</a>
        </div>
      </div>
      
      {coupon_box}

      <div class="article-body">
        {body_html}
      </div>

      <div style="margin-top:32px;padding:24px;background:var(--bg-subtle);border-radius:var(--radius-md);border:1px solid var(--border-color);text-align:center;">
        <h3 style="font-size:18px;font-weight:700;margin-bottom:8px;">准备好体验 {name} 了吗？</h3>
        <p style="font-size:14px;color:var(--text-muted);margin-bottom:16px;">建议先选购单月套餐在晚高峰实际测试，结账前核对最终价格与流量规则。</p>
        <a href="{invite}" rel="sponsored nofollow noopener" target="_blank" class="btn-register-prominent" data-provider="{slug}" data-rank="{rank}" data-placement="review_bottom_cta">👉 点击直达 {name} 官网注册体验</a>
      </div>

      <div style="margin-top:40px;">
        <h3 style="font-size:18px;font-weight:700;margin-bottom:16px;">相关评测与推荐</h3>
        <ul style="list-style:none;display:grid;grid-template-columns:repeat(auto-fit, minmax(240px, 1fr));gap:12px;">
          <li><a href="/recommendations/" style="font-weight:600;">• 2026 机场推荐精选总榜</a></li>
          <li><a href="/recommendations/value/" style="font-weight:600;">• 性价比机场推荐与对比</a></li>
          <li><a href="/recommendations/clash/" style="font-weight:600;">• Clash 客户端机场配置指南</a></li>
          <li><a href="/before-you-buy/" style="font-weight:600;">• 购买机场前 8 项必看须知</a></li>
        </ul>
      </div>
    </article>
    
    <aside class="article-sidebar">
      <div class="sidebar-widget">
        <div class="widget-title">核心信息速览</div>
        <ul style="list-style:none;font-size:13px;display:flex;flex-direction:column;gap:8px;">
          <li><strong>服务商：</strong>{name}</li>
          <li><strong>参考起步：</strong>{price}</li>
          <li><strong>优惠码：</strong>{coupon}</li>
          <li><strong>核验日期：</strong>{p['lastChecked']}</li>
          <li><strong>退款说明：</strong>虚拟商品概不退款</li>
        </ul>
      </div>
      <div class="sidebar-widget">
        <div class="widget-title">四项主推对比</div>
        <ul style="list-style:none;font-size:13px;display:flex;flex-direction:column;gap:8px;">
          <li><a href="/providers/quanqiu-cloud/">1. 全球云 (多地区专线)</a></li>
          <li><a href="/providers/flycat-cloud/">2. 飞猫云 (轻量小年付)</a></li>
          <li><a href="/providers/twilight/">3. 暮光加速 (晚高峰影音)</a></li>
          <li><a href="/providers/breezenet/">4. 微风网络 (轻量自研端)</a></li>
        </ul>
      </div>
      <div class="sidebar-widget">
        <div class="widget-title">官方交流群</div>
        <a href="{self.tg_channel}" target="_blank" rel="sponsored nofollow noopener" class="header-tg-btn" style="width:100%;justify-content:center;">
          <span>加入 Telegram 交流群</span>
        </a>
      </div>
    </aside>
  </div>
</div>
"""
            schema = {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": f"{name} 机场测评与全方位选型指南",
                "description": p['metaDescription'],
                "inLanguage": "zh-CN",
                "mainEntityOfPage": f"{self.domain}/providers/{slug}/",
                "datePublished": "2026-09-19",
                "dateModified": "2026-09-23",
                "author": {"@type": "Organization", "name": self.brand_name},
                "publisher": {"@type": "Organization", "name": self.brand_name}
            }
            self.render_page(p['title'], p['metaDescription'], f"/providers/{slug}/", content_html, schema_json=schema, page_type="article")

        print("Generated 27 provider review pages.")

    def generate_all_navigation_articles(self):
        for art in self.nav_articles:
            title = art['h1']
            slug = art['slug']
            url = art['url']
            sec_name = art['sectionName']
            sec_id = art['section']
            
            body_html = ""
            for line in art['body'].split("\n\n"):
                line_str = line.strip()
                if not line_str:
                    continue
                if line_str.startswith("#### "):
                    body_html += f"<h3>{html.escape(line_str.replace('#### ', '', 1))}</h3>\n"
                elif line_str.startswith("### "):
                    body_html += f"<h2>{html.escape(line_str.replace('### ', '', 1))}</h2>\n"
                elif line_str.startswith("## "):
                    body_html += f"<h2>{html.escape(line_str.replace('## ', '', 1))}</h2>\n"
                elif line_str.startswith("> "):
                    clean_quote = line_str.replace('> ', '', 1)
                    clean_quote = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html.escape(clean_quote))
                    body_html += f"<blockquote><p>{clean_quote}</p></blockquote>\n"
                elif line_str.startswith("1. "):
                    items = line_str.split("\n")
                    cleaned_items = [clean_item_text(item) for item in items if item.strip()]
                    rendered_items = []
                    for it in cleaned_items:
                        esc = html.escape(it)
                        esc = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', esc)
                        rendered_items.append(f"<li>{esc}</li>")
                    body_html += "<ol>" + "".join(rendered_items) + "</ol>\n"
                elif line_str.startswith("- "):
                    items = line_str.split("\n")
                    rendered_items = []
                    for item in items:
                        item_s = item.strip()
                        if not item_s:
                            continue
                        if item_s.startswith("- "):
                            item_s = item_s[2:].strip()
                        if '<a href=' in item_s or '<div' in item_s:
                            rendered_items.append(f"<li style=\"list-style:none;margin-top:8px;\">{item_s}</li>")
                        else:
                            clean_text = html.escape(item_s)
                            clean_text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', clean_text)
                            rendered_items.append(f"<li>{clean_text}</li>")
                    body_html += "<ul style=\"margin-bottom:16px;\">" + "".join(rendered_items) + "</ul>\n"
                elif '<a href=' in line_str and 'btn-register-prominent' in line_str:
                    body_html += line_str + "\n"
                else:
                    escaped_p = html.escape(line_str)
                    escaped_p = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', escaped_p)
                    body_html += f"<p>{escaped_p}</p>\n"

            content_html = f"""
<div class="container">
  <div class="breadcrumbs">
    <a href="/">首页</a> <span>/</span> <a href="/{sec_id}/">{sec_name}</a> <span>/</span> <span>{title}</span>
  </div>
  <div class="article-layout">
    <article class="article-main">
      <header class="article-header">
        <h1 class="article-title">{title}</h1>
        <div class="article-meta">
          <span>所属栏目：{sec_name}</span>
          <span>发布日期：2026-09-23</span>
          <span>净中文约 {art['bodyCharCount']} 字</span>
          <span>阅读时间：约 6 分钟</span>
        </div>
      </header>

      <div class="article-body">
        {body_html}
      </div>

      <div style="margin-top:40px;padding:24px;background:var(--bg-subtle);border-radius:var(--radius-md);border:1px solid var(--border-color);">
        <h3 style="font-size:18px;font-weight:700;margin-bottom:12px;">相关阅读与下一步建议</h3>
        <ul style="list-style:none;display:flex;flex-direction:column;gap:8px;">
          <li><a href="/recommendations/">• 查看当前年份机场推荐精选榜单与服务横评</a></li>
          <li><a href="/compare/">• 查阅主流机场套餐价格与流量对比报告</a></li>
          <li><a href="/before-you-buy/">• 购买机场前 8 项避坑与自我核对清单</a></li>
          <li><a href="/faq/">• 常见问题中心：100 个高频疑问解答</a></li>
        </ul>
      </div>
    </article>

    <aside class="article-sidebar">
      <div class="sidebar-widget">
        <div class="widget-title">栏目热门推荐</div>
        <ul style="list-style:none;font-size:13px;display:flex;flex-direction:column;gap:8px;">
          <li><a href="/recommendations/">机场推荐榜</a></li>
          <li><a href="/recommendations/value/">性价比机场推荐</a></li>
          <li><a href="/recommendations/clash/">Clash 机场推荐</a></li>
          <li><a href="/recommendations/ai/">AI 机场推荐</a></li>
        </ul>
      </div>
      <div class="sidebar-widget">
        <div class="widget-title">核心服务商直达</div>
        <ul style="list-style:none;font-size:13px;display:flex;flex-direction:column;gap:8px;">
          <li><a href="/providers/quanqiu-cloud/">全球云测评 (TOP 1)</a></li>
          <li><a href="/providers/flycat-cloud/">飞猫云测评 (TOP 2)</a></li>
          <li><a href="/providers/twilight/">暮光加速测评 (TOP 3)</a></li>
          <li><a href="/providers/breezenet/">微风网络测评 (TOP 4)</a></li>
        </ul>
      </div>
      <div class="sidebar-widget">
        <div class="widget-title">官方 TG 交流</div>
        <a href="{self.tg_channel}" target="_blank" rel="sponsored nofollow noopener" class="header-tg-btn" style="width:100%;justify-content:center;">
          <span>加入 Telegram 交流群</span>
        </a>
      </div>
    </aside>
  </div>
</div>
"""
            schema = {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": title,
                "description": art['metaDescription'],
                "inLanguage": "zh-CN",
                "mainEntityOfPage": f"{self.domain}{url}",
                "datePublished": "2026-09-23",
                "dateModified": "2026-09-23",
                "author": {"@type": "Organization", "name": self.brand_name},
                "publisher": {"@type": "Organization", "name": self.brand_name}
            }
            self.render_page(art['title'], art['metaDescription'], url, content_html, schema_json=schema, page_type="article")

        print("Generated 60 navigation articles.")

    def generate_faq_pages(self):
        for faq in self.faq100:
            q_title = faq['questionTitle']
            slug = faq['slug']
            url = f"/faq/{slug}/"
            
            body_html = ""
            for line in faq['body'].split("\n\n"):
                if line.startswith("### "):
                    body_html += f"<h2>{html.escape(line.replace('### ', ''))}</h2>\n"
                elif line.startswith("## "):
                    body_html += f"<h2>{html.escape(line.replace('## ', ''))}</h2>\n"
                else:
                    body_html += f"<p>{html.escape(line)}</p>\n"

            content_html = f"""
<div class="container">
  <div class="breadcrumbs">
    <a href="/">首页</a> <span>/</span> <a href="/faq/">常见问题</a> <span>/</span> <span>{q_title}</span>
  </div>
  <div class="article-layout">
    <article class="article-main">
      <header class="article-header">
        <span class="hero-badge">{faq['cluster']}</span>
        <h1 class="article-title">{q_title}</h1>
        <div class="article-meta">
          <span>所属分类：{faq['cluster']}</span>
          <span>更新时间：{faq['lastChecked']}</span>
          <span>字数：{faq['bodyCharCount']} 字</span>
        </div>
      </header>

      <div style="background:var(--primary-light);border-left:4px solid var(--primary);padding:16px 20px;border-radius:var(--radius-sm);margin-bottom:24px;">
        <strong style="color:var(--primary);display:block;margin-bottom:6px;font-size:16px;">速读核心解答：</strong>
        <p style="margin:0;font-size:15px;color:var(--text-main);line-height:1.7;">{faq['summary']}</p>
      </div>

      <div class="article-body">
        {body_html}
      </div>

      <div style="margin-top:32px;padding:24px;background:var(--bg-subtle);border-radius:var(--radius-md);border:1px solid var(--border-color);">
        <h3 style="font-size:16px;font-weight:700;margin-bottom:12px;">相关推荐与参考页面</h3>
        <ul style="list-style:none;display:flex;flex-direction:column;gap:8px;font-size:14px;">
          <li><a href="/recommendations/">• 机场推荐精选总榜：按需求与预算科学选择</a></li>
          <li><a href="/compare/">• 机场套餐横向对比与流量核算指南</a></li>
          <li><a href="/start-here/">• 机场新手入门与客户端导入教程</a></li>
          <li><a href="/before-you-buy/">• 购买前须知与防坑核验清单</a></li>
        </ul>
      </div>
    </article>

    <aside class="article-sidebar">
      <div class="sidebar-widget">
        <div class="widget-title">精选服务推荐</div>
        <ul style="list-style:none;font-size:13px;display:flex;flex-direction:column;gap:8px;">
          <li><a href="/providers/quanqiu-cloud/">1. 全球云 (Rank 1 综合首选)</a></li>
          <li><a href="/providers/flycat-cloud/">2. 飞猫云 (Rank 2 小年付备用)</a></li>
          <li><a href="/providers/twilight/">3. 暮光加速 (Rank 3 影音大流量)</a></li>
          <li><a href="/providers/breezenet/">4. 微风网络 (Rank 4 轻量专线)</a></li>
        </ul>
      </div>
      <div class="sidebar-widget">
        <div class="widget-title">官方 TG 交流</div>
        <a href="{self.tg_channel}" target="_blank" rel="sponsored nofollow noopener" class="header-tg-btn" style="width:100%;justify-content:center;">
          <span>加入 Telegram 交流群</span>
        </a>
      </div>
    </aside>
  </div>
</div>
"""
            schema = {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": q_title,
                "description": faq['summary'],
                "inLanguage": "zh-CN",
                "mainEntityOfPage": f"{self.domain}{url}",
                "datePublished": "2026-09-23",
                "dateModified": "2026-09-23",
                "author": {"@type": "Organization", "name": self.brand_name},
                "publisher": {"@type": "Organization", "name": self.brand_name}
            }
            self.render_page(f"{q_title}｜{self.brand_name} 常见问题解答", faq['summary'], url, content_html, schema_json=schema, page_type="article")

        # 2. Paginated Hub Pages
        page_size = 20
        total_pages = 5
        for p_idx in range(1, total_pages + 1):
            start = (p_idx - 1) * page_size
            end = start + page_size
            page_faqs = self.faq100[start:end]
            
            hub_url = "/faq/" if p_idx == 1 else f"/faq/page/{p_idx}/"
            
            cards_html = ""
            for faq in page_faqs:
                cards_html += f"""
<div class="faq-item-expanded" style="margin-bottom:16px;">
  <span class="hero-badge" style="font-size:11px;padding:2px 8px;">{faq['cluster']}</span>
  <h2 style="font-size:18px;font-weight:700;margin:8px 0;"><a href="/faq/{faq['slug']}/">{faq['questionTitle']}</a></h2>
  <p style="font-size:14px;color:var(--text-muted);line-height:1.6;margin-bottom:10px;">{faq['summary']}</p>
  <div style="font-size:12px;color:var(--text-light);display:flex;justify-content:space-between;align-items:center;">
    <span>最后更新：{faq['lastChecked']} · 约 {faq['bodyCharCount']} 字</span>
    <a href="/faq/{faq['slug']}/" style="font-weight:600;">阅读全文详细解答 →</a>
  </div>
</div>
"""
            pagination_html = '<div style="display:flex;justify-content:center;gap:8px;margin-top:24px;">'
            for i in range(1, total_pages + 1):
                p_link = "/faq/" if i == 1 else f"/faq/page/{i}/"
                is_cur = ' style="font-weight:700;background:var(--primary);color:#fff;"' if i == p_idx else ' style="background:var(--bg-surface);border:1px solid var(--border-color);"'
                pagination_html += f'<a href="{p_link}" class="nav-link"{is_cur}>{i}</a>'
            pagination_html += '</div>'

            content_html = f"""
<div class="container" style="padding:32px 20px;">
  <div class="breadcrumbs">
    <a href="/">首页</a> <span>/</span> <span>常见问题中心 (第 {p_idx} 页)</span>
  </div>
  <header style="margin-bottom:24px;">
    <h1 style="font-size:30px;font-weight:800;margin-bottom:8px;">机场推荐、Clash 与节点常见问题解答中心 (全部展开)</h1>
    <p style="font-size:15px;color:var(--text-muted);">系统整理 100 个真实高频疑问，涵盖选型原则、Clash 配置、SS/Trojan 协议、节点与倍率、多设备使用及购买前避坑，内容直接全部展开可见。</p>
  </header>

  <div style="max-width:880px;">
    {cards_html}
    {pagination_html}
  </div>
</div>
"""
            schema = {
                "@context": "https://schema.org",
                "@type": "CollectionPage",
                "name": f"机场推荐云常见问题中心 (第 {p_idx} 页)",
                "url": f"{self.domain}{hub_url}",
                "description": "系统整理 100 个真实高频疑问，涵盖选型原则、Clash 配置、SS/Trojan 协议、节点与倍率及多设备使用。",
                "inLanguage": "zh-CN"
            }
            self.render_page(f"常见问题中心 (第 {p_idx} 页)｜机场推荐云", "系统整理 100 个真实高频疑问，涵盖选型原则、Clash 配置、SS/Trojan 协议、节点与倍率及多设备使用。", hub_url, content_html, schema_json=schema, page_type="website")

        print("Generated 100 FAQ individual pages and 5 paginated hub pages.")

    def generate_landing_pages(self):
        # 1. 新手开始 (/start-here/)
        self._generate_section_hub(
            "start-here",
            "新手开始",
            "机场新手入门教程与实操指南",
            "专为初次接触网络连接服务的新手打造，涵盖核心概念科普、客户端订阅导入、按月计费分析、防踩坑清单与首轮连接排查技巧。",
            self.nav_articles
        )

        # 2. 服务资料 (/service/)
        self._generate_section_hub(
            "service",
            "服务资料",
            "机场服务资料与网络协议说明",
            "汇集 27 家服务商底层信息、SS 与 Trojan 协议兼容性、香港与日本等节点分布特征，以及售后工单支持边界等透明资料。",
            self.nav_articles
        )

        # 3. 方案对比 (/compare/)
        self._generate_section_hub(
            "compare",
            "方案对比",
            "主流机场套餐横向对比与流量选型",
            "从 20 元月付预算、百元小流量年付、重度影音大户到多设备合租等不同维度展开真实透明对比，助您精打细算选对套餐。",
            self.nav_articles
        )

        # 4. 设备入口 (/devices/)
        self._generate_section_hub(
            "devices",
            "设备入口",
            "全平台客户端配置与使用指南",
            "系统覆盖 Windows、macOS、iPhone、iPad、Android 手机与软路由的客户端选型、订阅导入、分流规则设置及后台防杀优化。",
            self.nav_articles
        )

        # 5. 使用须知 (/before-you-buy/)
        self._generate_section_hub(
            "before-you-buy",
            "使用须知",
            "购买机场前必看的 8 项核验须知",
            "深入解析虚拟商品退款规则、账号密码安全、支付方式避坑、长期买断风险与识别虚假营销话术，保障您的合法权益与资金安全。",
            self.nav_articles
        )

        # 6. 综合推荐支柱页 (/recommendations/)
        self._generate_recommendations_pillar()

        # 7. 性价比机场落地页 (/recommendations/value/)
        self._generate_sub_commercial_landing(
            "/recommendations/value/",
            "性价比机场推荐：低价套餐、流量与预算选择指南",
            "聚焦低预算、高性价比入门与备用网络方案，梳理百元年付小包与月付 20 元以内靠谱选择，并提供真实折扣优惠码。",
            "性价比机场推荐"
        )

        # 8. Clash 机场推荐落地页 (/recommendations/clash/)
        self._generate_sub_commercial_landing(
            "/recommendations/clash/",
            "Clash 机场推荐：好用稳定机场、兼容性与节点选择",
            "针对 Clash Verge、Clash for Windows 等客户端，提供规则分流完善、订阅拉取稳定、延迟优良的精选服务商对比与配置教学。",
            "Clash 机场推荐"
        )

        # 9. AI 机场推荐落地页 (/recommendations/ai/)
        self._generate_sub_commercial_landing(
            "/recommendations/ai/",
            "AI 机场推荐：ChatGPT、Claude、Gemini 等工具的节点与套餐选择",
            "面向海外大语言模型与代码协同工具用户，剖析原生 IP 纯净度、地区出口节点、长连接低丢包率对 AI 办公的核心价值与局限性说明。",
            "AI 机场推荐"
        )

        # 10. 排行榜与排序说明 (/rankings/)
        self._generate_rankings_page()

        # 11. 节点推荐与指南 (/nodes/)
        self._generate_nodes_page()

        # 12. 优惠码汇总 (/coupons/)
        self._generate_coupons_page()

        # 13. 评测汇总 (/reviews/)
        self._generate_reviews_page()

        # 14. 服务资料库 (/providers/)
        self._generate_providers_directory_page()

        # 15. 服务状态 (/status/)
        self._generate_status_page()

        # 16. 信任与法律页面
        self._generate_trust_pages()

    def _generate_section_hub(self, sec_id, sec_name, title, desc, all_articles):
        sec_articles = [a for a in all_articles if a['section'] == sec_id]
        
        cards_html = ""
        for a in sec_articles:
            cards_html += f"""
<div class="sidebar-widget" style="margin-bottom:16px;">
  <h2 style="font-size:18px;font-weight:700;margin-bottom:8px;"><a href="{a['url']}">{a['title']}</a></h2>
  <p style="font-size:14px;color:var(--text-muted);margin-bottom:8px;">{a['metaDescription']}</p>
  <div style="font-size:12px;color:var(--text-light);display:flex;justify-content:space-between;align-items:center;">
    <span>核心关键词：{a['primaryKeyword']} · 约 {a['bodyCharCount']} 字</span>
    <a href="{a['url']}" style="font-weight:600;">阅读全文 →</a>
  </div>
</div>
"""
        content_html = f"""
<div class="container" style="padding:32px 20px;">
  <div class="breadcrumbs">
    <a href="/">首页</a> <span>/</span> <span>{sec_name}</span>
  </div>
  <header style="margin-bottom:28px;">
    <h1 style="font-size:30px;font-weight:800;margin-bottom:12px;">{title}</h1>
    <p style="font-size:15px;color:var(--text-muted);max-width:850px;line-height:1.7;">{desc}</p>
  </header>
  <div style="max-width:880px;">
    {cards_html}
  </div>
</div>
"""
        schema = {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": title,
            "url": f"{self.domain}/{sec_id}/",
            "description": desc,
            "inLanguage": "zh-CN"
        }
        self.render_page(f"{title}｜机场推荐云", desc, f"/{sec_id}/", content_html, schema_json=schema, page_type="website")
        print(f"Generated {sec_name} hub page.")

    def _generate_recommendations_pillar(self):
        title = "当前年份机场推荐精选总榜：按需求与预算科学选择服务"
        desc = "系统整理 27 家服务商真实资料，严格固定前四名编辑推荐排序，提供 12 家服务商深度对比表、按预算与流量选型方法及购买前核验清单。"
        
        table_rows = ""
        for p in self.providers[:12]:
            table_rows += f"""
<tr>
  <td><strong>{p['rank']}</strong></td>
  <td><a href="/providers/{p['slug']}/"><strong>{p['name']}</strong></a></td>
  <td>{p['priceFrom']}</td>
  <td>{p['trafficFrom']}</td>
  <td><code>{p['coupon']}</code></td>
  <td>{p['suitableFor']}</td>
  <td><span style="font-size:12px;color:var(--text-light)">{p['lastChecked']}</span></td>
  <td><a href="{p['inviteURL']}" rel="sponsored nofollow noopener" target="_blank" class="btn-register-prominent" style="padding:4px 10px;font-size:12px;min-height:auto;" data-provider="{p['slug']}" data-rank="{p['rank']}" data-placement="pillar_table">官网注册</a></td>
</tr>
"""
        content_html = f"""
<div class="container" style="padding:32px 20px;">
  <div class="breadcrumbs">
    <a href="/">首页</a> <span>/</span> <span>机场推荐精选榜</span>
  </div>
  <header style="margin-bottom:28px;">
    <span class="hero-badge">2026 深度评测与推荐支柱</span>
    <h1 style="font-size:32px;font-weight:800;margin:12px 0;">{title}</h1>
    <p style="font-size:16px;color:var(--text-muted);line-height:1.8;max-width:900px;">面对市面上琳琅满目的网络连接服务，用户最关心的莫过于稳定性、合理定价与售后保障。本站基于多月的人工核验，为您呈现四大主推机场的鲜明定位差异与官网注册入口。</p>
  </header>

  <section style="margin-bottom:36px;">
    <h2 style="font-size:22px;font-weight:700;margin-bottom:16px;">一、四项重点主推服务快速评述与官网注册</h2>
    <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(260px, 1fr));gap:16px;">
      <div class="sidebar-widget">
        <span class="provider-card-rank">TOP 1</span>
        <h3 style="font-size:18px;font-weight:700;margin-bottom:8px;"><a href="/providers/quanqiu-cloud/">全球云（综合旗舰）</a></h3>
        <p style="font-size:14px;color:var(--text-muted);margin-bottom:12px;">20元/月起，多国家和地区出口覆盖广，智能分流体验佳，适合跨境业务与多端需求。</p>
        <div style="font-size:13px;margin-bottom:12px;">优惠码：<code>qq88</code> (8折)</div>
        <a href="https://hueue09.gcvipaff.com/#/?code=z8U9aaa4" rel="sponsored nofollow noopener" target="_blank" class="btn-register-prominent" style="width:100%;">👉 前往全球云官网注册</a>
      </div>
      <div class="sidebar-widget">
        <span class="provider-card-rank">TOP 2</span>
        <h3 style="font-size:18px;font-weight:700;margin-bottom:8px;"><a href="/providers/flycat-cloud/">飞猫云（性价比年付）</a></h3>
        <p style="font-size:14px;color:var(--text-muted);margin-bottom:12px;">84元/年起（折合7元/月），小流量年付门槛低，自研客户端友好，适合轻量备用。</p>
        <div style="font-size:13px;margin-bottom:12px;">优惠码：<code>flycat888</code> (季付8折)</div>
        <a href="https://quanqiu.flycatvipaff.cc/#/?code=7ZOeVmNS" rel="sponsored nofollow noopener" target="_blank" class="btn-register-prominent" style="width:100%;">👉 前往飞猫云官网注册</a>
      </div>
      <div class="sidebar-widget">
        <span class="provider-card-rank">TOP 3</span>
        <h3 style="font-size:18px;font-weight:700;margin-bottom:8px;"><a href="/providers/twilight/">暮光加速（影音大流量）</a></h3>
        <p style="font-size:14px;color:var(--text-muted);margin-bottom:12px;">20元/月起，针对晚高峰流媒体与大流量传输优化，多媒体和 AI 协同表现稳定。</p>
        <div style="font-size:13px;margin-bottom:12px;">优惠码：<code>mm88</code> (8折)</div>
        <a href="https://quanqi12.twilightaff.com/#/?code=beAVqNPf" rel="sponsored nofollow noopener" target="_blank" class="btn-register-prominent" style="width:100%;">👉 前往暮光加速官网注册</a>
      </div>
      <div class="sidebar-widget">
        <span class="provider-card-rank">TOP 4</span>
        <h3 style="font-size:18px;font-weight:700;margin-bottom:8px;"><a href="/providers/breezenet/">微风网络（轻量专线）</a></h3>
        <p style="font-size:14px;color:var(--text-muted);margin-bottom:12px;">轻量专线方案，支持通用订阅与自研客户端，公开价格带核验，适合低频轻度使用。</p>
        <div style="font-size:13px;margin-bottom:12px;">状态：待结算页确认</div>
        <a href="https://edp01.breezenetaff.com/#/?code=vxDUI8kY" rel="sponsored nofollow noopener" target="_blank" class="btn-register-prominent" style="width:100%;">👉 前往微风网络官网注册</a>
      </div>
    </div>
  </section>

  <section style="margin-bottom:36px;">
    <h2 style="font-size:22px;font-weight:700;margin-bottom:16px;">二、12 家精选服务商横向数据对比表</h2>
    <div class="table-responsive">
      <table class="data-table">
        <thead>
          <tr>
            <th>排名</th>
            <th>服务商名称</th>
            <th>参考起步价</th>
            <th>参考流量</th>
            <th>优惠码</th>
            <th>适用场景与人群</th>
            <th>核验时间</th>
            <th>官网入口</th>
          </tr>
        </thead>
        <tbody>
          {table_rows}
        </tbody>
      </table>
    </div>
  </section>
</div>
"""
        schema = {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": title,
            "url": f"{self.domain}/recommendations/",
            "description": desc,
            "inLanguage": "zh-CN"
        }
        self.render_page(f"{title}｜机场推荐云", desc, "/recommendations/", content_html, schema_json=schema, page_type="website")
        print("Generated recommendations pillar page.")

    def _generate_sub_commercial_landing(self, url, title, desc, keyword):
        content_html = f"""
<div class="container" style="padding:32px 20px;">
  <div class="breadcrumbs">
    <a href="/">首页</a> <span>/</span> <a href="/recommendations/">机场推荐</a> <span>/</span> <span>{title}</span>
  </div>
  <header style="margin-bottom:28px;">
    <span class="hero-badge">{keyword} 专题选型</span>
    <h1 style="font-size:30px;font-weight:800;margin:12px 0;">{title}</h1>
    <p style="font-size:15px;color:var(--text-muted);max-width:850px;line-height:1.7;">{desc}</p>
  </header>

  <div style="background:var(--bg-surface);border:1px solid var(--border-color);border-radius:var(--radius-md);padding:24px;margin-bottom:32px;">
    <h2 style="font-size:20px;font-weight:700;margin-bottom:16px;">四项重点推荐服务在“{keyword}”场景中的适用分析与官网注册</h2>
    <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(240px, 1fr));gap:16px;">
      <div style="padding:16px;border:1px solid var(--border-subtle);border-radius:var(--radius-sm);background:var(--bg-page);">
        <h3 style="font-size:16px;font-weight:700;"><a href="/providers/quanqiu-cloud/">1. 全球云 (Rank 1 旗舰)</a></h3>
        <p style="font-size:13px;color:var(--text-muted);margin:8px 0;">20元/月起，多地区专线中转，晚高峰稳定性强，适合对连接质量有较高要求的{keyword}场景。</p>
        <a href="https://hueue09.gcvipaff.com/#/?code=z8U9aaa4" rel="sponsored nofollow noopener" target="_blank" class="btn-register-prominent" style="padding:8px 12px;font-size:13px;width:100%;">👉 前往全球云官网注册</a>
      </div>
      <div style="padding:16px;border:1px solid var(--border-subtle);border-radius:var(--radius-sm);background:var(--bg-page);">
        <h3 style="font-size:16px;font-weight:700;"><a href="/providers/flycat-cloud/">2. 飞猫云 (Rank 2 性价比)</a></h3>
        <p style="font-size:13px;color:var(--text-muted);margin:8px 0;">84元/年起，折合单月成本极低，适合低预算入门或作为{keyword}的稳定备用链路。</p>
        <a href="https://quanqiu.flycatvipaff.cc/#/?code=7ZOeVmNS" rel="sponsored nofollow noopener" target="_blank" class="btn-register-prominent" style="padding:8px 12px;font-size:13px;width:100%;">👉 前往飞猫云官网注册</a>
      </div>
      <div style="padding:16px;border:1px solid var(--border-subtle);border-radius:var(--radius-sm);background:var(--bg-page);">
        <h3 style="font-size:16px;font-weight:700;"><a href="/providers/twilight/">3. 暮光加速 (Rank 3 影音大流)</a></h3>
        <p style="font-size:13px;color:var(--text-muted);margin:8px 0;">20元/月起，侧重大流量与多媒体吞吐，适合高并发或多设备协同的{keyword}需求。</p>
        <a href="https://quanqi12.twilightaff.com/#/?code=beAVqNPf" rel="sponsored nofollow noopener" target="_blank" class="btn-register-prominent" style="padding:8px 12px;font-size:13px;width:100%;">👉 前往暮光加速官网注册</a>
      </div>
      <div style="padding:16px;border:1px solid var(--border-subtle);border-radius:var(--radius-sm);background:var(--bg-page);">
        <h3 style="font-size:16px;font-weight:700;"><a href="/providers/breezenet/">4. 微风网络 (Rank 4 轻量专线)</a></h3>
        <p style="font-size:13px;color:var(--text-muted);margin:8px 0;">轻量专线方案，支持通用订阅导入，适合轻度使用且追求简洁配置的用户。</p>
        <a href="https://edp01.breezenetaff.com/#/?code=vxDUI8kY" rel="sponsored nofollow noopener" target="_blank" class="btn-register-prominent" style="padding:8px 12px;font-size:13px;width:100%;">👉 前往微风网络官网注册</a>
      </div>
    </div>
  </div>
</div>
"""
        self.render_page(f"{title}｜机场推荐云", desc, url, content_html, page_type="website")
        print(f"Generated {keyword} landing page.")

    def _generate_rankings_page(self):
        title = "机场排行榜与排序说明：编辑展示原则与合作关系透明披露"
        desc = "系统说明机场推荐云的展示排序机制、评测维度与商业合作披露，客观呈现各项服务的适用场景与局限性，不伪造行业权威排名。"
        content_html = f"""
<div class="container" style="padding:32px 20px;">
  <div class="breadcrumbs">
    <a href="/">首页</a> <span>/</span> <span>机场排行榜说明</span>
  </div>
  <header style="margin-bottom:28px;">
    <h1 style="font-size:30px;font-weight:800;margin-bottom:12px;">{title}</h1>
    <p style="font-size:15px;color:var(--text-muted);max-width:850px;line-height:1.7;">{desc}</p>
  </header>
  <div class="article-body" style="max-width:850px;">
    <h2>一、排序机制与编辑原则说明</h2>
    <p>本站公开展示的机场推荐榜单（全球云第一、飞猫云第二、暮光加速第三、微风网络第四）体现了本站当前的重点推荐顺序与商业合作策略。本站明确声明：该排序不代表经过实验室严格单盲测试证明的绝对性能排名，亦不存在行业公认的绝对客观榜单。</p>
    
    <h2>二、四项主推服务定位与官网注册对照</h2>
    <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(240px, 1fr));gap:16px;margin:20px 0;">
      <div style="padding:16px;border:1px solid var(--border-color);border-radius:var(--radius-sm);">
        <h3>1. 全球云 (TOP 1)</h3>
        <p style="font-size:13px;color:var(--text-muted);margin:8px 0;">多地区专线中转，综合表现首选，优惠码 qq88 享 8 折。</p>
        <a href="https://hueue09.gcvipaff.com/#/?code=z8U9aaa4" rel="sponsored nofollow noopener" target="_blank" class="btn-register-prominent" style="padding:6px 12px;font-size:12px;width:100%;">👉 前往全球云官网注册</a>
      </div>
      <div style="padding:16px;border:1px solid var(--border-color);border-radius:var(--radius-sm);">
        <h3>2. 飞猫云 (TOP 2)</h3>
        <p style="font-size:13px;color:var(--text-muted);margin:8px 0;">84元/年小流量包（折合7元/月），备用入门首选。</p>
        <a href="https://quanqiu.flycatvipaff.cc/#/?code=7ZOeVmNS" rel="sponsored nofollow noopener" target="_blank" class="btn-register-prominent" style="padding:6px 12px;font-size:12px;width:100%;">👉 前往飞猫云官网注册</a>
      </div>
      <div style="padding:16px;border:1px solid var(--border-color);border-radius:var(--radius-sm);">
        <h3>3. 暮光加速 (TOP 3)</h3>
        <p style="font-size:13px;color:var(--text-muted);margin:8px 0;">大流量专线，晚高峰 4K 影音优化，优惠码 mm88 享 8 折。</p>
        <a href="https://quanqi12.twilightaff.com/#/?code=beAVqNPf" rel="sponsored nofollow noopener" target="_blank" class="btn-register-prominent" style="padding:6px 12px;font-size:12px;width:100%;">👉 前往暮光加速官网注册</a>
      </div>
      <div style="padding:16px;border:1px solid var(--border-color);border-radius:var(--radius-sm);">
        <h3>4. 微风网络 (TOP 4)</h3>
        <p style="font-size:13px;color:var(--text-muted);margin:8px 0;">轻量专线方案，自研客户端开箱即用，价格待结算页核验。</p>
        <a href="https://edp01.breezenetaff.com/#/?code=vxDUI8kY" rel="sponsored nofollow noopener" target="_blank" class="btn-register-prominent" style="padding:6px 12px;font-size:12px;width:100%;">👉 前往微风网络官网注册</a>
      </div>
    </div>
  </div>
</div>
"""
        self.render_page(f"{title}｜机场推荐云", desc, "/rankings/", content_html, page_type="website")
        print("Generated rankings page.")

    def _generate_nodes_page(self):
        title = "机场节点推荐与选择指南：地区、延迟与线路说明"
        desc = "详细解析香港、日本、新加坡、美西等主流节点地区的网络特点与延迟差异，指导用户如何按办公、影音、游戏等场景科学选择节点。"
        content_html = f"""
<div class="container" style="padding:32px 20px;">
  <div class="breadcrumbs">
    <a href="/">首页</a> <span>/</span> <span>节点推荐与指南</span>
  </div>
  <header style="margin-bottom:28px;">
    <h1 style="font-size:30px;font-weight:800;margin-bottom:12px;">{title}</h1>
    <p style="font-size:15px;color:var(--text-muted);max-width:850px;line-height:1.7;">{desc}</p>
  </header>
  <div class="article-body" style="max-width:850px;">
    <h2>一、主流节点地区的网络特性与延迟参考</h2>
    <ul>
      <li><strong>香港节点 (HK)</strong>：物理延迟最低（20~50ms），交互极度灵敏；</li>
      <li><strong>日本节点 (JP)</strong>：骨干网络优良（50~80ms），适合开发者工具与学术查阅；</li>
      <li><strong>新加坡节点 (SG)</strong>：东南亚枢纽（60~90ms），流媒体与多平台解锁良好；</li>
      <li><strong>美国节点 (US)</strong>：跨洋骨干（130~180ms），IP 纯净度高，海外服务覆盖最全。</li>
    </ul>

    <h2>二、四项主推服务的节点覆盖优势</h2>
    <p>第一名<strong>全球云</strong>部署了全面的多地区专线出口，第二名<strong>飞猫云</strong>精耕低延迟香港节点，第三名<strong>暮光加速</strong>强化了晚高峰影音线路，第四名<strong>微风网络</strong>提供轻量专线节点。所有服务均可直达官网完成注册与订阅拉取。</p>
  </div>
</div>
"""
        self.render_page(f"{title}｜机场推荐云", desc, "/nodes/", content_html, page_type="website")
        print("Generated nodes page.")

    def _generate_coupons_page(self):
        title = "机场优惠码汇总与核验：新用户折扣与省钱建议"
        desc = "集中整理全球云、飞猫云、暮光加速等服务商经人工核验的有效优惠码，说明适用条件、门槛与结算页使用方法，不制造虚假折扣。"
        content_html = f"""
<div class="container" style="padding:32px 20px;">
  <div class="breadcrumbs">
    <a href="/">首页</a> <span>/</span> <span>机场优惠码汇总</span>
  </div>
  <header style="margin-bottom:28px;">
    <h1 style="font-size:30px;font-weight:800;margin-bottom:12px;">{title}</h1>
    <p style="font-size:15px;color:var(--text-muted);max-width:850px;line-height:1.7;">{desc}</p>
  </header>
  <div style="max-width:850px;">
    <div class="table-responsive" style="margin-bottom:32px;">
      <table class="data-table">
        <thead>
          <tr>
            <th>服务商</th>
            <th>专属优惠码</th>
            <th>折扣口径</th>
            <th>核验日期</th>
            <th>官网直达</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>全球云 (Rank 1)</strong></td>
            <td><code class="coupon-code">qq88</code></td>
            <td>8 折优惠，结账页有效</td>
            <td>2026-09-19</td>
            <td><a href="https://hueue09.gcvipaff.com/#/?code=z8U9aaa4" rel="sponsored nofollow noopener" target="_blank" class="btn-register-prominent" style="padding:4px 10px;font-size:12px;min-height:auto;">官网注册</a></td>
          </tr>
          <tr>
            <td><strong>飞猫云 (Rank 2)</strong></td>
            <td><code class="coupon-code">flycat888</code></td>
            <td>新用户季付及以上 8 折</td>
            <td>2026-09-19</td>
            <td><a href="https://quanqiu.flycatvipaff.cc/#/?code=7ZOeVmNS" rel="sponsored nofollow noopener" target="_blank" class="btn-register-prominent" style="padding:4px 10px;font-size:12px;min-height:auto;">官网注册</a></td>
          </tr>
          <tr>
            <td><strong>暮光加速 (Rank 3)</strong></td>
            <td><code class="coupon-code">mm88</code></td>
            <td>8 折优惠，适用大流量套餐</td>
            <td>2026-09-19</td>
            <td><a href="https://quanqi12.twilightaff.com/#/?code=beAVqNPf" rel="sponsored nofollow noopener" target="_blank" class="btn-register-prominent" style="padding:4px 10px;font-size:12px;min-height:auto;">官网注册</a></td>
          </tr>
          <tr>
            <td><strong>微风网络 (Rank 4)</strong></td>
            <td>暂无优惠码</td>
            <td>以结算页为准</td>
            <td>2026-09-19</td>
            <td><a href="https://edp01.breezenetaff.com/#/?code=vxDUI8kY" rel="sponsored nofollow noopener" target="_blank" class="btn-register-prominent" style="padding:4px 10px;font-size:12px;min-height:auto;">官网注册</a></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</div>
"""
        self.render_page(f"{title}｜机场推荐云", desc, "/coupons/", content_html, page_type="website")
        print("Generated coupons page.")

    def _generate_reviews_page(self):
        title = "机场测评汇总：逐个查看 27 家服务商价格、套餐与节点资料"
        desc = "全景索引本站收录的全部 27 家服务商独立测评，每一家均包含套餐起步价、主打卖点、线路支持与购买前核对要点。"
        
        cards_html = ""
        for p in self.provider_reviews:
            cards_html += f"""
<div class="provider-card" style="padding:16px;">
  <span class="provider-card-rank">TOP {p['rank']}</span>
  <h2 style="font-size:17px;font-weight:700;margin-bottom:6px;"><a href="{p['url']}">{p['name']}</a></h2>
  <div style="font-size:14px;color:var(--primary);font-weight:600;margin-bottom:6px;">{p['priceFrom']}</div>
  <p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;flex-grow:1;">{p['suitableFor']}</p>
  <div class="provider-card-actions">
    <a href="{p['url']}" class="btn-provider-review">查看 {p['name']} 独立测评</a>
    <a href="{p['inviteURL']}" rel="sponsored nofollow noopener" target="_blank" class="btn-register-prominent" style="padding:8px;font-size:12px;min-height:auto;">👉 官网注册查看套餐</a>
  </div>
</div>
"""
        content_html = f"""
<div class="container" style="padding:32px 20px;">
  <div class="breadcrumbs">
    <a href="/">首页</a> <span>/</span> <span>机场测评汇总</span>
  </div>
  <header style="margin-bottom:28px;">
    <h1 style="font-size:30px;font-weight:800;margin-bottom:12px;">{title}</h1>
    <p style="font-size:15px;color:var(--text-muted);max-width:850px;line-height:1.7;">{desc}</p>
  </header>
  <div class="providers-grid">
    {cards_html}
  </div>
</div>
"""
        self.render_page(f"{title}｜机场推荐云", desc, "/reviews/", content_html, page_type="website")
        print("Generated reviews aggregate page.")

    def _generate_providers_directory_page(self):
        title = "机场服务资料库：27 家服务商信息与核验索引"
        desc = "汇集全部 27 家服务商的基础资料、套餐价格梯度、协议支持、核验状态与官方购买入口，提供中立透明的选型参考。"
        
        list_html = ""
        for p in self.providers:
            list_html += f"""
<div class="sidebar-widget" style="margin-bottom:14px;">
  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
    <div>
      <span class="provider-card-rank" style="position:static;display:inline-block;margin-right:8px;">TOP {p['rank']}</span>
      <strong style="font-size:17px;"><a href="/providers/{p['slug']}/">{p['name']}</a></strong>
      <span style="font-size:13px;color:var(--primary);margin-left:8px;">{p['priceFrom']}</span>
    </div>
    <a href="{p['inviteURL']}" rel="sponsored nofollow noopener" target="_blank" class="btn-register-prominent" style="padding:4px 12px;font-size:12px;min-height:auto;">官网注册</a>
  </div>
  <p style="font-size:13px;color:var(--text-muted);margin-top:8px;">{p['summary']}</p>
</div>
"""
        content_html = f"""
<div class="container" style="padding:32px 20px;">
  <div class="breadcrumbs">
    <a href="/">首页</a> <span>/</span> <span>服务资料库</span>
  </div>
  <header style="margin-bottom:28px;">
    <h1 style="font-size:30px;font-weight:800;margin-bottom:12px;">{title}</h1>
    <p style="font-size:15px;color:var(--text-muted);max-width:850px;line-height:1.7;">{desc}</p>
  </header>
  <div style="max-width:880px;">
    {list_html}
  </div>
</div>
"""
        self.render_page(f"{title}｜机场推荐云", desc, "/providers/", content_html, page_type="website")
        print("Generated providers directory page.")

    def _generate_status_page(self):
        title = "机场服务状态与人工数据核验日志"
        desc = "记录本站所有 27 家服务商最近一次人工核验的时间、价格变动记录、优惠码有效性及条款跟踪说明。"
        content_html = f"""
<div class="container" style="padding:32px 20px;">
  <div class="breadcrumbs">
    <a href="/">首页</a> <span>/</span> <span>服务状态日志</span>
  </div>
  <header style="margin-bottom:28px;">
    <h1 style="font-size:30px;font-weight:800;margin-bottom:12px;">{title}</h1>
    <p style="font-size:15px;color:var(--text-muted);max-width:850px;line-height:1.7;">{desc}</p>
  </header>
  <div class="article-body" style="max-width:850px;">
    <h2>人工核验工作机制</h2>
    <p>本站严格摒弃任何虚假的“实时监控”或自动化模拟测速脚本，所有展示的数据均由编辑团队定期手动打开服务商结算页与控制台进行比对核验。最后一次全量核验日期为：<strong>2026-09-19</strong>（全站产物编译更新于 2026-09-23）。</p>
    
    <h2>核验重点与常见状态</h2>
    <ul>
      <li><strong>全球云</strong>：价格与套餐结构稳定，优惠码 <code>qq88</code> 有效（8折），状态正常；</li>
      <li><strong>飞猫云</strong>：年付小包 84 元/年记录有效，新用户优惠码 <code>flycat888</code> 有效，状态正常；</li>
      <li><strong>暮光加速</strong>：大流量多媒体套餐结构稳定，优惠码 <code>mm88</code> 有效，状态正常；</li>
      <li><strong>微风网络</strong>：公开记录存在价格口径差异，当前标明“待结算页核验”，状态跟踪中。</li>
    </ul>
  </div>
</div>
"""
        self.render_page(f"{title}｜机场推荐云", desc, "/status/", content_html, page_type="website")
        print("Generated status page.")

    def _generate_trust_pages(self):
        trust_pages = [
            ("about", "关于我们：机场推荐与测评编辑说明", "介绍机场推荐云的创立初衷、服务受众、内容定位、核验流程与防坑理念，说明我们如何为新手提供透明参考。"),
            ("contact", "联系我们：机场资料纠错与 Telegram 交流频道", "提供真实资料纠错通道、商务咨询与意见反馈说明，欢迎读者协助我们保持信息的准确与及时。"),
            ("editorial-policy", "机场推荐编辑原则与独立性声明", "系统阐述本站在选题策划、排序依据、事实与观点区分以及利益冲突防范方面的严格准则。"),
            ("methodology", "机场测评方法论与数据核验标准", "详述本站在收集服务商资料、核实价格梯度、评估线路兼容性与记录最后核验时间时的标准化流程。"),
            ("corrections", "资料纠错政策与更新日志规范", "说明本站如何接收读者反馈、核对错误事实、更新页面内容以及记录重大变更日志的透明机制。"),
            ("affiliate-disclosure", "邀请链接与商业合作透明披露", "详细披露本站如何使用邀请链接维系运营、推广佣金机制以及如何确保商业合作不损害事实真实性。"),
            ("privacy", "隐私政策声明", "说明机场推荐云如何尊重访客隐私，本站不搜集敏感个人信息，不使用高侵入性第三方追踪探针。"),
            ("terms", "服务条款与免责声明", "明确本站内容的参考性质、知识产权声明及用户在遵守所在地法律法规前提下文明合规使用工具的责任。"),
            ("disclaimer", "免责声明", "声明本站提供的信息仅供技术交流与合规网络研究参考，本站与第三方服务商不存在直接担保或从属关系。")
        ]
        
        for slug, title, desc in trust_pages:
            extra_content = ""
            if slug == "contact":
                extra_content = f"""
<div style="background:var(--primary-light);border:1px solid var(--primary-border);border-radius:var(--radius-md);padding:24px;margin:24px 0;">
  <h3 style="font-size:18px;font-weight:700;margin-bottom:8px;color:var(--text-main);">官方 Telegram 交流频道与纠错入口</h3>
  <p style="font-size:14px;color:var(--text-muted);margin-bottom:16px;">如果您在阅读过程中发现任何服务商价格变动、节点资料调整或优惠码失效，欢迎加入我们的官方 Telegram 交流群随时提交反馈，我们将第一时间核实并修正：</p>
  <a href="{self.tg_channel}" target="_blank" rel="sponsored nofollow noopener" class="btn-register-prominent" style="display:inline-flex;align-items:center;gap:8px;">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/></svg>
    <span>点击加入官方 Telegram 交流频道 (t.me/+U77JVhkbnhgzM2Q9)</span>
  </a>
</div>
"""
            content_html = f"""
<div class="container" style="padding:32px 20px;">
  <div class="breadcrumbs">
    <a href="/">首页</a> <span>/</span> <span>{title.split('：')[0]}</span>
  </div>
  <header style="margin-bottom:28px;">
    <h1 style="font-size:30px;font-weight:800;margin-bottom:12px;">{title}</h1>
    <p style="font-size:15px;color:var(--text-muted);max-width:850px;line-height:1.7;">{desc}</p>
  </header>
  <div class="article-body" style="max-width:850px;">
    <h2>内容概述与正文说明</h2>
    <p>{desc}</p>
    {extra_content}
    <p>机场推荐云（jichangtuijian.cloud）致力于构建一个纯净、透明、带核验日期的中文网络服务资料库。在互联网信息纷繁复杂的当下，我们坚信唯有坚持客观记录、不夸大宣传、不制造虚假排名的中立态度，才能真正帮助新手用户少走弯路。</p>
    <p>本站严格遵循合规表达准则，所有网络协议与工具均在合规中立的语境下进行技术解读。如果您在阅读过程中发现任何数据有误，或有任何建设性意见，欢迎通过我们的公开渠道与我们取得联系。</p>
  </div>
</div>
"""
            self.render_page(f"{title}｜机场推荐云", desc, f"/{slug}/", content_html, page_type="website")

        print("Generated 9 trust and legal pages.")

    def generate_sitemap_and_robots_and_rss(self):
        robots_content = f"""User-agent: *
Allow: /

Sitemap: {self.domain}/sitemap.xml
"""
        with open(os.path.join(self.output_dir, "robots.txt"), "w", encoding="utf-8") as f:
            f.write(robots_content)

        unique_urls = sorted(list(set(self.sitemap_urls)))
        sitemap_items = ""
        for url in unique_urls:
            sitemap_items += f"""  <url>
    <loc>{url}</loc>
    <lastmod>{self.today_iso}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{"1.0" if url == f"{self.domain}/" else "0.8"}</priority>
  </url>\n"""

        sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{sitemap_items}</urlset>
"""
        with open(os.path.join(self.output_dir, "sitemap.xml"), "w", encoding="utf-8") as f:
            f.write(sitemap_xml)

        rss_items = ""
        for art in self.nav_articles[:15]:
            rss_items += f"""    <item>
      <title>{html.escape(art['title'])}</title>
      <link>{self.domain}{art['url']}</link>
      <description>{html.escape(art['metaDescription'])}</description>
      <pubDate>Wed, 23 Sep 2026 12:00:00 +0800</pubDate>
      <guid>{self.domain}{art['url']}</guid>
    </item>\n"""

        rss_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>{html.escape(self.brand_name)}</title>
    <link>{self.domain}/</link>
    <description>{html.escape(self.profile['siteTopic'])}</description>
    <language>zh-CN</language>
    <lastBuildDate>Wed, 23 Sep 2026 12:00:00 +0800</lastBuildDate>
{rss_items}  </channel>
</rss>
"""
        with open(os.path.join(self.output_dir, "rss.xml"), "w", encoding="utf-8") as f:
            f.write(rss_xml)

        content_404 = f"""
<div class="container" style="padding:64px 20px;text-align:center;">
  <h1 style="font-size:48px;font-weight:800;color:var(--primary);margin-bottom:16px;">404 - 页面未找到</h1>
  <p style="font-size:16px;color:var(--text-muted);margin-bottom:24px;">抱歉，您访问的页面不存在或已被移动。</p>
  <div style="display:flex;justify-content:center;gap:12px;">
    <a href="/" class="btn-primary">返回首页</a>
    <a href="/recommendations/" class="btn-secondary">查看机场推荐</a>
    <a href="/faq/" class="btn-secondary">查阅常见问题</a>
  </div>
</div>
"""
        self.render_page("404 页面未找到｜机场推荐云", "抱歉，您访问的页面不存在或已被移动。", "/404.html", content_404, page_type="website")

        print(f"Generated robots.txt, sitemap.xml ({len(unique_urls)} URLs), rss.xml and 404.html.")

    def run_all(self):
        print("Starting static site compilation...")
        self.clean_output_dir()
        self.generate_home_page()
        self.generate_all_provider_pages()
        self.generate_all_navigation_articles()
        self.generate_faq_pages()
        self.generate_landing_pages()
        self.generate_sitemap_and_robots_and_rss()
        print("Static site compilation completed successfully!")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    generator = SiteGenerator(base_dir)
    generator.run_all()
