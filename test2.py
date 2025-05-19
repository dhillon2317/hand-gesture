import cv2
import time  # Import time module for adding delay
import mediapipe as mp
import pyautogui
from feature import get_distance

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=2  # Set to 2 to detect two hands
)
draw = mp.solutions.drawing_utils

# Initialize variables for smoothing mouse movement
prev_x, prev_y = 0, 0
alpha = 0.7  # Smoothing factor

def recognize_gesture(landmarks):
    # Define the landmarks for the thumb and index finger tips
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    
    # Calculate the distance between the thumb and index finger tips
    distance = get_distance(thumb_tip, index_tip)
    
    # Define gesture based on distance
    if distance < 0.05:  # Adjust the threshold as needed
        pyautogui.click()
        return "Left Click"
    else:
        return "No Click"

def move_mouse(landmarks):
    global prev_x, prev_y, alpha
    # Use the index finger tip to move the mouse cursor
    index_tip = landmarks[8]
    screen_width, screen_height = pyautogui.size()
    x, y = int(index_tip[0] * screen_width), int(index_tip[1] * screen_height)
    
    # Smooth the mouse movement
    smooth_x = int(prev_x * alpha + x * (1 - alpha))
    smooth_y = int(prev_y * alpha + y * (1 - alpha))
    
    pyautogui.moveTo(smooth_x, smooth_y)
    prev_x, prev_y = smooth_x, smooth_y

def check_both_hands_gesture(landmarks1, landmarks2):
    # Check if all fingertips are touching together for both hands
    fingertips1 = [landmarks1[i] for i in [4, 8, 12, 16, 20]]
    fingertips2 = [landmarks2[i] for i in [4, 8, 12, 16, 20]]
    
    distances1 = [get_distance(fingertips1[i], fingertips1[i+1]) for i in range(len(fingertips1)-1)]
    distances2 = [get_distance(fingertips2[i], fingertips2[i+1]) for i in range(len(fingertips2)-1)]
    
    if all(d < 0.05 for d in distances1) and all(d < 0.05 for d in distances2):
        return True
    return False

def main():
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    # Set the frame rate to 60 FPS
    cap.set(cv2.CAP_PROP_FPS, 60)
    
    print("Camera opened:", cap.isOpened())
    
    cv2.namedWindow('Frame1', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Frame1', 1280, 720)  # Adjust the window size to fit your screen
    
    try:
        while cap.isOpened():
            start_time = time.time()
            ret, frame = cap.read()
            
            if not ret:
                print("Error: Could not read frame")
                break

            frame = cv2.flip(frame, 1)
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            processed = hands.process(frameRGB)

            if processed.multi_hand_landmarks:
                if len(processed.multi_hand_landmarks) == 2:
                    landmarks1 = [(lm.x, lm.y) for lm in processed.multi_hand_landmarks[0].landmark]
                    landmarks2 = [(lm.x, lm.y) for lm in processed.multi_hand_landmarks[1].landmark]
                    
                    if check_both_hands_gesture(landmarks1, landmarks2):
                        pyautogui.hotkey('win', 'tab')
                        gesture = "Switch Desktop"
                    else:
                        gesture = "No Gesture"
                else:
                    for hand_landmarks in processed.multi_hand_landmarks:
                        draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)
                        
                        landmarks = [(lm.x, lm.y) for lm in hand_landmarks.landmark]
                        gesture = recognize_gesture(landmarks)
                        move_mouse(landmarks)
                        cv2.putText(frame, gesture, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3, cv2.LINE_AA)

            cv2.imshow('Frame1', frame)

            if cv2.getWindowProperty('Frame1', cv2.WND_PROP_VISIBLE) < 1:
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            # Ensure the loop runs at 60 FPS
            elapsed_time = time.time() - start_time
            time.sleep(max(1./60 - elapsed_time, 0))
                
    finally:
        if cap.isOpened():
            cap.release()
        cv2.destroyAllWindows()
        time.sleep(1)  # Add a small delay before destroying windows to ensure it closes properly
        print("Resources released")

if __name__ == "__main__":
    main()