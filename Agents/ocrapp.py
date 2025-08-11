# import openai
# from pdf2image import convert_from_bytes
# from io import BytesIO
# import base64
# import time
# import streamlit as st

# openai.api_key = st.secrets["api_keys"]["openai"]

# def image_to_base64(img):
#     buf = BytesIO()
#     img.save(buf, format="PNG")
#     return base64.b64encode(buf.getvalue()).decode("utf-8")

# def extract_text_with_gpt4o(image):
#     base64_image = image_to_base64(image)
#     response = openai.chat.completions.create(
#         model="gpt-4o",
#         messages=[
#             {
#                 "role": "user",
#                 "content": [
#                     {"type": "text", "text": "Extract all readable text from this image."},
#                     {
#                         "type": "image_url",
#                         "image_url": {
#                             "url": f"data:image/png;base64,{base64_image}",
#                             "detail": "high"
#                         },
#                     },
#                 ],
#             }
#         ],
#         max_tokens=2000,
#         temperature=0,
#     )
#     return response.choices[0].message.content

# @st.cache_resource(show_spinner="Converting PDF...")
# def convert_pdf_to_images(pdf_bytes):
#     return convert_from_bytes(pdf_bytes, dpi=100)  # Lower DPI for faster processing

# def extract_pdf_text_with_gpt4o(pdf_bytes):
#     images = convert_pdf_to_images(pdf_bytes)
#     all_text = []

#     for i, img in enumerate(images):
#         with st.spinner(f"🔍 Processing page {i + 1}..."):
#             try:
#                 page_text = extract_text_with_gpt4o(img)
#                 all_text.append(page_text)
#                 time.sleep(0.8)
#             except Exception as e:
#                 all_text.append(f"[Error on page {i + 1}]: {e}")
#                 st.error(f"Error on page {i + 1}: {e}")

#     return "\n\n".join(all_text)




# import os
# import time
# import io
# from pdf2image import convert_from_bytes
# from google.cloud import vision
# from PIL import Image
# import streamlit as st
# import os
# import json

# # with open("gcloud_key.json", "w") as f:
# #     json.dump(json.loads(st.secrets["google_cloud"]["credentials"]), f)


# import os, json

# creds_str = os.getenv("GOOGLE_CLOUD_CREDENTIALS")
# if not creds_str:
#     raise RuntimeError("GOOGLE_CLOUD_CREDENTIALS not found.")

# # Remove leading/trailing triple quotes if present
# creds_str = creds_str.strip().strip('"""').strip()

# # Now parse JSON
# creds_data = json.loads(creds_str)

# # Write to file for GCP SDK
# with open("gcloud_key.json", "w") as f:
#     json.dump(creds_data, f)

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcloud_key.json"





# # Step 2: Now safe to import and use Google client
# from google.cloud import vision
# def get_vision_client():
#     return vision.ImageAnnotatorClient()

# # ➕ your other code here...


# @st.cache_resource(show_spinner="Converting PDF...")
# def convert_pdf_to_images(pdf_bytes):
#     return convert_from_bytes(pdf_bytes, dpi=300)  # Higher DPI for better OCR

# def extract_text_with_vision(image: Image.Image) -> str:
#     client = get_vision_client() 
#     buf = io.BytesIO()
#     image.save(buf, format="PNG")
#     image_bytes = buf.getvalue()

#     image_vision = vision.Image(content=image_bytes)
#     response = client.text_detection(image=image_vision)

#     if response.error.message:
#         raise Exception(f"Vision API error: {response.error.message}")

#     texts = response.text_annotations
#     return texts[0].description if texts else "(No text detected)"

# def extract_pdf_text_with_vision(pdf_bytes) -> str:
#     images = convert_pdf_to_images(pdf_bytes)
#     all_text = []

