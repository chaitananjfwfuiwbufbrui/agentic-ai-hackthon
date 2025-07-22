import os
from dotenv import load_dotenv
from vertexai.preview.vision_models import ImageGenerationModel
import vertexai
import os

# Load variables from .env file
load_dotenv()

# Optional: manually fetch them if you want to reuse
project_id = os.getenv("PROJECT_ID")
location = os.getenv("LOCATION")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
print(project_id,GOOGLE_APPLICATION_CREDENTIALS)
# Initialize Vertex AI
vertexai.init(project=project_id, location=location)
# Step 3: Load the model
generation_model = ImageGenerationModel.from_pretrained("imagen-4.0-generate-preview-06-06")

# Step 4: Prompt input
prompt_text = "a infograph on butterfly life cycle"

# Step 5: Generate images
images = generation_model.generate_images(
    prompt=prompt_text,
    number_of_images=4,
    aspect_ratio="1:1",
    negative_prompt="",
    person_generation="allow_all",
    safety_filter_level="block_few",
    add_watermark=True,
)

# Step 6: Save image
def save_image(image, index):
    # image is a PIL.Image or similar object with .save()
    filename = f"scene_{index + 1}.png"
    image.save(filename)
    print(f"Saved: {filename}")

# Step 7: Save all generated images
for i, img in enumerate(images):
    save_image(img, i)
