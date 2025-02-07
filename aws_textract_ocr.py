import boto3
import os
import json

def extract_text_from_image(image_path):
    textract_client = boto3.client("textract")

    try:
        with open(image_path, "rb") as img_file:
            image_bytes = img_file.read()

        response = textract_client.detect_document_text(Document={"Bytes": image_bytes})

        extracted_text = "\n".join(
            [item["Text"] for item in response["Blocks"] if item["BlockType"] == "LINE"]
        )

        return extracted_text

    except Exception as e:
        print(f"Textract API Error: {e}")
        return ""

image_path = r"D:\OCR_script_extraction\images\sample_1.jpeg"

text = extract_text_from_image(image_path)

if text:
    with open("data.json", "w") as json_file:
        json.dump({"extracted_text": text}, json_file, indent=4)
    print("Extracted text saved to data.json!")
else:
    print("No text extracted.")
