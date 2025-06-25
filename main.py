import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import os
from gtts import gTTS

# Uncomment and set path if Tesseract is not in your PATH environment variable
# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

def pdf_to_images(pdf_path, output_folder):
    doc = fitz.open(pdf_path)
    image_paths = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=300)

        image_path = os.path.join(output_folder, f"page_{page_num + 1}.png")
        pix.save(image_path)
        image_paths.append(image_path)

        print(f"Saved page {page_num + 1} as {image_path}")

    return image_paths

def images_to_text(image_paths, text_output_folder):
    text_files = []

    for img_path in image_paths:
        text = pytesseract.image_to_string(Image.open(img_path), lang='eng')

        text_filename = os.path.splitext(os.path.basename(img_path))[0] + ".txt"
        text_file_path = os.path.join(text_output_folder, text_filename)

        with open(text_file_path, "w", encoding="utf-8") as text_file:
            text_file.write(text)

        text_files.append(text_file_path)
        print(f"Extracted text from {img_path} saved to {text_file_path}")

    return text_files

def texts_to_audio(text_files, audio_output_folder, lang='en', voice='com'):
    audio_paths = []

    for text_file in text_files:
        with open(text_file, "r", encoding="utf-8") as file:
            text_content = file.read().strip()

        if text_content:  # Only proceed if text is not empty
            tts = gTTS(text=text_content, lang=lang, tld=voice)
            audio_filename = os.path.splitext(os.path.basename(text_file))[0] + ".mp3"
            audio_file_path = os.path.join(audio_output_folder, audio_filename)
            tts.save(audio_file_path)
            audio_paths.append(audio_file_path)

            print(f"Audio created: {audio_file_path}")
        else:
            print(f"Skipped empty text file: {text_file}")

    return audio_paths

if __name__ == "__main__":
    input_pdf = "/home/shai/workspace/hadas/Story.pdf"  # Replace with your PDF file path
    images_folder = "pdf_images"
    texts_folder = "pdf_texts"
    audio_folder = "pdf_audio"

    # Create output directories if they don't exist
    os.makedirs(images_folder, exist_ok=True)
    os.makedirs(texts_folder, exist_ok=True)
    os.makedirs(audio_folder, exist_ok=True)

    # Step 1: PDF to Images
    #image_files = pdf_to_images(input_pdf, images_folder)

    # Step 2: Images to Text
    #text_files = images_to_text(image_files, texts_folder)

    # Step 3: Text to Audio (Female voice, English)
    texts_to_audio(text_files, audio_folder, lang='en', voice='com')

    print("PDF to MP3 conversion completed.")
