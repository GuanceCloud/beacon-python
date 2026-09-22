# Beacon Python 自有贡献者

Beacon Python 保留完整的 OpenTelemetry Python Contrib 提交历史，以便通过 Git Log、Blame 和提交链接追溯代码来源。因此 GitHub 的 Contributors 图表可能同时列出上游作者，不能直接当作 Beacon 项目成员名单。本文件单独记录已核对身份的 GuanceCloud 下游与 Beacon 自有贡献者；不替代 Git 历史、许可证署名，也不表示仓库管理权限。

## 已核对名单

| GitHub 账号 | 历史 Git 署名 | 可追溯的下游贡献示例 |
| --- | --- | --- |
| [@lrwh](https://github.com/lrwh) | `liurui` | [旧 `gtrace` 发行包与 Profiling 实现](https://github.com/GuanceCloud/beacon-python/commit/55658637367c766ba3d2444d844e85881495370e)、[Beacon Python 工程初始化](https://github.com/GuanceCloud/beacon-python/commit/9fa18964fa1fc6470cac6b45d86d649ddadddd55) |

名单依据 GitHub 对上述提交作者账号的关联以及实际下游改动核对；继承的上游作者不会仅因历史合入而进入本名单。

## 维护规则

- Beacon 自有 PR 合入 `main` 时，如产生新的贡献者，在同一 PR 或紧随其后的文档 PR 中补充账号、Git 署名和至少一个可访问的提交或 PR 链接。仅有 Git 署名而无法确认账号时先保留署名与证据，不猜测身份。
- 同步上游版本时保留官方原始提交和作者，不因合入上游历史而自动把官方作者加入本名单。上游作者若直接提交 Beacon 专有改动，可按上一条加入。
- 对别名、遗漏或归属的修正通过 PR 提交证据。名单只用于区分 Beacon 自有贡献，不修改原始提交的作者信息。

完整提交链仍以 `main` 的 Git 历史为准；本名单随项目维护更新。
