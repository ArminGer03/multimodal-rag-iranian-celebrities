from metis import MetisAIChat
from prompt import create_persian_biography_prompt
import json
import time

if __name__ == "__main__":
    # Configuration

    # Initialize chat client
    chat = MetisAIChat()

    input_json = {
        "era": "دودمان پهلوی، جمهوری اسلامی ایران",
        "nick-names": [],
        "name": "کامبیز آتابای",
        "occupation": [
            "مدیر فوتبال",
            "مربی"
        ],
        "death": {
            "date": "",
            "location": {
                "province": "",
                "city": "",
                "coordinates": {
                    "latitude": "",
                    "longitude": ""
                }
            },
            "tomb_location": {
                "province": "",
                "city": "",
                "coordinates": {
                    "latitude": "",
                    "longitude": ""
                }
            }
        },
        "works": [
            "مدیر کل فنی و خدمات عمومی در دربار پهلوی",
            "رئیس دفتر فرح پهلوی در نیویورک",
            "دهمین رئیس فدراسیون فوتبال ایران",
            "ششمین رئیس کنفدراسیون فوتبال آسیا"
        ],
        "birth": {
            "date": "1939-02-02",
            "location": {
                "province": "تهران",
                "city": "تهران",
                "coordinates": {
                    "latitude": "35.6895",
                    "longitude": "51.3890"
                }
            }
        },
        "image": [
            "https://commons.wikimedia.org/wiki/Special:FilePath/Kambiz_Atabay.jpg"
        ],
        "sex": "male",
        "events": []
    }

    # Get response with retry logic
    prompt = create_persian_biography_prompt(input_json)
    # Start timer
    start_time = time.time()

    response = chat.get_response_with_retry(prompt)

    # Calculate elapsed time
    elapsed_time = time.time() - start_time

    if response:
        print(f"Bot response: {response}")
        print(f"Time taken: {elapsed_time:.2f} seconds")
    else:
        print("Failed to get response from the bot")
        print(f"Time elapsed before failure: {elapsed_time:.2f} seconds")