import requests
from bs4 import BeautifulSoup
import re

print("Scraping the API (Data Base) page on INE.pt...")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    url = "https://www.ine.pt/xportal/xmain?xpid=INE&xpgid=ine_api_v2"
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    # Look for any forms, code examples, or documentation links
    forms = soup.find_all('form')
    code_blocks = soup.find_all('code')
    doc_links = soup.find_all('a', href=True)

    if forms:
        print("--- Found Forms ---")
        for form in forms:
            print(form)
            print("---")

    if code_blocks:
        print("--- Found Code Blocks ---")
        for code in code_blocks:
            print(code.get_text(strip=True))
            print("---")
            
    if doc_links:
        print("--- Found Links ---")
        for link in doc_links:
            link_text = link.get_text(strip=True)
            link_href = link.get('href')
            if any(keyword in link_text.lower() or keyword in link_href.lower() for keyword in ['doc', 'guide', 'example', 'v2', 'json', 'xml']):
                full_link = requests.compat.urljoin(url, link_href)
                print(f"Text: {link_text}\nURL: {full_link}\n")


except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")

except Exception as e:
    print(f"An unexpected error occurred: {e}")