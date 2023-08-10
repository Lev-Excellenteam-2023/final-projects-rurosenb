import os
import asyncio
from PresentationParser import PresentationParser
from GPTCommunicator import GPTCommunicator
from SlideExplanation import SlideExplanation
from PresentationExporter import PresentationExporter

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
UPLOADS_FOLDER = os.getenv('UPLOADS_FOLDER_PATH')

OUTPUTS_FOLDER = os.getenv('OUTPUTS_FOLDER_PATH')



async def process_presentation(presentation_path, name_file):
    parser = PresentationParser(presentation_path)
    communicator = GPTCommunicator()
    exporter = PresentationExporter(name_file)

    presentation_data = parser.parse_presentation()
    explanations = []

    for slide in presentation_data.slides:
        slide_text = parser.extract_text(slide)
        slide_explanation = SlideExplanation(slide_text)
        prompt = slide_explanation.generate_prompt()
        response = await communicator.send_prompt(prompt)
        ai_reply = communicator.extract_response(response)
        explanation = slide_explanation.generate_explanation(ai_reply)
        explanations.append(explanation)
    exporter.save_explanations(explanations)


async def process_new_files():
    while True:
        print("Checking for new files...")
        pptx_files = [file for file in os.listdir(UPLOADS_FOLDER)]

        for pptx_file in pptx_files:
            #name_file = os.path(pptx_file)[0]
            name_file = pptx_file
            print("name file: ", name_file)
            json_file = name_file + ".json"
            print("json_file: ", json_file)
            json_file_path = os.path.join(OUTPUTS_FOLDER, json_file)
            print("json_file_path: ", json_file_path)

            if not os.path.exists(json_file_path):
                presentation_path = os.path.join(UPLOADS_FOLDER, pptx_file)
                print(f"Processing file: {pptx_file}")
                await process_presentation(presentation_path, name_file)
                print(f"File processed: {pptx_file}")
                os.remove(os.path.join(UPLOADS_FOLDER, pptx_file))

        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(process_new_files())
