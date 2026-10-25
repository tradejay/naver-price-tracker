"""
SMTP Email Notification Engine with Alert Aggregation.
"""
import smtplib
from email.message import EmailMessage
from datetime import datetime
from typing import List, Dict, Any

class PriceAlertNotifier:
    def __init__(self, smtp_server: str, smtp_port: int, sender_email: str, sender_password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        
    def send_alert_report(self, receivers: List[str], alerts: List[Dict[str, Any]], html_content: str) -> bool:
        """
        Sends an HTML warning email when unauthorized low-price listings are detected.
        """
        msg = EmailMessage()
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        msg['Subject'] = f"[네이버 최저가 트래킹] 로지텍 MSRP 미만 할인 경보 ({now_str} / {len(alerts)}건)"
        msg['From'] = self.sender_email
        msg['To'] = ", ".join(receivers)
        
        msg.set_content(f"네이버 최저가 모니터링: 총 {len(alerts)}건의 비인가 할인 상품이 적발되었습니다.")
        msg.add_alternative(html_content, subtype='html')
        
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
