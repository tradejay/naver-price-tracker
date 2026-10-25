"""
Domain-rule-based noise cleaner for e-commerce price monitoring.
Prevents false-positive price alerts caused by installation services, accessories, or parts.
"""

SERVICE_KEYWORDS = [
    '설치비', '설치 비', '출장비', '시공비', '설치 비용', '설치료', '설치 공사',
    '기본설치', '현장설치', '엔지니어 방문'
]

ACCESSORY_KEYWORDS = [
    '확장마이크', '확장 마이크', 'ex mic', 'tv마운트', 'tv 마운트', '전용 리모컨',
    '리모컨', '보호필름', '케이블 키트', '테이블 마운트', '월 마운트', '라이저 마운트',
    '마운트 브라켓', '파워서플라이', '연장 케이블'
]

def check_service_or_accessory(title: str):
    """
    Checks if the product title corresponds to an installation service or peripheral accessory.
    
    Returns:
        'service': If matched with installation or labor costs.
        'accessory': If matched with mounting brackets or peripheral parts.
        False: If it is considered a main product candidate.
    """
    if not title:
        return False
    t = title.lower()
    
    # Exception rule: Dedicated carts/stands (e.g. Rally Board Cart) are standalone hardware,
    # not simple low-cost mounting accessories.
    if 'cart' in t or '카트' in t:
        if '952-000251' in t or 'board' in t or '보드' in t:
            return False
            
    if any(k in t for k in SERVICE_KEYWORDS):
        return 'service'
        
    if any(k in t for k in ACCESSORY_KEYWORDS):
        return 'accessory'
        
    return False

def is_valid_main_product(title: str, price: int, min_threshold: int) -> bool:
    """
    Validates whether an extracted item is a genuine hardware unit above the baseline threshold.
    """
    noise_type = check_service_or_accessory(title)
    if noise_type:
        return False
    if price < min_threshold:
        return False
    return True
