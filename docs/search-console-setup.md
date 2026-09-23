# Google Search Console 与 Bing Webmaster Tools 配置指南

## 一、Google Search Console 接入步骤
1. 访问 [Google Search Console](https://search.google.com/search-console)。
2. 选择“网址前缀”方式，输入：`https://jichangtuijian.cloud`。
3. 验证方式推荐使用 **HTML 标记** 或 **DNS TXT 记录**：
   - 若使用 HTML 标记，将验证代码填入 `data/site-seo-profile.json` 中的 `googleSiteVerification` 字段后重新构建。
4. 验证成功后，点击左侧“站点地图 (Sitemaps)”，提交：`https://jichangtuijian.cloud/sitemap.xml`。
5. 定期在“效果 (Performance)”菜单中导出真实的 Query、Clicks、Impressions 和 CTR，用于更新 `docs/keyword-coverage.csv`。

## 二、Bing Webmaster Tools 接入步骤
1. 访问 [Bing Webmaster Tools](https://www.bing.com/webmasters)。
2. 可直接通过导入 Google Search Console 账号一键同步站点所有权与站点地图。
3. 提交 `https://jichangtuijian.cloud/sitemap.xml`。

## 三、IndexNow 极速索引配置
1. 获得 IndexNow Key（可使用 32 位随机十六进制字符串）。
2. 将该密钥放置在网站根目录下，如 `public/{key}.txt`。
3. 每次发布新文章或更新服务时，通过 POST 请求推送更新 URL 至 `https://api.indexnow.org/indexnow`。
