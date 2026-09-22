# Beacon Python 开发入口

本仓库以独立仓库方式维护完整的 [OpenTelemetry Python Contrib](https://github.com/open-telemetry/opentelemetry-python-contrib) 源码和历史，不是 GitHub Fork。产品总入口是 [GuanceCloud/beacon](https://github.com/GuanceCloud/beacon)。当前为开发工程，尚无 Beacon Python 正式发行；源码存在及下述本地测试结果不等于对外支持承诺。

开发主线为 `main`。首次导入保留了旧 [GuanceCloud/opentelemetry-python-contrib](https://github.com/GuanceCloud/opentelemetry-python-contrib/tree/gtrace) 的 `gtrace` 提交历史，并合入官方 `v0.65b0` 发布标签。固定来源见[基线记录](upstream.lock.json)，后续升级流程见[上游同步](UPSTREAM.md)。配套 OpenTelemetry Python Core 开发依赖固定到 `v1.44.0`，以根目录 [pyproject.toml](../pyproject.toml) 和 [uv.lock](../uv.lock) 为准。

## 代码与验证入口

| 内容 | 位置 |
| --- | --- |
| 自有发行包与 `gtrace` 命令 | [guance-opentelemetry-distro](../guance-opentelemetry-distro/) |
| 自有 Profiling 扩展 | [guance-sdk-extension-profiling](../sdk-extension/guance-sdk-extension-profiling/) |
| 上游自动插桩及测试 | [instrumentation](../instrumentation/) |
| 构建与贡献约定 | [CONTRIBUTING.md](../CONTRIBUTING.md) |
| 发行准备项 | [RELEASING.md](RELEASING.md) |

从仓库根目录执行以下开发验证；运行完整上游矩阵仍需按[贡献指南](../CONTRIBUTING.md)准备环境：

```bash
uvx --from uv==0.12.1 uv lock --check
uvx --from uv==0.12.1 uv run --frozen --package guance-opentelemetry-distro --with pytest pytest -q guance-opentelemetry-distro/tests sdk-extension/guance-sdk-extension-profiling/tests
```

目前仅完成上述自有包测试，尚未完成完整上游测试矩阵、DataKit 接收端兼容、运行环境矩阵和候选制品验收。继承的 `gtrace`、Profiling 源码及示例仍使用原有 Guance 命名；既有 PyPI Guance 包不属于 Beacon 发行。当前源码已改变依赖和行为，但仍保留旧包版本号，仅供开发验证，不得以同名同版本覆盖既有制品。Beacon 产品制品身份与发布方式须在发行前明确，不应把继承的上游或旧仓库发布流程当作 Beacon 发行入口。
