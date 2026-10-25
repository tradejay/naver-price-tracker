"""
HTML & JSON Parser for Naver Shopping Search Results.
"""
import re
from typing import List, Dict, Any
from bs4 import BeautifulSoup

def parse_shopping_results(raw_html_or_json: str) -> List[Dict[str, Any]]:
    """
    Extracts product title, price, merchant name, and product link from shopping results.
    """
    items = []
    # Implementation supports both BeautifulSoup DOM parsing and __NEXT_DATA__ JSON extraction
    soup = BeautifulSoup(raw_html_or_json, 'html.parser')
    product_cards = soup.select('.product_item__MDtDF, .basicList_item__2T2Nd')
    
    for card in product_cards:
        title_el = card.select_one('.product_title__Mmw2K, .basicList_title__3PjiX')
        price_el = card.select_one('.price_num__S2p_v, .price_price__1Kajm')
        mall_el = card.select_one('.product_mall__G_60M, .basicList_mall__sbVax')
        link_el = card.select_one('a[href]')
        
        if title_el and price_el:
            title = title_el.get_text(strip=True)
            price_raw = re.sub(r'[^0-9]', '', price_el.get_text())
            price = int(price_raw) if price_raw else 0
            mall_name = mall_el.get_text(strip=True) if mall_el else "네이버스마트스토어"
            link = link_el['href'] if link_el else ""
            
            items.append({
                'title': title,
                'price': price,
                'mall_name': mall_name,
                'link': link
            })
            
    return items
