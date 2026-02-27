#!/usr/bin/env python3
"""
Replace About Us page (ID 1887) demo content with Malcolm's Story.
Maps each Avada section to the LOE narrative structure:
  Section 1: Features intro → Hero / chapter titles
  Section 2: Image banners → Malcolm's story with images
  Section 3: Team members → Six chapters of Malcolm's journey
  Section 4: Tabs → My Story / What I Found / Why This Book
  Section 5: Process steps → Three journeys (Understand / Survive / Transform)
  Section 6: Counter circles → Key numbers (10 years / 3 allegations / 3 children)
"""

import base64
import requests
from pathlib import Path

env = {}
for line in open(Path(__file__).parent.parent / '.env'):
    line = line.strip()
    if line and '=' in line and not line.startswith('#'):
        k, v = line.split('=', 1); env[k.strip()] = v.strip()

WP_SITE_URL = env['WP_SITE_URL'].rstrip('/')
WP_USERNAME = env['WP_USERNAME']
WP_APP_PASSWORD = env['WP_APP_PASSWORD']
PAGE_ID = 1887  # About Us


def replace_nth(content, old, new, n):
    """Replace the nth occurrence (1-based) of old with new."""
    idx, count = 0, 0
    while True:
        idx = content.find(old, idx)
        if idx == -1:
            return content
        count += 1
        if count == n:
            return content[:idx] + new + content[idx + len(old):]
        idx += len(old)


def wp_auth():
    return base64.b64encode(f"{WP_USERNAME}:{WP_APP_PASSWORD}".encode()).decode()


def get_page(page_id):
    r = requests.get(
        f'{WP_SITE_URL}/wp-json/wp/v2/pages/{page_id}?context=edit',
        headers={'Authorization': f'Basic {wp_auth()}'}, timeout=30
    )
    return r.json().get('content', {}).get('raw', '')


def update_page(page_id, content):
    r = requests.post(
        f'{WP_SITE_URL}/wp-json/wp/v2/pages/{page_id}',
        headers={'Authorization': f'Basic {wp_auth()}', 'Content-Type': 'application/json'},
        json={'content': content, 'status': 'draft', 'title': "Malcolm's Story"},
        timeout=60,
    )
    return r.status_code in (200, 201)


