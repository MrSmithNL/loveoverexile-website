#!/usr/bin/env python3
"""
Generate 6 missing images with Malcolm's updated guidelines:
- love-over-exile in filenames (fully spelled out, not LOE)
- Real people shown from behind / side profile (Gemini API limitation: no frontal faces)
- Detailed, scene-specific prompts matching parental alienation themes
- Style matching professional photography from avada-recruitment reference images
- Web-optimised before upload

Images:
  1. love-over-exile-home-hero-1.jpg  — replaces background_slider_images ID 1058
  2. love-over-exile-home-hero-2.jpg  — replaces background_slider_images ID 1057
  3. love-over-exile-home-card-understanding.jpg — replaces loe-home-card-understanding.jpg
  4. love-over-exile-home-card-survival.jpg      — replaces loe-home-card-survival.jpg
  5. love-over-exile-home-card-freedom.jpg       — replaces loe-home-card-freedom.jpg
  6. love-over-exile-about-portrait.jpg          — replaces about-recruitment-02.jpg (for About page)

Note on style reference: The Gemini API key does not support direct style reference images
(that requires Vertex AI). Style is described in the prompt instead:
  "Professional photography style matching Avada Recruitment demo — cinematic lighting,
   warm amber tones, shallow depth of field, high-quality editorial photography"
"""

import os
import sys
import base64
import json
import io
import time
import requests
from pathlib import Path

import warnings
warnings.filterwarnings('ignore')

# Load .env
env_path = Path(__file__).parent.parent / '.env'
env_vars = {}
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, v = line.split('=', 1)
            env_vars[k.strip()] = v.strip()

GOOGLE_AI_API_KEY = env_vars['GOOGLE_AI_API_KEY']
WP_SITE_URL = env_vars['WP_SITE_URL'].rstrip('/')
WP_USERNAME = env_vars['WP_USERNAME']
WP_APP_PASSWORD = env_vars['WP_APP_PASSWORD']

# Style prefix — matches the visual quality of the Avada Recruitment reference images
STYLE = (
    'Professional editorial photography, warm amber and honey tones, '
    'shallow depth of field, cinematic composition, high detail, '
    'realistic and authentic, moody yet hopeful atmosphere'
)

