import os
import json
import re
import markdown
import subprocess
from bs4 import BeautifulSoup
from datetime import datetime

# --- CONFIGURATION ---
ARTICLES_DIR = 'articles'
POSTS_OUTPUT_DIR = 'posts'
HOME_OUTPUT_DIR = '.'
DB_FILE = 'converted_files.json'
POST_TEMPLATE_FILE = 'posts.html'
HOME_TEMPLATE_FILE = 'home_template.html'
AUTHOR_NAME = 'pineppolis'

# UPDATE THIS: Use your custom domain or GitHub Pages URL
# Example: 'https://pineppolis.github.io/kartenstadt'
BASE_URL = 'https://pineppolis.github.io/kartenstadt'

def load_template(filepath):
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found.")
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def load_history():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    return []

def save_history(history):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=4)

def get_preview_text(html_content):
    """Extracts the first paragraph from generated HTML."""
    soup = BeautifulSoup(html_content, 'html.parser')
    first_p = soup.find('p')
    return str(first_p) if first_p else ""

def generate_rss(articles_data):
    """Generates an RSS 2.0 feed file with full content."""
    rss_items = ""
    for art in articles_data[:15]:
        full_url = f"{BASE_URL}/{art['link']}"
        # We use art['full_content'] inside CDATA to ship the whole post
        rss_items += f"""
        <item>
            <title>{art['title']}</title>
            <link>{full_url}</link>
            <description><![CDATA[{art['full_content']}]]></description>
            <pubDate>{art['date'].strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
            <guid isPermaLink="true">{full_url}</guid>
        </item>"""

    rss_feed = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
    <title>Kartenstadt</title>
    <link>{BASE_URL}/</link>
    <description>Karte-map; Stadt-city</description>
    <language>en-us</language>
    <lastBuildDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')}</lastBuildDate>
    <atom:link href="{BASE_URL}/feed.xml" rel="self" type="application/rss+xml" />
    {rss_items}
</channel>
</rss>"""

    with open('feed.xml', 'w', encoding='utf-8') as f:
        f.write(rss_feed.strip())
    print("Generated: feed.xml")

def push_to_github():
    """Automates git add, commit, and push."""
    try:
        print("\n--- Syncing with GitHub ---")
        subprocess.run(["git", "add", "."], check=True)
        commit_message = f"Site update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("Successfully pushed to GitHub!")
    except subprocess.CalledProcessError as e:
        print(f"Git sync failed. Error: {e}")

def build_site():
    if not os.path.exists(POSTS_OUTPUT_DIR):
        os.makedirs(POSTS_OUTPUT_DIR)

    post_template = load_template(POST_TEMPLATE_FILE)
    home_template = load_template(HOME_TEMPLATE_FILE)
    if not post_template or not home_template: return

    history = load_history()
    files = [f for f in os.listdir(ARTICLES_DIR) if f.endswith('.md')]
    articles_data = []
    new_conversions = 0

    print("--- Starting Build ---")

    for filename in files:
        md_path = os.path.join(ARTICLES_DIR, filename)
        timestamp = os.path.getmtime(md_path)
        date_obj = datetime.fromtimestamp(timestamp)

        title = filename.replace('.md', '').replace('-', ' ').replace('_', ' ').title()
        link = f"{POSTS_OUTPUT_DIR}/{filename.replace('.md', '.html')}"

        with open(md_path, 'r', encoding='utf-8') as f:
            md_text = f.read()

        # Pre-processing
        md_text = re.sub(r'%%(.*?)%%', lambda m: f' <span class="comment">%%{m.group(1).replace("\\n", " ")}%%</span> ', md_text, flags=re.DOTALL)
        md_text = re.sub(r'~~(.*?)~~', r'<del>\1</del>', md_text)
        md_text = re.sub(r'\[\[#\^([\w-]+)\]\]', r'<a href="#\1" class="wikilink">#\1</a>', md_text)

        # Image Pre-processing with Absolute URLs for RSS compatibility
        image_pattern = r'!\[\[\s*([^|\]]+\.[a-zA-Z]{3,4})\s*(?:\|\s*(\d+)\s*)?\]\]'
        def image_to_html(match):
            img_filename, img_width = match.group(1).strip(), match.group(2)
            img_path = f"{BASE_URL}/assets/{img_filename}"
            return f'<img src="{img_path}" alt="{img_filename}"' + (f' width="{img_width}">' if img_width else '>')

        md_text = re.sub(image_pattern, image_to_html, md_text)

        # Markdown to HTML
        html_body = markdown.markdown(md_text, extensions=['extra', 'sane_lists', 'smarty'])

        # Collapsible H2 Logic
        if "<h2>" in html_body:
            parts = html_body.split('<h2>')
            new_html = parts[0]
            for part in parts[1:]:
                if '</h2>' in part:
                    heading_title, rest = part.split('</h2>', 1)
                    new_html += f'<details open><summary><h2>{heading_title}</h2></summary>{rest}</details>'
                else: new_html += f'<h2>{part}'
            html_body = new_html

        preview = get_preview_text(html_body)

        # Always track for the RSS feed and Home page list
        articles_data.append({
            'title': title,
            'date': date_obj,
            'display_date': date_obj.strftime('%Y-%m-%d'),
            'link': link,
            'preview': preview,
            'full_content': html_body
        })

        if filename not in history:
            final_post = post_template.replace('{title}', title).replace('{body}', html_body).replace('{author}', AUTHOR_NAME).replace('{date}', date_obj.strftime('%B %d, %Y'))
            soup = BeautifulSoup(final_post, 'html.parser')
            with open(os.path.join(POSTS_OUTPUT_DIR, filename.replace('.md', '.html')), 'w', encoding='utf-8') as f:
                f.write(soup.prettify())
            history.append(filename)
            new_conversions += 1
            print(f"Generated Post: {title}")

    # Generate Home Page
    articles_data.sort(key=lambda x: x['date'], reverse=True)
    list_items = "".join([f'<article class="article-card"><div class="card-header"><h2><a href="{a["link"]}">{a["title"]}</a></h2><span class="post-meta">{a["display_date"]}</span></div><div class="preview-content">{a["preview"]}</div><a href="{a["link"]}" class="read-more">View Post _</a></article>' for a in articles_data])

    final_home = home_template.replace("{articles_placeholder}", list_items)
    with open(os.path.join(HOME_OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(final_home)

    generate_rss(articles_data)
    save_history(history)
    print(f"\nBuild Finished. Index and RSS updated.")

    # Push to GitHub
    push_to_github()

if __name__ == "__main__":
    if not os.path.exists(ARTICLES_DIR): os.makedirs(ARTICLES_DIR)
    else: build_site()
