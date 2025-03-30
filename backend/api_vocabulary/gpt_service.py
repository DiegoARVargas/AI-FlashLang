import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_example_sentence(word: str, translation: str) -> tuple[str, str]:
    prompt = (
        f"Generate a simple English sentence using the word '{word}' "
        f"(which means '{translation}' in Spanish). "
        f"Then translate the sentence to Spanish."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=120
    )

    result = response.choices[0].message.content.strip().split("\n")

    # Intentamos dividir el resultado si vienen separados
    if len(result) >= 2:
        example = result[0]
        translation = result[1]
    else:
        # Si no viene separado, se devuelve como está
        example = translation = result[0]

    return example, translation
