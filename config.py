import os
from pathlib import Path
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
# Model Configuration
PROJECT_ROOT = Path(__file__).parent.absolute()
MODEL_PATH = PROJECT_ROOT / "models" / "elephant_model_windows.pt"

# Video Configuration
VIDEO_SOURCE = 0            # 0 for default webcam, or path to video file
DISPLAY_WIDTH = 800         # Display window width
DISPLAY_HEIGHT = 600        # Display window height
FRAME_SKIP = 2             # Process every nth frame to reduce computation
CONFIDENCE_THRESHOLD = 0.56# Minimum confidence score for detection
NMS_THRESHOLD = 0.4         # Non-Maximum Suppression threshold
# Add to your existing config.py
MIN_ELEPHANT_SIZE = 5000  # Minimum pixel area for elephant detection
MAX_ALERTS_PER_HOUR = 6   # Rate limiting
ALERT_IMAGE_QUALITY = 95  # JPEG quality (1-100)
# Verify model file exists
if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}")

# Twilio Configuration
TWILIO_ACCOUNT_SID = ''  # Should start with AC
TWILIO_AUTH_TOKEN = ''    # Case-sensitive
TWILIO_PHONE_NUMBER = ''  # Format: +1XXXXXXXXXX (no spaces)
ALERT_PHONE_NUMBER = ''  # Must be verified in Twilio if trial account  # Number to receive alerts
ALERT_COOLDOWN = 60  # 5 minutes between alerts (seconds)


# Add these to your existing config.py
# Geofence Configuration (example coordinates)
GEOFENCE_BOUNDARY = [
    (12.9716, 77.5946),  # Vertex 1
    (12.9352, 77.6245),  # Vertex 2
    (12.9239, 77.5733)   # Vertex 3
]  # Automatically closes polygon
# GPS Configuration
GPS_PORT = 'COM3'  # Windows COM port  # Linux USB port for Android
GPS_BAUDRATE = 9600
