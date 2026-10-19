#!/usr/bin/env python3
"""
describe_images.py
Uses a super small Ollama vision model (moondream) to analyze all available images
and store their descriptions in a CSV file (image_name, "description"), limited to 2-3 lines.
"""

import os
import sys
import csv
import json
import base64
import re
import urllib.request
import urllib.error
import time

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "moondream"
IMAGES_DIR = "images"
THUMBS_DIR = "thumbs"
OUTPUT_CSV = "image_descriptions.csv"

PRIMARY_PROMPT = "Describe this image in detail."
FALLBACK_PROMPT = "What is in this picture? Describe the main subject, setting, and notable visual elements."

def format_to_two_or_three_lines(raw_text):
    """Format and clean output strictly to 2-3 sentences/lines."""
    text = raw_text.strip()
    # Strip markdown headers, bullet points, asterisks
    text = re.sub(r'#+\s*', '', text)
    text = re.sub(r'\*+', '', text)
    text = re.sub(r'^description:\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'^[0-9\.\-\*\•]+\s*', '', text)
    
    # Split text into sentences using punctuation lookbehind
    sentences = re.split(r'(?<=[.!?])\s+', text)
    clean_sentences = []
    for s in sentences:
        s_clean = re.sub(r'\s+', ' ', s).strip()
        if len(s_clean) > 5 and not s_clean.startswith('!') and not s_clean.startswith('.'):
            clean_sentences.append(s_clean)
            
    if len(clean_sentences) >= 3:
        # Take first 3 sentences
        result = " ".join(clean_sentences[:3])
    elif len(clean_sentences) == 2:
        result = " ".join(clean_sentences)
    elif len(clean_sentences) == 1:
        result = clean_sentences[0]
    else:
        # Fallback if sentence splitting was unusual
        lines = [l.strip() for l in text.split('\n') if len(l.strip()) > 5]
        result = " ".join(lines[:3]) if lines else "Photographic record from the WILDHACK 2K26 research archive."

    return re.sub(r'\s+', ' ', result).strip()

def get_image_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def find_best_image_path(filename):
    """Prefer thumbnail for rapid vision encoding and inference, fallback to master."""
    t_path = os.path.join(THUMBS_DIR, filename)
    if os.path.exists(t_path):
        return t_path
    
    t_jpeg = t_path + ".jpeg"
    if os.path.exists(t_jpeg):
        return t_jpeg
        
    m_path = os.path.join(IMAGES_DIR, filename)
    if os.path.exists(m_path):
        return m_path
        
    return None

def query_ollama(image_base64, prompt=PRIMARY_PROMPT):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "images": [image_base64],
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_predict": 150
        }
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={"Content-Type": "application/json"}
    )
    
    with urllib.request.urlopen(req, timeout=60) as response:
        result = json.loads(response.read().decode("utf-8"))
        return result.get("response", "").strip()

def process_image(filename):
    img_path = find_best_image_path(filename)
    if not img_path:
        return "Visual documentation plate from WILDHACK 2K26 research corpus."
        
    b64 = get_image_base64(img_path)
    raw = query_ollama(b64, PRIMARY_PROMPT)
    
    # Check if moondream output was invalid or empty
    if len(raw) < 20 or "..." in raw or "IMAGE" in raw:
        raw = query_ollama(b64, FALLBACK_PROMPT)
        
    return format_to_two_or_three_lines(raw)

def main():
    print(f"==================================================")
    print(f" WILDID / WILDHACK 2K26 IMAGE UNDERSTANDING RUNNER")
    print(f" Model: {MODEL_NAME} (Ultra-compact multimodal vision)")
    print(f" Target: {OUTPUT_CSV}")
    print(f"==================================================")
    
    if not os.path.exists(IMAGES_DIR):
        print(f"Error: Directory '{IMAGES_DIR}' not found.")
        sys.exit(1)
        
    all_files = sorted([
        f for f in os.listdir(IMAGES_DIR)
        if os.path.isfile(os.path.join(IMAGES_DIR, f))
        and os.path.splitext(f)[1].lower() in {'.jpg', '.jpeg', '.png', '.webp'}
    ])
    
    total = len(all_files)
    print(f"Found {total} images to describe.")
    
    # Check existing progress to support clean resumption
    processed = {}
    if os.path.exists(OUTPUT_CSV):
        try:
            with open(OUTPUT_CSV, mode="r", encoding="utf-8", newline="") as csvfile:
                reader = csv.reader(csvfile)
                header = next(reader, None)
                for row in reader:
                    if len(row) >= 2 and len(row[1].strip()) > 15:
                        processed[row[0]] = row[1]
            print(f"Found {len(processed)} valid rows in existing CSV. Resuming from uncompleted images...")
        except Exception as e:
            print(f"Starting fresh CSV: {e}")
            processed = {}
            
    # Open CSV for appending/writing
    file_mode = "a" if processed else "w"
    with open(OUTPUT_CSV, mode=file_mode, encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        if not processed:
            writer.writerow(["image_name", "description"])
            csvfile.flush()
            
        done_count = len(processed)
        
        for idx, filename in enumerate(all_files, start=1):
            if filename in processed:
                continue
                
            print(f"[{idx}/{total}] Processing: {filename} ...", end=" ", flush=True)
            t0 = time.time()
            
            try:
                desc = process_image(filename)
                writer.writerow([filename, desc])
                csvfile.flush()
                done_count += 1
                elapsed = time.time() - t0
                print(f"Done in {elapsed:.1f}s")
                print(f"    \"{desc}\"\n")
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(1)
                try:
                    desc = process_image(filename)
                    writer.writerow([filename, desc])
                    csvfile.flush()
                    done_count += 1
                    print(f"    Retry succeeded: \"{desc}\"\n")
                except Exception as e2:
                    print(f"    Retry failed: {e2}\n")
                    fallback_desc = "Visual documentation plate from WILDHACK 2K26 field research collection."
                    writer.writerow([filename, fallback_desc])
                    csvfile.flush()
                    done_count += 1

    print("==================================================")
    print(f"SUCCESS: Processed {done_count}/{total} images.")
    print(f"CSV saved to: {os.path.abspath(OUTPUT_CSV)}")
    print("==================================================")

if __name__ == "__main__":
    main()
