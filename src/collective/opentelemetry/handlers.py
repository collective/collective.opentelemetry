from AccessControl import getSecurityManager
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.trace import Span
from zope.component import adapter
from ZPublisher.interfaces import IPubFailure, IPubAfterTraversal
from ZPublisher.pubevents import PubFailure, PubAfterTraversal
from .interfaces import SPAN_KEY


@adapter(IPubAfterTraversal)
def after_pub_traversal(event: PubAfterTraversal):
    """Record the view as the HTTP route after traversal"""
    request = event.request
    span = request.environ.get(SPAN_KEY)
    if span:
        published = request.get("PUBLISHED")

        # Record view name
        view_name = published.__class__.__name__
        # Unwrap view metaclasses generated by ZCML
        klass = next(c for c in published.__class__.__mro__ if ".metaconfigure" not in c.__module__)
        view_name = f"{klass.__module__}.{klass.__name__}"
        span.update_name(view_name)
        span.set_attribute(SpanAttributes.HTTP_ROUTE, view_name)

        # Record user id
        user_id = getSecurityManager().getUser().getId()
        span.set_attribute(SpanAttributes.ENDUSER_ID, user_id)


@adapter(IPubFailure)
def on_pub_failure(event: PubFailure):
    """Record exceptions"""
    span: Span = event.request.environ.get(SPAN_KEY)
    if span:
        span.record_exception(event.exc_info[1])
