from __future__ import annotations

import hashlib
import os
import threading
import time
from collections import deque
from typing import Annotated

import requests
from fastapi import FastAPI, Query

from opentelemetry import trace

app = FastAPI(title="Beacon Python Demo")

_retained_allocations: deque[list[bytearray]] = deque(maxlen=8)


def _trace_context() -> dict[str, str]:
    context = trace.get_current_span().get_span_context()
    if not context.is_valid:
        return {"trace_id": "unavailable", "span_id": "unavailable"}
    return {
        "trace_id": format(context.trace_id, "032x"),
        "span_id": format(context.span_id, "016x"),
    }


def _cpu_work(rounds: int) -> str:
    digest = b"beacon-python-demo"
    for _ in range(rounds):
        digest = hashlib.sha256(digest).digest()
    return digest.hex()[:16]


def _lock_contention(hold_ms: int) -> None:
    lock = threading.Lock()

    def wait_for_lock() -> None:
        with lock:
            return

    with lock:
        worker = threading.Thread(
            target=wait_for_lock, name="demo-lock-waiter"
        )
        worker.start()
        time.sleep(hold_ms / 1000)
    worker.join()


def _handled_exceptions(count: int = 200) -> None:
    for index in range(count):
        try:
            raise ValueError(f"expected demo exception {index}")
        except ValueError:
            pass


@app.get("/health")
def health() -> dict[str, object]:
    return {"status": "ok", **_trace_context()}


@app.get("/work")
def work(
    rounds: Annotated[int, Query(ge=1_000, le=2_000_000)] = 100_000,
    memory_kb: Annotated[int, Query(ge=1, le=8_192)] = 512,
    lock_ms: Annotated[int, Query(ge=1, le=1_000)] = 50,
) -> dict[str, object]:
    digest = _cpu_work(rounds)
    _retained_allocations.append([bytearray(1024) for _ in range(memory_kb)])
    _lock_contention(lock_ms)
    _handled_exceptions()

    base_url = os.environ.get("DEMO_BASE_URL", "http://127.0.0.1:8000")
    health_response = requests.get(f"{base_url}/health", timeout=2)
    health_response.raise_for_status()

    return {
        "status": "work-complete",
        "cpu_digest": digest,
        "retained_memory_kb": memory_kb,
        "lock_hold_ms": lock_ms,
        "downstream_status": health_response.status_code,
        **_trace_context(),
    }
