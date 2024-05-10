
import cv2
from openCV_movement_detection.details_movement import change_frame, get_mask, contour_movement, text_movement, \
    make_video_no_roi, make_video_roi


class VideoMovementClass:

    def detect_movement(self, path, rois=None, no_rois=None, min_contour_area=10, circularity_threshold=0.5, blur=1, brightness=1):
        cap = cv2.VideoCapture(path)
        ret, prev_frame = cap.read()
        prev_frame_gray = change_frame(prev_frame, brightness)
        if no_rois:
            prev_frame_gray = make_video_no_roi(prev_frame_gray, no_rois)
        if rois:
            prev_frame_gray = make_video_roi(prev_frame_gray, rois)
        text_list = []
        count = 0
        prev_count = 1
        while True:
            ret, next_frame = cap.read()
            if not ret:
                break
            count += 1
            if (count % 20) == 0:
                next_frame_gray = change_frame(next_frame, brightness)
                if no_rois:
                    next_frame_gray = make_video_no_roi(next_frame_gray, no_rois)
                if rois:
                    next_frame_gray = make_video_roi(next_frame_gray, rois)
                mask = get_mask(prev_frame_gray, next_frame_gray, blur)
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                movement_detected = contour_movement(contours, circularity_threshold, min_contour_area)
                text_list.append(text_movement(movement_detected, prev_count, count))
                prev_frame_gray = next_frame_gray
                prev_count = count
        cap.release()
        return text_list


