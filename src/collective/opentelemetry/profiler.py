from .interfaces import SPAN_KEY
from pyinstrument import Profiler

import re


PROFILE_COOKIE_RE = re.compile(r"(^|;)\s*profile=1(;|$)")


def profiler_middleware_factory(app):
    def profiler_middleware(environ, start_response):
        # check if enabled (by setting the cookie profile=1)
        cookie = environ.get("HTTP_COOKIE") or ""
        enabled = PROFILE_COOKIE_RE.search(cookie)

        # if not enabled, just run the app
        if not enabled:
            return app(environ, start_response)

        # run the app with the profiler
        with Profiler() as profiler:
            result = app(environ, start_response)

        # add profile event to opentelemetry span
        span = environ[SPAN_KEY]
        span.add_event(
            "profile", attributes={"profile.text": profiler.output_text(show_all=True)}
        )

        return result

    return profiler_middleware
