# Beacon Python FastAPI Demo

这个 Demo 使用 `beacon-otel 0.1.0rc2`，用于验证：

- FastAPI 服务端自动插桩；
- `requests` 客户端自动插桩；
- Trace 与 Profile 的上下文关联；
- CPU 栈采样，并为内存、线程锁竞争和已处理异常采样制造可控负载。

`/work` 会调用本服务的 `/health`，因此一次请求会产生服务端和客户端 Span，并制造一段有界的 Profiling 负载。

## 安装

在本目录执行：

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
beacon --version
```

应输出 `Beacon Python 0.1.0rc2`。

## 连接 DataKit

下面以本机 DataKit 的 OTLP/gRPC Trace 接口 `127.0.0.1:4317` 和 pprof 接口 `127.0.0.1:9529` 为例：

```bash
export OTEL_SERVICE_NAME=beacon-python-demo
export OTEL_RESOURCE_ATTRIBUTES=deployment.environment.name=demo
export OTEL_EXPORTER_OTLP_ENDPOINT=http://127.0.0.1:4317
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc

export OTEL_PROFILING_ENABLED=true
export OTEL_PROFILING_PPROF_UPLOAD_URL=http://127.0.0.1:9529/profiling/v1/input
```

Profile 默认每 60 秒聚合并导出一次；需要缩短或延长时，可以设置
`OTEL_PROFILING_EXPORT_INTERVAL`。

先用默认的 CPU 栈采样完成基础验收。需要专项验证其他采集器时，再分别开启：

```bash
export OTEL_PROFILING_LOCK_ENABLED=true
export OTEL_PROFILING_MEMORY_ENABLED=true

# 已处理异常采集要求 Python 3.12 及以上。
export OTEL_PROFILING_EXCEPTION_ENABLED=true
```

内存采集周期默认跟随 Profile 导出周期，也可以通过
`OTEL_PROFILING_MEMORY_INTERVAL` 单独调整。

启动应用：

```bash
beacon uvicorn app:app --host 127.0.0.1 --port 8000
```

在另一个终端产生负载：

```bash
for index in $(seq 1 20); do
  curl -fsS 'http://127.0.0.1:8000/work?rounds=100000&memory_kb=512&lock_ms=50'
  echo
done
```

等待至少一个导出周期后，在观测端按服务名 `beacon-python-demo` 查询。`/work` 响应中的 `trace_id` 和 `span_id` 可用于定位对应 Trace。

## 不连接接收端的本地冒烟

可以把 Trace 输出到终端，并将 Profile 写成本地 pprof 文件：

```bash
export OTEL_SERVICE_NAME=beacon-python-demo
export OTEL_TRACES_EXPORTER=console
export OTEL_METRICS_EXPORTER=none
export OTEL_LOGS_EXPORTER=none

export OTEL_PROFILING_ENABLED=true
export OTEL_PROFILING_EXPORTER=pprof
export OTEL_PROFILING_PPROF_PATH=otel-profiles/demo
export OTEL_PROFILING_INCLUDE_TRACE_CONTEXT=false

beacon uvicorn app:app --host 127.0.0.1 --port 8000
```

请求 `/work` 后，终端应出现 FastAPI 和 `requests` Span，`otel-profiles/` 下应生成 `.pprof` 文件。本地 pprof 编码器无法表示部分无符号 Trace/Span ID，因此这个仅验证本地文件输出的模式关闭了 Profile 中的 Trace 上下文；DataKit 的 pprof 上传路径不需要该规避配置。
