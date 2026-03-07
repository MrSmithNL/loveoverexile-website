#!/usr/bin/env python3
"""
Generate LOE images using Imagen 4, optimise for web, and upload to WordPress.
Then update the page's Avada shortcodes with the new image URLs.

Usage: python3 scripts/generate-images.py

Standards:
- SEO-friendly filenames: loe-[page]-[section]-[descriptor].jpg
- Web-optimised: resized + compressed JPEG, never raw API output
- No watermarks: Imagen 4 does not add watermarks
- Section-specific prompts: every image tailored to its placement

See ~/.claude/skills/website-image-generator/SKILL.md for full documentation.
"""

import os
import sys
import base64
import json
import time
import io
import requests
from pathlib import Path

# Load .env file
env_path = Path(__file__).parent.parent / '.env'
env_vars = {}
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            key, val = line.split('=', 1)
            env_vars[key.strip()] = val.strip()

GOOGLE_AI_API_KEY = env_vars['GOOGLE_AI_API_KEY']
WP_SITE_URL = env_vars['WP_SITE_URL'].rstrip('/')
WP_USERNAME = env_vars['WP_USERNAME']
WP_APP_PASSWORD = env_vars['WP_APP_PASSWORD']

# --- Web optimisation targets ---
# (max_width, max_height, quality, max_size_kb)
SIZE_PROFILES = {
    '16:9':  (1920, 1080, 82, 150),  # Wide section backgrounds
    '9:16':  (768,  1366, 82, 100),  # Mobile hero
    '4:3':   (900,  675,  80, 90),   # Cards and inline images
}

