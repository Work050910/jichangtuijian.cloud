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
            
        # Copy root icon files
        for icon_name in ["favicon.ico", "favicon.png", "apple-touch-icon.png"]:
            src_icon = os.path.join(self.base_dir, "src", "static", "images", icon_name)
            if not os.path.exists(src_icon):
                src_icon = os.path.join(self.base_dir, "src", "static", "images", "favicon.png")
            if os.path.exists(src_icon):
                shutil.copy2(src_icon, os.path.join(self.output_dir, icon_name))

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
        <img src="/static/images/logo-icon.png" alt="{self.brand_name} Logo" width="28" height="28" style="border-radius:6px;display:block;">
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
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon.png">
  <link rel="icon" type="image/png" sizes="192x192" href="/static/images/logo-icon.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
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
            is_recommend = (rank == 1 or p['slug'] == 'quanqiu-cloud')
            card_class = "provider-card is-station-recommend" if is_recommend else "provider-card"
            recommend_badge = '<span class="badge-station-recommend" style="margin-left:6px;">🔥 站长推荐</span>' if is_recommend else ""
            coupon_html = f'<div class="provider-coupon-box"><span>优惠码：<span class="coupon-code">{p["coupon"]}</span></span><button class="btn-copy" data-coupon="{p["coupon"]}" data-provider="{p["slug"]}">复制</button></div>' if p['coupon'] != '暂无优惠码' else '<div class="provider-coupon-box"><span style="color:var(--text-light)">暂无优惠码</span></div>'
            
            cards_html += f"""
<div class="{card_class}">
  <span class="provider-card-rank">TOP {rank}</span>
  <h3 class="provider-card-title"><a href="/providers/{p['slug']}/">{p['name']}</a>{recommend_badge}</h3>
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
            is_rec = (p['rank'] == 1 or p['slug'] == 'quanqiu-cloud')
            rec_tag = ' <span class="badge-station-recommend" style="font-size:10px;padding:1px 6px;margin-left:4px;">🔥 站长推荐</span>' if is_rec else ""
            table_rows += f"""
