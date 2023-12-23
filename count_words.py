import os
import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
import re

def get_text_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    texts = soup.stripped_strings
    return ' '.join(texts)

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return ' '.join(visible_texts)

def count_words_in_blog(repo_owner, repo_name, file_path):
    try:
        raw_url = f'https://raw.githubusercontent.com/{repo_owner}/{repo_name}/main/{file_path}'
        response = requests.get(raw_url)
        response.raise_for_status()

        html_content = response.text
        plain_text = text_from_html(html_content)

        words = re.findall(r'\b\w+\b', plain_text)

        word_count = len(words)
        print(f"Word count of the blog after the update: {word_count}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if _name_ == "_main_":
    repo_owner = os.getenv("REPO_OWNER")
    repo_name = os.getenv("REPO_NAME")
    file_path = os.getenv("FILE_PATH")

    count_words_in_blog(repo_owner, repo_name, file_path)
