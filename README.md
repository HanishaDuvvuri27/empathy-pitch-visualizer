# AI Assignment Partial Implementation

This repository implements partial solutions for two challenges extracted from the assessment PDF.

## Challenge 1: The Empathy Engine (Partial)
- Text input (CLI)
- Emotion detection (VADER sentiment)
- Emotion-to-voice mapping (Positive/Neutral/Negative)
- Vocal parameter modulation (rate, volume, voice selection)
- Audio output: writes `.wav` via pyttsx3

> Note: This implementation does not include advanced pitch control via SSML or external TTS APIs.

### Run
1. Install dependencies:

```bash
python -m pip install pyttsx3 vaderSentiment
```

2. Generate audio:

```bash
python empathy_engine.py --text "I am thrilled to be part of this conversation." --output empathy.wav
```

## Challenge 2: The Pitch Visualizer (Partial)
- Text input (CLI)
- Narrative segmentation (simple split)
- Prompt engineering (enhanced prompt template)
- Image generation: local placeholder image created via Pillow
- Storyboard presentation: generates `storyboard.html` with image panels

> Note: This implementation does not call an external image generation API (e.g., DALL-E or Stable Diffusion), to keep it runnable without API keys.

### Run
1. Install dependencies:

```bash
python -m pip install pillow
```

2. Generate storyboard:

```bash
python pitch_visualizer.py --text "The team closed the deal and celebrated. Later, the client gave positive feedback. Next, they planned the next campaign." --output-dir pitch_out
```

## Missing must-have coverage (per instructions)
- Challenge 1: Most core requirements implemented. Secondary intensity scaling and LLm pitch mapping are omitted.
- Challenge 2: Image API generation replaced with placeholder image generation to satisfy local demonstration.

## Notes
- Please run the scripts in your workspace root (`AI _ ASSIGNEMNT_ SUBMIS`).
- This is a progress checkpoint for review and later push.
