import os
from PIL import Image, ImageDraw, ImageFont
import random

# Ensure directory exists
output_dir = "static/images/assessment"
os.makedirs(output_dir, exist_ok=True)

# Define questions to match main.py exactly
questions_data = [
    ("q1", "Social Battery", "social_battery"),
    ("q2", "Communication", "communication"),
    ("q3", "Workspace", "workspace"),
    ("q4", "Problem Solving", "problem_solving"),
    ("q5", "Meeting Role", "meeting_role"),
    ("q6", "Learning Style", "learning_style"),
    ("q7", "Goal: Path", "goal_path"),
    ("q8", "Goal: Vision", "goal_vision"),
    ("q9", "Goal: Speed", "goal_speed"),
    ("q10", "Goal: Choice", "goal_choice")
]

options = ["a", "b"]

# Bright, modern colors
colors = [
    (99, 102, 241), # Indigo
    (236, 72, 153), # Pink
    (16, 185, 129), # Emerald
    (245, 158, 11), # Amber
    (59, 130, 246), # Blue
    (139, 92, 246)  # Violet
]

def create_placeholder(filename, text, subtext):
    width, height = 800, 500
    color = random.choice(colors)
    
    img = Image.new('RGB', (width, height), color=color)
    d = ImageDraw.Draw(img)
    
    # Try to load a font, fall back to default
    try:
        # MacOS usually has Arial
        font_large = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 60)
        font_small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 30)
    except:
        try:
             font_large = ImageFont.truetype("/Library/Fonts/Arial.ttf", 60)
             font_small = ImageFont.truetype("/Library/Fonts/Arial.ttf", 30)
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()

    # Draw Text centered
    def draw_centered(text, font, y_offset, fill=(255, 255, 255)):
        bbox = d.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) / 2
        y = (height - text_height) / 2 + y_offset
        d.text((x, y), text, fill=fill, font=font)

    draw_centered(text, font_large, -30)
    draw_centered(subtext, font_small, 40)
    
    path = os.path.join(output_dir, filename)
    img.save(path)
    print(f"Created {path}")

# Generate images
print("Generating images...")
for q_prefix, q_title, q_slug in questions_data:
    for opt in options:
        # Expected format: q1_social_battery_a.png
        filename = f"{q_prefix}_{q_slug}_{opt}.png"
        create_placeholder(filename, q_title, f"Option {opt.upper()}")

print("All placeholders created.")
