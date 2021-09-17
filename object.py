import cv2


class Object:
    def __init__(self, path):
        self.img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        self.name = path[8:-4]
        self.width = self.img.shape[1]
        self.height = self.img.shape[0]
        self.location = None

    def matching(self, screen):
        matching_values = cv2.matchTemplate(screen, self.img, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(matching_values)

        start_loc = max_loc
        end_loc = (start_loc[0] + self.width, start_loc[1] + self.height)

        if max_val > 0.8:
            self.location = [start_loc, end_loc]
            return True
        else:
            return False

