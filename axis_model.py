x_max_cord = []
x_min_cord = []
z_max_cord = []
z_min_cord = []


def set_x_max(val):
    global x_max_cord
    x_max_cord.append(val)


def set_x_min(val):
    global x_min_cord
    x_min_cord.append(val)


def set_z_max(val):
    global z_max_cord
    z_max_cord.append(val)


def set_z_min(val):
    global z_min_cord
    z_min_cord.append(val)


def get_x_max():
    global x_max_cord
    return x_max_cord


def get_x_min():
    global x_min_cord
    return x_min_cord


def get_z_max():
    global z_max_cord
    return z_max_cord


def get_z_min():
    global z_min_cord
    return z_min_cord
