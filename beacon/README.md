# Beacon Python 开发入口

本仓库以独立仓库方式维护完整的 [OpenTelemetry Python Contrib](https://github.com/open-telemetry/opentelemetry-python-contrib) 源码和历史，不是 GitHub Fork。产品总入口是 [GuanceCloud/beacon](https://github.com/GuanceCloud/beacon)。当前为开发工程，尚无 Beacon Python 正式发行；源码存在及下述本地测试结果不等于对外支持承诺。

开发主线为 `main`。首次导入保留了旧 [GuanceCloud/opentelemetry-python-contrib](https://github.com/GuanceCloud/opentelemetry-python-contrib/tree/gtrace) 的 `gtrace` 提交历史，并合入官方 `v0.65b0` 发布标签。Beacon Python 开发版本以[版本文件](version.properties)为唯一手工修改入口；Contrib `v0.65b0` 与配套 Core `v1.44.0` 的 tag 和完整提交均见[基线记录](upstream.lock.json)。Core 实际开发依赖仍以根目录 [pyproject.toml](../pyproject.toml) 和 [uv.lock](../uv.lock) 为准，并由版本检查脚本核对。后续升级流程见[上游同步](UPSTREAM.md)。

## 代码与验证入口

| 内容 | 位置 |
| --- | --- |
| Beacon 主安装包及 `beacon` 命令 | [beacon-otel](../beacon-otel/) |
| 上游自动插桩发行包 | [opentelemetry-distro](../opentelemetry-distro/) |
| 自有 Profiling 扩展 | [beacon-profiling](../sdk-extension/beacon-profiling/) |
| 上游自动插桩及测试 | [instrumentation](../instrumentation/) |
| 构建与贡献约定 | [CONTRIBUTING.md](../CONTRIBUTING.md) |
| Beacon 版本与上游基线检查 | [check-version.py](scripts/check-version.py) |
| FastAPI Demo | [examples/fastapi-demo](examples/fastapi-demo/) |
| 发行准备项 | [RELEASING.md](RELEASING.md) |

从仓库根目录执行以下开发验证；运行完整上游矩阵仍需按[贡献指南](../CONTRIBUTING.md)准备环境：

```bash
python beacon/scripts/check-version.py
python -m unittest discover -s beacon/tests
uvx --from uv==0.12.1 uv lock --check
uvx --from uv==0.12.1 uv run --frozen --package beacon-otel --with pytest pytest -q beacon-otel/tests
uvx --from uv==0.12.1 uv run --frozen --package beacon-profiling --with pytest pytest -q sdk-extension/beacon-profiling/tests
```

目前已实现 `beacon-otel`、`beacon` 命令与 `beacon-profiling`；`0.1.0rc1` 已发布到 PyPI，并完成 FastAPI Demo、DataKit Trace 与 pprof 入库验收。当前源码准备发布 `0.1.0rc2`，修正 Profile CPU 时间和内存快照调度，并将 Profile 默认导出周期设为可覆盖的 60 秒。旧 `gtrace` 发行包已从本仓库移除；既有 PyPI Guance 包不属于 Beacon 发行，不得以同名同版本覆盖既有制品。不应把继承的上游或旧仓库发布流程当作 Beacon 发行入口。
