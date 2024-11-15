from transformers import AutoTokenizer, AutoModelForCausalLM


tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-1B")


text = "Hello, how can I help you?"
inputs = tokenizer(text, return_tensors="pt")  # For PyTorch


outputs = model.generate(
    inputs["input_ids"],
    max_length=50,  # Maximum tokens to generate
    num_return_sequences=1,  # Number of outputs
    no_repeat_ngram_size=2,  # Prevent repetition
    temperature=0.7  # Adjust creativity
)
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(response)
