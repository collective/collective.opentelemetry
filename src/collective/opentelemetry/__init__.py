from opentelemetry.instrumentation.wsgi import OpenTelemetryMiddleware


def wsgi_middleware_factory(global_config):
    def filter(app):
        return OpenTelemetryMiddleware(app)

    return filter