# Images to generate
# (filename, aspect_ratio, max_dim_w, max_dim_h, max_kb, quality, prompt)
IMAGES = [
    (
        'love-over-exile-home-hero-1.jpg',
        '16:9', 1920, 1080, 150, 82,
        (
            f'A wide, cinematic scene of a man in his late forties, seen from behind, '
            f'standing alone at a large rain-streaked window in a quiet, dimly lit apartment at night. '
            f'His shoulders are slightly bowed under the weight of unspoken grief. '
            f'On the windowsill beside him, a framed family photograph is barely visible. '
            f'The city lights outside glow in soft blues and ambers, creating a contrast between '
            f'the cold world outside and the warmth of the room behind him. '
            f'The scene evokes the quiet desolation of parental estrangement — a parent separated '
            f'from their child, alone but not without hope. '
            f'{STYLE}. No text, no watermark, no children visible.'
        ),
    ),
    (
        'love-over-exile-home-hero-2.jpg',
        '16:9', 1920, 1080, 150, 82,
        (
            f'A wide, cinematic scene of a man in his mid-forties, seen in three-quarter profile, '
            f'sitting on a wooden park bench at golden hour in autumn. '
            f'He sits upright with a quiet dignity, hands resting on his knees, looking toward '
            f'a children\'s playground in the soft-focus distance. His expression is one of '
            f'patient, enduring love — a parent who has not given up. '
            f'Fallen leaves surround the bench. The late afternoon sun casts long, warm shadows. '
            f'The image captures the emotional reality of parental alienation: watching from a '
            f'distance, holding onto love despite everything. '
            f'{STYLE}. No text, no watermark, no children in sharp focus.'
        ),
    ),
    (
        'love-over-exile-home-card-understanding.jpg',
        '4:3', 900, 675, 90, 80,
        (
            f'An over-the-shoulder scene of a man in his forties, seated at a home office desk '
            f'in the evening, carefully reading through legal documents, court papers, and '
            f'psychological research spread before him. '
            f'A warm desk lamp illuminates the papers. His posture communicates focused determination '
            f'— a parent trying to understand what is happening to his family. '
            f'Post-it notes, a legal pad with handwritten notes, and highlighted documents '
            f'surround him. The scene represents the search for understanding in the face of '
            f'parental alienation — researching the system, the tactics, the psychology. '
            f'{STYLE}. No text on documents is readable, no watermark.'
        ),
    ),
    (
        'love-over-exile-home-card-survival.jpg',
        '4:3', 900, 675, 90, 80,
        (
            f'A man in his mid-forties, seen from behind, walking purposefully along a forest path '
            f'in early morning. Ground mist hovers at ankle height. The path winds forward through '
            f'dense trees, with golden morning light breaking through the canopy ahead. '
            f'His posture is upright and determined — not defeated, but walking forward with '
            f'quiet resilience despite the difficulty of the journey. '
            f'The image represents the survival phase of parental alienation: the long walk through '
            f'pain toward something better, one step at a time. '
            f'{STYLE}. No text, no watermark.'
        ),
    ),
    (
        'love-over-exile-home-card-freedom.jpg',
        '4:3', 900, 675, 90, 80,
        (
            f'A man in his late forties, seen in side profile, sitting cross-legged on a hillside '
            f'or cliff overlooking the ocean. His face is turned slightly upward, eyes gently closed, '
            f'a subtle peaceful expression. The sky behind him is a vast expanse of warm sunrise '
            f'colours — gold, pink, and blue. '
            f'His posture is open and relaxed — not tense, not in pain. '
            f'The image represents the inner freedom that can be found after years of pain from '
            f'parental alienation: the radical acceptance, the surrender, the unconditional love '
            f'that Viktor Frankl called the last human freedom. '
            f'{STYLE}. No text, no watermark.'
        ),
    ),
    (
        'love-over-exile-about-portrait.jpg',
        '3:4', 800, 1067, 100, 80,
        (
            f'A man in his late forties, seen from slightly behind and to the side, sitting at a '
            f'wooden writing desk by a large window. Morning light streams in from the window. '
            f'He is writing in a notebook, surrounded by books, printed research papers, and '
            f'handwritten notes. A cup of coffee rests beside his notebook. '
            f'The scene conveys someone who has lived through something profound and is now '
            f'translating that experience into words — a writer and survivor. '
            f'The bookshelves behind him suggest a man of depth and learning. '
            f'The image represents Malcolm Smith, the author of Love Over Exile: a man who '
            f'walked through ten years of parental alienation and came out the other side with '
            f'a story worth telling. '
            f'{STYLE}. No full face visible, no text, no watermark.'
        ),
    ),
]

# Map: new filename → replacement info
# For cards: the home page already has loe-home-card-*.jpg URLs to replace
# For hero: replace background_slider_images IDs
CARD_REPLACEMENTS = {
    'love-over-exile-home-card-understanding.jpg': 'loe-home-card-understanding.jpg',
    'love-over-exile-home-card-survival.jpg':      'loe-home-card-survival.jpg',
    'love-over-exile-home-card-freedom.jpg':       'loe-home-card-freedom.jpg',
}
HOME_PAGE_ID = 1023


def generate_image(client, filename, aspect_ratio, prompt):
    from google.genai import types
    resp = client.models.generate_images(
        model='imagen-4.0-generate-001',
        prompt=prompt,
        config=types.GenerateImagesConfig(
            numberOfImages=1,
            aspectRatio=aspect_ratio,
            outputMimeType='image/jpeg',
        )
    )
    if not resp.generated_images:
        raise ValueError('No images returned — safety filter or empty response')
    return resp.generated_images[0].image.image_bytes


