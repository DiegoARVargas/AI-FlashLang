import genanki
import random

def get_flashlang_model(allow_duplicates=False):
    model_id = 1607392319
    if allow_duplicates:
        model_id = random.randrange(1 << 30, 1 << 31)

    return genanki.Model(
        model_id=model_id,
        name="AIFlashLang Model",
        fields=[
            {"name": "Word"},
            {"name": "Translation"},
            {"name": "Example"},
            {"name": "ExampleTranslation"},
            {"name": "Audio"},
            {"name": "ExampleAudio"},
            {"name": "Image"},
        ],
        templates=[
            {
                "name": "FlashLang Card",
                "qfmt": """
<style>
    .customCard {
        margin: 0 auto;
  
        position: relative;
        display: flex;
        justify-content: center;
        align-items: center;
    
        background-color: #0b0716;
        box-shadow: 1px 3px 10px rgba(18, 62, 119, 0.1);
        border-radius: 8px;
        min-height: 200px;
        max-width: 400px;
    
        font-weight: 500;
        font-size: 18px;
        font-family: \"Inter\", sans-serif;
        color: #fbfafe;
    }
    .horizontalPadding {
        width: 100%;
        padding-left: 16px;
        padding-right: 16px;
    }
    .targetWord {
        font-size: 26px;
        font-weight: 600;
    }
    .wordAudioButtonFront {
        position: absolute;
        top: 12px;
        right: 18px;
    }
    .replay-button {
        padding: 8px;
    }
    .replay-button svg {
        width: 28px;
        height: 28px;
    }
    .replay-button svg path {
        fill: #8369ed;
    }
    .replay-button svg circle {
        fill: none;
        stroke: none;
    }
</style>
  <div class=\"customCard horizontalPadding\">
    <div class=\"targetWord\">{{Word}}</div>
    <div class=\"wordAudioButtonFront\">{{Audio}}</div>
  </div>
  <script>
    document.addEventListener('DOMContentLoaded', function () {
      const audio = document.querySelector('.wordAudioButtonFront audio');
      if (audio) audio.play();
    });
  </script>
""",
                "afmt": """
<style>
    .customCard {
        margin: 0 auto;
  
        position: relative;
        display: flex;
        justify-content: center;
        align-items: center;
    
        background-color: #0b0716;
        box-shadow: 1px 3px 10px rgba(18, 62, 119, 0.1);
        border-radius: 8px;
        min-height: 200px;
        max-width: 400px;
    
        font-weight: 500;
        font-size: 18px;
        font-family: \"Inter\", sans-serif;
        color: #fbfafe;
    }
    .cardBack {
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
    
        padding-top: 24px;
        padding-bottom: 8px;
        padding-left: 16px;
        padding-right: 16px;
    }
    .targetWordContainer {
        margin-top: 8px;
        margin-bottom: 24px;
    }
    .targetWord {
        font-size: 26px;
        font-weight: 600;
    }
    .wordAudioButtonBack {
      margin-left: 8px;
    }
    .replay-button {
        padding: 8px;
    }
    .replay-button svg {
        width: 28px;
        height: 28px;
    }
    .replay-button svg path {
      fill: #8369ed;
    }
    .replay-button svg circle {
      fill: none;
      stroke: none;
    }
    .header {
      color: #9ca3af;
      font-weight: 500;
      margin-top: 12px;
      margin-bottom: 4px;
    }
    .dividerLine {
        width: 100%;
        border-bottom: 1px solid #e5e7eb;
        margin-top: 8px;
        margin-bottom: 8px;
    }
    .nightMode .dividerLine {
        border-color: #1f2937;
    }
    .definitionsList {
        list-style: none;
        margin: 0;
        padding: 0;
        padding-left: 16px;
    }
    .image img {
      width: 100%;
      height: auto;
      margin-top: 12px;
      margin-bottom: 12px;
    }
    .sentenceAudioButton {
      margin-left: 8px;
      cursor: pointer;
    }
    .sentenceTranslation {
        color: #6b7280;
        font-weight: 400;
        font-style: italic;
        padding-right: 15px;
        padding-top: 8px;
    }
  
    .nightMode .sentenceTranslation {
        color: #9ca3af;
    }
    .horizontalPadding {
        width: 100%;
        padding-left: 16px;
        padding-right: 16px;
    }
    .indent {
        margin-left: 12px;
    }
    .centerVertically {
        display: flex;
        align-items: center;
    }

  </style>
  <div class=\"customCard cardBack\">
    <div class=\"horizontalPadding centerVertically targetWordContainer\">
      <span class=\"targetWord\">{{Word}}</span>
      <span class=\"wordAudioButtonBack\">{{Audio}}</span>
    </div>
    
    <div class=\"dividerLine\"></div>

    {{#Translation}}
    <div class=\"horizontalPadding\">
      <div class=\"header\">Translation:</div>
        <div class=\"indent\">
            <ul class=\"definitionsList\">
                <li>{{Translation}}</li>
            </ul>
        </div>
    </div>
    {{/Translation}}
  
    {{#Image}}
    <div class=\"image\">{{Image}}</div>
    {{/Image}}

    <div class=\"dividerLine\"></div>

    {{#Example}}
    <div class=\"horizontalPadding\">
      <div class=\"header centerVertically\">Example:</div>
      <div class=\"indent\">
        <div class=\"centerVertically\" style=\"position: relative; gap: 5px\">
            <span>\"{{Example}}\"</span>
            <span class=\"sentenceAudioButton\">{{ExampleAudio}}</span>
        </div>
      </div>
      <div id=\"translatedSentence\" class=\"sentenceTranslation\">{{hint:ExampleTranslation}}</div>
    </div>
    {{/Example}}

    <div class=\"dividerLine\"></div>
    
  </div>
  <script>
    document.addEventListener('DOMContentLoaded', function () {
      document.querySelectorAll('.wordAudioButtonBack, .sentenceAudioButton').forEach(button => {
        const audio = button.querySelector('audio');
        if (audio) button.addEventListener('click', () => audio.play());
      });
  
      const wordAudio = document.querySelector('.wordAudioButtonBack audio');
      if (wordAudio) wordAudio.play();
      setTimeout(() => {
        const exampleAudio = document.querySelector('.sentenceAudioButton audio');
        if (exampleAudio) exampleAudio.play();
      }, 1000);
    });
  </script>
"""
            }
        ]
    )
