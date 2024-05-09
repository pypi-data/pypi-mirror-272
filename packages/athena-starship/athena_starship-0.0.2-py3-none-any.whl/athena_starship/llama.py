from swarms import HuggingfaceLLM

llama = HuggingfaceLLM(
    model_name="gradientai/Llama-3-8B-Instruct-262k",
    max_tokens=1000,
    temperature=0.5,
)

