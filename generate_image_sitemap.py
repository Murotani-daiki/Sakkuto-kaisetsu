import os
import re
from xml.dom import minidom
from datetime import datetime

# Configuration
BASE_URL = "https://sakutto-kaisetsu.com/"
FILES_DIR = "."
SITEMAP_FILENAME = "sitemap-image.xml"

def get_html_files():
    """Return a list of HTML files in the directory except special ones."""
    exclude = ["search.html", "sitemap.html", "google-verification.html", "page2.html"]
    files = [f for f in os.listdir(FILES_DIR) if f.endswith(".html") and f not in exclude]
    return files

def extract_images_from_html(filepath):
    """Extract image URLs and their alt text/context from the HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract article title for default captions
    title_match = re.search(r'<h1>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
    article_title = title_match.group(1).strip().replace('<br>', ' ') if title_match else ""

    # Find images in featured-image and manga-section
    # We look for <img src="..." alt="...">
    img_pattern = r'<img\s+[^>]*src=["\'](img/[^"\']+)["\'][^>]*alt=["\']([^"\']*)["\'][^>]*>'
    
    matches = re.finditer(img_pattern, content, re.IGNORECASE)
    images = []
    seen_urls = set()

    for match in matches:
        img_url = match.group(1)
        alt_text = match.group(2)
        
        if img_url not in seen_urls:
            # Use alt text if available, otherwise use article title
            caption = alt_text if alt_text else article_title
            images.append({
                "url": BASE_URL + img_url,
                "caption": caption,
                "title": article_title
            })
            seen_urls.add(img_url)

    return images

def create_image_sitemap():
    """Generate the sitemap-image.xml file."""
    html_files = get_html_files()
    
    # Create the root element
    urlset = minidom.Document().createElement('urlset')
    urlset.setAttribute('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    urlset.setAttribute('xmlns:image', 'http://www.google.com/schemas/sitemap-image/1.1')
    
    doc = minidom.Document()
    doc.appendChild(urlset)

    for filename in html_files:
        filepath = os.path.join(FILES_DIR, filename)
        images = extract_images_from_html(filepath)
        
        if not images:
            continue

        url_element = doc.createElement('url')
        
        loc = doc.createElement('loc')
        loc.appendChild(doc.createTextNode(BASE_URL + filename))
        url_element.appendChild(loc)

        for img in images:
            img_element = doc.createElement('image:image')
            
            img_loc = doc.createElement('image:loc')
            img_loc.appendChild(doc.createTextNode(img["url"]))
            img_element.appendChild(img_loc)
            
            if img["caption"]:
                img_caption = doc.createElement('image:caption')
                img_caption.appendChild(doc.createTextNode(img["caption"]))
                img_element.appendChild(img_caption)
            
            if img["title"]:
                img_title = doc.createElement('image:title')
                img_title.appendChild(doc.createTextNode(img["title"]))
                img_element.appendChild(img_title)
            
            url_element.appendChild(img_element)

        urlset.appendChild(url_element)

    # Write to file
    xml_str = doc.toprettyxml(indent="  ", encoding="UTF-8")
    with open(SITEMAP_FILENAME, "wb") as f:
        f.write(xml_str)
    
    print(f"Generated {SITEMAP_FILENAME} with {len(html_files)} articles and their images.")

if __name__ == "__main__":
    create_image_sitemap()