# --- Image definitions ---
# (seo_filename, aspect_ratio, prompt)
# Prompts are section-specific and describe subject, mood, lighting, style
IMAGES = [
    # ── Hero ──────────────────────────────────────────────────────────────────
    (
        'loe-home-hero-mobile.jpg',
        '9:16',
        (
            'A solitary figure stands at a large window in a quiet room at dusk, silhouetted against '
            'a soft golden-pink sky. The mood is contemplative and quietly hopeful — solitude with '
            'warmth on the horizon. Interior warm tones, cool twilight outside. Cinematic photography, '
            'high quality, dramatic light, no text, no watermark.'
        ),
    ),

    # ── Category cards (3) — represent three main sections of the book ────────
    (
        'loe-home-card-understanding.jpg',
        '4:3',
        (
            'An open hardcover book on a wooden desk, surrounded by handwritten research notes, '
            'reading glasses, and a warm desk lamp casting golden light. The atmosphere is scholarly '
            'and purposeful — the light of understanding. Close-up lifestyle photography, warm amber '
            'tones, clean composition, no text, no watermark.'
        ),
    ),
    (
        'loe-home-card-survival.jpg',
        '4:3',
        (
            'A winding forest path in early morning mist, golden light breaking through the canopy '
            'ahead, symbolising a difficult journey with hope at the end. The path leads forward into '
            'the light. Professional nature photography, moody yet hopeful atmosphere, rich greens and '
            'gold, no people visible, no text, no watermark.'
        ),
    ),
    (
        'loe-home-card-freedom.jpg',
        '4:3',
        (
            'Two open palms gently releasing a single white feather into warm sunrise light, shot from '
            'close up against a soft golden sky. The gesture represents release, surrender, and freedom. '
            'Studio photography, minimal and serene, warm light, shallow depth of field, no text, '
            'no watermark.'
        ),
    ),

    # ── Section backgrounds (4 full-width) ────────────────────────────────────
    (
        'loe-home-section-bg-understanding.jpg',
        '16:9',
        (
            'Wide atmospheric view of a grand library or formal reading room — tall bookshelves lining '
            'the walls, shafts of light from high windows illuminating motes of dust, rows of wooden '
            'desks. The mood is serious and institutional, representing research, law, and the pursuit '
            'of truth. Cinematic, no people, warm with cool shadows, no text, no watermark.'
        ),
    ),
    (
        'loe-home-section-bg-survival.jpg',
        '16:9',
        (
            'A dramatic wide landscape — a lone, winding path cuts through a dense misty forest at '
            'dawn, golden light breaking through the canopy far ahead. The scene is both challenging '
            'and hopeful: the way forward exists, even through darkness. Cinematic nature photography, '
            'deep greens and golds, no people, no text, no watermark.'
        ),
    ),
    (
        'loe-home-section-bg-freedom.jpg',
        '16:9',
        (
            'A vast, open ocean at sunrise — deep blue water reflecting warm gold and pink sky, '
            'the horizon stretching to infinity. The feeling is boundless freedom and possibility '
            'after great difficulty. Shot from water level on a calm morning. Cinematic seascape, '
            'sweeping and serene, no people, no text, no watermark.'
        ),
    ),
    (
        'loe-home-section-bg-love.jpg',
        '16:9',
        (
            'A single lit candle glowing warmly in a dark, quiet room, its flame reflected softly '
            'on a polished wooden surface. Beside it, a small framed photograph faces away from '
            'camera. The mood is one of quiet, enduring love across distance — intimate and deeply '
            'human. Cinematic still life, warm amber tones, deep shadows, no text, no watermark.'
        ),
    ),

    # ── Section inline images (4 portrait, shown alongside text) ──────────────
    (
        'loe-home-inline-understanding.jpg',
        '4:3',
        (
            'A professional person in their 40s, seen from behind or in profile, carefully reading '
            'documents at a desk by a large window. Natural daylight. Books and folders around them. '
            'The mood is focused, analytical, and quietly determined. Professional lifestyle photography, '
            'warm neutral tones, no face shown, no text, no watermark.'
        ),
    ),
    (
        'loe-home-inline-survival.jpg',
        '4:3',
        (
            'A person in their 40s standing outdoors in early morning dappled light, seen from the '
            'side or slightly behind, looking out across a landscape. Their posture communicates quiet '
            'strength and forward resolve. Professional portrait photography, warm natural light, '
            'calm and resilient atmosphere, no text, no watermark.'
        ),
    ),
    (
        'loe-home-inline-freedom.jpg',
        '4:3',
        (
            'A person sitting outdoors in a peaceful garden or hillside, cross-legged, face gently '
            'tilted upward toward warm afternoon sunlight, eyes closed in stillness and peace. '
            'The mood is meditative, still, and free. Professional lifestyle photography, golden '
            'hour light, warm and serene, no text, no watermark.'
        ),
    ),
    (
        'loe-home-inline-love.jpg',
        '4:3',
        (
            'A handwritten letter on aged cream paper, beside a folded photograph and a single small '
            'dried flower, all resting on a warm wooden surface in soft afternoon light. '
            'The image evokes love preserved across time and distance. Professional still-life '
            'photography, warm honey tones, beautiful and intimate, no readable text, no watermark.'
        ),
    ),

    # ── About section (wide background) ───────────────────────────────────────
    (
        'loe-home-about-bg.jpg',
        '16:9',
        (
            'A writer at a wooden desk in a warmly lit study, seen from a distance — shelves of books '
            'behind them, a notebook open before them, natural light from a window to their side. '
            'The mood is reflective, purposeful, and deeply human. Professional lifestyle photography, '
            'warm amber tones, bookish and intimate atmosphere, no face visible, no text, no watermark.'
        ),
    ),
]

# Map old demo image filenames → new LOE filenames
OLD_TO_NEW_FILENAME = {
    'avada-recruitment-hero-mobile-2.jpg': 'loe-home-hero-mobile.jpg',
    'permanent-staffing-1.jpg':            'loe-home-card-understanding.jpg',
    'temporary-staffing-1.jpg':            'loe-home-card-survival.jpg',
    'contract-staffing-1.jpg':             'loe-home-card-freedom.jpg',
    'job-placement-22.jpg':               'loe-home-section-bg-understanding.jpg',
    'executive-search-11.jpg':            'loe-home-section-bg-survival.jpg',
    'jobs-posting-2.jpg':                 'loe-home-section-bg-freedom.jpg',
    'career-counseling-11.jpg':           'loe-home-section-bg-love.jpg',
    'job-placement-03.jpg':               'loe-home-inline-understanding.jpg',
    'executive-search-03.jpg':            'loe-home-inline-survival.jpg',
    'jobs-posting-03.jpg':                'loe-home-inline-freedom.jpg',
    'career-counseling-03.jpg':           'loe-home-inline-love.jpg',
    'about-recruitment-01.jpg':           'loe-home-about-bg.jpg',
}

# WordPress home page ID
HOME_PAGE_ID = 1023


