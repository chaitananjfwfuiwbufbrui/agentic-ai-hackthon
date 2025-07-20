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
prompt_text = """
📖 Storyboard + Image Generation Prompts
🟣 Scene 1: The Misty Woods of Curion
Narrative:
Lia enters the whispering woods, chasing a glowing blue flame dancing on the wind.

Image Prompt:
A Ghibli-style pastel forest, mist-covered, with a small glowing blue flame floating just ahead. A young girl in a herbalist cloak chases it, surrounded by strange, oversized flowers and magical moths.

🟠 Scene 2: Lithium — The Light Heir
Narrative:
Lia meets Lith, the shy and light-footed elemental prince of Alkalia, who controls pink flames and floats slightly above the ground.

Key Concept: Lightest alkali metal, pink flame, low reactivity.

Image Prompt:
A boy with pale silver hair, glowing pink eyes, and a flowing lavender cloak, floating inches above a crystal ground. Pink flames trail gently from his fingers.

🔵 Scene 3: Sodium — The Bright Companion
Narrative:
Lith introduces Lia to Sodi, a warm and energetic spirit who bursts into a bright yellow flame when excited.

Key Concept: Bright yellow flame, more reactive than lithium, soft metal.

Image Prompt:
A cheerful young girl with glowing yellow tattoos, surrounded by small flame orbs. She lights up a dark corridor in golden light, standing barefoot on a pool of saltwater.

🟣 Scene 4: Potassium — The Violet Storm Dancer
Narrative:
The trio travels to the highlands, where they meet Kato, the rebellious violet-flame dancer who sparks electricity when he moves.

Key Concept: Violet flame, high reactivity, soft and stored in oil.

Image Prompt:
A dark-skinned dancer-boy with stormy eyes, crackling violet energy around his fingertips. He’s mid-air, spinning over a pond with leaping flame wisps and arcs of lightning.

🔴 Scene 5: Rubidium — The Red-Glint Sentinel
Narrative:
Deep underground, Rubi guards the portal to the ancient spring of Francium. She’s protective and explosive when provoked.

Key Concept: Highly reactive, reddish flame, more unstable.

Image Prompt:
A tall warrior princess in armor with glowing red-orange veins, standing beside a cave of bubbling molten metal. Her eyes glow dimly red, and her sword is steaming from heat.

🟡 Scene 6: Cesium — The Golden Cascade
Narrative:
Floating on a cloud-sea, Lia meets Cesa, a golden ethereal being with a melting aura, who causes the sea around her to bubble with every step.

Key Concept: Golden flame, reacts explosively with water, softest metal.

Image Prompt:
A golden-haired celestial being with translucent robes and glowing golden fingertips, standing on a floating sea platform with bubbling water around. The sky is peach and lavender.

⚫ Scene 7: Francium — The Vanishing Flame
Narrative:
Finally, in the quiet heart of Elementara, Lia catches a glimpse of Fran, the rarest of all, flickering like a dream. He speaks in riddles and disappears before she can touch him.

Key Concept: Radioactive, rarest, most reactive, least stable.

Image Prompt:
A faint shadow of a boy made of flame and mist, hovering in a starlit cave. His form flickers between solid and vapor, eyes glowing a mysterious silver. Time appears frozen around him.

🌟 Final Scene: Return to the Table of Elements
Narrative:
The elemental spirits gift Lia a glowing scroll — the Periodic Table — each of their orbs placed in the Group 1 column. She vows to explore the rest of Elementara.

Image Prompt:
Lia holds a glowing periodic table scroll with light lines connecting elements. Behind her, the elemental spirits of Group 1 float in the air, each glowing in their flame color.
"""

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
