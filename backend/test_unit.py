import os
import tempfile
import shutil
import pytest
from main import pdf_to_images, images_to_text, texts_to_audio
from gtts import gTTS

@pytest.fixture
def sample_text_file():
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, "sample.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("Hello world!")
    yield file_path
    shutil.rmtree(temp_dir)

def test_texts_to_audio(sample_text_file):
    temp_dir = tempfile.mkdtemp()
    audio_files = texts_to_audio([sample_text_file], temp_dir)
    assert len(audio_files) == 1
    assert os.path.exists(audio_files[0])
    shutil.rmtree(temp_dir)

def test_gtts_direct():
    tts = gTTS(text="Hello test", lang='en')
    temp_dir = tempfile.mkdtemp()
    audio_path = os.path.join(temp_dir, "test.mp3")
    tts.save(audio_path)
    assert os.path.exists(audio_path)
    shutil.rmtree(temp_dir)
