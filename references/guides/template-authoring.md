# 模板编写指南

新增或修改模板时，遵守以下约束。

## 必备字段

每个模板以 `id`（形如 `family/name`）为 YAML 键，必备字段：

- `family`
- `name`
- `detection_signals`
- `required_sections`
- `optional_sections`
- `fallback`

以上 6 个字段为必备字段（现有 55 个模板全覆盖）。另有可选字段：`template_path`（product 族模板指向 `templates/` 下的产物模板，路径相对 `references/` 解析）、`notes`（与相邻模板的区分等补充说明）、`section_checklists`（按章节列 2-4 条可判定核对项，章节名须取自 `required_sections`，供生成后逐项核对；论文族模板已配置，新模板按需添加，不配则该字段缺省）。

## 编写规则

1. 先判断是否能复用现有模板，不要轻易新增。
2. 新模板必须归属一个明确模板族。
3. `required_sections` 只放该模板必须出现的章节。
4. `optional_sections` 放“看内容而定”的章节，不要为了完整而堆砌。
5. `detection_signals` 写用户语言和内容信号，不要只写抽象标签。
6. 与相邻模板容易误判时，用 `notes` 写明区分（现有 `product/weekly-monthly-report` 与 `business/weekly-monthly-report` 即如此）。
7. 变更模板时，同步检查 `registry.yaml`、`taxonomy.yaml` 和 `SKILL.md`。
8. 配置 `section_checklists` 时，每条必须是可判定的问题（能答"是/否"），不要写"内容应详实"这类不可核对的表述。

## 新增模板前自检

- 这个模板和现有模板的区别是否足够清晰
- 是否有稳定的识别信号
- 是否有明确的 fallback 或相邻替代模板
- 是否真的需要新模板，而不是给旧模板加可选章节
