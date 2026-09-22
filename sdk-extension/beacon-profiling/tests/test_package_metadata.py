from importlib.metadata import distribution

from opentelemetry.sdk.extension.profiling import __version__


def test_beacon_profiling_distribution_identity():
    package = distribution("beacon-profiling")

    assert package.metadata["Name"] == "beacon-profiling"
    assert package.version == __version__
    assert any(
        entry_point.group == "opentelemetry_pre_instrument"
        and entry_point.name == "profiling"
        for entry_point in package.entry_points
    )