def main():
    print('Fetching About Us page...')
    content = get_page(PAGE_ID)
    original = content
    changed = 0

    def r(old, new, label=''):
        nonlocal content, changed
        if old in content:
            content = content.replace(old, new)
            changed += 1
            if label:
                print(f'  ✓ {label}')
        else:
            if label:
                print(f'  — not found: {label}')

    def rn(old, new, n, label=''):
        nonlocal content, changed
        before = content
        content = replace_nth(content, old, new, n)
        if content != before:
            changed += 1
            if label:
                print(f'  ✓ {label} (occurrence {n})')
        else:
            if label:
                print(f'  — not found: {label} (occurrence {n})')

    # ── Section 1: Chapter/hero intro titles ──────────────────────────────────
    print('\nSection 1: Intro/hero titles')
    r(
        'we offer high quality staffing services',
        'my name is malcolm smith.\nthis is my story.',
        'main heading'
    )
    r('timely interviews', 'growing up in a closed sect', 'chapter 1')
    r('building the trust', 'marriage, faith, and family', 'chapter 2')
    r('talent acquisition', 'the years of exile', 'chapter 3')
    r('hire an employee', 'read the book', 'CTA 1')
    r(
        'expert guidance for start-ups &amp;&nbsp; small businesses',
        'three false allegations. three investigations.',
        'chapter 4'
    )
    r('join our program', 'get notified', 'CTA 2')

    # ── Section 2: Image banners ───────────────────────────────────────────────
    print('\nSection 2: Image banner text')
    r(
        'Benefit from the best workforce solutions globally',
        'Born in the Netherlands into a closed Christian community, I grew up in a world '
        'with its own rules and no room for questions. When my marriage ended and I left, '
        'I had no preparation for what would follow.',
        'banner text 1'
    )
    r(
        'Access top-tier creative thinkers tailored to your business needs',
        'Over the following decade, I was systematically separated from my three children '
        'through false allegations, court battles, and a campaign of manipulation I was '
        'entirely unprepared for.',
        'banner text 2'
    )
    r(
        'CEO &amp; Co-Director',
        'author, father of three',
        'person label'
    )
    r(
        'Montes purus aces lorem egestas metus feugiat ultrices dui elementum diam. Adipiscing pellente sque amet.',
        'I did not set out to write a book about parental alienation. I set out to survive it. '
        'And in surviving it — and coming out the other side — I discovered that the worst thing '
        'that can happen to a parent can also become a doorway to something you could not have '
        'reached any other way.',
        'main narrative para'
    )

    # ── Highlighted text ──────────────────────────────────────────────────────
    print('\nHighlights')
    rn('your ideal recruitment agency', 'a father who would not stop fighting', 1, 'highlight 1')
    r('start bright future with us', 'love is not defeated by distance', 'highlight 2')
    r('we make it happen', 'and it can for you, too', 'highlight 3')
    rn('your ideal recruitment agency', 'there is a path through this', 2, 'highlight 4')

    # ── Section 3: Team members → Six chapters ────────────────────────────────
    print('\nSection 3: Chapter names (team members → story chapters)')
    r('mike corkery', 'the early years', 'chapter name 1')
    r('lizzie williams', 'becoming a father', 'chapter name 2')
    r('gardner hudson', 'the divorce', 'chapter name 3')
    r('shyann volkman', 'three false accusations', 'chapter name 4')
    r('lamar stroman', 'the surrender', 'chapter name 5')
    r('rubien mrazda', 'the other side', 'chapter name 6')
    r('meet our certified recruitment experts', 'the journey that led to this book', 'section heading')

    # Job titles → chapter subtitles
    r('<p>Associate Consultant</p>', '<p>Childhood and the sect</p>', 'job title 1')
    r('<p>Head of Recruitment</p>', '<p>Marriage and fatherhood</p>', 'job title 2')
    r('<p>Marketing Executive</p>', '<p>When the alienation began</p>', 'job title 3')
    r('<p>Operations Manager</p>', '<p>The hardest years</p>', 'job title 4')
    r('<p>Senior Consultant</p>', '<p>Surrender and transformation</p>', 'job title 5')

    # Chapter descriptions (replacing lorem ipsum — 3 occurrences)
    r(
        'Nulla acnia tempus lectus, sit amet lema umligula phareta vamus quam consecter varius quam.',
        'Growing up in the Exclusive Brethren in the Netherlands, I was raised in a world '
        'that discouraged contact with the outside. I knew nothing else, and questioned nothing.',
        'chapter desc (plain)'
    )
    rn(
        '<p>Nulla acnia tempus lectus, sit amet lema umligula phareta vamus quam consecter varius quam.</p>',
        '<p>When my marriage ended and I left the community, I lost far more than I expected. '
        'What followed was a decade of parental alienation — something I hadn\'t heard of, and '
        'couldn\'t yet name.</p>',
        1,
        'chapter desc 1 (HTML)'
    )
    rn(
        '<p>Nulla acnia tempus lectus, sit amet lema umligula phareta vamus quam consecter varius quam.</p>',
        '<p>Over the following years, I was arrested three times on false allegations of sexual '
        'abuse of my own children. Each time, I was cleared. But by then, the damage to my '
        'relationship with my children was devastating.</p>',
        2,
        'chapter desc 2 (HTML)'
    )

    # ── Section 4: Tabs ───────────────────────────────────────────────────────
    print('\nSection 4: Tabs')
    r('title="mission"', 'title="my story"', 'tab title 1')
    r('title="integrity"', 'title="what i found"', 'tab title 2')
    r('title="expertise"', 'title="why this book"', 'tab title 3')
    r('Get industry-leading recruitment plans', 'a story worth telling', 'tabs section heading')

    # Tab body text (all three tabs have the same lorem ipsum — replace by position)
    tab_lorem = '<p>Facilisis quis pharetra at lacinia eget tellus. Nulla cursus tempus posuere faucibus. Vestibulum blandit quam lorem. Rhoncus sed gravida metus ac aliquam.</p>'
    rn(
        tab_lorem,
        '<p>For ten years, I lived what you are living now. The false allegations. The court '
        'battles. The silence from my children. The feeling that no one believed me, and no one '
        'could help me. I did not write this book from the outside. I wrote it from inside '
        'the fire.</p>',
        1,
        'tab content 1 (my story)'
    )
    rn(
        tab_lorem,
        '<p>In the deepest moment of despair — when I had no strategy left and nothing to hold '
        'onto — something unexpected happened. The ten years of struggle had been preparing me '
        'for a transformation I could not have planned. I discovered that love is not something '
        'that can be taken from you.</p>',
        2,
        'tab content 2 (what i found)'
    )
    rn(
        tab_lorem,
        '<p>I wrote <em>Love Over Exile</em> because no book existed that held both things at '
        'once: the hard practical reality of surviving parental alienation, and the deeper '
        'question of what to do with the pain when the battle is over. This book is that guide — '
        'from someone who walked every step of it.</p>',
        3,
        'tab content 3 (why this book)'
    )

    # ── Section 5: Process steps → Three journeys ────────────────────────────
    print('\nSection 5: Journey steps')
    r(
        'facilitating the hiring process &amp; ensuring a good match',
        'the path from exile to freedom',
        'steps section heading'
    )
    r("identify employer's need", 'understanding what is happening', 'step 1 title')
    r('interviews &amp; selection', 'surviving the system', 'step 2 title')
    r('contract offer &amp; follow-up', 'finding inner freedom', 'step 3 title')

    # Step body texts
    r(
        'We post job listings on multiple social media platforms including job boards and websites to attract suitable candidates',
        'Everything you are experiencing has a name. Parental alienation is documented, '
        'researched, and — crucially — survivable. Understanding what is happening is '
        'the foundation of everything.',
        'step 1 text'
    )
    r(
        "We understand the client's specific hiring requirements, including job roles, skills and qualifications for consideration",
        'There is no single strategy that works for everyone. But there are principles — '
        'tested in the fire — that can help you navigate the courts, your co-parent, '
        'and your child without losing yourself.',
        'step 2 text'
    )
    r(
        'We arrange interviews between the employer and shortlisted candidates and assist in employment terms.',
        'The legal battle is real — but it is only part of the journey. The deeper work '
        'of radical acceptance, unconditional love, and forgiveness is what transforms '
        'survival into something greater.',
        'step 3 text'
    )

    # Process section body texts
    r(
        'At mattis elementum semper tellus donec ornare. Dis dolor pellentesque dui auctor urna nam lectus.',
        'Everything you are experiencing has a name. Parental alienation is a recognised '
        'form of family violence — and understanding the system is the beginning of surviving it.',
        'process body 1'
    )
    r(
        'Nunc sed vitae sed tristique nisal dolor tellus are interdum ipsum erat pellentes.',
        'Parental alienation is a long game. This section gives you the framework — '
        'what to do, what not to do, and how to stay whole for the journey ahead.',
        'process body 2'
    )
    r(
        'Pretium tellus kitae sed tristiq nisal dolor neus tellus duit egestas vulputate.',
        'The battle is real, and it will take everything you have. But what you do '
        'with what it gives you — that is yours to choose.',
        'process body 3'
    )
    r(
        'Fusce laoreet scelerisque libero rhoncus arcu luctus pharet. Donec egestas felis.',
        'The path to inner freedom is possible even while the battle is ongoing. '
        'It begins with a choice you can make today.',
        'process body 4'
    )

    # ── Section 6: Stats / Counter circles ────────────────────────────────────
    print('\nSection 6: Stats')
    r(
        'our recruitment fulfilment<br />\nnumbers are massive',
        'ten years. three allegations.\none unbreakable love.',
        'stats heading'
    )
    r('90%', '10 years', 'stat 1 display')
    r('98%', '3 times', 'stat 2 display')
    r('85%', '3 children', 'stat 3 display')
    r('offer acceptance rate', 'in systematic alienation', 'stat 1 label')
    r('job success rate', 'false allegations of abuse', 'stat 2 label')
    r('final interviews rate', 'children who came home', 'stat 3 label')

    # ── Push to WordPress ──────────────────────────────────────────────────────
    print(f'\nTotal replacements: {changed}')

    if content == original:
        print('ERROR: No changes made — check string matching')
        return

    if update_page(PAGE_ID, content):
        print(f'Successfully pushed Malcolm\'s Story as draft (ID {PAGE_ID})')
        with open('/tmp/about-updated.txt', 'w') as f:
            f.write(content)
        print('Saved to /tmp/about-updated.txt')
    else:
        print('ERROR: Failed to push to WordPress')


if __name__ == '__main__':
    main()
