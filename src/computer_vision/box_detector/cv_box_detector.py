import cv2
import numpy as np
from src.domain.entities import Image
from src.domain.box_detector import BoxDetector
from typing import Optional

class CVBoxDetector(BoxDetector):
    """
    Determines whether a box (rectangular shape) is present in an image.
    """

    def has_box(self, raw_bytes: bytes, image: Optional[Image] = None) -> bool:
        # ---- Get numpy image ----
        img_array = np.frombuffer(raw_bytes, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        if img is None:
            return False

        # ---- Preprocessing ----
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        edges = cv2.Canny(blur, 50, 150)

        # ---- Find contours ----
        contours, _ = cv2.findContours(
            edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 1000:
                continue  # ignore small noise

            # Approximate contour
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

            # ---- Box criteria ----
            if len(approx) == 4 and cv2.isContourConvex(approx):
                x, y, w, h = cv2.boundingRect(approx)
                aspect_ratio = w / float(h)

                # reasonable rectangle shape
                if 0.3 < aspect_ratio < 3.5:
                    return True

        return False