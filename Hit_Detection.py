import cv2
import numpy as np

# Camera calibration parameters
focal_length = 1000  # In pixels
real_object_width = 0.01  # In meters

def estimate_distance(pixel_width):
    # Calculate the distance from the camera to the object
    return (real_object_width * focal_length) / pixel_width

# Function to calculate Euclidean distance in pixels between two points
def euclidean_distance_pixels(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Function to convert pixel distance to real-world distance
def pixel_to_real_distance(pixel_distance, distance_to_object):
    real_distance = pixel_distance * (real_object_width / distance_to_object)
    return real_distance

# This function generates uniform points with a small gap between the first and second centers
def draw_dotted_line(img, pt1, pt2, color, thickness=1, gap=20):
    dist = ((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)**0.5
    pts = []
    for i in np.arange(0, dist, gap):
        r = i / dist
        x = int((pt1[0] * (1 - r) + pt2[0] * r) + 0.5)
        y = int((pt1[1] * (1 - r) + pt2[1] * r) + 0.5)
        pts.append((x, y))
    for p in pts:
        cv2.circle(img, p, thickness, color, -1)

video_path = r"E:\AUB\Research Bakarji\Codes\teensy\Data_hits2.mp4" 
cap = cv2.VideoCapture(video_path)
object_coordinates = []

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Apply a mask to detect green color
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_green = np.array([35, 100, 100])
    upper_green = np.array([85, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Clear previous frame's object coordinates
    frame_coordinates = []

    for contour in contours:
        if cv2.contourArea(contour) > 500:
            x, y, w, h = cv2.boundingRect(contour)
            center_x = x + w // 2
            center_y = y + h // 2
            
            # Draw a circle at the center
            cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
            
            # Display the coordinates of the center
            cv2.putText(frame, f"Center: ({center_x}, {center_y})", 
                        (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.7, (255, 255, 255), 2, cv2.LINE_AA)
            
            pixel_width = w  # Using width as an approximation of size

            # Estimate distance to the object
            distance = estimate_distance(pixel_width)

            # Draw bounding box and distance
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f'Distance: {distance:.2f} m', 
                        (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.7, (0, 255, 0), 2, cv2.LINE_AA)

            # Save the coordinates of this object
            frame_coordinates.append([center_x, center_y, distance, pixel_width])

    # Append this frame's object coordinates to the overall list
    object_coordinates.append(frame_coordinates)

    # Calculate distance between centers of the first two rectangles in meters
    if len(frame_coordinates) >= 2:
        center1 = frame_coordinates[0][:2]  # (center_x, center_y)
        center2 = frame_coordinates[1][:2]  # (center_x, center_y)
        distance_to_object1 = frame_coordinates[0][2]  # distance to object 1
        distance_to_object2 = frame_coordinates[1][2]  # distance to object 2
        pixel_distance = euclidean_distance_pixels(center1, center2)
        
        # Calculate the average distance to the objects
        average_distance = (distance_to_object1 + distance_to_object2) / 2
        real_distance_between_centers = pixel_to_real_distance(pixel_distance, average_distance)

        # Draw the distance in meters on the frame
        midpoint_x = (center1[0] + center2[0]) // 2
        midpoint_y = (center1[1] + center2[1]) // 2
        cv2.putText(frame, f'Center Dist: {real_distance_between_centers:.4f} cm', 
                    (midpoint_x, midpoint_y), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.7, (255, 0, 0), 2, cv2.LINE_AA)
        
        # Draw a dotted line between the centers
        draw_dotted_line(frame, tuple(center1), tuple(center2), (255, 0, 0), thickness=3, gap=10)

    cv2.imshow('Tracked Video', frame)
    
    # Increase the delay to slow down the video playback, press q to quit
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
