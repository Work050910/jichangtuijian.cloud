# SEO 配置层批量替换与全站重构规范契约 (SEO Profile Replacement Contract)

## 1. 契约目标与背景
本项目将 SEO 关键词、Hero 标语、页脚品牌段落、导航栏目和文章规划完全解耦至单一配置层 `data/site-seo-profile.json` 与 `docs/site-seo-profile.json`。
当未来需要使用另一条万能提示词对全站关键词进行批量升级或整体换词时，必须严格通过本契约接口进行数据注入与重构，**严禁在代码库、模板或正文中执行盲目的全局字符串查找替换**。

## 2. 批量替换接口规范输入 (Input Schema)
替换指令必须提供以下完整结构体（缺失部分自动降级沿用默认或推导）：
- `newPrimaryKeywords`: 核心关键词列表（1~6 个）
- `newSecondaryKeywords`: 辅助关键词列表（5~15 个）
- `newLongTailKeywords`: 长尾关键词列表（10~30 个）
- `newHeroKeywords`: 首页首屏 Hero 关键词列表（覆盖至少 8 个）
- `newFooterKeywords`: 页脚关键词说明列表（覆盖 5~8 个）
- `newHeroSubtitleText`: 首屏 H1 下方 90~160 字的自然通顺说明句
- `newFooterParagraph1`: 页脚 70~130 字的网站长期覆盖主题说明
- `newNavigationItems`: 新导航数组（包含 label, url, primaryKeyword, supportingKeywords, articleSeeds, articleCount）
- `preservedAssets`:
  - 27 家服务商基础数据（全球云、飞猫云、暮光加速、微风网络等）
  - 前四名固定排名与展示顺序
  - 原始邀请链接与 code 参数（绝对不可变更）
  - 优惠码与折扣说明
  - 信任页面（关于、联系、编辑原则、评测方法、披露、隐私、条款、免责声明）

## 3. 标准替换执行流程 (Execution Procedure)
1. **读取旧配置**：读取 `data/site-seo-profile.json` 与当前所有产物 URL 列表。
2. **规范化与意图消歧**：去重、清理全半角与大小写，将旧活动词移入 `inactiveKeywords`。
3. **URL 301 映射检测**：若变更导航 URL，必须建立新旧 URL 映射表写入 Web 服务器重定向规则，禁止直接制造 404 或无脑重定向到首页。
4. **生成新数据层**：更新 `data/site-seo-profile.json` 并同步至 `docs/site-seo-profile.json`。
5. **模板与内容重编译**：
   - 首页 Hero 眉题、H1、首屏说明重新渲染
   - 导航 Header 与 Footer 自动读取新配置更新
   - 栏目落地页重新对齐新关键词
   - 重新生成 `docs/navigation-content-matrix.md` 与 `docs/keyword-coverage.csv`
6. **旧关键词残留扫描**：扫描公开 HTML 产物，确认 `inactiveKeywords` 没有无意义残留在公开正文或 Meta 中。
7. **全自动化验证**：运行 `python3 builder/verify_seo.py` 跑通全部 SEO、结构化数据、字符数与黑名单测试。

## 4. 安全红线
- 无论关键词如何替换，**严禁修改四大主推机场的前四名排序与原始邀请链接**。
- **严禁输出任何第三方参考博客（如二毛、猫梦、Gaterank等）名称与来源句式**。
