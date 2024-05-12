from opentelemetry import context as context_api
from opentelemetry.context import attach, set_value

from opentelemetry.instrumentation.utils import (
    _SUPPRESS_INSTRUMENTATION_KEY,
)

from syntrac_opentelemetry.semconv.ai import SpanAttributes, SyntracSpanKindValues

from syntrac_opentelemetry.instrumentation.langchain.utils import (
  _with_tracer_wrapper,
  process_request,
  process_response,
)


@_with_tracer_wrapper
def workflow_wrapper(tracer, to_wrap, wrapped, instance, args, kwargs):
    """Instruments and calls every function defined in TO_WRAP."""
    if context_api.get_value(_SUPPRESS_INSTRUMENTATION_KEY):
        return wrapped(*args, **kwargs)

    name = to_wrap.get("span_name")
    kind = to_wrap.get("kind") or SyntracSpanKindValues.WORKFLOW.value

    attach(set_value("workflow_name", name))

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
async def aworkflow_wrapper(tracer, to_wrap, wrapped, instance, args, kwargs):
    """Instruments and calls every function defined in TO_WRAP."""
    if context_api.get_value(_SUPPRESS_INSTRUMENTATION_KEY):
        return wrapped(*args, **kwargs)

    name = to_wrap.get("span_name")
    kind = to_wrap.get("kind") or SyntracSpanKindValues.WORKFLOW.value

    attach(set_value("workflow_name", name))

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
