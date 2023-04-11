import openai

from wikigpt.config import Config


class OpenAIChatbot:
    def __init__(self, config: Config):
        openai.api_key = config.openai_api_key
        self.model = config.openai_model

    def complete(self, prompt):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ]

        )
        message = response.choices[0].message.content
        return message
