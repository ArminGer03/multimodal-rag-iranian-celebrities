# import time
import json
from typing import List, Dict
#
# from metis import MetisAIChat
# from tqdm import tqdm  # الاستيراد الجديد
#
#
# def process_person_data(person_data: List[Dict]) -> List[Dict]:
#     """
#     Process person data to add face descriptions to their bios
#
#     Args:
#         person_data: List of person dictionaries with images and bios
#
#     Returns:
#         Updated person data with face descriptions added to bios
#     """
#     chat = MetisAIChat()
#
#     # tqdm تضيف شريط تقدّم حول الloop
#     for person in tqdm(person_data, desc="Processing persons", unit="person"):
#         # Skip if no images available
#         if not person.get('images') or len(person['images']) == 0:
#             tqdm.write(f"\nNo images found for {person['id']}, skipping...")
#             continue
#
#         image_urls = person['images']
#         face_description = chat.get_face_description(image_urls)
#
#         if face_description and face_description != "UNCLEAR":
#             person['cleaned_bio'] += f"{face_description}"
#         elif face_description == "UNCLEAR":
#             tqdm.write(f"\nImage was unclear for {person['id']}")
#         else:
#             tqdm.write(f"\nFailed to get face description for {person['id']}")
#
#         time.sleep(1)
#
#     return person_data
#
#
# # الاستخدام الرئيسي
# if __name__ == "__main__":
#     with open('saved_data (1).json', 'r', encoding='utf-8') as f:
#         data = json.load(f)
#     # print(len(data))
#
#     # Process فقط أوّل عنصرين
#     updated_data = process_person_data(data)
#
#     with open('updated_persons.json', 'w', encoding='utf-8') as f:
#         json.dump(updated_data, f, ensure_ascii=False, indent=2)
#
#     print("Processing complete. Updated data saved to updated_persons.json")
#
#
#


# الاستخدام الرئيسي
if __name__ == "__main__":
    with open('updated_persons.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(len(data))
    for d in data[:6]:
        print(d)

    # # Process فقط أوّل عنصرين
    # updated_data = process_person_data(data)
    #
    # with open('updated_persons.json', 'w', encoding='utf-8') as f:
    #     json.dump(updated_data, f, ensure_ascii=False, indent=2)

    print("Processing complete. Updated data saved to updated_persons.json")