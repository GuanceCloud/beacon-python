# Beacon Python

`beacon-otel` 是 Beacon Python 的主安装包，当前仍处于开发阶段，尚未正式发布。

以下是正式发布后的安装用法；目前请从本仓库构建开发制品验证。安装主包和所需框架的自动插桩插件。例如，FastAPI 应用可安装：

```bash
pip install 'beacon-otel[fastapi]'
```

需要 Profiling 时安装：

```bash
pip install 'beacon-otel[fastapi,profiling]'
```

先激活安装 Beacon 的虚拟环境，再配置 OTLP 接收端并启动应用；也可以在 `beacon` 后传入该虚拟环境内可执行文件的完整路径：

```bash
export OTEL_SERVICE_NAME=my-service
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
beacon uvicorn myapp:app
```

`beacon --version` 显示 Beacon Python 产品版本。当前提供 `requests`、`flask`、`fastapi` 可选依赖；其他框架的自动插桩包可根据 OpenTelemetry 官方说明单独安装。安装包存在不代表所有框架和运行环境已获 Beacon 支持；首发支持范围以发行说明中的实际验收结果为准。

可选依赖仅安装对应的自动插桩插件；应用框架本身仍由应用自行安装。不要在同一 Python 环境中混装旧版 `guance-sdk-extension-profiling`，其自动插桩入口会与 `beacon-profiling` 冲突。

`beacon` 默认选择 Beacon 的 OpenTelemetry distro/configurator，并沿用标准 `OTEL_*` 环境变量。用户显式设置的 `OTEL_PYTHON_DISTRO` 或 `OTEL_PYTHON_CONFIGURATOR` 不会被覆盖。Profiling 默认关闭，启用方式见[Profiling 文档](../sdk-extension/beacon-profiling/README.rst)。
