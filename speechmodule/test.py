from google.cloud import vision

def detect_text_gcs(gcs_image_uri):
    client = vision.ImageAnnotatorClient()

    image = vision.Image()
    image.source.image_uri = gcs_image_uri

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        print('Detected text:')
        print(texts[0].description)
    else:
        print("No text detected.")

    if response.error.message:
        raise Exception(f'{response.error.message}')

# Replace with your GCS image URI
gcs_image_uri = r"E:\ai projects 2025\hackthon\speechmodule\test.jpg"
detect_text_gcs(gcs_image_uri)
