import cv2
import torch
import os
import time
from alert_manager import AlertManager
from yolov5 import YOLOv5
from config import CONFIDENCE_THRESHOLD, NMS_THRESHOLD, MIN_ELEPHANT_SIZE

class ElephantDetector:
    def __init__(self):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.last_detection_time = 0  # Initialize time tracking
        
        # Load model with updated autocast settings
        torch.backends.cudnn.benchmark = True
        self.model = YOLOv5('models/elephant_model_windows.pt', device=self.device)
        
        # Handle autocast deprecation warning
        if hasattr(torch, 'amp'):
            self.model.amp = lambda enabled: torch.amp.autocast('cuda', enabled=enabled)
        else:
            self.model.amp = lambda enabled: torch.cuda.amp.autocast(enabled=enabled)
        
        self.model.conf = max(CONFIDENCE_THRESHOLD, 0.7)
        self.model.iou = NMS_THRESHOLD
        self.alert_manager = AlertManager()
        os.makedirs("alerts", exist_ok=True)

    def _is_valid_detection(self, det):
        """Check if detection meets all criteria"""
        x1, y1, x2, y2, conf, cls = det
        if int(cls) != 0 or conf < self.model.conf:
            return False
            
        # Check minimum size requirement
        area = (x2 - x1) * (y2 - y1)
        return area >= MIN_ELEPHANT_SIZE

    def detect(self, frame):
        results = self.model.predict(frame, size=640)
        detections = [det for det in results.pred[0] if self._is_valid_detection(det)]
        
        if detections:
            current_time = time.time()
            
            # Draw all valid detections
            for det in detections:
                x1, y1, x2, y2, conf, _ = det
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(frame, f"Elephant: {conf:.2f}", (int(x1), int(y1)-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
            
            # Only send alert for new detections
            if current_time - self.last_detection_time > 10:  # 10 sec minimum between alerts
                self.alert_manager.send_alert(frame)
                self.last_detection_time = current_time
            
        return frame