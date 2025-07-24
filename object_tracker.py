import cv2
import numpy as np
import time

def main():
    # Initialize video capture from Iriun Webcam (USB)
    cap = cv2.VideoCapture(2) 

    if not cap.isOpened():
        print("Error: Could not open Iriun Webcam. ")
        return

    # Read the first frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame from Iriun Webcam.")
        cap.release()
        return

    # Allow user to select a region of interest (ROI) for tracking
    bbox = cv2.selectROI("Select Object", frame, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow("Select Object")

    # Extract the template (ROI) for matching
    x, y, w, h = [int(v) for v in bbox]
    template = frame[y:y+h, x:x+w]
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)  # Convert to grayscale for matching check

    # Initialize the CSRT tracker
    tracker = cv2.TrackerCSRT_create()
    tracker.init(frame, bbox)

    while True:
        start_time = time.time()  # For FPS calculation
        ret, frame = cap.read()
        if not ret:
            print("Error: Lost connection to Iriun Webcam.")
            break

        # Create a grayscale copy for template matching
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Always perform template matching
        result = cv2.matchTemplate(frame_gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Update tracker
        success, tracker_bbox = tracker.update(frame)

        # Decide whether to use tracker or template matching
        if success and max_val < 0.7:
            # Tracker is successful, and template match is weak: use tracker
            x, y, w, h = [int(v) for v in tracker_bbox]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Tracking (Tracker)", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        elif max_val > 0.7:
            # Strong template match: reinitialize tracker
            new_x, new_y = max_loc
            new_bbox = (new_x, new_y, w, h)  # Keep original width/height
            tracker = cv2.TrackerCSRT_create()
            tracker.init(frame, new_bbox)
            x, y, w, h = [int(v) for v in new_bbox]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Tracking (Reacquired)", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        else:
            # Neither tracker nor template matching is successful
            cv2.putText(frame, "Lost, searching...", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

        # Calculate and display FPS
        fps = 1.0 / (time.time() - start_time)
        cv2.putText(frame, f"FPS: {fps:.2f}", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

        # Display the frame
        cv2.imshow("Object Tracker", frame)

        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Clean up
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()