import random
import math
import pygame

def ball_collision(x1, y1, v1x, v1y, x2, y2, v2x, v2y, m1=1.0, m2=1.0):
    """
    二维小球弹性碰撞
    :param x1,y1: 球1圆心坐标
    :param v1x,v1y: 球1当前速度
    :param x2,y2: 球2圆心坐标
    :param v2x,v2y: 球2当前速度
    :param m1,m2: 质量，默认都为1
    :return: (v1x_new, v1y_new), (v2x_new, v2y_new)
    """
    dx = x1 - x2
    dy = y1 - y2
    dist = math.hypot(dx, dy)
    if dist < 1e-9:
        return (v1x, v1y), (v2x, v2y)
    # 法线单位向量
    nx = dx / dist
    ny = dy / dist
    # 切向单位向量
    tx = -ny
    ty = nx
    # 速度投影到法向、切向
    v1n = v1x * nx + v1y * ny
    v1t = v1x * tx + v1y * ty
    v2n = v2x * nx + v2y * ny
    v2t = v2x * tx + v2y * ty

    # 切向速度不变
    v1t_new = v1t
    v2t_new = v2t
    # 法向一维弹性碰撞公式
    v1n_new = ((m1 - m2) * v1n + 2 * m2 * v2n) / (m1 + m2)
    v2n_new = ((m2 - m1) * v2n + 2 * m1 * v1n) / (m1 + m2)

    # 转回xy分量
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
        # X墙壁碰撞
        if self.px <= self.r:
            self.px = self.r
            self.vx = -self.vx
        elif self.px >= wall.size[0] - self.r:
            self.px = wall.size[0] - self.r
            self.vx = -self.vx
        # Y墙壁碰撞
        if self.py <= self.r:
            self.py = self.r
            self.vy = -self.vy
        elif self.py >= wall.size[1] - self.r:
            self.py = wall.size[1] - self.r
            self.vy = -self.vy

    def distance(self, other):
        return cal_distance(self.px, self.py, other.px, other.py)

    def collision_pp(self, other):
        # 一次计算得到两个球新速度，只调用一次
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

    def run(self, p_list: list[Particle], wall: Wall):
        # pygame初始化
        pygame.init()
        SCALE = 60  # 缩放系数：物理坐标 × scale -> 像素
        w_pixel = int(wall.size[0] * SCALE)
        h_pixel = int(wall.size[1] * SCALE)
        screen = pygame.display.set_mode((w_pixel, h_pixel))
        pygame.display.set_caption("2D Elastic Collision")
        clock = pygame.time.Clock()
        dt = 1/60  # 固定物理时间步

        running = True
        while running:
            # 窗口事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # 物理更新
            self.flush(p_list, dt)

            # 粒子两两碰撞检测
            for key in self.key_dict:
                dist = self.key_dict[key]
                idx_lt = key.split('--')
                idx1 = int(idx_lt[0].strip('p'))
                idx2 = int(idx_lt[-1])
                p1 = p_list[idx1]
                p2 = p_list[idx2]
                if dist <= (p1.r + p2.r):
                    p1.collision_pp(p2)

            # 墙碰撞
            for p in p_list:
                p.collision_wall(wall)

            # ========== 渲染 ==========
            screen.fill((0, 0, 0))
            for p in p_list:
                px_pix = int(p.px * SCALE)
                py_pix = int(p.py * SCALE)
                r_pix = max(2, int(p.r * SCALE))
                pygame.draw.circle(screen, p.color, (px_pix, py_pix), r_pix)

            pygame.display.flip()
            clock.tick(60)
        pygame.quit()

    def flush(self, p_list, dt):
        # 移动粒子
        for p in p_list:
            p.motion(dt)

        # 清空列表，防止内存累积
        self.__distance.clear()
        self.__key_lt.clear()

        # 计算所有两两距离
        for idx, particle in enumerate(p_list):
            for i in range(idx + 1, len(p_list)):
                dist = particle.distance(p_list[i])
                self.__distance.append(dist)
                self.__key_lt.append(f'p{idx}--{i}')
        self.key_dict = dict(zip(self.__key_lt, self.__distance))
        return self.key_dict


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
            # 保证生成位置不和已有粒子重叠
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


if __name__ == '__main__':
    wall = Wall((10, 10))
    p_list = gen_particles(50, wall, radius=0.1)
    g_state = GlobalState()
    g_state.run(p_list, wall)
