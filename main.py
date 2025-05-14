import requests
from bs4 import BeautifulSoup
import time
import csv
#          CONFIGURATION
BASE_URL = "https://www.jumia.com.ng/laptops/"
HEADERS = {"User-Agent": "Mozilla/5.0"}
OUTPUT_FILE = "products.csv"
DELAY_BETWEEN_REQUESTS = 2  # seconds
MAX_RETRIES = 3
#          END OF CONFIGURATION
FIELDS = ["Name", "Price", "Availability", "Rating", "URL", "Reviews", "Details"]

# -------------- Scraping Procedures --------------
def get_html(url):
    """Fetch HTML content with retries and proper error handling"""
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()  # Raise exception for HTTP errors
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"[Retry {attempt + 1}] Error: {e}")
            time.sleep(DELAY_BETWEEN_REQUESTS)
    return None


def parse_list_page(html):
    """Extract product cards from a category page with proper selectors"""
    soup = BeautifulSoup(html, "html.parser")
    # Updated selector to match partial class name
    products = soup.find_all("article", class_=lambda c: c and "prd" in c.split())
    product_data = []

    for product in products:
        name_elem = product.find("h3", class_="name")
        price_elem = product.find("div", class_="prc")
        link_elem = product.find("a", class_="core")
        rating_elem = product.find("div", class_="stars")

        # Get absolute URL
        product_url = link_elem["href"] if link_elem else ""
        if product_url.startswith("/"):
            product_url = f"https://www.jumia.com.ng{product_url}"

        product_info = {
            "Name": name_elem.text.strip() if name_elem else "N/A",
            "Price": price_elem.text.strip() if price_elem else "N/A",
            "Availability": "Available",  # Implement actual check if needed
            "Rating": rating_elem.text.strip() if rating_elem else "N/A",
            "URL": product_url,
            "Reviews": "N/A",  # Placeholder until details page is scraped
            "Details": "N/A"
        }
        product_data.append(product_info)

    return product_data


def parse_product_detail_page(url):
    """Collect additional details from product page with proper selectors"""
    html = get_html(url)
    if not html:
        return {"Details": "N/A", "Reviews": "N/A"}

    soup = BeautifulSoup(html, "html.parser")

    # Updated CSS selectors for details and reviews
    details = soup.find("div", class_="markup -mhm -pvl -oxa -sc")
    reviews = soup.find("div", class_="reviews")

    return {
        "Details": details.get_text(strip=True, separator=" ") if details else "N/A",
        "Reviews": reviews.text.strip() if reviews else "N/A"
    }


def find_next_page_url(soup):
    """Find next page URL with proper handling"""
    next_btn = soup.find("a", {"aria-label": "Next Page"})
    return next_btn["href"] if next_btn and "href" in next_btn.attrs else None

# ------------- My Main Program ------------
def main():
    all_products = []
    current_url = BASE_URL

    while current_url and len(all_products) < 50:
        print(f"Scraping page: {current_url}")
        html = get_html(current_url)

        if not html:
            print("Failed to load page. Moving to next page...")
            continue

        products = parse_list_page(html)
        soup = BeautifulSoup(html, "html.parser")

        for product in products:
            if len(all_products) >= 50:
                break  # Stop if we have enough products
            print(f"Visiting: {product['URL']}")
            extra_info = parse_product_detail_page(product["URL"])
            product.update(extra_info)
            all_products.append(product)
            time.sleep(DELAY_BETWEEN_REQUESTS)

        # Check again after processing the page's products
        if len(all_products) >= 50:
            break

        # Find next page
        next_page = find_next_page_url(soup)
        if next_page:
            current_url = f"https://www.jumia.com.ng{next_page}" if next_page.startswith("/") else next_page
        else:
            current_url = None

        time.sleep(DELAY_BETWEEN_REQUESTS)

    # Trim to exactly 100 products if needed
    all_products = all_products[:50]

    # Save to CSV
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(all_products)

    print(f"\nFinished. {len(all_products)} products saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()