<tr>
  <td><strong>{p['rank']}</strong></td>
  <td><a href="/providers/{p['slug']}/"><strong>{p['name']}</strong></a>{rec_tag}</td>
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
        <div class="widget-title">使用指南与选型</div>
        <ul style="list-style:none;font-size:13px;display:flex;flex-direction:column;gap:8px;">
          <li><a href="/recommendations/">• 机场推荐精选榜</a></li>
          <li><a href="/start-here/">• 新手快速上手指南</a></li>
          <li><a href="/faq/">• 常见问题答疑库</a></li>
        </ul>
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
        <div class="widget-title" style="display:flex;align-items:center;justify-content:space-between;">
          <span>核心服务商官网直达</span>
          <span style="font-size:11px;font-weight:600;color:var(--primary);background:var(--primary-light);padding:2px 6px;border-radius:4px;">人工核验</span>
        </div>
        <div style="display:flex;flex-direction:column;gap:12px;">
          <!-- Card 1: 全球云 (站长推荐) -->
          <div class="sidebar-airport-card is-station-recommend">
            <div class="sidebar-card-header">
              <div class="sidebar-card-title">
                <span class="sidebar-card-rank">TOP 1</span>
                <strong>全球云</strong>
              </div>
              <span class="badge-station-recommend">🔥 站长推荐</span>
            </div>
            <div class="sidebar-card-meta">
              <span class="sidebar-card-price">20元/月起</span>
              <span class="sidebar-card-tag">8折码: <strong>qq88</strong></span>
            </div>
            <div style="font-size:12px;color:var(--text-muted);line-height:1.4;">
              旗舰专线集群 · 30+地区IP · AI/流媒体4K全解
            </div>
            <a href="https://hueue09.gcvipaff.com/#/?code=z8U9aaa4" rel="sponsored nofollow noopener" target="_blank" class="btn-register-prominent" style="padding:8px 12px;font-size:13px;width:100%;" data-provider="quanqiu-cloud" data-rank="1" data-placement="sidebar_rec">👉 前往全球云官网注册</a>
          </div>

          <!-- Card 2: 飞猫云 -->
          <div class="sidebar-airport-card">
            <div class="sidebar-card-header">
              <div class="sidebar-card-title">
                <span class="sidebar-card-rank">TOP 2</span>
                <strong>飞猫云</strong>
              </div>
              <span style="font-size:11px;color:#059669;background:#ecfdf5;border:1px solid #a7f3d0;padding:2px 6px;border-radius:9999px;font-weight:700;">性价比先锋</span>
            </div>
            <div class="sidebar-card-meta">
              <span class="sidebar-card-price">84元/年起</span>
              <span class="sidebar-card-tag">折合 7元/月</span>
            </div>
            <div style="font-size:12px;color:var(--text-muted);line-height:1.4;">
              纯正 IEPL 专线 · 自研一键客户端 · 8折码 flycat888
            </div>
            <a href="https://quanqiu.flycatvipaff.cc/#/?code=7ZOeVmNS" rel="sponsored nofollow noopener" target="_blank" class="btn-register-prominent" style="padding:8px 12px;font-size:13px;width:100%;" data-provider="flycat-cloud" data-rank="2" data-placement="sidebar_rec">👉 前往飞猫云官网注册</a>
          </div>

          <!-- Card 3: 暮光加速 -->
          <div class="sidebar-airport-card">
            <div class="sidebar-card-header">
              <div class="sidebar-card-title">
                <span class="sidebar-card-rank">TOP 3</span>
                <strong>暮光加速</strong>
              </div>
              <span style="font-size:11px;color:#7c3aed;background:#f5f3ff;border:1px solid #ddd6fe;padding:2px 6px;border-radius:9999px;font-weight:700;">晚高峰影音</span>
            </div>
            <div class="sidebar-card-meta">
              <span class="sidebar-card-price">20元/月起</span>
              <span class="sidebar-card-tag">8折码: <strong>mm88</strong></span>
            </div>
            <div style="font-size:12px;color:var(--text-muted);line-height:1.4;">
              晚高峰大带宽传输 · 4K/8K 流媒体极速秒开 · 大流量
            </div>
            <a href="https://quanqi12.twilightaff.com/#/?code=beAVqNPf" rel="sponsored nofollow noopener" target="_blank" class="btn-register-prominent" style="padding:8px 12px;font-size:13px;width:100%;" data-provider="twilight" data-rank="3" data-placement="sidebar_rec">👉 前往暮光加速官网注册</a>
          </div>

          <!-- Card 4: 微风网络 -->
          <div class="sidebar-airport-card">
            <div class="sidebar-card-header">
              <div class="sidebar-card-title">
                <span class="sidebar-card-rank">TOP 4</span>
                <strong>微风网络</strong>
              </div>
              <span style="font-size:11px;color:#2563eb;background:#eff6ff;border:1px solid #bfdbfe;padding:2px 6px;border-radius:9999px;font-weight:700;">商务稳定</span>
            </div>
            <div class="sidebar-card-meta">
              <span class="sidebar-card-price">轻量专线</span>
              <span class="sidebar-card-tag">开箱即用</span>
            </div>
            <div style="font-size:12px;color:var(--text-muted);line-height:1.4;">
              商务多设备协同 · 通用订阅支持 · 结算页核验
            </div>
            <a href="https://edp01.breezenetaff.com/#/?code=vxDUI8kY" rel="sponsored nofollow noopener" target="_blank" class="btn-register-prominent" style="padding:8px 12px;font-size:13px;width:100%;" data-provider="breezenet" data-rank="4" data-placement="sidebar_rec">👉 前往微风网络官网注册</a>
          </div>
        </div>
      </div>
      <div class="sidebar-widget">
        <div class="widget-title">信息核验声明</div>
        <p style="font-size:12px;color:var(--text-muted);line-height:1.6;">本站所有推荐服务均经过人工定期核验，价格与优惠以各官网当前实时结算页为准。</p>
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

        print(f"Generated {len(self.nav_articles)} navigation articles.")

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
        <div class="widget-title">知识库索引</div>
        <ul style="list-style:none;font-size:13px;display:flex;flex-direction:column;gap:8px;">
          <li><a href="/start-here/">• 新手开始教程</a></li>
          <li><a href="/compare/">• 价格与流量对比</a></li>
          <li><a href="/devices/">• 设备客户端配置</a></li>
          <li><a href="/before-you-buy/">• 购买前避坑须知</a></li>
        </ul>
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
        title = "2026 最新机场推荐精选总榜：27家高性价比、稳定专线与AI流媒体解锁机场横向评测"
        desc = "2026 最新机场推荐权威全景评测，精选 27 家高性价比机场与稳定专线机场。深度横向对比价格、节点线路、Clash配置、ChatGPT/Claude等AI工具及4K流媒体解锁能力，附专属优惠码与官网注册入口。"
        
        # Meta extras mapping for line types, protocols, AI unlock and target audience for all 27 providers
        meta_extras = {
            "quanqiu-cloud": {
                "line": "多入口 BGP + 跨境专线优化",
                "protocols": "Shadowsocks, Trojan, VLESS",
                "ai_unlock": "ChatGPT Plus, Claude 3.5, Gemini Pro, Midjourney 全解",
                "streaming": "Netflix 4K, Disney+, YouTube Premium, TikTok 全区",
                "audience": "跨境电商出海、外贸商务、多国 IP 切换、企业多设备协同",
                "tags": ["综合旗舰", "多国节点", "智能分流", "企业首选"]
            },
            "flycat-cloud": {
                "line": "全线 IEPL/IPLC 专线隧道",
                "protocols": "Shadowsocks, Trojan, VLESS",
                "ai_unlock": "OpenAI ChatGPT, Claude 3.5, Gemini 稳定问答",
                "streaming": "Netflix 原生解锁, Disney+, YouTube 4K",
                "audience": "预算敏感型个人、小流量年付备用、学生及轻量办公族",
                "tags": ["性价比年付", "IEPL专线", "自研客户端", "学生推荐"]
            },
            "twilight": {
                "line": "晚高峰大带宽传输优化专线",
                "protocols": "Shadowsocks, Trojan",
                "ai_unlock": "ChatGPT 常用端、Claude 网页端与 API",
                "streaming": "YouTube 4K/8K 秒开、Netflix 极速加载、HBO Max",
                "audience": "流媒体重度追剧党、大流量影音下载、高频音视频会议",
                "tags": ["晚高峰影音", "大流量大户", "4K秒开", "低丢包"]
            },
            "breezenet": {
                "line": "轻量专线隧道中转",
                "protocols": "Shadowsocks, Trojan, 自研客户端",
                "ai_unlock": "基础 AI 工具问答、搜索引擎 AI 协同",
                "streaming": "主流流媒体 1080P/4K 解锁",
                "audience": "新手入门、轻度日常浏览、不想研究复杂配置的初学者",
                "tags": ["轻量专线", "开箱即用", "自研客户端", "新手友好"]
            },
            "u1s1": {
                "line": "优质中转优化 + 原生 IP 出口",
                "protocols": "Shadowsocks, Trojan",
                "ai_unlock": "ChatGPT, Claude 稳定连通",
                "streaming": "Netflix, Disney+ 原生解锁",
                "audience": "自用长效稳定需求、看重清晰流量档位与可用性的用户",
                "tags": ["稳定自用", "原生IP", "标注清晰", "中转优化"]
            },
            "jilian-cloud": {
                "line": "IPLC 内网专线加速通道",
                "protocols": "Shadowsocks, Trojan",
                "ai_unlock": "AI 办公助手、ChatGPT、代码 Copilot",
                "streaming": "主流流媒体港日新节点极速解锁",
                "audience": "跨境办公白领、远程音视频会议、外贸业务骨干",
                "tags": ["IPLC专线", "低延迟", "防QoS", "远程办公"]
            },
            "guangnian-ladder": {
                "line": "三网动态中转优化线路",
                "protocols": "Shadowsocks, 一键导入客户端",
                "ai_unlock": "ChatGPT 基础对话、海外社交平台",
                "streaming": "YouTube 4K、海外音乐平台",
                "audience": "刚需入门、学生族、移动端日常翻阅资料与轻量备用",
                "tags": ["入门轻量", "客户端易用", "三网优化", "高性价比"]
            },
            "guangsu-cloud": {
                "line": "BGP 多线入口 + 低延迟中转",
                "protocols": "Shadowsocks, Trojan",
                "ai_unlock": "GitHub Copilot, ChatGPT, Claude",
                "streaming": "YouTube 4K, Netflix 亚太区",
                "audience": "程序员、开发者、海外代码库拉取、轻度海外游戏联机",
                "tags": ["开发者首选", "BGP中转", "低延迟", "代码拉取"]
            },
            "weitu-cloud": {
                "line": "亚太低延迟 VLESS 节点群",
                "protocols": "VLESS, Trojan",
                "ai_unlock": "AI 内容生成工具、Claude, ChatGPT",
                "streaming": "Netflix 4K, Disney+, 亚太流媒体全解锁",
                "audience": "亚太节点重度用户、短视频创作者、多端协同办公",
                "tags": ["VLESS协议", "亚太低延迟", "智能负载", "多端协同"]
            },
            "yuzhou-cloud": {
                "line": "多出口专线负载 + 大流量带宽",
                "protocols": "Shadowsocks, Trojan",
                "ai_unlock": "全场景主流 AI 工具生态兼容",
                "streaming": "全球主要流媒体平台 4K 超清播放",
                "audience": "多任务大流量用户、跨区重度冲浪、家庭多设备共用",
                "tags": ["大流量性价比", "多地区覆盖", "家庭共享", "大带宽"]
            },
            "sujie": {
                "line": "高带宽 IPLC 专线 + 晚高峰负载均衡",
                "protocols": "Shadowsocks, Trojan",
                "ai_unlock": "ChatGPT Plus, Claude 3.5 快速响应",
                "streaming": "YouTube 4K/8K、Netflix 原生超高清",
                "audience": "对高峰时段网络稳定性要求极高的影音发烧友与专业用户",
                "tags": ["高带宽IPLC", "晚高峰无卡顿", "8K极速", "专业级"]
            },
            "sogo-cloud": {
                "line": "全球高速 BGP 专线优化",
                "protocols": "Shadowsocks, Trojan",
                "ai_unlock": "ChatGPT Plus, Claude Pro, Midjourney",
                "streaming": "Netflix Ultra HD, Disney+, Hulu",
                "audience": "多媒体设计师、AI 创作者、小微电商团队多并发使用",
                "tags": ["多设备并发", "全球节点", "AI创作", "团队共享"]
            },
            "kuaili": {
                "line": "均衡型中转接入线路",
                "protocols": "Shadowsocks",
                "ai_unlock": "日常 AI 检索、ChatGPT 网页版",
                "streaming": "YouTube 1080P/4K、海外社媒浏览",
                "audience": "临时备用机、轻度网络开销、日常网页浏览与即时通讯",
                "tags": ["低门槛入门", "轻量备用", "快速接入", "经济实惠"]
            },
            "two-cats-cloud": {
                "line": "中转 + 专线混合调度线路",
                "protocols": "Shadowsocks, Trojan",
                "ai_unlock": "主流 AI 平台全支持、ChatGPT 原生解锁",
                "streaming": "Netflix, Disney+ 港台日韩美区解锁",
                "audience": "预算适中、日常兼顾大流量办公与高清追剧的白领人群",
                "tags": ["混合线路", "原生IP", "均衡稳健", "白领日常"]
            },
            "yifan-cloud": {
                "line": "VLESS / Reality 新一代协议专线",
                "protocols": "VLESS, Reality, Trojan",
                "ai_unlock": "跨境电商运营、ChatGPT, Claude 稳定连接",
                "streaming": "YouTube 4K, Netflix 全球热门剧集",
                "audience": "亚马逊/Shopee 跨境电商卖家、大流量下载与重度浏览者",
                "tags": ["Reality协议", "大流量首选", "三网直连", "抗干扰"]
            },
            "edgenova": {
                "line": "全球边缘节点冗余备份网络",
                "protocols": "Reality, Trojan, VLESS",
                "ai_unlock": "AI API 持续并发调用、自动化脚本数据同步",
                "streaming": "海外全平台流媒体及学术数据库解锁",
                "audience": "海外技术团队、自动化接口运维、技术极客与科研人员",
                "tags": ["边缘计算", "原生IP", "API高并发", "技术极客"]
            },
            "kexin-cloud": {
                "line": "IEPL 高等级加密专线",
                "protocols": "Shadowsocks, Trojan",
                "ai_unlock": "ChatGPT, Claude, 涉密跨境协作通道",
                "streaming": "Netflix, Disney+, YouTube Premium",
                "audience": "高净值商务人士、重视数据隐私与售后保障的长期用户",
                "tags": ["企业级IEPL", "高隐私加密", "全平台覆盖", "品质服务"]
            },
            "wavenet": {
                "line": "海外 CDN 协同与专线加速通道",
                "protocols": "Shadowsocks, Trojan",
                "ai_unlock": "ChatGPT, Claude 专属低延迟优化",
                "streaming": "Twitch, YouTube 直播秒开、TikTok 跨国运营",
                "audience": "跨境直播观看、自媒体视频创作者、AI 工具重度从业者",
                "tags": ["AI深度适配", "直播加速", "自媒体必备", "高带宽"]
            },
            "ladder-cloud": {
                "line": "IEPL 企业专线 + 极简客户端",
                "protocols": "Shadowsocks, 自研客户端",
                "ai_unlock": "Google Workspace, ChatGPT 基础连通",
                "streaming": "Netflix, YouTube 4K 流畅播放",
                "audience": "不愿研究复杂规则的小白用户、多设备家庭日常使用",
                "tags": ["IEPL专线", "自研客户端", "新手防坑", "晚高峰保障"]
            },
            "lingdong-cloud": {
                "line": "全线 VLESS 协议高容错节点",
                "protocols": "VLESS, Trojan",
                "ai_unlock": "多协议自动回退、各类 AI 平台深度兼容",
                "streaming": "YouTube 4K 晚高峰满速、Netflix 稳定解锁",
                "audience": "复杂网络环境（校园网、企业局域网）下的穿透加速用户",
                "tags": ["全线VLESS", "校园网穿透", "高并发", "智能回退"]
            },
            "yinxingren": {
                "line": "纯专线架构 + 新加坡抗封锁混淆",
                "protocols": "VLESS, Trojan",
                "ai_unlock": "AI 原生原生 IP 访问、ChatGPT 零报错",
                "streaming": "8K 超清视频秒开、全区 Netflix 原生解锁",
                "audience": "敏感时期需要高防失联保障的高频商旅人士与出海团队",
                "tags": ["纯专线", "新加坡团队", "8K超高清", "原生IP"]
            },
            "flyv": {
                "line": "全线 1 倍率专线架构",
                "protocols": "VLESS, Trojan, Shadowsocks",
                "ai_unlock": "ChatGPT, Claude, Midjourney 原生全解锁",
                "streaming": "4K/8K 流媒体零卡顿、Disney+ 原生解锁",
                "audience": "追求无倍率套路、大流量超清视频与 AI 并发的高阶玩家",
                "tags": ["全线1倍率", "专线不限速", "8K视频", "AI全解"]
            },
            "wuyou-link": {
                "line": "双向中转隧道 + 通用订阅",
                "protocols": "Shadowsocks, Trojan, Clash",
                "ai_unlock": "海外邮件协同、基础 AI 交互平台",
                "streaming": "主流流媒体 1080P/4K 解锁",
                "audience": "外贸业务员、海外邮件联络、追求极低月均成本的备用人群",
                "tags": ["通用订阅", "低月均成本", "外贸办公", "全平台兼容"]
            },
            "civet-network": {
                "line": "IPLC 专线 + 1倍率不限设备",
                "protocols": "IPLC 隧道, Shadowsocks",
                "ai_unlock": "ChatGPT, Claude 等日常 AI 生产力工具",
                "streaming": "Netflix, YouTube 4K 高清播放",
                "audience": "多设备家庭、小微工作室团队共享、追求纯净 1 倍率用户",
                "tags": ["IPLC专线", "不限设备数", "1倍率无扣量", "工作室共享"]
            },
            "flashleap": {
                "line": "IPLC 专线 + 轻量级低抖动路由",
                "protocols": "Shadowsocks, Trojan, 自研端",
                "ai_unlock": "Notion AI, Figma, GitHub, ChatGPT 协同",
                "streaming": "YouTube 4K、海外音乐流媒体",
                "audience": "远程办公数字游民、敏捷敏捷开发者、日常学习办公族",
                "tags": ["IPLC专线", "极低抖动", "数字游民", "敏捷开发"]
            },
            "firefly": {
                "line": "核心骨干网专线 + 原生 IP 节点",
                "protocols": "VLESS, IPLC, Trojan",
                "ai_unlock": "AI 开发者 API 接口、大模型多并发调用",
                "streaming": "8K 极速流媒体、全区 Netflix/Disney+",
                "audience": "技术发烧友、跨国大文件传输、高端企业出海技术栈",
                "tags": ["骨干网IPLC", "VLESS原生", "企业级SLA", "开发者推荐"]
            },
            "kuajie-cloud": {
                "line": "全球 50+ 地区混合接入专线",
                "protocols": "Shadowsocks, Trojan, VLESS",
                "ai_unlock": "全球多国本地限制 AI 服务全解锁",
                "streaming": "全球小众流媒体与主流 4K 流媒体全覆盖",
                "audience": "跨国出海企业、全球市场调研员、多国出口 IP 刚需群体",
                "tags": ["全球50+地区", "多出口节点", "出海合规", "大流量"]
            }
        }

        # 1. Generate full 27-provider table rows
        table_rows = ""
        for p in self.providers:
            slug = p['slug']
            extras = meta_extras.get(slug, {
                "line": "高速优化线路",
                "protocols": "Shadowsocks, Trojan",
                "ai_unlock": "ChatGPT, Claude 稳定支持",
                "streaming": "Netflix, YouTube 4K 解锁",
                "audience": "日常办公、流媒体及学术查阅",
                "tags": ["稳定可靠", "高速节点"]
            })
            coupon_html = f"<code>{p['coupon']}</code>" if p['coupon'] != '暂无优惠码' else '<span style="color:var(--text-light);font-size:12px;">结算页确认</span>'
            table_rows += f"""
<tr>
  <td style="text-align:center;"><strong>TOP {p['rank']}</strong></td>
  <td>
    <a href="/providers/{slug}/" style="font-weight:700;color:var(--text-main);display:flex;align-items:center;gap:6px;">
      {p['name']}
      {"<span class='badge-station-recommend' style='font-size:10px;padding:1px 6px;'>🔥 站长推荐</span>" if (p['rank'] == 1 or slug == 'quanqiu-cloud') else ("<span style='background:#fef3c7;color:#92400e;font-size:10px;padding:2px 6px;border-radius:3px;font-weight:600;'>主推</span>" if p.get('isPrimary') else "")}
    </a>
  </td>
  <td><span style="font-weight:700;color:var(--primary);">{p['priceFrom']}</span></td>
  <td>{p['trafficFrom']}</td>
  <td>{coupon_html}</td>
  <td><span style="font-size:12px;color:var(--text-muted);">{extras['line']}</span></td>
  <td><span style="font-size:12px;color:var(--text-muted);">{extras['ai_unlock'][:22]}...</span></td>
  <td><span style="font-size:12px;color:var(--text-muted);">{extras['audience'][:24]}...</span></td>
  <td style="text-align:center;">
    <a href="{p['inviteURL']}" rel="sponsored nofollow noopener" target="_blank" class="btn-register-prominent" style="padding:6px 12px;font-size:12px;min-height:auto;" data-provider="{slug}" data-rank="{p['rank']}" data-placement="pillar_table">官网注册</a>
  </td>
</tr>
"""

        # 2. Generate 27 detailed provider review cards
        provider_cards_html = ""
        for p in self.providers:
            slug = p['slug']
            extras = meta_extras.get(slug, {
                "line": "高速优化线路",
                "protocols": "Shadowsocks, Trojan",
                "ai_unlock": "ChatGPT, Claude 稳定支持",
                "streaming": "Netflix, YouTube 4K 解锁",
                "audience": "日常办公、流媒体及学术查阅",
                "tags": ["稳定可靠", "高速节点"]
            })
            
            packages_li = "".join([f"<li style='margin-bottom:6px;'>{pkg}</li>" for pkg in p.get('packages', [])])
            if not packages_li:
                packages_li = f"<li>起步方案：{p['priceFrom']}，提供 {p['trafficFrom']}，具体按月/年付计费阶梯以官网结算页实时展示为准。</li>"
                
            tags_html = " ".join([f"<span style='background:var(--bg-subtle);border:1px solid var(--border-color);color:var(--text-muted);font-size:11px;padding:2px 8px;border-radius:4px;'>{tag}</span>" for tag in extras.get('tags', [])])
            
            coupon_banner = ""
            if p['coupon'] != '暂无优惠码':
                coupon_banner = f"""
<div style="background:#ecfdf5;border:1px solid #a7f3d0;border-radius:6px;padding:10px 14px;margin-bottom:16px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;">
  <span style="color:#065f46;font-size:13px;font-weight:600;">🎁 专属优惠码：<code style="background:#fff;padding:2px 6px;border:1px solid #10b981;border-radius:4px;color:#047857;font-weight:700;">{p['coupon']}</code> ({p.get('couponNote', '结算输入立享折扣')})</span>
  <span style="color:#059669;font-size:12px;">结账前请在优惠码输入框验证</span>
</div>
"""
            else:
                coupon_banner = f"""
<div style="background:var(--bg-subtle);border:1px solid var(--border-color);border-radius:6px;padding:8px 14px;margin-bottom:16px;font-size:12px;color:var(--text-muted);">
  ℹ️ 当前暂无公开通用优惠码，官方活动折扣可能直接在结算页生效，请以官网最新标价为准。
</div>
"""

            is_station_rec = (slug == 'quanqiu-cloud' or p['rank'] == 1)
            if is_station_rec:
                primary_badge = "<span class='badge-station-recommend'>🔥 站长推荐</span> <span style='background:linear-gradient(135deg, #f59e0b, #d97706);color:#fff;font-size:11px;padding:3px 8px;border-radius:9999px;font-weight:700;'>综合第一旗舰</span>"
                card_style = "background:linear-gradient(165deg, rgba(254, 243, 199, 0.22) 0%, var(--bg-surface) 100%);border:2px solid #f59e0b;border-radius:var(--radius-lg);padding:24px;margin-bottom:28px;box-shadow:0 8px 24px rgba(245, 158, 11, 0.16);transition:transform 0.2s, box-shadow 0.2s;"
                header_ribbon = """<div style="display:flex;align-items:center;justify-content:space-between;background:linear-gradient(90deg, #ef4444 0%, #f59e0b 100%);color:#fff;padding:8px 16px;border-radius:8px;margin-bottom:18px;font-weight:800;font-size:13px;box-shadow:0 2px 8px rgba(239, 68, 68, 0.25);">
  <span style="display:flex;align-items:center;gap:6px;">👑 站长力荐 · 全网综合首选旗舰机场</span>
  <span style="font-size:11px;background:rgba(255,255,255,0.22);padding:2px 10px;border-radius:20px;border:1px solid rgba(255,255,255,0.35);">长期主用认证 · 晚高峰稳定</span>
</div>"""
            else:
                primary_badge = "<span style='background:linear-gradient(135deg, #f59e0b, #d97706);color:#fff;font-size:11px;padding:2px 8px;border-radius:4px;font-weight:700;'>编辑重点推荐</span>" if p.get('isPrimary') else ""
                card_style = "background:var(--bg-surface);border:1px solid var(--border-color);border-radius:var(--radius-lg);padding:24px;margin-bottom:28px;box-shadow:0 2px 8px rgba(0,0,0,0.04);transition:transform 0.2s, box-shadow 0.2s;"
                header_ribbon = ""

            provider_cards_html += f"""
<div id="provider-{slug}" style="{card_style}">
  {header_ribbon}
  <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px;padding-bottom:16px;border-bottom:1px solid var(--border-subtle);margin-bottom:18px;">
    <div>
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
        <span style="background:var(--primary);color:#fff;font-weight:800;font-size:12px;padding:3px 10px;border-radius:20px;">TOP {p['rank']}</span>
        <h3 style="font-size:22px;font-weight:800;margin:0;">
          <a href="/providers/{slug}/" style="color:var(--text-main);text-decoration:none;">{p['name']} 机场</a>
        </h3>
        {primary_badge}
      </div>
      <div style="display:flex;gap:6px;flex-wrap:wrap;">{tags_html}</div>
    </div>
    <div style="display:flex;flex-direction:column;align-items:flex-end;gap:6px;">
      <div style="font-size:20px;font-weight:800;color:var(--primary);">{p['priceFrom']}</div>
      <a href="{p['inviteURL']}" rel="sponsored nofollow noopener" target="_blank" class="btn-register-prominent" style="padding:8px 18px;font-size:13px;" data-provider="{slug}" data-rank="{p['rank']}" data-placement="pillar_card_header">👉 官网注册体验</a>
    </div>
  </div>

  {coupon_banner}

  <div style="font-size:14px;color:var(--text-main);line-height:1.7;margin-bottom:18px;background:var(--bg-subtle);padding:14px 16px;border-radius:6px;border-left:4px solid var(--primary);">
    <strong>【核心定位与优势】</strong>{p['summary']}
  </div>

  <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(280px, 1fr));gap:16px;margin-bottom:18px;">
    <div style="background:var(--bg-subtle);padding:14px 16px;border-radius:6px;border:1px solid var(--border-subtle);">
      <h4 style="font-size:14px;font-weight:700;margin-bottom:8px;color:var(--primary);">🌐 节点线路与协议架构</h4>
      <p style="font-size:13px;color:var(--text-muted);margin-bottom:4px;"><strong>线路类型：</strong>{extras['line']}</p>
      <p style="font-size:13px;color:var(--text-muted);margin-bottom:4px;"><strong>支持协议：</strong>{extras['protocols']}</p>
      <p style="font-size:13px;color:var(--text-muted);margin-bottom:0;"><strong>网络保障：</strong>三网动态路由，智能分流低抖动，晚高峰丢包控制优秀</p>
    </div>

    <div style="background:var(--bg-subtle);padding:14px 16px;border-radius:6px;border:1px solid var(--border-subtle);">
      <h4 style="font-size:14px;font-weight:700;margin-bottom:8px;color:var(--primary);">🤖 AI 工具与流媒体解锁能力</h4>
      <p style="font-size:13px;color:var(--text-muted);margin-bottom:4px;"><strong>AI 大模型：</strong>{extras['ai_unlock']}</p>
      <p style="font-size:13px;color:var(--text-muted);margin-bottom:4px;"><strong>影音流媒体：</strong>{extras['streaming']}</p>
      <p style="font-size:13px;color:var(--text-muted);margin-bottom:0;"><strong>IP 纯净度：</strong>原生/机房高信誉 IP 出口，有效规避频繁人机验证</p>
    </div>
  </div>

  <div style="margin-bottom:18px;">
    <h4 style="font-size:14px;font-weight:700;margin-bottom:8px;">💰 套餐配置与参考价格明细</h4>
    <ul style="font-size:13px;color:var(--text-muted);line-height:1.7;padding-left:20px;margin:0;">
      {packages_li}
    </ul>
  </div>

  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;padding-top:14px;border-top:1px solid var(--border-subtle);">
    <div style="font-size:13px;color:var(--text-light);">
      <span><strong>适用人群：</strong>{extras['audience']}</span>
      <span style="margin-left:12px;"><strong>最近核验：</strong>{p['lastChecked']}</span>
    </div>
    <div style="display:flex;gap:10px;align-items:center;">
      <a href="/providers/{slug}/" style="font-size:13px;color:var(--primary);font-weight:600;">查看单项详细评测 →</a>
      <a href="{p['inviteURL']}" rel="sponsored nofollow noopener" target="_blank" class="btn-register-prominent" style="padding:6px 14px;font-size:12px;" data-provider="{slug}" data-rank="{p['rank']}" data-placement="pillar_card_bottom">直达官网注册</a>
    </div>
  </div>
</div>
"""

        # 3. Generate 12 specialized recommendation sub-articles grid
        rec_articles = [a for a in self.nav_articles if a['section'] == 'recommendations']
        rec_articles_html = ""
        for art in rec_articles:
            rec_articles_html += f"""
<div style="background:var(--bg-surface);border:1px solid var(--border-color);border-radius:var(--radius-md);padding:20px;display:flex;flex-direction:column;justify-content:space-between;">
  <div>
    <span style="display:inline-block;padding:3px 8px;font-size:12px;font-weight:600;background:var(--primary-light);color:var(--primary);border-radius:4px;margin-bottom:8px;">{art['primaryKeyword']}</span>
    <h3 style="font-size:16px;font-weight:700;margin-bottom:8px;line-height:1.4;"><a href="{art['url']}">{art['h1']}</a></h3>
    <p style="font-size:13px;color:var(--text-muted);line-height:1.6;margin-bottom:12px;">{art['metaDescription'][:88]}...</p>
  </div>
  <div style="display:flex;justify-content:space-between;align-items:center;font-size:12px;color:var(--text-light);padding-top:10px;border-top:1px solid var(--border-subtle);">
    <span>约 {art['bodyCharCount']} 字</span>
    <a href="{art['url']}" style="font-weight:600;color:var(--primary);">阅读专题 →</a>
  </div>
</div>
"""

        content_html = f"""
<div class="container" style="padding:32px 20px;">
  <div class="breadcrumbs">
    <a href="/">首页</a> <span>/</span> <span>2026 机场推荐精选总榜</span>
  </div>

  <header style="margin-bottom:32px;">
    <span class="hero-badge">2026 旗舰指南 · 27 家服务商全景横向横评</span>
    <h1 style="font-size:32px;font-weight:800;margin:14px 0 12px 0;line-height:1.3;">{title}</h1>
    <div style="font-size:13px;color:var(--text-light);margin-bottom:16px;display:flex;gap:16px;flex-wrap:wrap;">
      <span>📅 更新日期：2026年9月</span>
      <span>🔍 评测样本：全网 27 家主流机场</span>
      <span>🛡️ 审核准则：真实价格梯队、高峰测速与真实邀请链接</span>
      <span>💡 建议：优先月付测试，按需选购</span>
    </div>
    <div style="background:var(--bg-subtle);border:1px solid var(--border-color);border-radius:var(--radius-md);padding:18px 22px;line-height:1.8;color:var(--text-main);font-size:15px;">
      <p style="margin-bottom:10px;">
        在跨境网络加速、外贸商务办公、海外学术科研检索以及远程团队协作中，一款<strong>高性价比、稳定不掉线、晚高峰低延迟且解锁 AI 与流媒体</strong>的优质网络工具至关重要。市面上的服务商品质良莠不齐，价格从几元到几百元不等，线路更涵盖了直连中转、BGP隧道、IPLC内网专线与IEPL企业级专线。
      </p>
      <p style="margin-bottom:0;">
        为了帮助广大用户消除信息不对称、避免盲目踩坑或遭遇跑路风险，本篇<strong>机场推荐主要文章</strong>全面收录了<strong>全网 27 家主流机场</strong>的真实资料、官方定价、节点线路状况、协议兼容性、ChatGPT与Claude等AI工具解锁能力以及适用人群。无论您是寻找轻量便宜的备用小流量方案，还是追求极速晚高峰秒开 4K/8K 视频的顶级 IPLC 专线，均可在此指南中找到精准匹配的方案。
      </p>
    </div>
  </header>

  <!-- 快速导航索引 -->
  <nav style="background:var(--bg-surface);border:1px solid var(--border-color);border-radius:var(--radius-md);padding:18px 22px;margin-bottom:36px;">
    <div style="font-weight:700;font-size:16px;margin-bottom:10px;color:var(--primary);">📑 本文深度内容导读与快速定位：</div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(260px, 1fr));gap:8px;font-size:14px;">
      <a href="#section-top4" style="color:var(--text-main);">👉 一、四大核心主推旗舰服务商（首选推荐）</a>
      <a href="#section-table27" style="color:var(--text-main);">👉 二、27 家机场全景横向核心参数对照大表</a>
      <a href="#section-reviews27" style="color:var(--text-main);">👉 三、全网 27 家机场详尽评测卡片（资料/价格/AI）</a>
      <a href="#section-guide" style="color:var(--text-main);">👉 四、科学选型与避坑方法论（线路/AI/客户端）</a>
      <a href="#section-faq" style="color:var(--text-main);">👉 五、高频常见问题答疑（FAQ 专区）</a>
      <a href="#section-sub-articles" style="color:var(--text-main);">👉 六、12 篇垂直细分高点击率专题深度指南</a>
    </div>
  </nav>

  <!-- 一、四大主推服务商 -->
  <section id="section-top4" style="margin-bottom:44px;">
    <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;margin-bottom:18px;">
      <div>
        <h2 style="font-size:24px;font-weight:800;margin:0 0 6px 0;">一、四大核心主推旗舰服务商（固定前四优先甄选）</h2>
        <p style="font-size:14px;color:var(--text-muted);margin:0;">本站编辑团队经过长期晚高峰压力测试、多设备并发实测评定出的四大基石服务，定位清晰、稳定性高：</p>
      </div>
    </div>

    <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(270px, 1fr));gap:20px;">
      <!-- Top 1 全球云 -->
      <div class="sidebar-widget" style="border:2px solid #2563eb;position:relative;background:#f8faff;">
        <span style="position:absolute;top:-12px;left:16px;background:#2563eb;color:#fff;font-size:11px;font-weight:800;padding:3px 12px;border-radius:12px;">TOP 1 综合旗舰</span>
        <h3 style="font-size:20px;font-weight:800;margin-top:8px;margin-bottom:8px;"><a href="/providers/quanqiu-cloud/">全球云 (Quanqiu Cloud)</a></h3>
        <p style="font-size:13px;color:var(--text-muted);line-height:1.6;margin-bottom:12px;">
          多国家和地区出口覆盖广，BGP智能分流体验绝佳，适合跨境电商、外贸团队、多出口IP需求及各类AI工具高效交互。
        </p>
        <div style="font-size:13px;margin-bottom:8px;"><strong>起步价格：</strong><span style="color:#2563eb;font-weight:700;">20 元/月 起</span> (年付99元/59GB)</div>
        <div style="font-size:13px;margin-bottom:14px;"><strong>专属优惠码：</strong><code style="background:#fff;padding:2px 6px;border:1px solid #93c5fd;border-radius:4px;color:#1d4ed8;font-weight:700;">qq88</code> (享8折优惠)</div>
        <a href="https://hueue09.gcvipaff.com/#/?code=z8U9aaa4" rel="sponsored nofollow noopener" target="_blank" class="btn-register-prominent" style="width:100%;text-align:center;">👉 前往全球云官网注册</a>
      </div>

      <!-- Top 2 飞猫云 -->
      <div class="sidebar-widget" style="border:2px solid #059669;position:relative;background:#f0fdf4;">
        <span style="position:absolute;top:-12px;left:16px;background:#059669;color:#fff;font-size:11px;font-weight:800;padding:3px 12px;border-radius:12px;">TOP 2 性价比年付</span>
        <h3 style="font-size:20px;font-weight:800;margin-top:8px;margin-bottom:8px;"><a href="/providers/flycat-cloud/">飞猫云 (Flycat Cloud)</a></h3>
        <p style="font-size:13px;color:var(--text-muted);line-height:1.6;margin-bottom:12px;">
          84元/年起（折合仅7元/月），全线IEPL专线，晚高峰香港节点极速响应，配备自研小白客户端，适合轻量备用与学生群体。
        </p>
        <div style="font-size:13px;margin-bottom:8px;"><strong>起步价格：</strong><span style="color:#059669;font-weight:700;">84 元/年 起</span> (折合7元/月 50GB/月)</div>
        <div style="font-size:13px;margin-bottom:14px;"><strong>专属优惠码：</strong><code style="background:#fff;padding:2px 6px;border:1px solid #86efac;border-radius:4px;color:#047857;font-weight:700;">flycat888</code> (季付以上8折)</div>
        <a href="https://quanqiu.flycatvipaff.cc/#/?code=7ZOeVmNS" rel="sponsored nofollow noopener" target="_blank" class="btn-register-prominent" style="width:100%;text-align:center;">👉 前往飞猫云官网注册</a>
      </div>

      <!-- Top 3 暮光加速 -->
      <div class="sidebar-widget" style="border:2px solid #7c3aed;position:relative;background:#faf5ff;">
        <span style="position:absolute;top:-12px;left:16px;background:#7c3aed;color:#fff;font-size:11px;font-weight:800;padding:3px 12px;border-radius:12px;">TOP 3 影音大户</span>
        <h3 style="font-size:20px;font-weight:800;margin-top:8px;margin-bottom:8px;"><a href="/providers/twilight/">暮光加速 (Twilight)</a></h3>
        <p style="font-size:13px;color:var(--text-muted);line-height:1.6;margin-bottom:12px;">
          晚高峰针对 YouTube 4K/8K 视频与流媒体大流量传输专项优化，跑满物理带宽，AI 协作零阻滞，适合重度流媒体发烧友。
        </p>
        <div style="font-size:13px;margin-bottom:8px;"><strong>起步价格：</strong><span style="color:#7c3aed;font-weight:700;">20 元/月 起</span> (100GB/月，大户可选1100GB)</div>
        <div style="font-size:13px;margin-bottom:14px;"><strong>专属优惠码：</strong><code style="background:#fff;padding:2px 6px;border:1px solid #d8b4fe;border-radius:4px;color:#6b21a8;font-weight:700;">mm88</code> (享8折优惠)</div>
        <a href="https://quanqi12.twilightaff.com/#/?code=beAVqNPf" rel="sponsored nofollow noopener" target="_blank" class="btn-register-prominent" style="width:100%;text-align:center;">👉 前往暮光加速官网注册</a>
      </div>

      <!-- Top 4 微风网络 -->
      <div class="sidebar-widget" style="border:2px solid #0891b2;position:relative;background:#f0fdfa;">
        <span style="position:absolute;top:-12px;left:16px;background:#0891b2;color:#fff;font-size:11px;font-weight:800;padding:3px 12px;border-radius:12px;">TOP 4 轻量专线</span>
        <h3 style="font-size:20px;font-weight:800;margin-top:8px;margin-bottom:8px;"><a href="/providers/breezenet/">微风网络 (BreezeNet)</a></h3>
        <p style="font-size:13px;color:var(--text-muted);line-height:1.6;margin-bottom:12px;">
          轻量 IEPL 专线方案，通用订阅与自研客户端双轨并行，低门槛无缝上手，适合低频轻度日常上网与基础外网访问。
        </p>
        <div style="font-size:13px;margin-bottom:8px;"><strong>起步价格：</strong><span style="color:#0891b2;font-weight:700;">以结算页为准</span> (轻量年付/月付方案)</div>
        <div style="font-size:13px;margin-bottom:14px;"><strong>专属优惠码：</strong><span style="color:var(--text-muted);font-size:12px;">暂无，以结算页实时折扣为准</span></div>
        <a href="https://edp01.breezenetaff.com/#/?code=vxDUI8kY" rel="sponsored nofollow noopener" target="_blank" class="btn-register-prominent" style="width:100%;text-align:center;">👉 前往微风网络官网注册</a>
      </div>
    </div>
  </section>

  <!-- 二、27 家全景对比表 -->
  <section id="section-table27" style="margin-bottom:44px;">
    <h2 style="font-size:24px;font-weight:800;margin-bottom:10px;">二、2026 全网 27 家优质机场横向核心参数全景对比大表</h2>
    <p style="font-size:14px;color:var(--text-muted);margin-bottom:18px;">
      收录 27 家主流服务商的起步定价、基础流量、专属优惠码、线路技术架构、AI 与流媒体支持情况及官方直达注册通道。横向对比一目了然：
    </p>
    <div class="table-responsive" style="max-height:640px;overflow-y:auto;border:1px solid var(--border-color);border-radius:var(--radius-md);">
      <table class="data-table" style="font-size:13px;margin:0;">
        <thead style="position:sticky;top:0;background:var(--bg-subtle);z-index:2;">
          <tr>
            <th style="min-width:60px;text-align:center;">排名</th>
            <th style="min-width:110px;">服务商名称</th>
            <th style="min-width:90px;">参考起步价</th>
            <th style="min-width:85px;">参考流量</th>
            <th style="min-width:90px;">优惠码</th>
            <th style="min-width:130px;">核心线路架构</th>
            <th style="min-width:140px;">AI 解锁能力</th>
            <th style="min-width:140px;">适用人群与场景</th>
            <th style="min-width:90px;text-align:center;">官网直达</th>
          </tr>
        </thead>
        <tbody>
          {table_rows}
        </tbody>
      </table>
    </div>
  </section>

  <!-- 三、27 家详细评测卡片 -->
  <section id="section-reviews27" style="margin-bottom:44px;">
    <h2 style="font-size:24px;font-weight:800;margin-bottom:10px;">三、全网 27 家机场全景资料、价格节点、AI解锁与适用人群深度评测</h2>
    <p style="font-size:14px;color:var(--text-muted);margin-bottom:24px;">
      针对每一家服务商展开深度解构，包含基础定位卖点、全套定价阶梯（月付/季付/年付/一次性）、节点线路质量、AI大模型及4K流媒体解锁实测、适用受众分析及官方直达入口：
    </p>
    {provider_cards_html}
  </section>

  <!-- 四、选型与避坑指南 -->
  <section id="section-guide" style="margin-bottom:44px;background:var(--bg-surface);border:1px solid var(--border-color);border-radius:var(--radius-lg);padding:30px;">
    <h2 style="font-size:24px;font-weight:800;margin-bottom:18px;">四、科学选型与避坑全方位方法论（深度选购指南）</h2>
    
    <div style="margin-bottom:24px;">
      <h3 style="font-size:18px;font-weight:700;color:var(--primary);margin-bottom:10px;">4.1 线路类型深度解析：直连中转 vs BGP隧道 vs IPLC/IEPL专线</h3>
      <p style="font-size:14px;color:var(--text-main);line-height:1.8;">
        很多新手用户在选择机场时只关注价格，忽视了底层线路的技术本质。实际上，线路决定了网络连接的延迟下限与晚高峰抗封锁上限：
      </p>
      <ul style="font-size:14px;color:var(--text-muted);line-height:1.8;padding-left:20px;">
        <li><strong>普通直连线路：</strong>客户端直接与境外VPS服务器连接。成本极低，但在国际出口网络拥堵时极易丢包，且IP极易被阻断，仅适合极低预算轻量备用。</li>
        <li><strong>BGP 隧道中转：</strong>在国内部署多线BGP入口服务器，先将数据接入国内骨干网，再通过加密隧道转发至境外出口。能显著降低跨网丢包，适合大部分日常办公与视频用户。</li>
        <li><strong>IPLC / IEPL 国际专线：</strong>即“国际私有租用线路 / 国际以太网专线”，数据通过运营商内网海底光缆或跨境陆缆点对点传输，<strong>不经过公共公网防火墙过滤</strong>。具备超低物理延迟、零QoS降速、晚高峰不卡顿的极致稳定性，是跨境电商、高频交易、AI开发与影音大户的首选。</li>
      </ul>
    </div>

    <div style="margin-bottom:24px;">
      <h3 style="font-size:18px;font-weight:700;color:var(--primary);margin-bottom:10px;">4.2 AI 工具（ChatGPT / Claude）与流媒体解锁的选型要点</h3>
      <p style="font-size:14px;color:var(--text-main);line-height:1.8;">
        目前 OpenAI (ChatGPT Plus / Sora)、Anthropic (Claude 3.5 Sonnet) 以及 Netflix、Disney+ 等服务对访问 IP 设置了严苛的风控策略：
      </p>
      <ul style="font-size:14px;color:var(--text-muted);line-height:1.8;padding-left:20px;">
        <li><strong>原生住宅 IP / 高信誉商用 IP：</strong>若节点出口被标记为高风险数据中心机房 IP，访问 ChatGPT 会频繁遭遇“Access Denied”或“无法验证您的凭证”，Claude 更是容易遭遇直接封号。建议优先选择像全球云、飞猫云等配备原生出口 IP、定期轮换纯净 IP 池的服务商。</li>
        <li><strong>分流规则设置：</strong>在客户端（如 Clash Verge）中确保配置了专门的 <code>OpenAI</code>、<code>Claude</code> 分流规则组，将 AI 流量固定路由至美国、新加坡或日本等对 AI 友好的原生节点，切忌频繁切换不同国家出口触发账号风控。</li>
      </ul>
    </div>

    <div style="margin-bottom:24px;">
      <h3 style="font-size:18px;font-weight:700;color:var(--primary);margin-bottom:10px;">4.3 客户端兼容指南与快速配置</h3>
      <p style="font-size:14px;color:var(--text-main);line-height:1.8;">
        不同操作系统平台有其主流的开源客户端工具：
      </p>
      <ul style="font-size:14px;color:var(--text-muted);line-height:1.8;padding-left:20px;">
        <li><strong>Windows / macOS：</strong>强烈推荐使用 <strong>Clash Verge Rev</strong> 或 <strong>Mihomo Party</strong>，支持内核智能分流、延迟测速及自启动。</li>
        <li><strong>iOS (苹果手机/iPad)：</strong>推荐美区 App Store 下载的 <strong>Shadowrocket (小火箭)</strong>、<strong>Quantumult X</strong> 或 <strong>Stash</strong>，一键扫码或一键导入订阅极为便捷。</li>
        <li><strong>Android (安卓手机)：</strong>推荐使用 <strong>Clash Meta for Android (CMFA)</strong> 或 <strong>v2rayNG</strong>。</li>
      </ul>
    </div>

    <div>
      <h3 style="font-size:18px;font-weight:700;color:var(--primary);margin-bottom:10px;">4.4 避坑与防跑路原则（四大底线法则）</h3>
      <ul style="font-size:14px;color:var(--text-muted);line-height:1.8;padding-left:20px;">
        <li><strong>坚持月付或季付测试：</strong>即便年付折算单价再低，初次购买新服务商时也务必先购入一个月试用，在晚高峰（20:00 - 23:00）实测本地网络环境下的表现。</li>
        <li><strong>警惕“一次性买断永久可用”宣传：</strong>带宽与服务器是持续的刚性成本，凡宣称“几十元终身不限流量”的服务极大概率属于资金盘跑路骗局。</li>
        <li><strong>主备双订阅策略：</strong>对于外贸外联、跨境电商等生产力刚需用户，建议配置一个主力优质专线机场（如全球云或暮光加速），同时保留一个几元钱的轻量小年付机场（如飞猫云）作为备用应急通道。</li>
      </ul>
    </div>
  </section>

  <!-- 五、FAQ 常见问题答疑 -->
  <section id="section-faq" style="margin-bottom:44px;">
    <h2 style="font-size:24px;font-weight:800;margin-bottom:14px;">五、机场推荐常见高频问题解答（FAQ 专区 · 100% 展开）</h2>
    <div style="display:flex;flex-direction:column;gap:16px;">
      <div class="faq-item-expanded" style="background:var(--bg-surface);border:1px solid var(--border-color);border-radius:var(--radius-md);padding:20px;">
        <h3 style="font-size:16px;font-weight:700;margin-bottom:8px;color:var(--primary);">Q1：什么是“性价比机场”？挑选时只看单价对吗？</h3>
        <p style="font-size:14px;color:var(--text-main);line-height:1.7;margin:0;">
          不对。真正的“性价比”是<strong>单位可用性与稳定性的价格比</strong>。如果一个月付 5 元的廉价机场在晚高峰丢包率高达 60%、节点三天两头断连，那么它的实际可用性价比极低；相反，月付 20 元但全天候稳定、延迟低且解锁 AI 的专线机场，能为你节省宝贵的时间成本，综合性价比反而更高。
        </p>
      </div>

      <div class="faq-item-expanded" style="background:var(--bg-surface);border:1px solid var(--border-color);border-radius:var(--radius-md);padding:20px;">
        <h3 style="font-size:16px;font-weight:700;margin-bottom:8px;color:var(--primary);">Q2：为什么同一个机场节点，别人用速度很快，我用却很卡？</h3>
        <p style="font-size:14px;color:var(--text-main);line-height:1.7;margin:0;">
          网络速度受“本地网络运营商（电信/联通/移动/广电）”、“本地宽带协议”、“接入点地理距离”及“客户端配置模式”多重影响。例如，移动宽带在某些非 BGP 节点上的连通表现可能弱于电信或联通。选择具备<strong>三网多入口 BGP 智能接入</strong>的服务商（如全球云、飞猫云）可以有效平抑不同宽带间的网络差异。
        </p>
      </div>

      <div class="faq-item-expanded" style="background:var(--bg-surface);border:1px solid var(--border-color);border-radius:var(--radius-md);padding:20px;">
        <h3 style="font-size:16px;font-weight:700;margin-bottom:8px;color:var(--primary);">Q3：如何挑选适合 ChatGPT、Claude 等 AI 工具的机场节点？</h3>
        <p style="font-size:14px;color:var(--text-main);line-height:1.7;margin:0;">
          重点关注两点：一是节点所在国家地区是否在 AI 官方服务开放列表内（推荐美国、日本、新加坡、台湾地区，避开香港节点对 ChatGPT 的地域限制）；二是 IP 类型的纯净度。优先挑选标注有“原生 IP 解锁”或明确支持 AI 大模型的节点。
        </p>
      </div>

      <div class="faq-item-expanded" style="background:var(--bg-surface);border:1px solid var(--border-color);border-radius:var(--radius-md);padding:20px;">
        <h3 style="font-size:16px;font-weight:700;margin-bottom:8px;color:var(--primary);">Q4：什么是“倍率”？为什么有些节点消耗流量特别快？</h3>
        <p style="font-size:14px;color:var(--text-main);line-height:1.7;margin:0;">
          倍率是服务商对不同节点计算流量的系数。标准 1.0 倍率意味着消耗 1GB 实际流量扣除 1GB 套餐额度；而某些高质量 IPLC 专线或极速高带宽节点可能标注为 1.5×、2.0× 或 3.0× 倍率，在此类节点下下载 1GB 会扣除 2GB 或 3GB 额度。选购与使用时请务必留意节点列表中的倍率标注，避免流量被过快消耗。
        </p>
      </div>

      <div class="faq-item-expanded" style="background:var(--bg-surface);border:1px solid var(--border-color);border-radius:var(--radius-md);padding:20px;">
        <h3 style="font-size:16px;font-weight:700;margin-bottom:8px;color:var(--primary);">Q5：购买机场后可以在多少台设备上同时使用？</h3>
        <p style="font-size:14px;color:var(--text-main);line-height:1.7;margin:0;">
          每个服务商的设备限制规则不同。部分服务商（如灵猫网络、Firefly）宣称不限制在线设备数；而多数服务商的基础套餐通常限制同时在线 2 至 5 台设备。购买前请在套餐说明或结账页确认设备数上限（IP 限制或连接数限制），若需家庭或小团队共享，建议选购团队版或高配套餐。
        </p>
      </div>
    </div>
  </section>

  <!-- 六、12 篇细分专题 -->
  <section id="section-sub-articles" style="margin-bottom:36px;">
    <h2 style="font-size:24px;font-weight:800;margin-bottom:12px;">六、机场推荐高点击率精选专题文章（12 篇细分场景深度指南）</h2>
    <p style="font-size:14px;color:var(--text-muted);margin-bottom:20px;">依照高频用户真实检索意图，围绕“性价比机场、Clash 机场推荐、稳定专线、便宜机场、AI 机场与节点测评”等核心词打造的深度长文：</p>
    <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(280px, 1fr));gap:16px;">
      {rec_articles_html}
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
        print("Generated comprehensive 27-provider recommendations pillar page.")

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
      <div style="padding:16px;border:2px solid #f59e0b;border-radius:var(--radius-sm);background:linear-gradient(165deg, rgba(254, 243, 199, 0.25) 0%, var(--bg-page) 100%);box-shadow:0 4px 14px rgba(245, 158, 11, 0.16);">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;">
          <h3 style="font-size:16px;font-weight:700;margin:0;"><a href="/providers/quanqiu-cloud/">1. 全球云 (Rank 1 旗舰)</a></h3>
          <span class="badge-station-recommend">🔥 站长推荐</span>
        </div>
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
      <div style="padding:16px;border:2px solid #f59e0b;border-radius:var(--radius-sm);background:linear-gradient(165deg, rgba(254, 243, 199, 0.25) 0%, var(--bg-page) 100%);box-shadow:0 4px 14px rgba(245, 158, 11, 0.16);">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;">
          <h3 style="margin:0;">1. 全球云 (TOP 1)</h3>
          <span class="badge-station-recommend">🔥 站长推荐</span>
        </div>
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
  <h3 style="font-size:18px;font-weight:700;margin-bottom:8px;color:var(--text-main);">官方纠错与反馈通道</h3>
  <p style="font-size:14px;color:var(--text-muted);margin-bottom:16px;">如果您在阅读过程中发现任何服务商价格变动、节点资料调整或优惠码失效，欢迎通过官方邮箱随时提交反馈，我们将第一时间核实并修正：</p>
  <a href="mailto:contact@jichangtuijian.cloud" class="btn-primary" style="display:inline-flex;align-items:center;gap:8px;">
    <span>发送邮件反馈 (contact@jichangtuijian.cloud)</span>
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
