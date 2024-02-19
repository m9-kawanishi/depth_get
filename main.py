import cv2
import numpy as np
from realsense_depth import DepthCamera
from graph import DepthDataVisualizer

class Application:
    def __init__(self):
        self.depth_colormap_scale = 0.05
        self.drawing = False
        self.ix, self.iy = -1, -1
        self.ex, self.ey = -1, -1
        self.dc = DepthCamera()

    def draw_rectangle(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.ix, self.iy = x, y
            self.ex, self.ey = x, y

        elif event == cv2.EVENT_MOUSEMOVE and self.drawing:
            self.ex, self.ey = x, y

        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            self.ex, self.ey = x, y
            depth_info = self.get_depth_info(self.ix, self.iy, self.ex, self.ey)
            a = DepthDataVisualizer()
            a.plot_data(depth_info)
            a.show()

    def get_depth_info(self, ix, iy, ex, ey):
        depth_frame = self.dc.get_frame()[-1]
        tmp = []
        for y in range(min(iy, ey), max(iy, ey)):
            for x in range(min(ix, ex), max(ix, ex)):
                depth = depth_frame.get_distance(x, y) * 1000  # Convert to mm
                tmp.append([x, y, depth])
        return tmp

    def run(self):
        while True:
            ret, depth_frame, color_frame, depth_map, frame = self.dc.get_frame()
            if not ret:
                break

            if self.ix != -1 and self.iy != -1 and self.ex != -1 and self.ey != -1:
                cv2.rectangle(color_frame, (self.ix, self.iy), (self.ex, self.ey), (0, 255, 0), 2)

            cv2.imshow("Depth Frame", depth_map)
            cv2.imshow("Color Frame", color_frame)
            cv2.setMouseCallback("Color Frame", self.draw_rectangle)

            if cv2.waitKey(1) & 0xFF == 27:  # ESC key
                break

        self.dc.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = Application()
    app.run()
