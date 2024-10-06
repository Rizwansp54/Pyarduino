import mediapipe as mp
import cv2
import time
import serial

# Initialize the serial connection to Arduino
ser = serial.Serial('COM3', 9600)
time.sleep(2)  # Allow some time for the serial connection to establish

def send_data(data):
    ser.write(str(data).encode())  # Convert data to string before sending
    print(f"Sent: {data}")

# Initialize MediaPipe components
mp_draw = mp.solutions.drawing_utils  # For drawing landmarks on images or frames
mp_hand = mp.solutions.hands

# Define tip IDs for fingers
tip_ids = [4, 8, 12, 16, 20]

# Open the webcam
video = cv2.VideoCapture(0)

# Initialize hand detection
with mp_hand.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while True:
        ret, image = video.read()
        
        # Check if the frame is read correctly
        if not ret:
            print("Failed to capture image.")
            break

        # Convert the image to RGB for MediaPipe processing
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        
        # Convert the image back to BGR for OpenCV
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Initialize list to hold landmarks
        landmark_list = []

        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                my_hands = hand_landmark
                for id, lm in enumerate(my_hands.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    landmark_list.append([id, cx, cy])
                
                # Draw the hand landmarks on the image
                mp_draw.draw_landmarks(image, my_hands, mp_hand.HAND_CONNECTIONS)

                # Initialize fingers list to count the number of fingers up
                fingers = []

                # Check thumb
                if landmark_list[tip_ids[0]][1] > landmark_list[tip_ids[0] - 1][1]:
                    fingers.append(1)  # Thumb is up
                else:
                    fingers.append(0)  # Thumb is down
                
                # Check other fingers
                for id in range(1, 5):
                    if landmark_list[tip_ids[id]][2] < landmark_list[tip_ids[id] - 2][2]:
                        fingers.append(1)  # Finger is up
                    else:
                        fingers.append(0)  # Finger is down

                # Count the total number of fingers up
                total_fingers = fingers.count(1)

                send_data(total_fingers)  # Send the number of fingers to Arduino
                time.sleep(0.5)  # Slight delay for sending data

                # Display the count and LED status on the image
                cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, str(total_fingers), (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                cv2.putText(image, "LED", (100, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)

        # Show the resulting image
        cv2.imshow("Frame", image)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break

# Release the webcam and close all OpenCV windows
video.release()
cv2.destroyAllWindows()