def optimise_image(raw_bytes, max_w, max_h, max_kb, quality):
    from PIL import Image
    img = Image.open(io.BytesIO(raw_bytes)).convert('RGB')
    if img.width > max_w or img.height > max_h:
        img.thumbnail((max_w, max_h), Image.LANCZOS)
    for q in range(quality, 45, -5):
        buf = io.BytesIO()
        img.save(buf, format='JPEG', quality=q, optimize=True)
        size_kb = buf.tell() // 1024
        if size_kb <= max_kb:
            print(f'    Optimised: {img.width}×{img.height}px, {size_kb} KB (q={q})')
            return buf.getvalue()
    print(f'    Note: could not reach {max_kb} KB target — using q=45')
    return buf.getvalue()


def upload_to_wordpress(img_bytes, filename):
    wp_auth = base64.b64encode(f"{WP_USERNAME}:{WP_APP_PASSWORD}".encode()).decode()
    headers = {
        'Authorization': f'Basic {wp_auth}',
        'Content-Type': 'image/jpeg',
        'Content-Disposition': f'attachment; filename="{filename}"',
    }
    resp = requests.post(
        f'{WP_SITE_URL}/wp-json/wp/v2/media',
        headers=headers, data=img_bytes, timeout=60,
    )
    if resp.status_code in (200, 201):
        d = resp.json()
        url = d.get('source_url', '')
        wp_id = d.get('id', '?')
        print(f'    Uploaded: ID {wp_id} → {url}')
        return url, wp_id
    else:
        raise RuntimeError(f'Upload failed: {resp.status_code} — {resp.text[:200]}')


def get_page_content(page_id):
    wp_auth = base64.b64encode(f"{WP_USERNAME}:{WP_APP_PASSWORD}".encode()).decode()
    headers = {'Authorization': f'Basic {wp_auth}'}
    resp = requests.get(
        f'{WP_SITE_URL}/wp-json/wp/v2/pages/{page_id}?context=edit',
        headers=headers, timeout=30
    )
    return resp.json().get('content', {}).get('raw', '')


def update_page(page_id, content):
    wp_auth = base64.b64encode(f"{WP_USERNAME}:{WP_APP_PASSWORD}".encode()).decode()
    headers = {'Authorization': f'Basic {wp_auth}', 'Content-Type': 'application/json'}
    resp = requests.post(
        f'{WP_SITE_URL}/wp-json/wp/v2/pages/{page_id}',
        headers=headers,
        json={'content': content, 'status': 'draft'},
        timeout=60,
    )
    if resp.status_code not in (200, 201):
        raise RuntimeError(f'Page update failed: {resp.status_code}')
    print(f'  Page {page_id} updated successfully (draft)')


