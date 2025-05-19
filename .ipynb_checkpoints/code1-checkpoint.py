import cv2 
def main():
    cap = cv2 .VideoCapture(0)

    try:
        while cap.isOpened():
            ret,frame = cap.read()

            if not ret :
                break
            frame = cv2.flip(frame , 1)

            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

        if __name__ =="__main__":
            main()