from opentelemetry import context as context_api
from opentelemetry.instrumentation.utils import _SUPPRESS_INSTRUMENTATION_KEY

from syntrac_opentelemetry.semconv.ai import SpanAttributes, SyntracSpanKindValues

from syntrac_opentelemetry.instrumentation.langchain.utils import (
  _with_tracer_wrapper,
  process_request,
  process_response,
)


@_with_tracer_wrapper
def task_wrapper(tracer, to_wrap, wrapped, instance, args, kwargs):
    """Instruments and calls every function defined in TO_WRAP."""
    if context_api.get_value(_SUPPRESS_INSTRUMENTATION_KEY):
        return wrapped(*args, **kwargs)

    # Some Langchain objects are wrapped elsewhere, so we ignore them here
    if instance.__class__.__name__ in ("AgentExecutor"):
        return wrapped(*args, **kwargs)

    if hasattr(instance, "name") and instance.name:
        name = f"{to_wrap.get('span_name')}.{instance.name.lower()}"
    elif to_wrap.get("span_name"):
        name = to_wrap.get("span_name")
    else:
        name = f"langchain.task.{instance.__class__.__name__}"
    kind = to_wrap.get("kind") or SyntracSpanKindValues.TASK.value
    with tracer.start_as_current_span(name) as span:
        span.set_attribute(
            SpanAttributes.SYNTRAC_SPAN_KIND,
            kind,
        )
        span.set_attribute(SpanAttributes.SYNTRAC_ENTITY_NAME, name)

        process_request(span, args, kwargs)
        return_value = wrapped(*args, **kwargs)
        process_response(span, return_value)

    return return_value


@_with_tracer_wrapper
async def atask_wrapper(tracer, to_wrap, wrapped, instance, args, kwargs):
    """Instruments and calls every function defined in TO_WRAP."""
    if context_api.get_value(_SUPPRESS_INSTRUMENTATION_KEY):
        return wrapped(*args, **kwargs)

    # Some Langchain objects are wrapped elsewhere, so we ignore them here
    if instance.__class__.__name__ in ("AgentExecutor"):
        return wrapped(*args, **kwargs)

    if hasattr(instance, "name") and instance.name:
        name = f"{to_wrap.get('span_name')}.{instance.name.lower()}"
    elif to_wrap.get("span_name"):
        name = to_wrap.get("span_name")
    else:
        name = f"langchain.task.{instance.__class__.__name__}"
    kind = to_wrap.get("kind") or SyntracSpanKindValues.TASK.value
    with tracer.start_as_current_span(name) as span:
        span.set_attribute(
            SpanAttributes.SYNTRAC_SPAN_KIND,
            kind,
        )
        span.set_attribute(SpanAttributes.SYNTRAC_ENTITY_NAME, name)

        process_request(span, args, kwargs)
        return_value = await wrapped(*args, **kwargs)
        process_response(span, return_value)

    return return_value
