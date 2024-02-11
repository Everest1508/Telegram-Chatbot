from translate import Translator
from langdetect import detect

def detect_language(text):
    try:
        detected_lang = detect(text)
        return detected_lang
    except:
        return "Unknown"

def translate_marathi_to_english(text):
    translator = Translator(to_lang="en", from_lang=detect_language(text))
    translation = translator.translate(text)
    return translation

# Example usage
marathi_text = "तुम्ही कसे आहात?"
english_translation = translate_marathi_to_english(marathi_text)
print(f"Marathi: {marathi_text}")
print(f"English: {english_translation}")
