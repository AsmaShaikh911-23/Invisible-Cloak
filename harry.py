import cv2
import numpy as np

def invisibility_cloak():

    cap = cv2.VideoCapture(0)

    print("Initializing camera...")

    # Capture background
    for i in range(60):
        ret, background = cap.read()

    background = cv2.flip(background, 1)

    print("Background captured!")
    print("Press 'q' to quit")

    while cap.isOpened():

        ret, frame = cap.read()

        if not ret:
            break

        # Flip frame
        frame = cv2.flip(frame, 1)

        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Red color mask
        lower_red1 = np.array([0, 120, 70])
        upper_red1 = np.array([10, 255, 255])

        lower_red2 = np.array([170, 120, 70])
        upper_red2 = np.array([180, 255, 255])

        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

        mask = mask1 + mask2

        # Remove noise
        kernel = np.ones((3, 3), np.uint8)

        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_OPEN,
            kernel,
            iterations=2
        )

        mask = cv2.dilate(mask, kernel, iterations=1)

        # Inverse mask
        mask_inv = cv2.bitwise_not(mask)

        # Current frame without cloak
        res1 = cv2.bitwise_and(frame, frame, mask=mask_inv)

        # Background only where cloak is present
        res2 = cv2.bitwise_and(background, background, mask=mask)

        # Final output
        final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

        # Show output
        cv2.imshow("Invisibility Cloak", final_output)

        # Quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    invisibility_cloak()