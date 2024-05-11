import tiktoken


def get_tokenizer(encoding_type: str):
    """
    Returns the appropriate tokenizer based on the given encoding type.
    """
    if "k_base" in encoding_type:
        return tiktoken.get_encoding(encoding_type)
    else:
        return tiktoken.encoding_for_model(encoding_type)


def truncate_text_to_tokens(text, max_tokens, encoding_type):
    """
    Truncates text to the specified maximum number of tokens.
    """
    tokenizer = get_tokenizer(encoding_type)
    tokens = tokenizer.encode(text)
    if len(tokens) > max_tokens:
        return tokenizer.decode(tokens[:max_tokens])
    return text


def adjust_text(content, prompt_token_length, output_token_length, max_total_tokens, model):
    """
    Adjusts the input content based on the token limits for OpenAI's API.
    """
    max_tokens_for_input = max_total_tokens - (prompt_token_length + output_token_length)
    adjusted_text = truncate_text_to_tokens(content, max_tokens_for_input, model)
    return adjusted_text


