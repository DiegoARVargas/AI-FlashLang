import genanki

FLASHLANG_MODEL_ID = 1607392319

flashlang_model = genanki.Model(
    FLASHLANG_MODEL_ID,
    name="FlashLang Card Model",
    fields=[
        {"name": "Word"},
        {"name": "Translation"},
        {"name": "Example"},
        {"name": "ExampleTranslation"},
        {"name": "WordAudio"},
        {"name": "SentenceAudio"},
        {"name": "Image"}
    ],
    templates=[
        {
            "name": "FlashLang Card",
            "qfmt": "<div style='font-size: 30px;'>{{Word}}</div><br>{{WordAudio}}",
            "afmt": "{{FrontSide}}<hr>"
                    "<div style='font-size: 20px;'>{{Translation}}</div>"
                    "<div style='margin-top: 10px;'>{{Example}}</div>"
                    "<div style='color: gray;'>{{ExampleTranslation}}</div>"
                    "{{SentenceAudio}}"
                    "<div>{{Image}}</div>"
        }
    ],
    css="""
        .card {
            font-family: Arial;
            text-align: center;
            color: #333;
            background-color: #f9f9f9;
            background-image: url('_flashy.png');
            background-size: cover;
            background-position: center;
        }
    """
)
