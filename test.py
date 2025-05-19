import cv2
import time  # Import time module for adding delay
import mediapipe as mp

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode = False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1
)

def main():
    cap = cv2.VideoCapture(0)
    draw = mp.solutions.drawing_utils
    
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
            #frame = cv2.flip(frame, 1)  # Uncomment if you want to flip the frame vertically
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            processed = hands.process(frameRGB)
            landmarks_list = []

            if processed.multi_hand_landmarks:
                hands_landmarks = processed.multi_hand_landmarks[0]
                draw.draw_landmarks(frame, hands_landmarks,mpHands.HAND_CONNECTIONS)

                for lm in hands_landmarks:
                    landmarks_list.append((lm.x,lm.y))

                print(landmarks_list)

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
