"""Beacon defaults for OpenTelemetry Python auto-instrumentation."""

from __future__ import annotations

import os

from opentelemetry.environment_variables import (
    OTEL_LOGS_EXPORTER,
    OTEL_METRICS_EXPORTER,
    OTEL_TRACES_EXPORTER,
)
from opentelemetry.instrumentation.distro import BaseDistro
from opentelemetry.sdk._configuration import _OTelSDKConfigurator
from opentelemetry.sdk.environment_variables import OTEL_EXPORTER_OTLP_PROTOCOL


class BeaconConfigurator(_OTelSDKConfigurator):
    """Configure the OTel SDK using its standard environment variables."""


class BeaconDistro(BaseDistro):
    """Select OTLP defaults without overriding explicit user settings."""

    def _configure(self, **kwargs: object) -> None:
        os.environ.setdefault(OTEL_TRACES_EXPORTER, "otlp")
        os.environ.setdefault(OTEL_METRICS_EXPORTER, "otlp")
        os.environ.setdefault(OTEL_LOGS_EXPORTER, "otlp")
        os.environ.setdefault(OTEL_EXPORTER_OTLP_PROTOCOL, "grpc")
