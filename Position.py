class Position:

    def __init__(self, x, y, z, delta, flag):
        self._x = x
        self._y = y
        self._z = z
        self._delta = delta
        self._flag = flag

    def get_x(self):
        return self._x

    def set_x(self, x):
        self._x = x

    def get_y(self):
        return self._y

    def set_y(self, y):
        self._y = y

    def get_z(self):
        return self._z

    def set_z(self, z):
        self._z = z

    def get_delta(self):
        return self._delta

    def set_delta(self, delta):
        self._delta = delta

    def get_flag(self):
        return self._flag

    def set_flag(self, flag):
        self._flag = flag
