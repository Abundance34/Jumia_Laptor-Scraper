# Jumia_Laptor-Scraper
WEB SCRAPING LAPTOPS IN JUMIA NIGERIA USING PYTHON
- ### This python script extracts product information from the 'laptops' category on 'Jumia Nigeria' (https://www.jumia.com.ng/laptops/). it visits each product's page to get the product name, price, availability, rating, reviews and product details by visiting each product's page.
HOW TO INSTALL DEPENDENCIES
- ### pip install requests BeautifulSoup (copy and paste this in your python to install your libaries/dependencies)
HOW TO RUN THE THE SCRIPT (EXAMPLES)
- ### Python main.py
ANY ASSUMPTIONS YOU MADE
- ### The Extraction stops after 50 products for demonstration (adjustable by modifying len(all_products) < 50).
- ### The Availability is hardcoded as "Available" due to missing in-stock indicators on the listing page.
- ### Every single product ratings and details information are visible to the public.
WHAT CHALLENGES YOU ENCOUNTERED (PAGINATION, BLOCKING, PARSING QUIRKS)
- ### Pagination: Inaccurate "Next Page" detection results in an initial infinite loop. fixed by verifying the number of products and the existence of the page.
- ### Blocking: Steered clear of delays and User-Agent headers.
- ### Parsing quirks: Partial matching was necessary for dynamic class names (such as class="prd").
HOW YOU TESTED YOUR SCRAPER
- ### Output consistency over several runs was confirmed.
- ### Missing data ("N/A" handling) was checked.
- ### I kept an eye on logs for retries and HTTP problems.






