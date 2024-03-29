from .interfaces import SPAN_KEY
from AccessControl import getSecurityManager
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.trace import Span
from plone.caching.hooks import Intercepted
from transaction.interfaces import TransientError
from zExceptions import NotFound
from zExceptions import Redirect
from zExceptions import Unauthorized
from zope.component import adapter
from ZPublisher.interfaces import IPubAfterTraversal
from ZPublisher.interfaces import IPubFailure
from ZPublisher.pubevents import PubAfterTraversal
from ZPublisher.pubevents import PubFailure


IGNORED_EXCEPTIONS = (NotFound, Redirect, Unauthorized, Intercepted)


def get_view_class(obj):
    if obj.__class__.__name__ == "method":
        class_name, module_name = get_view_class(obj.__self__)
        return f"{class_name}.{obj.__name__}", module_name
    # Unwrap view metaclasses generated by ZCML
    klass = next(
        c
        for c in obj.__class__.__mro__
        if ".metaconfigure" not in c.__module__
        and "plone.rest.zcml" not in c.__module__
    )
    return klass.__name__, klass.__module__


@adapter(IPubAfterTraversal)
def after_pub_traversal(event: PubAfterTraversal):
    """Record the view as the HTTP route after traversal"""
    request = event.request
    span = request.environ.get(SPAN_KEY)
    if span:
        published = request.get("PUBLISHED")

        # Record view name
        class_name, module_name = get_view_class(published)
        view_name = f"{class_name} [{module_name}]"
        span.update_name(view_name)
        span.set_attribute(SpanAttributes.HTTP_ROUTE, view_name)

        # Record user id
        user_id = getSecurityManager().getUser().getId()
        if user_id:
            span.set_attribute(SpanAttributes.ENDUSER_ID, user_id)


@adapter(IPubFailure)
def on_pub_failure(event: PubFailure):
    """Record exceptions"""
    span: Span = event.request.environ.get(SPAN_KEY)
    if span:
        # Add view name for exceptions
        if "http.route" not in getattr(span, "attributes", {}):
            class_name, module_name = get_view_class(event.exc_info[1])
            view_name = f"{class_name} [{module_name}]"
            span.update_name(view_name)
            span.set_attribute(SpanAttributes.HTTP_ROUTE, view_name)

        # Record exception, unless its one we intentionally ignore
        err = event.exc_info[1]
        if isinstance(err, IGNORED_EXCEPTIONS):
            return
        if isinstance(err, TransientError) and event.request.supports_retry():
            return
        span.record_exception(err)
