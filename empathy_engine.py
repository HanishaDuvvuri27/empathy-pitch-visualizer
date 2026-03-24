import argparse
import os
from pathlib import Path

try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
except ImportError:
    SentimentIntensityAnalyzer = None

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

EMOTION_PROFILES = {
    "positive": {"rate": 180, "volume": 1.0, "voice_hint": "female"},
    "neutral": {"rate": 150, "volume": 0.8, "voice_hint": "male"},
    "negative": {"rate": 120, "volume": 0.7, "voice_hint": "male"},
}


def detect_emotion(text: str) -> str:
    if not SentimentIntensityAnalyzer:
        raise RuntimeError("Please install vaderSentiment (pip install vaderSentiment)")

    sia = SentimentIntensityAnalyzer()
    scores = sia.polarity_scores(text)
    compound = scores["compound"]

    if compound >= 0.2:
        return "positive"
    elif compound <= -0.2:
        return "negative"
    else:
        return "neutral"


def map_emotion_to_params(emotion: str) -> dict:
    profile = EMOTION_PROFILES.get(emotion, EMOTION_PROFILES["neutral"])
    return profile


def build_voice_kwargs(profile: dict) -> dict:
    # pyttsx3 does not support explicit pitch control in a cross-platform way.
    # We'll emulate pitch tendency via changing preset voices if available.
    return {
        "rate": profile["rate"],
        "volume": profile["volume"],
        "voice_hint": profile["voice_hint"],
    }


def synthesize_to_file(text: str, output_file: str, profile: dict):
    if not pyttsx3:
        raise RuntimeError("Please install pyttsx3 (pip install pyttsx3)")

    engine = pyttsx3.init()
    engine.setProperty("rate", profile["rate"])
    engine.setProperty("volume", profile["volume"])

    # Attempt voice selection if available
    voices = engine.getProperty("voices")
    hint = profile.get("voice_hint", "")
    for v in voices:
        if hint.lower() in v.name.lower() or hint.lower() in getattr(v, "id", "").lower():
            engine.setProperty("voice", v.id)
            break

    output_file = str(Path(output_file).with_suffix(".wav"))
    engine.save_to_file(text, output_file)
    engine.runAndWait()
    return output_file


def main():
    parser = argparse.ArgumentParser(description="Empathy Engine CLI (partial implementation)")
    parser.add_argument("--text", required=False, help="Text to synthesize")
    parser.add_argument("--output", default="empathy_output.wav", help="Output WAV file")
    args = parser.parse_args()

    text = args.text
    if not text:
        text = input("Enter text for empathy engine: ")

    emotion = detect_emotion(text)
    profile = map_emotion_to_params(emotion)
    output_path = synthesize_to_file(text, args.output, profile)

    print(f"Emotion detected: {emotion}")
    print(f"Applied parameters: rate={profile['rate']} volume={profile['volume']}")
    print(f"Audio output written to: {output_path}")


if __name__ == "__main__":
    main()
