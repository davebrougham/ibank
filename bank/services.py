import anthropic
from django.conf import settings

import logging 

class ClaudeService:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    def get_structured_response(self, prompt):
        try:
            logging.warning(f"Claude prompt: {prompt}")
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )
            logging.warning(f"Claude response: {response.content[0].text}")
            structured_response = self.parse_response(response.content[0].text)
            
            return structured_response
        except Exception as e:
            logging.error(f"Error calling Claude API: {str(e)}")
            return None

    def parse_response(self, raw_response):
        return raw_response
