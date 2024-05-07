import traceback

from fastapi import Request
from opentelemetry import trace

from omegi.OmegiTracer import OmegiTracer


def fastapi_handler(omegi_tracer: OmegiTracer):
    async def handler(request: Request, exc: Exception):
        return await __omegi_handler_fastapi__(request, exc, omegi_tracer)
    return handler


async def __omegi_handler_fastapi__(request: Request, exc: Exception, omegi_tracer: OmegiTracer):
    # current_span = omegi_tracer.get_current_span()
    # with omegi_tracer.tracer.start_span("exception", context=current_span.context) as span:
    #     span.set_attribute("exception.type", str(type(exc)))
    #     span.set_attribute("exception.message", str(exc))
    #     span.set_attribute("exception.stacktrace", "".join(traceback.format_tb(exc.__traceback__)))
    __create_span__(exc)
    raise exc


def __omegi_handler_django__(exc, context):
    __create_span__(exc)
    raise exc


def __omegi_handler_flask__(exc):
    __create_span__(exc)
    raise exc


def __create_span__(exc: Exception):
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("exception") as span:
        span.set_attribute("exception.type", str(type(exc)))
        span.set_attribute("exception.message", str(exc))
        span.set_attribute("exception.stacktrace", "".join(traceback.format_tb(exc.__traceback__)))