def main():
    from google import genai
    client = genai.Client(api_key=GOOGLE_AI_API_KEY)

    print('=' * 60)
    print('Love Over Exile — Image Generation v3')
    print('Missing images + updated naming + real people prompts')
    print('=' * 60)

    output_dir = Path('/tmp/loe-images-v3')
    output_dir.mkdir(exist_ok=True)

    url_mapping = {}   # filename → (wp_url, wp_id)

    for filename, aspect, max_w, max_h, max_kb, quality, prompt in IMAGES:
        print(f'\n[{filename}]')
        print(f'  Aspect: {aspect}  |  Target: max {max_kb} KB')

        raw_path = output_dir / f'raw-{filename}'
        opt_path = output_dir / filename

        # Generate
        if raw_path.exists():
            print('  [cached] using cached raw image')
            raw_bytes = raw_path.read_bytes()
        else:
            try:
                raw_bytes = generate_image(client, filename, aspect, prompt)
                raw_path.write_bytes(raw_bytes)
                print(f'  Generated: {len(raw_bytes)//1024} KB raw')
            except Exception as e:
                print(f'  ERROR generating: {e}')
                continue

        # Optimise
        if opt_path.exists():
            print('  [cached] using cached optimised image')
            opt_bytes = opt_path.read_bytes()
        else:
            try:
                opt_bytes = optimise_image(raw_bytes, max_w, max_h, max_kb, quality)
                opt_path.write_bytes(opt_bytes)
            except Exception as e:
                print(f'  ERROR optimising: {e}')
                continue

        # Upload
        try:
            wp_url, wp_id = upload_to_wordpress(opt_bytes, filename)
            url_mapping[filename] = (wp_url, wp_id)
        except Exception as e:
            print(f'  ERROR uploading: {e}')

        time.sleep(1)

    print(f'\n\nUploaded: {len(url_mapping)}/{len(IMAGES)} images')

    if not url_mapping:
        print('No images uploaded — skipping page update')
        return

    # Save mapping
    mapping = {k: {'url': v[0], 'id': v[1]} for k, v in url_mapping.items()}
    (output_dir / 'url-mapping.json').write_text(json.dumps(mapping, indent=2))

    # Update home page
    print(f'\nFetching home page (ID {HOME_PAGE_ID})...')
    content = get_page_content(HOME_PAGE_ID)
    original = content
    replaced = 0

    # 1. Replace card URLs
    for new_filename, old_v2_filename in CARD_REPLACEMENTS.items():
        if new_filename not in url_mapping:
            print(f'  SKIP card {new_filename} — not uploaded')
            continue
        new_url = url_mapping[new_filename][0]
        # Cards were uploaded in v2 run with paths like:
        old_url = f'{WP_SITE_URL}/wp-content/uploads/2026/02/{old_v2_filename}'
        if old_url in content:
            content = content.replace(old_url, new_url)
            print(f'  Replaced card: {old_v2_filename} → {new_filename}')
            replaced += 1
        else:
            print(f'  WARN: card URL not found in page: {old_url}')
            # Try to find any URL containing the old filename
            import re
            matches = re.findall(rf'https?://[^"]*{re.escape(old_v2_filename)}', content)
            if matches:
                for m in matches:
                    content = content.replace(m, new_url)
                    print(f'    Replaced alt URL: {m} → {new_url}')
                    replaced += 1

    # 2. Replace hero slider media IDs
    hero_1 = url_mapping.get('love-over-exile-home-hero-1.jpg')
    hero_2 = url_mapping.get('love-over-exile-home-hero-2.jpg')

    if hero_1 and hero_2:
        new_id_1 = hero_1[1]
        new_id_2 = hero_2[1]
        old_slider = 'background_slider_images="1058,1057"'
        new_slider = f'background_slider_images="{new_id_1},{new_id_2}"'
        if old_slider in content:
            content = content.replace(old_slider, new_slider)
            print(f'  Replaced slider IDs: 1058,1057 → {new_id_1},{new_id_2}')
            replaced += 1
        else:
            # Try any existing slider IDs pattern
            import re
            m = re.search(r'background_slider_images="(\d+,\d+)"', content)
            if m:
                content = content.replace(m.group(0), new_slider)
                print(f'  Replaced slider IDs (found: {m.group(1)}) → {new_id_1},{new_id_2}')
                replaced += 1
            else:
                print('  WARN: background_slider_images not found in page content')

    print(f'\nTotal replacements: {replaced}')

    if content != original:
        update_page(HOME_PAGE_ID, content)
        (output_dir / 'home-final.txt').write_text(content)
        print('Updated content saved to /tmp/loe-images-v3/home-final.txt')
    else:
        print('WARNING: No changes made to content')

    print('\nAbout portrait (love-over-exile-about-portrait.jpg):')
    if 'love-over-exile-about-portrait.jpg' in url_mapping:
        print(f'  Ready for About page → {url_mapping["love-over-exile-about-portrait.jpg"][0]}')
    print('\nDone!')


if __name__ == '__main__':
    main()
