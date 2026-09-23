# 机场推荐云 (jichangtuijian.cloud)

面向中文新手的机场服务资料、上手入口与场景化对比纯静态知识库与推荐站点。
以公开核验的方案说明、透明对比维度、100 题 FAQ 知识库和系统化教程为主，为读者提供带核验日期的中立选型参考，不夸大宣传、不制造虚假案例或绝对性能背书。

---

## 快速导航与技术特性

- **官方域名**：`https://jichangtuijian.cloud`
- **品牌名称**：机场推荐云 / jichangtuijian.cloud
- **定位**：从了解方案到配置订阅，清楚开始每一步
- **技术框架**：零外部依赖的高性能 Python 3 静态生成引擎（Universal 科技极简主题设计，纯静态输出至 `public/`）
- **核心数据层**：解耦至 `data/site-seo-profile.json`，支持一键批量替换全站关键词与导航
- **收录服务**：27 家独立机场全量测评（单篇净中文 800~1200 字）
- **商业主推**：严格固化前四名服务商顺序及专属邀请链接与优惠码（全球云 TOP 1、飞猫云 TOP 2、暮光加速 TOP 3、微风网络 TOP 4）
- **知识库体系**：100 个高频 FAQ 问答矩阵（严格满足 9 大配额，支持分页抓取）
- **合规隔离**：内置参考源黑名单扫描，彻底隔离第三方参考博客名称（二毛、猫梦、Gaterank 等）与来源句式

---

## 常用命令

### 1. 生产构建 (Build)
```bash
python3 builder/build.py
```
一键将所有页面、XML Sitemap、RSS、Robots.txt 及静态资源渲染至 `public/` 目录。

### 2. 本地开发预览 (Preview)
```bash
python3 -m http.server 8080 --directory public
```
启动后在浏览器访问 `http://localhost:8080` 即可实时预览全站页面。

### 3. 全自动化 SEO 与合规性验收 (Verify)
```bash
python3 builder/verify_seo.py
```
运行完整的 36 项自动化测试套件：
- 静态产物完整性（HTML、sitemap.xml、robots.txt、rss.xml、404 等）
- Sitemap 绝对 URL 与无坏链检测
- 固定前四名服务商排序、专属邀请链接与 `rel="sponsored nofollow noopener"` 属性
- 27 家独立测评页存在性与唯一 Canonical 检查
- 参考源隔离黑名单与内部字段隔离扫描（0 命中）
- 汉字正文字数严格校验（800~1200 净中文字符）
- 100 题 FAQ 9 大配额（18/14/10/10/8/14/10/8/8）与分页可抓取性
- 首页 Hero（90~160 字）与页脚（70~130 字）关键词字符数边界
- HTML 规范性（单 H1、Title、Description、HTTPS Canonical、JSON-LD）

---

## 维护与更新指南

### 1. 新增或更新服务商数据
- 编辑 `data/providers.json`；
- 修改对应服务商的 `priceFrom`、`trafficFrom`、`packages`、`coupon`、`inviteURL` 或 `lastChecked`；
- 运行 `python3 scripts/generate_content_database.py` 重新生成测评正文与 `docs/provider-review-matrix.md`；
- 运行 `python3 builder/build.py` 重新编译全站。

### 2. 批量替换关键词与导航层
本站遵循 [docs/seo-profile-replacement-contract.md](docs/seo-profile-replacement-contract.md) 替换契约：
- 编辑 `data/site-seo-profile.json`，替换 `primaryKeywords`、`heroKeywords`、`footerKeywords` 或 `navigationItems`；
- 重新运行 `scripts/generate_nav_articles.py` 与 `builder/build.py`；
- 契约保证：无论如何换词，前四名服务顺序与原始邀请链接始终完整保留。

### 3. 字符数计算与排除规则
- **统计标准**：仅统计文章正文主体中的净汉字字符数（`len(re.findall(r'[\u4e00-\u9fa5]', body))`）；
- **排除区域**：页眉、页脚、主导航、面包屑、侧边栏、推荐榜卡片、HTML 标签、代码块、免责声明与相关推荐链接不计入正文字数。
- **正文要求**：所有独立测评页与导航文章必须严格保持在 800 至 1200 净中文字符之间。

### 4. 分析统计与事件埋点
在 `src/static/js/main.js` 中已预留隐私友好的第一方事件监听：
- `provider_detail_view`：用户访问机场独立测评页触发，记录 `provider` 与 `page_path`；
- `affiliate_click`：点击带 `rel="sponsored"` 的邀请按钮时触发，记录 `provider`、`rank`、`placement` 与 `page_path`；
- `coupon_copy`：点击一键复制优惠码按钮时触发，记录 `provider` 与 `coupon`。
- **接入与关闭**：若需接入 Google Analytics 4，只需在 `<head>` 中填入标准 gtag 代码，`main.js` 会自动调用 `gtag('event')` 分发；未接入时脚本自动降级，绝不影响网站正常运行。

---

## 部署上线指南

本项目为标准的纯静态站点（Pure Static Site），可直接部署到任何现代静态托管平台：

### 1. Cloudflare Pages
- **Build command**: `python3 builder/build.py`
- **Build output directory**: `public`

### 2. Vercel / Netlify
- **Build command**: `python3 builder/build.py`
- **Output directory**: `public`

### 3. GitHub Pages
- 将构建后的 `public/` 目录推送到 `gh-pages` 分支或在 GitHub Actions 中配置发布步骤。

### 4. Nginx 自建服务器
```nginx
server {
    listen 443 ssl http2;
    server_name jichangtuijian.cloud;
    root /var/www/jichangtuijian.cloud/public;
    index index.html;
    error_page 404 /404.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

---

## 核心文档索引

- [docs/site-seo-profile.json](docs/site-seo-profile.json): 全站单一 SEO 配置源
- [docs/seo-profile-replacement-contract.md](docs/seo-profile-replacement-contract.md): 关键词与导航替换规范契约
- [docs/keyword-map.md](docs/keyword-map.md): 关键词聚类与意图分析
- [docs/keyword-coverage.csv](docs/keyword-coverage.csv): 关键词全量覆盖与落地页映射表
- [docs/reference-publisher-blocklist.md](docs/reference-publisher-blocklist.md): 参考发布者名称隔离黑名单
- [docs/provider-review-matrix.md](docs/provider-review-matrix.md): 27 家服务商测评全景矩阵
- [docs/navigation-content-matrix.md](docs/navigation-content-matrix.md): 导航高质量文章矩阵
- [docs/faq-keywords-100.csv](docs/faq-keywords-100.csv): 100 题 FAQ 长尾问答数据集
- [docs/faq-content-matrix.md](docs/faq-content-matrix.md): 100 题 FAQ 规划矩阵
- [docs/content-plan.md](docs/content-plan.md): 60 个后续发布选题路线图
- [docs/publishing-guide.md](docs/publishing-guide.md): 内容发布与更新操作手册
- [docs/search-console-setup.md](docs/search-console-setup.md): Search Console / Bing / IndexNow 接入说明
- [docs/launch-checklist.md](docs/launch-checklist.md): 网站上线最终核对清单
