from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from app.settings import settings

def setup_telemetry(app):
    resource = Resource(attributes={
        "service.name": settings.OTEL_SERVICE_NAME
    })

    trace.set_tracer_provider(TracerProvider(resource=resource))
    
    # We send traces to Jaeger via OTLP
    otlp_exporter = OTLPSpanExporter(endpoint="http://jaeger:4317", insecure=True)
    
    span_processor = BatchSpanProcessor(otlp_exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)

    # Instrument FastAPI
    FastAPIInstrumentor.instrument_app(app)