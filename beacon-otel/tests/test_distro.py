"""Beacon OpenTelemetry distro defaults."""

from __future__ import annotations

import os

import pytest
from beacon_otel.distro import BeaconDistro

from opentelemetry.environment_variables import (
    OTEL_LOGS_EXPORTER,
    OTEL_METRICS_EXPORTER,
    OTEL_TRACES_EXPORTER,
)
from opentelemetry.sdk.environment_variables import OTEL_EXPORTER_OTLP_PROTOCOL


def test_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in (
        OTEL_TRACES_EXPORTER,
        OTEL_METRICS_EXPORTER,
        OTEL_LOGS_EXPORTER,
        OTEL_EXPORTER_OTLP_PROTOCOL,
    ):
        monkeypatch.delenv(key, raising=False)

    BeaconDistro().configure()

    assert os.environ[OTEL_TRACES_EXPORTER] == "otlp"
    assert os.environ[OTEL_METRICS_EXPORTER] == "otlp"
    assert os.environ[OTEL_LOGS_EXPORTER] == "otlp"
    assert os.environ[OTEL_EXPORTER_OTLP_PROTOCOL] == "grpc"


def test_explicit_settings_are_preserved(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(OTEL_TRACES_EXPORTER, "console")
    monkeypatch.setenv(OTEL_METRICS_EXPORTER, "none")
    monkeypatch.setenv(OTEL_LOGS_EXPORTER, "none")
    monkeypatch.setenv(OTEL_EXPORTER_OTLP_PROTOCOL, "http/protobuf")

    BeaconDistro().configure()

    assert os.environ[OTEL_TRACES_EXPORTER] == "console"
    assert os.environ[OTEL_METRICS_EXPORTER] == "none"
    assert os.environ[OTEL_LOGS_EXPORTER] == "none"
    assert os.environ[OTEL_EXPORTER_OTLP_PROTOCOL] == "http/protobuf"
