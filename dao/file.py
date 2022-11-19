import os


class RobotFile:
    def __init__(self, draw_one):
        self.draw_one_dir = draw_one
        self.draw_one_map = []
        self.draw_one_len = 0
        self._read_file_map()

    def _read_file_map(self):
        file_dir = self.draw_one_dir
        file_lines = open(file_dir).read().splitlines()
        draw_one_map = []
        for lines in file_lines:
            lines_arr = lines.split(",")
            idx = int(lines_arr[0])
            poem = lines_arr[1]
            explain = lines_arr[2]
            draw_one_map[idx] = (poem, explain)

        self.draw_one_map = draw_one_map
        self.draw_one_len = len(draw_one_map)
