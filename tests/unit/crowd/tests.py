from crowd.apps import CrowdConfig


def test_crowd_config():
    assert CrowdConfig.name == "crowd"
