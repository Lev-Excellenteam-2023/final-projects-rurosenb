# This class will handle processing each slide separately and generating explanations.
import asyncio

class SlideExplanation:
    def __init__(self, slide_text):
        self.slide_text = slide_text

    def generate_prompt(self):
        # Prepend any additional context or instructions for the GPT model
        prompt = "I have a presentation that I studied in class, Please explain the content of the this slide:\n"
        # Append the slide text to the prompt
        prompt += self.slide_text
        return prompt

    def generate_explanation(self, gpt_response):
        # Process the AI's response to extract relevant information
        # and generate an explanation based on the reply

        # Example implementation:
        explanation = "Explanation:\n"
        explanation += gpt_response  # Assuming the AI's reply is the explanation itself

        return explanation
