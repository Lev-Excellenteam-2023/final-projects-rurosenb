# This class will handle saving the explanations for all slides in a JSON file.
import json

class PresentationExporter:
    def __init__(self, presentation_name):
        self.presentation_name = presentation_name.split("/")[-1].split(".")[0]

    def save_explanations(self, explanations):
        # Convert the explanations to JSON format
        json_data = json.dumps(explanations, indent=4)

        # Save the JSON data to a file
        output_file = f"{self.presentation_name}.json"
        with open(output_file, "w") as file:
            file.write(json_data)

        print(f"Explanations saved to {output_file}")