def optimise_image(img_bytes, aspect_ratio):
    """
    Optimise raw image bytes for web delivery.
    - Resize to target dimensions for the aspect ratio
    - Compress to JPEG with quality tuning
    - Target file sizes per SIZE_PROFILES
    Returns optimised bytes.
    """
    from PIL import Image

    max_w, max_h, quality, max_kb = SIZE_PROFILES[aspect_ratio]

    img = Image.open(io.BytesIO(img_bytes)).convert('RGB')

    # Resize if larger than target
    if img.width > max_w or img.height > max_h:
        img.thumbnail((max_w, max_h), Image.LANCZOS)

    # Try compressing, reducing quality until under max_kb
    for q in range(quality, 50, -5):
        buf = io.BytesIO()
        img.save(buf, format='JPEG', quality=q, optimize=True)
        size_kb = buf.tell() // 1024
        if size_kb <= max_kb:
            print(f'    Optimised: {img.width}×{img.height}px, {size_kb} KB (quality={q})')
            return buf.getvalue()

    # If still too big, return best attempt
    buf.seek(0)
    print(f'    Note: could not hit {max_kb} KB target — using q=50')
    return buf.getvalue()


def generate_image(client, filename, aspect_ratio, prompt):
    """Generate one image using Imagen 4."""
    from google.genai import types
    response = client.models.generate_images(
        model='imagen-4.0-generate-001',
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio=aspect_ratio,
            output_mime_type='image/jpeg',
        )
    )
    if not response.generated_images:
        raise ValueError('No images returned — likely blocked by safety filter')
    return response.generated_images[0].image.image_bytes


def upload_to_wordpress(img_bytes, filename):
    """Upload image bytes to WordPress media library. Returns the URL."""
    wp_auth = base64.b64encode(
        f"{WP_USERNAME}:{WP_APP_PASSWORD}".encode()
    ).decode()
    headers = {
        'Authorization': f'Basic {wp_auth}',
        'Content-Type': 'image/jpeg',
        'Content-Disposition': f'attachment; filename="{filename}"',
    }
    response = requests.post(
        f'{WP_SITE_URL}/wp-json/wp/v2/media',
        headers=headers,
        data=img_bytes,
        timeout=60,
    )
    if response.status_code in (200, 201):
        data = response.json()
        url = data.get('source_url', '')
        wp_id = data.get('id', '?')
        print(f'    Uploaded: {url} (ID {wp_id})')
        return url
    else:
        raise RuntimeError(f'Upload failed: {response.status_code} — {response.text[:200]}')


def get_page_content(page_id):
    """Fetch current page Avada shortcodes."""
    wp_auth = base64.b64encode(
        f"{WP_USERNAME}:{WP_APP_PASSWORD}".encode()
    ).decode()
    headers = {'Authorization': f'Basic {wp_auth}'}
    response = requests.get(
        f'{WP_SITE_URL}/wp-json/wp/v2/pages/{page_id}?context=edit',
        headers=headers, timeout=30
    )
    data = response.json()
    return data.get('content', {}).get('raw', '')


def update_page(page_id, content):
    """Push updated content back to WordPress as draft."""
    wp_auth = base64.b64encode(
        f"{WP_USERNAME}:{WP_APP_PASSWORD}".encode()
    ).decode()
    headers = {
        'Authorization': f'Basic {wp_auth}',
        'Content-Type': 'application/json',
    }
    response = requests.post(
        f'{WP_SITE_URL}/wp-json/wp/v2/pages/{page_id}',
        headers=headers,
        json={'content': content, 'status': 'draft'},
        timeout=60,
    )
    if response.status_code in (200, 201):
        print(f'  Page {page_id} updated successfully (draft)')
    else:
        raise RuntimeError(f'Page update failed: {response.status_code} — {response.text[:200]}')


