"""Beacon distribution metadata and entry points."""

from __future__ import annotations

from importlib.metadata import distribution

from beacon_otel import __version__


def test_beacon_otel_distribution_identity() -> None:
    package = distribution("beacon-otel")
    assert package.metadata["Name"] == "beacon-otel"
    assert package.version == __version__
    for group, name in (
        ("console_scripts", "beacon"),
        ("opentelemetry_distro", "beacon"),
        ("opentelemetry_configurator", "beacon"),
    ):
        assert any(
            entry_point.group == group and entry_point.name == name
            for entry_point in package.entry_points
        )
