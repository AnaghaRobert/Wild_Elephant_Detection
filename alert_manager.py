from twilio.rest import Client
import time
import cv2
import os
from config import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_PHONE_NUMBER,
    ALERT_PHONE_NUMBER,
    ALERT_COOLDOWN,
    ALERT_IMAGE_QUALITY,MAX_ALERTS_PER_HOUR 
)

class AlertManager:
    def __init__(self):
        self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        self.alert_history = []
        
    def _clean_alert_history(self):
        """Remove old alerts from history"""
        current_time = time.time()
        self.alert_history = [t for t in self.alert_history 
                            if current_time - t < 3600]  # Keep last hour
        
    def can_send_alert(self):
        """Check if alert can be sent based on rate limits"""
        self._clean_alert_history()
        return len(self.alert_history) < MAX_ALERTS_PER_HOUR
        
    def send_alert(self, frame):
        try:
            # Always save image
            alert_img = f"alerts/elephant_{int(time.time())}.jpg"
            cv2.imwrite(alert_img, frame)
            
            # Try to send SMS if under limit
            try:
                message = self.client.messages.create(
                    body=f"🚨 Elephant Detected! View: {alert_img}",
                    from_=TWILIO_PHONE_NUMBER,
                    to=ALERT_PHONE_NUMBER
                )
                print("✅ Alert sent via SMS")
            except Exception as e:
                print(f"⚠️ SMS alert failed (saving locally): {str(e)}")
                
            return True
            
        except Exception as e:
            print(f"❌ Alert completely failed: {str(e)}")
            return False