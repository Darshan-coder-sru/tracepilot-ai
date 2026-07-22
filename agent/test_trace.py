import time

from opentelemetry import trace

from observability.telemetry import tracer


def main():
    with tracer.start_as_current_span("tracepilot-test") as span:
        span.set_attribute("test.message", "Hello from TracePilot AI")
        span.set_attribute("test.status", "success")

        print("🚀 TracePilot AI trace started!")

        time.sleep(2)

        print("✅ Trace completed!")


if __name__ == "__main__":
    main()