"""Optional, opt-in Phoenix tracing. Never enable with sensitive source documents."""
import os
from functools import lru_cache

@lru_cache(maxsize=1)
def initialize_observability():
    if os.getenv('MDI_ENABLE_TRACING', 'false').lower() != 'true':
        return False
    try:
        from phoenix.otel import register
        from openinference.instrumentation.openai import OpenAIInstrumentor
        tracer_provider = register(project_name='mdi-ai-capstone', auto_instrument=False)
        OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)
        return True
    except ImportError as exc:
        raise RuntimeError('Install optional observability dependencies from requirements-observability.txt') from exc
