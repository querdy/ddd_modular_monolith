from litestar.plugins.prometheus import PrometheusConfig, PrometheusController

prometheus_config = PrometheusConfig()


class CustomPrometheusController(PrometheusController):
    tags = ["Prometheus"]
