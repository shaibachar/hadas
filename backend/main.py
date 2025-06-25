from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
import os
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from gtts import gTTS
import shutil
import requests
from bs4 import BeautifulSoup
import re
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Uncomment and set path if Tesseract is not in your PATH environment variable
# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

PDF_DIR = "pdf_uploads"
IMG_DIR = "pdf_images"
TXT_DIR = "pdf_texts"
AUDIO_DIR = "pdf_audio"

os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(TXT_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

def pdf_to_images(pdf_path, output_folder):
    doc = fitz.open(pdf_path)
    image_paths = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=300)
        image_path = os.path.join(output_folder, f"page_{page_num + 1}.png")
        pix.save(image_path)
        image_paths.append(image_path)
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
    return text_files

def texts_to_audio(text_files, audio_output_folder, lang='en', voice='com'):
    audio_paths = []
    for text_file in text_files:
        with open(text_file, "r", encoding="utf-8") as file:
            text_content = file.read().strip()
        if text_content:
            tts = gTTS(text=text_content, lang=lang, tld=voice)
            audio_filename = os.path.splitext(os.path.basename(text_file))[0] + ".mp3"
            audio_file_path = os.path.join(audio_output_folder, audio_filename)
            tts.save(audio_file_path)
            audio_paths.append(audio_file_path)
    return audio_paths

@app.get("/")
def read_root():
    return {"message": "FastAPI backend is running!"}

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    # Save uploaded PDF
    pdf_path = os.path.join(PDF_DIR, file.filename)
    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # Convert PDF to images
    image_files = pdf_to_images(pdf_path, IMG_DIR)
    # Convert images to text
    text_files = images_to_text(image_files, TXT_DIR)
    # Convert text to audio
    audio_files = texts_to_audio(text_files, AUDIO_DIR)
    audio_filenames = [os.path.basename(f) for f in audio_files]
    return {"audio_files": audio_filenames}

@app.get("/audio/{filename}")
def get_audio(filename: str):
    audio_path = os.path.join(AUDIO_DIR, filename)
    if os.path.exists(audio_path):
        return FileResponse(audio_path, media_type="audio/mpeg", filename=filename)
    return JSONResponse(status_code=404, content={"error": "File not found"})

@app.post("/link-to-audio/")
def link_to_audio(link: str = Form(...)):
    try:
        response = requests.get(link, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract visible text
        texts = soup.stripped_strings
        text_content = ' '.join(texts)
        # Clean text: remove excessive whitespace, non-printable chars
        text_content = re.sub(r'\s+', ' ', text_content)
        text_content = re.sub(r'[^\x20-\x7E]+', '', text_content)
        text_content = text_content.strip()
        if not text_content:
            return JSONResponse(status_code=400, content={"error": "No readable text found at the link."})
        # Generate unique filename
        audio_filename = f"link_{uuid.uuid4().hex[:8]}.mp3"
        audio_file_path = os.path.join(AUDIO_DIR, audio_filename)
        tts = gTTS(text=text_content, lang='en', tld='com')
        tts.save(audio_file_path)
        return {"audio_file": audio_filename}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/text-to-audio/")
def text_to_audio(text: str = Form(...)):
    try:
        text_content = text.strip()
        if not text_content:
            return JSONResponse(status_code=400, content={"error": "No text provided."})
        audio_filename = f"text_{uuid.uuid4().hex[:8]}.mp3"
        audio_file_path = os.path.join(AUDIO_DIR, audio_filename)
        tts = gTTS(text=text_content, lang='en', tld='com')
        tts.save(audio_file_path)
        return {"audio_file": audio_filename}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
