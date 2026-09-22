# Beacon Python

Beacon Python 是 GuanceCloud 基于完整 OpenTelemetry Python Contrib 源码维护的 Python 自动插桩与增强工程，保留上游历史，按语言独立开发和发行。

当前处于开发阶段，尚无 Beacon Python 正式发行包。上游 OpenTelemetry 包及既有 Guance PyPI 包的下载地址和支持声明，不代表 Beacon Python 的发行结果。

## 开发入口

- [开发说明与工程布局](beacon/README.md)
- [源码来源与上游基线](beacon/upstream.lock.json)
- [同步 OpenTelemetry](beacon/UPSTREAM.md)
- [发行准备](beacon/RELEASING.md)
- [自有发行包与 `gtrace` 命令](guance-opentelemetry-distro/)
- [Profiling 扩展](sdk-extension/guance-sdk-extension-profiling/)
- [贡献指南](CONTRIBUTING.md)

开发主线为 `main`。从仓库根目录执行 `uvx --from uv==0.12.1 uv lock --check` 可检查开发依赖锁定状态；自有包测试及完整上游矩阵的入口见[开发说明](beacon/README.md)。依赖解析、构建或本地测试通过均不等于正式发行验收。

## Beacon Contributors

以下仅列已核对身份的 Beacon Python 下游贡献者，不将继承的上游作者自动计入名单；完整代码来源仍以 Git 历史为准。

| GitHub 账号 | Git 署名 | 可追溯的下游贡献 |
| --- | --- | --- |
| [@lrwh](https://github.com/lrwh) | `liurui` | [旧 `gtrace` 发行包与 Profiling 实现](https://github.com/GuanceCloud/beacon-python/commit/55658637367c766ba3d2444d844e85881495370e)、[Beacon Python 工程初始化](https://github.com/GuanceCloud/beacon-python/commit/9fa18964fa1fc6470cac6b45d86d649ddadddd55) |

## 产品与上游

- [Beacon 产品入口](https://github.com/GuanceCloud/beacon)
- [OpenTelemetry Python Contrib](https://github.com/open-telemetry/opentelemetry-python-contrib)
- [导入时的 Guance 自有实现](https://github.com/GuanceCloud/opentelemetry-python-contrib/tree/40b90737969d7dfd48a732a93a3a3734f55bff27)

保留上游源码布局、包名和[许可证](LICENSE)。Beacon 产品包身份与版本需在首次发行前确定，不以现有 Guance 包版本覆盖已发布制品。
