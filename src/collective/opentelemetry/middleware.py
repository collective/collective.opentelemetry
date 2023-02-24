from opentelemetry.trace import Span, get_tracer
from opentelemetry.instrumentation.wsgi import OpenTelemetryMiddleware
from .interfaces import SPAN_KEY


def request_hook(span: Span, environ: dict):
    # Store a reference to the span so it can be used from ZPublisher events
    environ[SPAN_KEY] = span


def wsgi_middleware_factory(global_config):
    apply_patches()

    def filter(app):
        return OpenTelemetryMiddleware(app, request_hook=request_hook)

    return filter


def apply_patches():
    tracer = get_tracer(__name__)

    from plone.namedfile import scaling

    scaling.scaleImage = tracer.start_as_current_span("scaleImage")(scaling.scaleImage)
