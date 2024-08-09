import tkinter as tk
import tkinter.messagebox
import random
from math import sin, cos, pi, log

# Constants
WIDTH = 888
HEIGHT = 500
HEART_X = WIDTH / 2
HEART_Y = HEIGHT / 2
SIDE = 11
HEART_COLOR = "pink"  # Color of the heart, can be changed


class Heart:
    def __init__(self, generate_frame=20):
        self._points = set()  # Original heart coordinate set
        self._edge_diffusion_points = set()  # Edge diffusion effect points
        self._center_diffusion_points = set()  # Center diffusion effect points
        self.all_points = {}  # Dynamic points for each frame

        self.build(2000)
        self.generate_frame = generate_frame

        for frame in range(generate_frame):
            self.calc(frame)

    def build(self, number):
        for _ in range(number):
            t = random.uniform(0, 2 * pi)
            x, y = heart_function(t)
            self._points.add((x, y))

        for _x, _y in list(self._points):
            for _ in range(3):
                x, y = scatter_inside(_x, _y, 0.05)
                self._edge_diffusion_points.add((x, y))

        point_list = list(self._points)
        for _ in range(4000):
            x, y = random.choice(point_list)
            x, y = scatter_inside(x, y, 0.17)
            self._center_diffusion_points.add((x, y))

    def calc(self, generate_frame):
        ratio = 10 * curve(generate_frame / 10 * pi)  # Smooth scaling factor
        halo_radius = int(4 + 6 * (1 + curve(generate_frame / 10 * pi)))
        halo_number = int(3000 + 4000 * abs(curve(generate_frame / 10 * pi) ** 2))

        all_points = []
        heart_halo_point = set()

        for _ in range(halo_number):
            t = random.uniform(0, 2 * pi)
            x, y = heart_function(t, shrink_ratio=11.6)
            x, y = shrink(x, y, halo_radius)
            if (x, y) not in heart_halo_point:
                heart_halo_point.add((x, y))
                x += random.randint(-14, 14)
                y += random.randint(-14, 14)
                size = random.choice((1, 2, 2))
                all_points.append((x, y, size))

        for x, y in self._points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 3)
            all_points.append((x, y, size))

        for x, y in self._edge_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))

        for x, y in self._center_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))

        self.all_points[generate_frame] = all_points

    @staticmethod
    def calc_position(x, y, ratio):
        force = 1 / (((x - HEART_X) ** 2 + (y - HEART_Y) ** 2) ** 0.520)
        dx = ratio * force * (x - HEART_X) + random.randint(-1, 1)
        dy = ratio * force * (y - HEART_Y) + random.randint(-1, 1)
        return x - dx, y - dy

    def render(self, render_canvas, render_frame):
        for x, y, size in self.all_points[render_frame % self.generate_frame]:
            render_canvas.create_rectangle(x, y, x + size, y + size, width=0, fill=HEART_COLOR)


def heart_function(t, shrink_ratio: float = SIDE):
    x = 16 * (sin(t) ** 3)
    y = -(13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t))
    x *= shrink_ratio
    y *= shrink_ratio
    x += HEART_X
    y += HEART_Y
    return int(x), int(y)


def scatter_inside(x, y, beta=0.15):
    ratio_x = -beta * log(random.random())
    ratio_y = -beta * log(random.random())
    dx = ratio_x * (x - HEART_X)
    dy = ratio_y * (y - HEART_Y)
    return x - dx, y - dy


def shrink(x, y, ratio):
    force = -1 / (((x - HEART_X) ** 2 + (y - HEART_Y) ** 2) ** 0.6)
    dx = ratio * force * (x - HEART_X)
    dy = ratio * force * (y - HEART_Y)
    return x - dx, y - dy


def curve(p):
    return 2 * (2 * sin(4 * p)) / (2 * pi)


def draw(main: tk.Tk, render_canvas: tk.Canvas, render_heart: Heart, render_frame=0):
    render_canvas.delete('all')
    render_heart.render(render_canvas, render_frame)
    main.after(160, draw, main, render_canvas, render_heart, render_frame + 1)


def love():
    root = tk.Tk()
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    x = (screenwidth - WIDTH) // 2
    y = (screenheight - HEIGHT) // 2 - 66
    root.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")
    root.title("❤")
    canvas = tk.Canvas(root, bg='black', height=HEIGHT, width=WIDTH)
    canvas.pack()

    heart = Heart()
    draw(root, canvas, heart)

    tk.Label(root, text="I Love You!", bg="black", fg="#FF99CC", font="Helvetica 25 bold").place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    root.mainloop()


def main_interface():
    root = tk.Tk()
    root.title('❤')
    root.resizable(0, 0)

    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    width = 300
    height = 100
    x = (screenwidth - width) / 2
    y = (screenheight - height) / 2 - 66
    root.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

    tk.Label(root, text='Honey, would you want to be my girlfriend?', width=37, font=('Arial', 12)).place(x=0, y=10)

    def ok():
        root.destroy()
        love()

    def no():
        tk.messagebox.showwarning('❤', 'One more chance!')

    def close_window():
        tk.messagebox.showwarning('❤', "You can't run away!")

    tk.Button(root, text='Yes', width=5, height=1, command=ok).place(x=80, y=50)
    tk.Button(root, text='No', width=5, height=1, command=no).place(x=160, y=50)
    root.protocol('WM_DELETE_WINDOW', close_window)

    root.mainloop()


if __name__ == '__main__':
    main_interface()