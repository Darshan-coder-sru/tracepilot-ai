# Groq pricing (USD per 1 million tokens) as of 2025
# Model: llama-3.1-8b-instant
PRICING = {
    "llama-3.1-8b-instant": {
        "input_per_million": 0.05,
        "output_per_million": 0.08,
    },
    "llama-3.3-70b-versatile": {
        "input_per_million": 0.59,
        "output_per_million": 0.79,
    },
    "mixtral-8x7b-32768": {
        "input_per_million": 0.24,
        "output_per_million": 0.24,
    },
}


def calculate_token_cost(
    model,
    prompt_tokens,
    completion_tokens
):
    """
    Calculate the USD cost for a Groq API call.

    Returns a dict with token counts and cost breakdown.
    """

    rates = PRICING.get(model, {
        "input_per_million": 0.0,
        "output_per_million": 0.0
    })

    input_cost = (prompt_tokens / 1_000_000) * rates["input_per_million"]
    output_cost = (completion_tokens / 1_000_000) * rates["output_per_million"]
    total_cost = input_cost + output_cost
    total_tokens = prompt_tokens + completion_tokens

    return {
        "model": model,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "input_cost_usd": input_cost,
        "output_cost_usd": output_cost,
        "total_cost_usd": total_cost,
    }


def extract_token_usage(groq_response):
    """
    Extract token usage from a Groq API response object.
    Returns (prompt_tokens, completion_tokens).
    """
    usage = getattr(groq_response, "usage", None)
    if usage is None:
        return 0, 0
    prompt_tokens = getattr(usage, "prompt_tokens", 0) or 0
    completion_tokens = getattr(usage, "completion_tokens", 0) or 0
    return prompt_tokens, completion_tokens


def print_token_report(cost_data):
    """
    Pretty-print token usage and cost to the console.
    """
    print("\n💰 TOKEN & COST TRACKING")
    print("=" * 40)
    print(f"Model             : {cost_data['model']}")
    print(f"Prompt Tokens     : {cost_data['prompt_tokens']:,}")
    print(f"Completion Tokens : {cost_data['completion_tokens']:,}")
    print(f"Total Tokens      : {cost_data['total_tokens']:,}")
    print(f"Input Cost        : ${cost_data['input_cost_usd']:.6f}")
    print(f"Output Cost       : ${cost_data['output_cost_usd']:.6f}")
    print(f"Total Cost        : ${cost_data['total_cost_usd']:.6f}")
