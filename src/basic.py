from kivy.core.window import Window

def move_into_window(position, window_size):
    position[0] = max(position[0], 0)
    position[0] = min(position[0], Window.size[0] - window_size[0])
    position[1] = max(position[1], 0)
    position[1] = min(position[1], Window.size[1] - window_size[1])
    return position
    