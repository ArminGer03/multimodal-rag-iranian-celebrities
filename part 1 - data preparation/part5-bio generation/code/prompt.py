import json

def create_persian_biography_prompt(json_data: dict) -> str:
    """
    Creates a prompt string for the Gemma model to generate a Persian biography
    from JSON data with consistent formatting.
    """
    # Convert the input JSON dictionary to a formatted JSON string
    input_json_string = json.dumps(json_data, ensure_ascii=False, indent=2)

    prompt = f"""Convert the following JSON biographical data into a flowing Persian text paragraph.

STRICT RULES:
- Only use information explicitly provided in the JSON
- Do NOT add any information not in the JSON
- Skip null, empty, or missing fields
- Write only one paragraph in Persian

PROPERTY HANDLING:
- name: Start with the full name
- birth.date: Can be string OR object {{year, month, day}} - extract year if string
- death: Skip if null or date is missing/empty
- occupation: If array, join with "و"
- works: If array of objects, extract titles only
- events: Extract title and description, ignore null fields
- era: Include if not "نامشخص"

Example:
Input: {{"name": "ابونصر منصور", "birth": {{"date": "حدود 960", "location": {{"city": "گیلان"}}}}, "occupation": "ستاره‌شناس، ریاضیدان", "works": ["مثلثات"], "death": {{"date": "1036"}}}}
Output: ابونصر منصور، در حدود سال ۹۶۰ در گیلان به دنیا آمد و در سال ۱۰۳۶ درگذشت. او به‌عنوان ستاره‌شناس و ریاضیدان فعالیت می‌کرد. از آثار شاخص او می‌توان به "مثلثات" اشاره نمود.

Now convert this JSON:
{input_json_string}

Output: """

    return prompt

def extract_biography_from_output(model_output: str) -> str:
    """
    Extracts the biography text from the model output.
    """
    # Since we're not using markers, extract text after "Output: "
    if "Output: " in model_output:
        parts = model_output.split("Output: ")
        if len(parts) > 1:
            # Get the last occurrence of Output:
            output_text = parts[-1].strip()

            # Remove any unwanted patterns that might appear
            # Remove if it starts with quotation marks
            if output_text.startswith('"') and output_text.endswith('"'):
                output_text = output_text[1:-1]

            # Remove if "Example" appears (model might generate another example)
            if "\nExample" in output_text:
                output_text = output_text.split("\nExample")[0].strip()

            # Remove if "Input:" appears (model might continue with more examples)
            if "\nInput:" in output_text:
                output_text = output_text.split("\nInput:")[0].strip()

            # Remove if "Now convert" appears
            if "\nNow convert" in output_text:
                output_text = output_text.split("\nNow convert")[0].strip()

            return output_text

    # If no "Output: " found, return the original
    return model_output.strip()
