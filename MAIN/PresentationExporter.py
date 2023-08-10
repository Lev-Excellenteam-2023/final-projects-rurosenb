# This class will handle saving the explanations for all slides in a JSON file.
import json
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
OUTPUTS_FOLDER = os.getenv('OUTPUTS_FOLDER_PATH')
#OUTPUTS_FOLDER = "C:\\targilim\Excellenteam_python_Project\\final-projects-rurosenb\\OUTPUT_FOLDER"


class PresentationExporter:
    def __init__(self, presentation_name):
        #self.presentation_name = presentation_name.split("/")[-1].split(".")[0]
        self.presentation_name = presentation_name

    def save_explanations(self, explanations):
        # Convert the explanations to JSON format
        json_data = json.dumps(explanations, indent=4)

        # Save the JSON data to a file
        output_file = OUTPUTS_FOLDER + '\\' + f"{self.presentation_name}"
        with open(output_file, "w") as file:
            file.write(json_data)

        print(f"Explanations saved to {output_file}")