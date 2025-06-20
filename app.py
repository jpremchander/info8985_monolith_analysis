from flask import Flask, request
from random import randint
import logging

from opentelemetry import trace, metrics

from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogProcessor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter

# -------------------- Setup Providers --------------------

resource = Resource.create({"service.name": "info8985-flask-app"})

# Tracing
trace.set_tracer_provider(TracerProvider(resource=resource))
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True))
)

# Metrics
reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint="http://localhost:4317", insecure=True)
)
metrics.set_meter_provider(MeterProvider(resource=resource, metric_readers=[reader]))

# Logging (OTEL to SigNoz)
logger_provider = LoggerProvider(resource=resource)
logger_exporter = OTLPLogExporter(endpoint="http://localhost:4317", insecure=True)
logger_provider.add_log_processor(BatchLogProcessor(logger_exporter))
otel_handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)
logging.getLogger().addHandler(otel_handler)

# -------------------- Init Tracer, Meter, Logger --------------------

tracer = trace.get_tracer("diceroller.tracer")
meter = metrics.get_meter("diceroller.meter")

roll_counter = meter.create_counter(
    "dice.rolls",
    description="The number of rolls by roll value",
)

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------- Flask Routes --------------------

@app.route("/rolldice")
def roll_dice():
    with tracer.start_as_current_span("roll") as roll_span:
        player = request.args.get('player', default=None, type=str)
        try:
            result = str(roll())
            roll_span.set_attribute("roll.value", result)
            roll_counter.add(1, {"roll.value": result})
            if player:
                logger.warning("%s is rolling the dice: %s", player, result)
            else:
                logger.warning("Anonymous player is rolling the dice: %s", result)
            return result
        except Exception as e:
            roll_span.record_exception(e)
            roll_span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
            logger.error("Error occurred: %s", e)
            return str(e), 500

def roll():
    sides = request.args.get('sides', default=6, type=int)
    if sides <= 0:
        raise ValueError("Number of sides must be greater than 0")
    return randint(1, sides)

# -------------------- Run App --------------------

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
