from opentelemetry.instrumentation.wsgi import OpenTelemetryMiddleware
from opentelemetry.trace import Span
from .interfaces import SPAN_KEY
from .patches import apply_patches


def request_hook(span: Span, environ: dict):
    # Store a reference to the span so it can be used from ZPublisher events
    environ[SPAN_KEY] = span


def wsgi_middleware_factory(global_config):
    apply_patches()

    def filter(app):
        return OpenTelemetryMiddleware(app, request_hook=request_hook)

    return filter
