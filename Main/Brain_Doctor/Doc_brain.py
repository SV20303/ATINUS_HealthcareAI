import os
import glob
import base64, random
from dotenv import load_dotenv
from PIL import Image
import matplotlib.pyplot as plt
from groq import Groq

# -----------------------------
# 1. Load Environment Variables
# -----------------------------
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise EnvironmentError("❌ GROQ_API_KEY not found in .env file.")

client = Groq(api_key=api_key)

# -----------------------------
# 2. Helper Functions
# -----------------------------
def get_image_files(image_path):
    # Check if the input is a single image file
    if os.path.isfile(image_path) and image_path.lower().endswith((".jpg", ".jpeg", ".png")):
        print("✅ Single image file provided")
        print("Example image path:", image_path)
        return [image_path]

    # Otherwise, treat it as a folder
    image_files = glob.glob(os.path.join(image_path, "**", "*.*"), recursive=True)
    image_files = [f for f in image_files if f.lower().endswith((".jpg", ".jpeg", ".png"))]

    if not image_files:
        raise FileNotFoundError("❌ No images found in the specified folder.")

    print(f"✅ Found {len(image_files)} images")
    print("Example image path:", image_files[0])
    return image_files

def show_sample_image(image_path):
    img = Image.open(image_path)
    plt.imshow(img)
    plt.axis("off")
    plt.title("Sample Image")
    plt.show()

def encode_images(image_files):
    encoded = {}
    for path in image_files:
        with open(path, "rb") as f:
            encoded_img = base64.b64encode(f.read()).decode("utf-8")
            filename = os.path.basename(path)
            encoded[filename] = encoded_img
    print(f"✅ Encoded {len(encoded)} images")
    print("Sample filename:", list(encoded.keys())[0])
    return encoded

def analysis_with_query(query, model, encoded_image):
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": query},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/jpeg;base64,{encoded_image}"
                }}
            ]
        }
    ]

    try:
        print("📡 Sending request to Groq API...")
        response = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        print("✅ Got response from Groq API")
        return response.choices[0].message.content
    except Exception as e:
        print("❌ Error while calling Groq API:", str(e))
        return "Error: Could not get a response."

# -----------------------------
# 3. Run the Workflow
# -----------------------------
image_folder = "/Users/saransh/Developer/ATINUS-AI_Medical_Assistant/Main/DATASETS/ACNE"x
image_files = get_image_files(image_folder)
show_sample_image(image_files[0])
encoded_images = encode_images(image_files)

# first_image_filename = list(encoded_images.keys())[0]
# encoded_image = encoded_images[first_image_filename]

random_filename = random.choice(list(encoded_images.keys()))
encoded_image = encoded_images[random_filename]

query = "What has happened to my skin?"
model = "meta-llama/llama-4-scout-17b-16e-instruct"

response = analysis_with_query(query, model, encoded_image)
print("\n🤖 Doctor's Response:", response)

if __name__ == "__main__":
    print("This will only run if Doc_brain.py is run directly")