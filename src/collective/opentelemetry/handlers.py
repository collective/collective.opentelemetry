from opentelemetry.trace import Span
from zope.component import adapter
from ZPublisher.interfaces import IPubFailure
from ZPublisher.pubevents import PubFailure
from .interfaces import SPAN_KEY


@adapter(IPubFailure)
def on_pub_failure(event: PubFailure):
    span: Span = event.request.environ.get(SPAN_KEY)
    if span:
        span.record_exception(event.exc_info[1])
