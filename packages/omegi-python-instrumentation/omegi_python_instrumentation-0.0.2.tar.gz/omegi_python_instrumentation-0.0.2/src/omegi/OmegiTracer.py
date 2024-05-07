import inspect
import os
import sys
import threading

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from omegi.KafkaSpanExporter import KafkaSpanExporter


class OmegiTracer:
    def __init__(self, service_name, kafka_server, topic, token):
        self.tracer_provider = TracerProvider()
        self.kafka_exporter = KafkaSpanExporter(kafka_server, topic, token)
        self.tracer_provider.add_span_processor(BatchSpanProcessor(self.kafka_exporter))
        trace.set_tracer_provider(self.tracer_provider)
        self.tracer = trace.get_tracer(service_name)
        self.project_root = self.__find_project_root__()

    def trace_function(self, frame, event, arg):
        if event == 'call':
            code = frame.f_code
            function_name = code.co_name
            module_name = code.co_filename

            if module_name.startswith(self.project_root) and 'omegi' not in module_name:
                span = self.tracer.start_span(f"{module_name}.{function_name}")
                span.set_attribute("module", module_name)
                span.set_attribute("name", function_name)
                span.set_attribute("thread.name", threading.current_thread().name)
                span.set_attribute("thread.id", threading.current_thread().ident)
                span.set_attribute("arguments", self.__get_args__(frame, inspect.getargvalues(frame).args))

                with trace.use_span(span):
                    frame.f_locals['_otel_span'] = span
                    return self.trace_function
        elif event == 'return':
            if '_otel_span' in frame.f_locals:
                span = frame.f_locals['_otel_span']
                span.end()

        return self.trace_function

    def get_current_span(self):
        return trace.get_current_span()

    def __get_args__(self, frame, raw):
        args = []
        for i, arg_name in enumerate(raw):
            arg_value = frame.f_locals[arg_name]
            args.append(f"{arg_name} : {arg_value}")
        return args

    def __find_project_root__(self):
        current_path = os.path.abspath(__file__)
        while True:
            if os.path.exists(os.path.join(current_path, 'requirements.txt')) or os.path.exists(os.path.join(current_path, 'setup.py')):
                return current_path
            parent_path = os.path.dirname(current_path)
            if parent_path == current_path:
                raise Exception("Project root not found.")
            current_path = parent_path

    def start_tracing(self):
        sys.setprofile(self.trace_function)

    def stop_tracing(self):
        sys.setprofile(None)

