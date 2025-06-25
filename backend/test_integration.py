import os
import requests

def test_link_to_audio():
    url = os.environ.get("API_BASE_URL", "http://backend:8080")
    link = "https://www.example.com"
    resp = requests.post(f"{url}/link-to-audio/", data={"link": link})
    assert resp.status_code == 200
    data = resp.json()
    assert "audio_file" in data
    audio_url = f"{url}/audio/{data['audio_file']}"
    audio_resp = requests.get(audio_url)
    assert audio_resp.status_code == 200
    assert audio_resp.headers["content-type"].startswith("audio/")

def test_text_to_audio():
    url = os.environ.get("API_BASE_URL", "http://backend:8080")
    text = "Hello, this is a test."
    resp = requests.post(f"{url}/text-to-audio/", data={"text": text})
    assert resp.status_code == 200
    data = resp.json()
    assert "audio_file" in data
    audio_url = f"{url}/audio/{data['audio_file']}"
    audio_resp = requests.get(audio_url)
    assert audio_resp.status_code == 200
    assert audio_resp.headers["content-type"].startswith("audio/")

def test_upload_pdf():
    url = os.environ.get("API_BASE_URL", "http://backend:8080")
    pdf_path = "test.pdf"
    # Create a simple PDF for testing
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Test PDF for integration.", ln=True)
    pdf.output(pdf_path)
    with open(pdf_path, "rb") as f:
        files = {"file": (pdf_path, f, "application/pdf")}
        resp = requests.post(f"{url}/upload-pdf/", files=files)
    os.remove(pdf_path)
    assert resp.status_code == 200
    data = resp.json()
    assert "audio_files" in data
    assert isinstance(data["audio_files"], list)
    # Optionally, check audio file download
    for audio_file in data["audio_files"]:
        audio_url = f"{url}/audio/{audio_file}"
        audio_resp = requests.get(audio_url)
        assert audio_resp.status_code == 200
        assert audio_resp.headers["content-type"].startswith("audio/")

if __name__ == "__main__":
    test_link_to_audio()
    test_text_to_audio()
    test_upload_pdf()
    print("All integration tests passed.")
