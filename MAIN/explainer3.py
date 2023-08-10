import os
import asyncio
from datetime import datetime

from PresentationParser import PresentationParser
from GPTCommunicator import GPTCommunicator
from SlideExplanation import SlideExplanation
from PresentationExporter import PresentationExporter
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DB.database import Upload  # Import the User and Upload classes from your database module

# Load environment variables from .env file
load_dotenv()
UPLOADS_FOLDER = os.getenv('UPLOADS_FOLDER_PATH')
OUTPUTS_FOLDER = os.getenv('OUTPUTS_FOLDER_PATH')
# Use os.getenv to get the value of the environment variable
DB_PATH = os.path.join(os.getenv('DB_FOLDER_PATH'), "gpt_explainer.db")

# Create the SQLAlchemy engine
engine = create_engine(f"sqlite:///{DB_PATH}", echo=True)
Session = sessionmaker(bind=engine)


async def process_presentation(presentation_path, name_file, session):
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

    # Update the status and finish_time in the database
    upload = session.query(Upload).filter_by(filename=name_file).first()
    if upload:
        upload.status = "done"
        upload.finish_time = datetime.now()
        session.commit()


async def process_new_files(session):
    while True:
        print("Checking for new files...")
        pptx_files = [file for file in os.listdir(UPLOADS_FOLDER)]

        for pptx_file in pptx_files:
            name_file = os.path.splitext(pptx_file)[0]  # Extract filename without extension
            json_file = name_file + ".json"
            json_file_path = os.path.join(OUTPUTS_FOLDER, json_file)

            if not os.path.exists(json_file_path):
                presentation_path = os.path.join(UPLOADS_FOLDER, pptx_file)
                print(f"Processing file: {pptx_file}")
                await process_presentation(presentation_path, name_file, session)
                print(f"File processed: {pptx_file}")
                os.remove(os.path.join(UPLOADS_FOLDER, pptx_file))

        await asyncio.sleep(10)


if __name__ == "__main__":
    session = Session()  # Create a session for database operations
    asyncio.run(process_new_files(session))
    session.close()  # Close the session when the script ends
