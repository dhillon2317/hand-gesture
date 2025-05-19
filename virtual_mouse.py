import cv2
def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    print("Camera opened:", cap.isOpened())
    
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            
            if not ret:
                print("Error: Could not read frame")
                break

            # Remove or adjust the flip line as per your requirement
            # frame = cv2.flip(frame, 0)  # Uncomment if you want to flip the frame vertically
            
            cv2.imshow('Frame1', frame)

            # Check if the window is closed
            if cv2.getWindowProperty('Frame1', cv2.WND_PROP_VISIBLE) < 1:
                cap.release()
                cv2.destroyWindow('Frame1')
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    finally:
        if cap.isOpened():
            cap.release()
        cv2.destroyAllWindows()
        time.sleep(1)  # Add a small delay before destroying windows to ensure it closes properly
        print("Resources released")

if __name__ == "__main__":
    main()
