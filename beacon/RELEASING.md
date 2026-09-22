# Beacon Python 发行准备

当前没有 Beacon Python 正式发行，也没有已批准的 Beacon 包名、制品集合或发布目标。继承的上游及历史上的 `gtrace` 包安装示例不是 Beacon 已发布的证据；[产品入口](https://github.com/GuanceCloud/beacon)以实际发布标签为准。

首次发行前需要在本仓库确定并验证：

1. Beacon 产品包与命令身份、版本标识，以及与上游和旧 Guance 包的共存或替代关系。当前 Profiling 扩展源码已变化但仍沿用已发布的 Guance 包版本号，禁止以相同名称和版本覆盖既有制品；候选发行前必须先确定新身份或新版本。
2. 固定的 Contrib、Python Core、第三方依赖与许可证来源；从固定提交构建候选制品并记录摘要。
3. 自有功能、上游影响范围、Python 运行环境、DataKit 接收端和升级回退的验证结果；将证据绑定同一提交和制品。
4. 发布权限、目标仓库或包索引、发行审批及回退流程；不得启用继承的 OpenTelemetry 发布工作流来发布 Beacon。
5. 每版发布说明、已知限制和版本化使用文档。首次发行后，再更新产品仓库的 Python 安装和 Release 入口。

各语言独立发行；不要求与 Beacon Java、Go 锁步，也不把本地测试通过视为发行验收。
