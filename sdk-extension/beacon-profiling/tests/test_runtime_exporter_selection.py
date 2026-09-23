from __future__ import annotations

from opentelemetry.sdk.extension.profiling.export import (
    CompatiblePPROFExporter,
)
from opentelemetry.sdk.extension.profiling.export.pprof import (
    PPROFProfileExporter,
)
from opentelemetry.sdk.extension.profiling.model.pprof_builder import (
    CompatiblePprofProfileBuilder,
    PprofProfileBuilder,
)
from opentelemetry.sdk.extension.profiling.runtime import Profiler


def test_runtime_defaults_to_compatible_exporter_for_env_fallback(
    monkeypatch,
):
    monkeypatch.delenv("OTEL_PROFILING_EXPORTER", raising=False)
    monkeypatch.setenv(
        "OTEL_PROFILING_PPROF_UPLOAD_URL",
        "http://collector:9529/profiling/v1/input",
    )

    exporter = Profiler._create_exporter_from_env()

    assert isinstance(exporter, CompatiblePPROFExporter)
    exporter.shutdown()


def test_runtime_explicit_otlp_exporter_overrides_env_fallback(
    monkeypatch,
):
    sentinel = object()
    monkeypatch.setenv("OTEL_PROFILING_EXPORTER", "otlp")
    monkeypatch.setenv(
        "OTEL_PROFILING_PPROF_UPLOAD_URL",
        "http://collector:9529/profiling/v1/input",
    )
    monkeypatch.setattr(
        "opentelemetry.sdk.extension.profiling.runtime.create_otlp_profile_exporter",
        lambda: sentinel,
    )

    exporter = Profiler._create_exporter_from_env()

    assert exporter is sentinel


def test_runtime_uses_compatible_pprof_builder_for_http_exporter(tmp_path):
    profiler = Profiler(
        exporter=CompatiblePPROFExporter(pprof_path=str(tmp_path / "prof"))
    )

    try:
        assert isinstance(profiler._builder, CompatiblePprofProfileBuilder)
    finally:
        profiler._exporter.shutdown()


def test_runtime_uses_standard_pprof_builder_for_file_exporter(tmp_path):
    profiler = Profiler(
        exporter=PPROFProfileExporter(directory=str(tmp_path / "prof"))
    )

    try:
        assert isinstance(profiler._builder, PprofProfileBuilder)
        assert not isinstance(profiler._builder, CompatiblePprofProfileBuilder)
    finally:
        profiler._exporter.shutdown()


def test_runtime_defaults_to_sixty_second_intervals(monkeypatch):
    monkeypatch.delenv("OTEL_PROFILING_EXPORT_INTERVAL", raising=False)
    monkeypatch.delenv("OTEL_PROFILING_MEMORY_INTERVAL", raising=False)

    profiler = Profiler(exporter=object())

    assert profiler._export_interval == 60.0
    assert profiler._memory_interval == 60.0


def test_runtime_interval_environment_variables_override_defaults(
    monkeypatch,
):
    monkeypatch.setenv("OTEL_PROFILING_EXPORT_INTERVAL", "17.5")
    monkeypatch.setenv("OTEL_PROFILING_MEMORY_INTERVAL", "23.5")

    profiler = Profiler(exporter=object())

    assert profiler._export_interval == 17.5
    assert profiler._memory_interval == 23.5


def test_runtime_interval_arguments_override_environment(monkeypatch):
    monkeypatch.setenv("OTEL_PROFILING_EXPORT_INTERVAL", "17.5")
    monkeypatch.setenv("OTEL_PROFILING_MEMORY_INTERVAL", "23.5")

    profiler = Profiler(
        exporter=object(),
        export_interval=31.5,
        memory_interval=37.5,
    )

    assert profiler._export_interval == 31.5
    assert profiler._memory_interval == 37.5
