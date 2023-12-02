# import the opencv library
import cv2

# define a video capture object
vid = cv2.VideoCapture(0)

# flag to indicate whether to capture an image
capture_image = False

while True:
    # Capture the video frame by frame
    ret, frame = vid.read()

    # Display the resulting frame
    cv2.imshow('frame', frame)
    # Check if the image needs to be captured
    if cv2.waitKey(1) & 0xFF == ord(' '):
        # Save the captured frame as an image
        cv2.imwrite('captured_image.jpg', frame)
        print("Image captured!")
        # Reset the flag
        capture_image = False

    # Check if the 'q' button is pressed to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()