#     for i, img in enumerate(images):
#         with st.spinner(f"🔍 Processing page {i + 1}..."):
#             try:
#                 page_text = extract_text_with_vision(img)
#                 all_text.append(f"--- Page {i + 1} ---\n{page_text.strip()}")
#                 time.sleep(0.5)  # Respect API quota
#             except Exception as e:
#                 error_msg = f"[Error on page {i + 1}]: {e}"
#                 all_text.append(error_msg)
#                 st.error(error_msg)

#     return "\n\n".join(all_text)





import os
import time
import io
import json
from pdf2image import convert_from_bytes
from google.cloud import vision
from PIL import Image
import streamlit as st


# --- Load GOOGLE_CLOUD_CREDENTIALS from env ---
creds_str = os.getenv("GOOGLE_CLOUD_CREDENTIALS")
if not creds_str:
    raise RuntimeError("GOOGLE_CLOUD_CREDENTIALS not found.")

# Debug: show safe preview of the raw value
print("DEBUG: GOOGLE_CLOUD_CREDENTIALS length:", len(creds_str))
print("DEBUG: GOOGLE_CLOUD_CREDENTIALS start preview:", creds_str[:100])
print("DEBUG: GOOGLE_CLOUD_CREDENTIALS end preview:", creds_str[-100:])

# Remove leading/trailing triple quotes if present
creds_str = creds_str.strip().strip('"""').strip()

# Debug: show safe preview after stripping
print("DEBUG: After stripping triple quotes, length:", len(creds_str))
print("DEBUG: After stripping, start preview:", creds_str[:100])
print("DEBUG: After stripping, end preview:", creds_str[-100:])

# Now parse JSON
try:
    creds_data = json.loads(creds_str)
except json.JSONDecodeError as e:
    print("DEBUG: Failed to decode JSON:", e)
    raise

# Debug: check top-level keys in parsed credentials
print("DEBUG: Parsed credential keys:", list(creds_data.keys()))
if "private_key" not in creds_data:
    print("WARNING: 'private_key' field is missing from credentials!")

# Write to file for GCP SDK
with open("gcloud_key.json", "w") as f:
    json.dump(creds_data, f)

# Debug: confirm file was written and has valid JSON
if os.path.exists("gcloud_key.json"):
    print("DEBUG: gcloud_key.json file exists.")
    try:
        with open("gcloud_key.json") as f:
            parsed_file = json.load(f)
            print("DEBUG: gcloud_key.json keys:", list(parsed_file.keys()))
    except json.JSONDecodeError as e:
        print("DEBUG: gcloud_key.json contains invalid JSON:", e)
else:
    print("ERROR: gcloud_key.json file was not created!")

# Set environment variable for Google SDK
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcloud_key.json"


# Step 2: Now safe to import and use Google client
def get_vision_client():
    return vision.ImageAnnotatorClient()


@st.cache_resource(show_spinner="Converting PDF...")
def convert_pdf_to_images(pdf_bytes):
    return convert_from_bytes(pdf_bytes, dpi=300)  # Higher DPI for better OCR


def extract_text_with_vision(image: Image.Image) -> str:
    client = get_vision_client()
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    image_bytes = buf.getvalue()

    image_vision = vision.Image(content=image_bytes)
    response = client.text_detection(image=image_vision)

    if response.error.message:
        raise Exception(f"Vision API error: {response.error.message}")

    texts = response.text_annotations
    return texts[0].description if texts else "(No text detected)"


def extract_pdf_text_with_vision(pdf_bytes) -> str:
    images = convert_pdf_to_images(pdf_bytes)
    all_text = []

    for i, img in enumerate(images):
        with st.spinner(f"🔍 Processing page {i + 1}..."):
            try:
                page_text = extract_text_with_vision(img)
                all_text.append(f"--- Page {i + 1} ---\n{page_text.strip()}")
                time.sleep(0.5)  # Respect API quota
            except Exception as e:
                error_msg = f"[Error on page {i + 1}]: {e}"
                all_text.append(error_msg)
                st.error(error_msg)

    return "\n\n".join(all_text)
























