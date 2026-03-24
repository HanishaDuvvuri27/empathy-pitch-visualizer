import argparse
import os
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    Image = None


def segment_narrative(text: str):
    # Basic sentence split; ensure at least 3 segments.
    raw_segments = [s.strip() for s in text.replace('!', '.').replace('?', '.').split('.') if s.strip()]
    if len(raw_segments) >= 3:
        return raw_segments[:3]

    # fallback if less than 3
    lines = text.strip().split('\n')
    if len(lines) >= 3:
        return [l for l in lines[:3] if l.strip()]

    # Final fallback: split by comma and pad to 3
    pieces = [p.strip() for p in text.split(',') if p.strip()]
    while len(pieces) < 3:
        pieces.append("...")
    return pieces[:3]


def enhance_prompt(segment: str):
    return f"A vivid illustration of: {segment}. High contrast colors, cinematic composition, expressive lighting."


def generate_placeholder_image(prompt: str, out_path: str):
    if Image is None:
        raise RuntimeError("Please install Pillow (pip install pillow)")

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    img = Image.new('RGB', (1024, 768), color=(245, 245, 245))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.load_default()
    except Exception:
        font = None

    draw.text((20, 20), 'Prompt:', fill='black', font=font)
    draw.text((20, 50), prompt, fill='darkslategray', font=font)
    img.save(out_path)
    return out_path


def render_html(segments, image_paths, output_html):
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write('<!doctype html>\n<html><head><meta charset="utf-8"><title>Pitch Visualization</title></head><body>\n')
        f.write('<h1>Pitch Visualizer Output (partial demo)</h1>\n')
        for i, (seg, img) in enumerate(zip(segments, image_paths), start=1):
            f.write(f'<div style="margin-bottom:30px;">\n')
            f.write(f'<h2>Scene {i}</h2>\n')
            f.write(f'<p>{seg}</p>\n')
            f.write(f'<img src="{Path(img).name}" style="max-width:80%; border: 1px solid #ccc;" alt="Scene {i}">\n')
            f.write('</div>\n')
        f.write('</body></html>')


def main():
    parser = argparse.ArgumentParser(description="Pitch Visualizer CLI (partial implementation)")
    parser.add_argument("--text", required=False, help="Narrative text to visualize")
    parser.add_argument("--output-dir", default="pitch_output", help="Output directory for assets")
    args = parser.parse_args()

    text = args.text
    if not text:
        text = input("Enter narrative text to visualize (3-5 sentences): ")

    segments = segment_narrative(text)
    enhanced_prompts = [enhance_prompt(s) for s in segments]

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    image_paths = []
    for idx, prompt in enumerate(enhanced_prompts, start=1):
        out_file = output_dir / f"scene_{idx}.png"
        image_paths.append(str(out_file))
        generate_placeholder_image(prompt, out_file)

    html_path = output_dir / "storyboard.html"
    render_html(segments, image_paths, html_path)

    print(f"Generated {len(image_paths)} placeholder images in {output_dir}")
    print(f"Storyboard ready at {html_path}")


if __name__ == "__main__":
    main()