def main():
    import warnings
    warnings.filterwarnings('ignore')
    from google import genai

    print('=' * 60)
    print('LOE Image Generation + Optimisation Pipeline')
    print('=' * 60)
    print(f'WordPress: {WP_SITE_URL}')
    print(f'Images to generate: {len(IMAGES)}')

    client = genai.Client(api_key=GOOGLE_AI_API_KEY)

    output_dir = Path('/tmp/loe-images-v2')
    output_dir.mkdir(exist_ok=True)

    url_mapping = {}  # new_filename → wp_url

    for filename, aspect_ratio, prompt in IMAGES:
        print(f'\n[{filename}]')
        print(f'  Aspect: {aspect_ratio}')

        raw_path = output_dir / f'raw-{filename}'
        opt_path = output_dir / filename

        # Generate (use raw cache if available)
        if raw_path.exists():
            print('  [cached raw] skipping generation')
            raw_bytes = raw_path.read_bytes()
        else:
            try:
                raw_bytes = generate_image(client, filename, aspect_ratio, prompt)
                raw_path.write_bytes(raw_bytes)
                print(f'  Generated: {len(raw_bytes)//1024} KB raw')
            except Exception as e:
                print(f'  ERROR generating: {e}')
                continue

        # Optimise (use optimised cache if available)
        if opt_path.exists():
            print('  [cached optimised] skipping optimisation')
            opt_bytes = opt_path.read_bytes()
        else:
            try:
                opt_bytes = optimise_image(raw_bytes, aspect_ratio)
                opt_path.write_bytes(opt_bytes)
            except Exception as e:
                print(f'  ERROR optimising: {e}')
                continue

        # Upload optimised version to WordPress
        try:
            wp_url = upload_to_wordpress(opt_bytes, filename)
            url_mapping[filename] = wp_url
        except Exception as e:
            print(f'  ERROR uploading: {e}')

        time.sleep(1)

    print(f'\n\nGenerated/uploaded: {len(url_mapping)}/{len(IMAGES)} images')

    # Save URL mapping
    mapping_path = output_dir / 'url-mapping.json'
    mapping_path.write_text(json.dumps(url_mapping, indent=2))
    print(f'URL mapping: {mapping_path}')

    if not url_mapping:
        print('No images uploaded — skipping page update')
        return

    # Fetch and update home page
    print(f'\nFetching home page (ID {HOME_PAGE_ID})...')
    content = get_page_content(HOME_PAGE_ID)
    if not content:
        print('ERROR: Could not fetch page content')
        return

    original = content
    replaced = 0
    base_urls = [
        f'{WP_SITE_URL}/wp-content/uploads/2024/11',
        f'{WP_SITE_URL}/wp-content/uploads/2024/12',
        f'{WP_SITE_URL}/wp-content/uploads/2026/02',  # previously uploaded unoptimised
    ]

    for old_name, new_name in OLD_TO_NEW_FILENAME.items():
        if new_name not in url_mapping:
            print(f'  SKIP {old_name} — no URL for {new_name}')
            continue
        new_url = url_mapping[new_name]
        for base in base_urls:
            old_url = f'{base}/{old_name}'
            if old_url in content:
                content = content.replace(old_url, new_url)
                print(f'  Replaced: {old_name} → {new_name}')
                replaced += 1

    # Also replace previously uploaded unoptimised versions (loe-* names from v1)
    v1_name_map = {
        'loe-hero-mobile.jpg':              'loe-home-hero-mobile.jpg',
        'loe-understanding-pa-card.jpg':    'loe-home-card-understanding.jpg',
        'loe-survival-guide-card.jpg':      'loe-home-card-survival.jpg',
        'loe-inner-freedom-card.jpg':       'loe-home-card-freedom.jpg',
        'loe-section-bg-understanding.jpg': 'loe-home-section-bg-understanding.jpg',
        'loe-section-bg-survival.jpg':      'loe-home-section-bg-survival.jpg',
        'loe-section-bg-freedom.jpg':       'loe-home-section-bg-freedom.jpg',
        'loe-section-img-understanding.jpg':'loe-home-inline-understanding.jpg',
        'loe-section-img-survival.jpg':     'loe-home-inline-survival.jpg',
        'loe-section-img-freedom.jpg':      'loe-home-inline-freedom.jpg',
        'loe-about-bg.jpg':                 'loe-home-about-bg.jpg',
    }
    for old_name, new_name in v1_name_map.items():
        if new_name not in url_mapping:
            continue
        new_url = url_mapping[new_name]
        old_url = f'{WP_SITE_URL}/wp-content/uploads/2026/02/{old_name}'
        if old_url in content:
            content = content.replace(old_url, new_url)
            print(f'  Replaced v1: {old_name} → {new_name}')
            replaced += 1

    print(f'\nTotal replacements: {replaced}')

    if content == original:
        print('WARNING: No changes — check if URLs matched')
    else:
        update_page(HOME_PAGE_ID, content)
        (output_dir / 'home-final.txt').write_text(content)
        print('Final content saved to /tmp/loe-images-v2/home-final.txt')

    print('\nDone!')


if __name__ == '__main__':
    main()
