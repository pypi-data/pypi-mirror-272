import pytest
from tokencurator.openai import get_tokenizer, truncate_text_to_tokens, adjust_text


def test_truncate_text_to_tokens():
    text = "Hello " * 100  # long text
    max_tokens = 50
    encoding_type = "gpt-3.5-turbo"  # assuming this is a valid type for demonstration
    tokenizer = get_tokenizer(encoding_type)
    expected_length = len(tokenizer.encode(text[:max_tokens]))

    truncated_text = truncate_text_to_tokens(text, max_tokens, encoding_type)
    truncated_tokens = tokenizer.encode(truncated_text)

    assert len(truncated_tokens) <= max_tokens, "Text was not truncated correctly"


def test_adjust_text():
    content = "Example text " * 100  # long text
    prompt_token_length = 10
    output_token_length = 10
    max_total_tokens = 50
    adjusted_text = adjust_text(content, prompt_token_length, output_token_length, max_total_tokens, "gpt-3.5-turbo")

    # You need to define what 'model_encoding_type' should be
    tokenizer = get_tokenizer("gpt-3.5-turbo")
    token_count = len(tokenizer.encode(adjusted_text))

    assert token_count <= (
            max_total_tokens - prompt_token_length - output_token_length), "Adjustment did not respect token limits"
