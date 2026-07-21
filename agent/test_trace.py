import time

from opentelemetry import trace

from observability.telemetry import tracer


def main():
    with tracer.start_as_current_span("agentwatch-test") as span:
        span.set_attribute("test.message", "Hello from AgentWatch AI")
        span.set_attribute("test.status", "success")

        print("🚀 AgentWatch AI trace started!")

        time.sleep(2)

        print("✅ Trace completed!")


if __name__ == "__main__":
    main()