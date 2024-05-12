import whisper
import os

def transcribe(recaptcha_location,verbose=False):
    model = whisper.load_model("base")
    if model is not None:
        result = model.transcribe(recaptcha_location)
        transcribed_text = result["text"].strip().replace(',', '').replace('.', '')
        transcribed_text = transcribed_text.lower()
        os.remove(recaptcha_location)
        if verbose:
            print(f'text transcribed by whisper : {transcribed_text}')
        return transcribed_text
    else:
        print("Failed to load the model.")