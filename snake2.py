import pygame
import random
import os

# 定义颜色
WHITE = (0xff, 0xff, 0xff)
BLACK = (0, 0, 0)
GREEN = (0, 0xff, 0)
RED = (0xff, 0, 0)
LINE_COLOR = (0x33, 0x33, 0x33)
FPS = 30

# 定义游戏难度等级，蛇移动速度逐渐加快
HARD_LEVEL = list(range(2, int(FPS / 2), 2))
hardness = HARD_LEVEL[0]

# 方向定义
D_LEFT, D_RIGHT, D_UP, D_DOWN = 0, 1, 2, 3

# 初始化 Pygame 和音频模块
pygame.init()
pygame.mixer.init()

# 游戏窗口尺寸
WIDTH, HEIGHT = 300, 300

# 蛇身体每一节的尺寸
CUBE_WIDTH = 20

# 计算屏幕可以容纳的网格数量
GRID_WIDTH_NUM, GRID_HEIGHT_NUM = int(WIDTH / CUBE_WIDTH), int(HEIGHT / CUBE_WIDTH)

# 设置窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("贪吃蛇")

# 获取资源文件路径
base_folder = os.path.dirname(__file__)
music_folder = os.path.join(base_folder, 'music')
img_folder = os.path.join(base_folder, 'images')

# 加载音乐和音效
pygame.mixer.music.load(os.path.join(music_folder, 'victory.ogg'))
bite_sound = pygame.mixer.Sound(os.path.join(music_folder, 'eat.wav'))

# 加载图片资源
back_img = pygame.image.load(os.path.join(img_folder, 'bgpic.png'))
snake_head_img = pygame.image.load(os.path.join(img_folder, 'snake.png'))
snake_head_img.set_colorkey(BLACK)
food_img = pygame.image.load(os.path.join(img_folder, 'food.png'))

# 调整背景图片和食物图片大小
background = pygame.transform.scale(back_img, (WIDTH, HEIGHT))
food = pygame.transform.scale(food_img, (CUBE_WIDTH, CUBE_WIDTH))

# 设置背景音乐音量并循环播放
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(loops=-1)

# 初始化计时器
clock = pygame.time.Clock()
running = True
counter = 0  # 游戏帧计数器

# 初始蛇的运动方向
direction = D_LEFT

# 初始化蛇的身体列表，包含头部位置
snake_body = [(int(GRID_WIDTH_NUM / 2) * CUBE_WIDTH, int(GRID_HEIGHT_NUM / 2) * CUBE_WIDTH)]

# 障碍物相关变量
NUM_OBSTACLES = 5
obstacles = []


# 生成障碍物
def generate_obstacles():
    obs_positions = []
    while len(obs_positions) < NUM_OBSTACLES:
        pos = (random.randint(0, GRID_WIDTH_NUM - 1), random.randint(0, GRID_HEIGHT_NUM - 1))
        if (pos[0] * CUBE_WIDTH, pos[1] * CUBE_WIDTH) not in snake_body and pos != food_pos:
            obs_positions.append(pos)
    return obs_positions


# 绘制障碍物
def draw_obstacles():
    for obs in obstacles:
        pygame.draw.rect(screen, RED, (obs[0] * CUBE_WIDTH, obs[1] * CUBE_WIDTH, CUBE_WIDTH, CUBE_WIDTH))


# 绘制网格
def draw_grids():
    for i in range(GRID_WIDTH_NUM):
        pygame.draw.line(screen, LINE_COLOR, (i * CUBE_WIDTH, 0), (i * CUBE_WIDTH, HEIGHT))
    for i in range(GRID_HEIGHT_NUM):
        pygame.draw.line(screen, LINE_COLOR, (0, i * CUBE_WIDTH), (WIDTH, i * CUBE_WIDTH))


# 绘制蛇
def draw_body(direction=D_LEFT):
    for sb in snake_body[1:]:
        screen.blit(food, sb)

    if direction == D_LEFT:
        rot = 0
    elif direction == D_RIGHT:
        rot = 180
    elif direction == D_UP:
        rot = 270
    elif direction == D_DOWN:
        rot = 90

    new_head_img = pygame.transform.rotate(snake_head_img, rot)
    head = pygame.transform.scale(new_head_img, (CUBE_WIDTH, CUBE_WIDTH))
    screen.blit(head, snake_body[0])


# 生成食物
def generate_food():
    while True:
        pos = (random.randint(0, GRID_WIDTH_NUM - 1), random.randint(0, GRID_HEIGHT_NUM - 1))
        if not (pos[0] * CUBE_WIDTH, pos[1] * CUBE_WIDTH) in snake_body and pos not in obstacles:
            return pos


# 绘制食物
def draw_food():
    screen.blit(food, (food_pos[0] * CUBE_WIDTH, food_pos[1] * CUBE_WIDTH))


# 判断蛇是否吃到食物
def grow():
    if snake_body[0][0] == food_pos[0] * CUBE_WIDTH and snake_body[0][1] == food_pos[1] * CUBE_WIDTH:
        bite_sound.play()
        return True
    return False


# 生成初始食物和障碍物
food_pos = generate_food()
obstacles = generate_obstacles()

# 游戏主循环
while running:
    clock.tick(FPS)

    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != D_DOWN:
                direction = D_UP
            elif event.key == pygame.K_DOWN and direction != D_UP:
                direction = D_DOWN
            elif event.key == pygame.K_LEFT and direction != D_RIGHT:
                direction = D_LEFT
            elif event.key == pygame.K_RIGHT and direction != D_LEFT:
                direction = D_RIGHT

    # 更新蛇的位置
    if counter % int(FPS / hardness) == 0:
        last_pos = snake_body[-1]

        # 身体部分移动
        for i in range(len(snake_body) - 1, 0, -1):
            snake_body[i] = snake_body[i - 1]

        # 更新头部位置
        if direction == D_UP:
            snake_body[0] = (snake_body[0][0], snake_body[0][1] - CUBE_WIDTH)
        elif direction == D_DOWN:
            snake_body[0] = (snake_body[0][0], snake_body[0][1] + CUBE_WIDTH)
        elif direction == D_LEFT:
            snake_body[0] = (snake_body[0][0] - CUBE_WIDTH, snake_body[0][1])
        elif direction == D_RIGHT:
            snake_body[0] = (snake_body[0][0] + CUBE_WIDTH, snake_body[0][1])

        # 检查碰撞
        if snake_body[0][0] < 0 or snake_body[0][0] >= WIDTH or snake_body[0][1] < 0 or snake_body[0][1] >= HEIGHT:
            running = False
        for sb in snake_body[1:]:
            if sb == snake_body[0]:
                running = False
        for obs in obstacles:
            if (snake_body[0][0] // CUBE_WIDTH, snake_body[0][1] // CUBE_WIDTH) == obs:
                running = False

        # 检查蛇是否吃到食物
        if grow():
            food_pos = generate_food()
            snake_body.append(last_pos)
            hardness = HARD_LEVEL[min(int(len(snake_body) / 10), len(HARD_LEVEL) - 1)]
            obstacles = generate_obstacles()

    # 绘制画面
    screen.blit(background, (0, 0))
    draw_grids()
    draw_body(direction)
    draw_food()
    draw_obstacles()

    # 更新计数器和屏幕
    counter += 1
    pygame.display.update()

# 退出游戏
pygame.quit()
