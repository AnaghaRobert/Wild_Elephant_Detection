import cv2
from detector import ElephantDetector
from config import VIDEO_SOURCE, DISPLAY_WIDTH, DISPLAY_HEIGHT, FRAME_SKIP

def main():
    detector = ElephantDetector()
    cap = cv2.VideoCapture(VIDEO_SOURCE)
    
    if not cap.isOpened():
        print("Error: Could not open video source")
        return
    
    print("Starting elephant detection system...")
    print(f"Settings: Confidence={detector.model.conf}, NMS={detector.model.iou}")
    
    try:
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret: 
                print("Video ended or error reading frame")
                break
            
            frame_count += 1
            if frame_count % FRAME_SKIP != 0:
                continue
            
            processed_frame = detector.detect(frame)
            display_frame = cv2.resize(processed_frame, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
            
            # Show processing info
            cv2.putText(display_frame, f"Frame: {frame_count}", (10, DISPLAY_HEIGHT-20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
            
            cv2.imshow('Elephant Detection', display_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("System stopped")

if __name__ == "__main__":
    main()