# 模板编写指南

新增或修改模板时，遵守以下约束。

## 必备字段

- `id`
- `family`
- `label`
- `best_for`
- `input_modalities`
- `detection_signals`
- `anti_signals`
- `required_sections`
- `optional_sections`

以上为必备字段。另有可选字段：`notes`（与相邻模板的区分等补充说明）、`section_checklists`（按章节列 2-4 条可判定核对项，章节名须取自 `required_sections`，供生成后逐项核对；论文族模板已配置，新模板按需添加，不配则该字段缺省）。

## 编写规则

1. 先判断是否能复用现有模板，不要轻易新增。
2. 新模板必须归属一个明确模板族。
3. 重复章节优先放到 `section_library`，不要把同样说明复制到多个模板。
4. `required_sections` 只放该模板必须出现的章节。
5. `optional_sections` 放“看内容而定”的章节，不要为了完整而堆砌。
6. `detection_signals` 写用户语言和内容信号，不要只写抽象标签。
7. `anti_signals` 用来排除容易误判的相邻模板。
8. 变更模板时，同步检查 `registry.yaml`、`taxonomy.yaml` 和 `SKILL.md`。
9. 配置 `section_checklists` 时，每条必须是可判定的问题（能答"是/否"），不要写"内容应详实"这类不可核对的表述。

## 新增模板前自检

- 这个模板和现有模板的区别是否足够清晰
- 是否有稳定的识别信号
- 是否有明确的 fallback 或相邻替代模板
- 是否真的需要新模板，而不是给旧模板加可选章节
