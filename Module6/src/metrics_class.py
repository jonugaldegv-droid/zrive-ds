from prometheus_client import Counter, Histogram

class Metric:
    def __init__(self):
        self.request_count = Counter(
            'app_requests_total', # Metric name
            'Total number of requests to the app', # Metric description
        )

        self.exceptions = Counter(
            'app_exceptions_total',
            'Total number of unhandled exceptions',
        )

        self.model_errors = Counter(
            'model_errors', 
            'Total number of errors due to model failing'
        )

        self.request_latency = Histogram(
            'app_request_latency_seconds',
            'Request latency in seconds'
        )

    def increase_requests(self):
        self.request_count.inc()

    def increase_exceptions(self):
        self.exceptions.inc()

    def increase_model_errors(self):
        self.model_errors.inc()

    def observe_latency(self, seconds: float):
        self.request_latency.observe(seconds)

metrics = Metric()