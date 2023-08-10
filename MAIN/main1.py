# Import the required classes
import asyncio

from PresentationParser import PresentationParser
from GPTCommunicator import GPTCommunicator
from SlideExplanation import SlideExplanation
from PresentationExporter import PresentationExporter

class Main:
    def __init__(self, presentation_file):
        self.presentation_file = presentation_file

    async def run(self):
        # Create instances of the classes
        parser = PresentationParser(self.presentation_file)
        communicator = GPTCommunicator()
        exporter = PresentationExporter(self.presentation_file)

        # Parse the presentation and get its data
        presentation_data = parser.parse_presentation()

        # Create a list to store slide explanations
        explanations = []

        # Iterate through each slide and process it
        for slide in presentation_data.slides:
            # Extract text from the slide
            slide_text = parser.extract_text(slide)

            # Create an instance of SlideExplanation for the current slide
            slide_explanation = SlideExplanation(slide_text)

            # Generate the prompt for GPT using slide text
            prompt = slide_explanation.generate_prompt()

            # Send the prompt to GPT and get the response
            response = await communicator.send_prompt(prompt)

            # Extract the AI's reply from the response
            ai_reply = communicator.extract_response(response)

            # Generate the explanation using the AI's reply
            explanation = slide_explanation.generate_explanation(ai_reply)

            # Add the explanation to the list
            explanations.append(explanation)

        # Save the list of explanations in a JSON file
        exporter.save_explanations(explanations)


if __name__ == "__main__":
    presentation_file = "C:/targilim/Ruty-Presentation.pptx"
    main = Main(presentation_file)
    asyncio.run(main.run())