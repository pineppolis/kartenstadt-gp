import os
import json
import re
import markdown
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
    paragraphs = [p for p in html_content.split('</p>') if '<p>' in p]
    if paragraphs:
        return paragraphs[0] + '</p>'
    return ""

def build_site():
    # 1. Setup Directories
    if not os.path.exists(POSTS_OUTPUT_DIR):
        os.makedirs(POSTS_OUTPUT_DIR)

    post_template = load_template(POST_TEMPLATE_FILE)
    home_template = load_template(HOME_TEMPLATE_FILE)
    if not post_template or not home_template: return

    history = load_history()
    files = [f for f in os.listdir(ARTICLES_DIR) if f.endswith('.md')]

    articles_data = [] # To store info for the home page
    new_conversions = 0

    print("--- Starting Build ---")

    for filename in files:
        md_path = os.path.join(ARTICLES_DIR, filename)
        timestamp = os.path.getmtime(md_path)
        date_obj = datetime.fromtimestamp(timestamp)

        # Metadata for Home Page
        title = filename.replace('.md', '').replace('-', ' ').replace('_', ' ').title()
        # Relative link used by index.html (which is in HOME_OUTPUT_DIR '.')
        link = f"{POSTS_OUTPUT_DIR}/{filename.replace('.md', '.html')}"

        # --- STEP A: CONVERT MARKDOWN TO POSTS ---
        # Read file
        with open(md_path, 'r', encoding='utf-8') as f:
            md_text = f.read()

        # Pre-processing (Comments, Del, Wikilinks)
        md_text = re.sub(r'%%(.*?)%%', lambda m: f' <span class="comment">%%{m.group(1).replace("\\n", " ")}%%</span> ', md_text, flags=re.DOTALL)
        md_text = re.sub(r'~~(.*?)~~', r'<del>\1</del>', md_text)
        md_text = re.sub(r'\[\[#\^([\w-]+)\]\]', r'<a href="#\1" class="wikilink">#\1</a>', md_text)

        # --- NEW IMAGE PREPROCESSING STEP ---
        # Match ![[ image.jpg | 400 ]]
        # Group 1: Filename.ext
        # Group 2: (Optional) Width
        image_pattern = r'!\[\[\s*([^|\]]+\.[a-zA-Z]{3,4})\s*(?:\|\s*(\d+)\s*)?\]\]'

        def image_to_html(match):
            img_filename = match.group(1).strip()
            img_width = match.group(2) # None if not specified

            # Construct the relative path *from the post output file's perspective*
            # Posts are in 'posts/', so 'assets' is one directory up '../assets/'.
            img_path = '../assets/' + img_filename

            if img_width:
                return f'<img src="{img_path}" alt="{img_filename}" width="{img_width}">'
            else:
                return f'<img src="{img_path}" alt="{img_filename}">'

        # Run the replacement
        md_text = re.sub(image_pattern, image_to_html, md_text)
        # ----------------------------------

        # Conversion
        html_body = markdown.markdown(md_text, extensions=['extra', 'sane_lists', 'smarty'])

        # Collapsible H2 Logic
        if "<h2>" in html_body:
            parts = html_body.split('<h2>')
            new_html = parts[0]
            for part in parts[1:]:
                if '</h2>' in part:
                    heading_title, rest = part.split('</h2>', 1)
                    new_html += f'<details open><summary><h2>{heading_title}</h2></summary>{rest}</details>'
                else:
                    new_html += f'<h2>{part}'
            html_body = new_html

        # Store preview for home page
        preview = get_preview_text(html_body)

        # Only save the .html file if it's new/not in history
        if filename not in history:
            final_post = post_template.replace('{title}', title) \
                                      .replace('{body}', html_body) \
                                      .replace('{author}', AUTHOR_NAME) \
                                      .replace('{date}', date_obj.strftime('%B %d, %Y'))

            # Beautify
            soup = BeautifulSoup(final_post, 'html.parser')
            with open(os.path.join(POSTS_OUTPUT_DIR, filename.replace('.md', '.html')), 'w', encoding='utf-8') as f:
                f.write(soup.prettify())

            history.append(filename)
            new_conversions += 1
            print(f"Generated Post: {title}")

        # Add to the list for the homepage (regardless of if it's new)
        articles_data.append({
            'title': title,
            'date': date_obj,
            'display_date': date_obj.strftime('%Y-%m-%d'),
            'link': link,
            'preview': preview
        })

    # --- STEP B: GENERATE HOME PAGE ---
    articles_data.sort(key=lambda x: x['date'], reverse=True)

    list_items = ""
    for art in articles_data:
        list_items += f"""
        <article class="article-card">
            <div class="card-header">
                <h2><a href="{art['link']}">{art['title']}</a></h2>
                <span class="post-meta">{art['display_date']}</span>
            </div>
            <div class="preview-content">
                {art['preview']}
            </div>
            <a href="{art['link']}" class="read-more">View Post _</a>
        </article>
        """

    final_home = home_template.replace("{articles_placeholder}", list_items)
    with open(os.path.join(HOME_OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(final_home)

    save_history(history)
    print(f"\nFinished: {new_conversions} new posts, index.html updated with {len(articles_data)} total articles.")

if __name__ == "__main__":
    if not os.path.exists(ARTICLES_DIR):
        os.makedirs(ARTICLES_DIR)
    else:
        build_site()
