from gtts import gTTS
import os

def texts_to_audio(text_files_folder, audio_output_folder, lang='en', voice='com'):
    audio_paths = []
    text_files = [f for f in os.listdir(text_files_folder) if f.endswith('.txt')]

    for text_file in text_files:
        text_file_path = os.path.join(text_files_folder, text_file)
        with open(text_file_path, "r", encoding="utf-8") as file:
            text_content = file.read().strip()

        if text_content:
            tts = gTTS(text=text_content, lang=lang, tld=voice)
            audio_filename = os.path.splitext(text_file)[0] + ".mp3"
            audio_file_path = os.path.join(audio_output_folder, audio_filename)
            tts.save(audio_file_path)
            audio_paths.append(audio_file_path)

            print(f"Audio created: {audio_file_path}")
        else:
            print(f"Skipped empty file: {text_file}")

    return audio_paths

if __name__ == "__main__":
    texts_folder = "pdf_texts"  # Edit if needed
    audio_folder = "pdf_audio"

    os.makedirs(audio_folder, exist_ok=True)

    # For a female voice, standard US English use ('com')
    texts_to_audio(texts_folder, audio_folder, lang='en', voice='com')

    print("Text to audio conversion completed.")
