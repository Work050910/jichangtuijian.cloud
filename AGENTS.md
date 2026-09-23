# AGENTS.md - 智能助手与维护代理工作区约定

本文档面向后续接手本项目维护、扩充内容或升级架构的 AI 智能代理（Google Antigravity / Codex / Claude 等）。在对本代码库执行任何修改前，请务必阅读并严格遵守以下准则：

## 一、不可动摇的商业与合规底线

1. **固定前四名服务商顺序**：
   - Rank 1：全球云 (`quanqiu-cloud`)
   - Rank 2：飞猫云 (`flycat-cloud`)
   - Rank 3：暮光加速 (`twilight`)
   - Rank 4：微风网络 (`breezenet`)
   - **绝对不可变更前四名展示排序**，无论任何横向对比、推荐榜单、首页模块还是文章推荐，都必须严格执行该顺序。

2. **原始邀请链接与代码保护**：
   - 全球云：`https://hueue09.gcvipaff.com/#/?code=z8U9aaa4`
   - 飞猫云：`https://quanqiu.flycatvipaff.cc/#/?code=7ZOeVmNS`
   - 暮光加速：`https://quanqi12.twilightaff.com/#/?code=beAVqNPf`
   - 微风网络：`https://edp01.breezenetaff.com/#/?code=vxDUI8kY`
   - 必须保留原始邀请链接及其 `code` 参数，不得替换为官网首页或自定义跳转地址。
   - 所有外链必须包含 `rel="sponsored nofollow noopener"` 属性。

3. **参考发布者严格隔离（四 B 规则）**：
   - 严禁将参考博客、评测站或竞品站点的名称（如二毛博客、猫梦博客、Gaterank、星维机场、三毛机场、一毛机场、一份机场、机场宝等）输出至公开页面的 HTML、JSON-LD、Meta、Sitemap 或 RSS。
   - 严禁使用“根据某某博客”“某评测站称”“资料来自某博客”等来源句式。
   - 构建后必须运行 `python3 builder/verify_seo.py` 确保黑名单检测 0 命中。

4. **合规表达与中立语境**：
   - 严禁使用“翻墙”“绕过监管”“突破封锁”“保证解锁”“永久稳定”“100%可用”“全网最快”“闭眼买”等违规营销或绝对化宣传用语。
   - 在中立网络工具、远程办公、跨境业务连接、网络隐私和客户端兼容的语境下编写文章。

## 二、架构与数据层维护准则

1. **单一数据源**：
   - SEO 关键词、Hero 标语、页脚段落及导航配置完全集中于 `data/site-seo-profile.json`。
   - 批量替换关键词或导航时，遵循 `docs/seo-profile-replacement-contract.md` 规范。

2. **内容质量与字数标准**：
   - 独立测评文章与导航深度文章的**净中文字符数必须严格控制在 800 至 1200 字之间**。
   - FAQ 100 问答矩阵严格维护 9 大配额，不得随意删减。

3. **构建与测试闭环**：
   - 任何改动完成后，必须在终端执行：
     ```bash
     python3 builder/build.py
     python3 builder/verify_seo.py
     ```
   - 必须确保 36 项测试全部通过（0 Errors, 0 Warnings）后方可交付。
