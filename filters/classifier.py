"""
Category Classifier for Logitech Video Collaboration Hardware.
Maps raw online merchant titles to official model catalogs.
"""

def classify_product(product_name: str) -> str:
    """
    Classifies a raw title string into an official Logitech product category.
    Handles typos, multi-language terms, and parts number (PN) matching.
    """
    if not isinstance(product_name, str):
        return "Others"
    name_norm = product_name.lower().replace(" ", "")
    
    # Meetup series
    if any(k in name_norm for k in ['meetup2', '미트업2', '밋업2']):
        return "Meetup 2"
    if any(k in name_norm for k in ['meetup', '밋업', '미트업']):
        return "Meetup"
        
    # Rally Board 65 Cart (Standalone Stand/Cart accessory sold separately)
    if '952-000251' in name_norm or (
        ('rally' in name_norm or '랠리' in name_norm or '랄리' in name_norm) and 
        ('board' in name_norm or '보드' in name_norm) and 
        any(c in name_norm for c in ['cart', '카트', '스탠드'])
    ):
        return "Rally Board 65 Cart"
        
    # Rally Board 65 All-in-One Touch Display
    if any(pn in name_norm for pn in ['960-001698', '960-001730']) or (
        ('rally' in name_norm or '랠리' in name_norm or '랄리' in name_norm) and 
        ('board' in name_norm or '보드' in name_norm)
    ):
        return "Rally Board 65"
        
    # Rally Bar Sub-models
    if any(k in name_norm for k in ['huddle', '허들', '해들', 'barhuddle', 'rallybarhuddle']):
        return "Rally Bar Huddle"
    if any(k in name_norm for k in ['barmini', 'rallybarmini', '미니바', '바미니', '미니']):
        return "Rally Bar Mini"
    if any(k in name_norm for k in ['rallybar', '랠리바', '랄리바']):
        return "Rally Bar"
        
    # Rally Modular Systems
    if any(k in name_norm for k in ['rallyplus', '랠리플러스', '랄리플러스']):
        return "Rally Plus"
    if any(k in name_norm for k in ['rallysystem', '랠리시스템', '랄리시스템']):
        return "Rally System"
    if any(k in name_norm for k in ['rallycamera', '랠리카메라', '랄리카메라']):
        return "Rally Camera"
        
    # Touch Controller / Tap series
    if any(k in name_norm for k in ['tapscheduler', '탭스케줄러', '스케줄러']):
        return "TAP Scheduler"
    if any(k in name_norm for k in ['tapip', '탭아이피', '탭ip']):
        return "TAP IP"
    if any(k in name_norm for k in ['tap', '탭', '터치컨트롤러']):
        return "TAP"
        
    return "Others"
