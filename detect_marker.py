import cv2 as cv
from cv2 import aruco
import numpy as np

marker_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)

param_markers = aruco.DetectorParameters_create()

cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    marker_corners, marker_IDs, reject = aruco.detectMarkers(
        gray_frame, marker_dict, parameters=param_markers
    )
    if marker_corners:
        for ids, corners in zip(marker_IDs, marker_corners):
            cv.polylines(
                frame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA
            )
            corners = corners.reshape(4, 2)
            corners = corners.astype(int)
            top_right = corners[0].ravel()
            top_left = corners[1].ravel()
            bottom_right = corners[2].ravel()
            bottom_left = corners[3].ravel()

            centroid_x = np.mean([top_right[0], top_left[0], bottom_right[0], bottom_left[0]]).astype(int)
            centroid_y = np.mean([top_right[1], top_left[1], bottom_right[1], bottom_left[1]]).astype(int)
            centroid = (centroid_x, centroid_y)

            

            # Draw centroid
            cv.circle(frame, centroid, 5, (0, 0, 255), -1)

            cv.putText(
                frame,
                f"id: {ids[0]}",
                (top_right[0], top_right[1]),
                cv.FONT_HERSHEY_PLAIN,
                1.3,
                (200, 100, 0),
                2,
                cv.LINE_AA,
            )
             # Print centroid coordinates
            print(f"Marker ID: {ids[0]} Centroid coordinates: {centroid}")

    cv.imshow("frame", frame)
    key = cv.waitKey(1)
    if key == ord("q"):
        break

cap.release()
cv.destroyAllWindows()
