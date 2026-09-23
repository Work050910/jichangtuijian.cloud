# 机场推荐云内容发布与更新操作手册 (Publishing Guide)

## 一、新增或更新服务商流程
1. 在 `data/providers.json` 中找到对应服务商（或在末尾追加新服务商对象）。
2. 核实必填字段：`name`, `slug`, `rank`, `inviteURL`, `coupon`, `priceFrom`, `trafficFrom`, `summary`, `packages`, `suitableFor`, `lastChecked`。
3. 若属于前四名主推服务，确保 `rank` 保持 1~4 顺序，且邀请链接与参数原样保留。
4. 运行 `python3 builder/build.py` 重新生成静态页面，系统将自动生成对应的规范测评页与内链。

## 二、新增导航文章流程
1. 在 `scripts/generate_nav_articles.py` 或内容源中添加文章定义（标题、slug、主关键词、搜索意图）。
2. 文章正文净中文必须控制在 **800 至 1200 字之间**，严禁过短或超过上限。
3. 必须在正文中自然嵌入四项主推服务（全球云、飞猫云、暮光加速、微风网络）的专属推荐段落。
4. 重新构建并运行自动化校验脚本：`python3 builder/verify_seo.py`。

## 三、敏感词与参考源隔离自查
- 严禁将参考博客名称（二毛、猫梦、Gaterank等）写入任何可见文章。
- 严禁使用“翻墙”“100%永久可用”等合规风险词。
- 价格与优惠变动必须标注“以结算页为准”和最后核验时间。
