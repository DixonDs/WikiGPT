class PageSplitter:
    def __init__(self, max_tokens, tokenizer):
        self.max_tokens = max_tokens
        self.tokenizer = tokenizer

    def split(self, text):
        chunks = PageSplitter._create_chunks(text, self.max_tokens, self.tokenizer)
        return [self.tokenizer.decode(chunk) for chunk in chunks]

    # https://github.com/openai/openai-cookbook/blob/main/examples/Entity_extraction_for_long_documents.ipynb
    # Split a text into smaller chunks of size n, preferably ending at the end of a sentence
    @staticmethod
    def _create_chunks(text, n, tokenizer):
        tokens = tokenizer.encode(text)
        """Yield successive n-sized chunks from text."""
        i = 0
        while i < len(tokens):
            # Find the nearest end of sentence within a range of 0.5 * n and 1.5 * n tokens
            j = min(i + int(1.5 * n), len(tokens))
            while j > i + int(0.5 * n):
                # Decode the tokens and check for full stop or newline
                chunk = tokenizer.decode(tokens[i:j])
                if chunk.endswith(".") or chunk.endswith("\n"):
                    break
                j -= 1
            # If no end of sentence found, use n tokens as the chunk size
            if j == i + int(0.5 * n):
                j = min(i + n, len(tokens))
            yield tokens[i:j]
            i = j
