import random
import math
import pygame
import threading
import time

def ball_collision(x1, y1, v1x, v1y, x2, y2, v2x, v2y, m1=1.0, m2=1.0):
    dx = x1 - x2
    dy = y1 - y2
    dist = math.hypot(dx, dy)
    if dist < 1e-9:
        return (v1x, v1y), (v2x, v2y)
    nx = dx / dist
    ny = dy / dist
    tx = -ny
    ty = nx
    v1n = v1x * nx + v1y * ny
    v1t = v1x * tx + v1y * ty
    v2n = v2x * nx + v2y * ny
    v2t = v2x * tx + v2y * ty

    v1t_new = v1t
    v2t_new = v2t
    v1n_new = ((m1 - m2) * v1n + 2 * m2 * v2n) / (m1 + m2)
    v2n_new = ((m2 - m1) * v2n + 2 * m1 * v1n) / (m1 + m2)

    v1x_new = v1n_new * nx + v1t_new * tx
    v1y_new = v1n_new * ny + v1t_new * ty
    v2x_new = v2n_new * nx + v2t_new * tx
    v2y_new = v2n_new * ny + v2t_new * ty
    return (v1x_new, v1y_new), (v2x_new, v2y_new)


class Particle:
    def __init__(self, velocity_x: float, velocity_y: float, position_x: float, position_y: float, radius=0.1):
        self.vx = velocity_x
        self.vy = velocity_y
        self.px = position_x
        self.py = position_y
        self.r = radius
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

    def collision_wall(self, wall):
        if self.px <= self.r:
            self.px = self.r
            self.vx = -self.vx
        elif self.px >= wall.size[0] - self.r:
            self.px = wall.size[0] - self.r
            self.vx = -self.vx
        if self.py <= self.r:
            self.py = self.r
            self.vy = -self.vy
        elif self.py >= wall.size[1] - self.r:
            self.py = wall.size[1] - self.r
            self.vy = -self.vy

    def distance(self, other):
        return cal_distance(self.px, self.py, other.px, other.py)

    def collision_pp(self, other):
        (v1x, v1y), (v2x, v2y) = ball_collision(
            self.px, self.py, self.vx, self.vy,
            other.px, other.py, other.vx, other.vy
        )
        self.vx, self.vy = v1x, v1y
        other.vx, other.vy = v2x, v2y

    def motion(self, dt: float):
        self.px += self.vx * dt
        self.py += self.vy * dt


class Wall:
    def __init__(self, size: tuple[float]):
        self.size = size


class GlobalState:
    def __init__(self):
        self.__distance = []
        self.__key_lt = []
        self.key_dict = {}

    def flush(self, p_list, dt):
        for p in p_list:
            p.motion(dt)
        self.__distance.clear()
        self.__key_lt.clear()
        for idx, particle in enumerate(p_list):
            for i in range(idx + 1, len(p_list)):
                dist = particle.distance(p_list[i])
                self.__distance.append(dist)
                self.__key_lt.append(f'p{idx}--{i}')
        self.key_dict = dict(zip(self.__key_lt, self.__distance))


def cal_distance(px1, py1, px2, py2):
    return math.sqrt((px1 - px2) ** 2 + (py1 - py2) ** 2)


def gen_random_param(num, wall, radius=0.1):
    params = []
    position_lt = []
    x_lim, y_lim = wall.size
    for n in range(num):
        while True:
            px = random.uniform(radius, x_lim - radius)
            py = random.uniform(radius, y_lim - radius)
            if all(cal_distance(px, py, *coord) >= 2 * radius for coord in position_lt):
                position_lt.append((px, py))
                break
        vx, vy = [random.random() for _ in range(2)]
        param = [vx, vy, px, py]
        params.append(param)
    return params


def gen_particles(num, wall, radius=0.1):
    p_list = []
    params = gen_random_param(num, wall, radius)
    for param in params:
        p_list.append(Particle(*param, radius))
    return p_list


# =====物理子线程函数=====
def physics_thread(p_list, wall, lock, stop_event, dt=1/60):
    g_state = GlobalState()
    print("物理子线程启动")
    while not stop_event.is_set():
        # 上锁：修改粒子数据期间，渲染线程不能读
        with lock:
            g_state.flush(p_list, dt)
            for key in g_state.key_dict:
                dist = g_state.key_dict[key]
                idx_lt = key.split('--')
                idx1 = int(idx_lt[0].strip('p'))
                idx2 = int(idx_lt[-1])
                p1 = p_list[idx1]
                p2 = p_list[idx2]
                if dist <= (p1.r + p2.r):
                    p1.collision_pp(p2)
            for p in p_list:
                p.collision_wall(wall)
        time.sleep(dt)


# =====主线程：pygame渲染=====
def render_main(wall: Wall, p_list, lock, stop_event):
    pygame.init()
    SCALE = 60
    w_pixel = int(wall.size[0] * SCALE)
    h_pixel = int(wall.size[1] * SCALE)
    screen = pygame.display.set_mode((w_pixel, h_pixel))
    pygame.display.set_caption("多线程小球碰撞")
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                stop_event.set()  # 通知物理线程退出

        screen.fill((0, 0, 0))
        # 上锁：读取粒子信息的时候，物理线程不能写
        with lock:
            for p in p_list:
                px_pix = int(p.px * SCALE)
                py_pix = int((wall.size[1] - p.py) * SCALE)
                r_pix = max(2, int(p.r * SCALE))
                pygame.draw.circle(screen, p.color, (px_pix, py_pix), r_pix)

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == '__main__':
    wall = Wall((10, 10))
    p_list = gen_particles(50, wall, radius=0.1)

    lock = threading.Lock()
    stop_event = threading.Event()  # 用来安全终止子线程

    # 创建物理子线程
    phy_thread = threading.Thread(
        target=physics_thread,
        args=(p_list, wall, lock, stop_event, 1/60),
        daemon=True
    )
    phy_thread.start()

    # 主线程渲染
    render_main(wall, p_list, lock, stop_event)
    phy_thread.join()
    print("程序正常退出")
