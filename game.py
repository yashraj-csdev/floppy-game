from js import document, Image, requestAnimationFrame
import random
import math

canvas = document.getElementById("gameCanvas")
ctx = canvas.getContext("2d")

WIDTH = 400
HEIGHT = 600

# ---------- GAME STATE ----------
game_started = False

# ---------- BIRD ----------
bird_x = 100
bird_y = 300
velocity = 0
gravity = 0.4
jump_strength = -7

bird_img = None

# ---------- PIPE ----------
pipe_x = WIDTH
pipe_width = 60
pipe_speed = 2
pipe_height = random.randint(150, 300)
pipe_gap = random.randint(140, 200)

pipe_img = None

def reset_pipe():
    global pipe_x, pipe_height, pipe_gap
    pipe_x = WIDTH
    pipe_height = random.randint(150, 300)
    pipe_gap = random.randint(140, 200)

# ---------- LOAD USER IMAGES ----------
def load_image(input_id):
    file = document.getElementById(input_id).files.item(0)
    if not file:
        return None
    img = Image.new()
    img.src = document.URL.createObjectURL(file)
    return img

bird_img = load_image("birdInput")
pipe_img = load_image("pipeInput")

# ---------- INPUT ----------
def jump(event=None):
    global velocity, game_started
    game_started = True
    velocity = jump_strength

canvas.addEventListener("click", jump)
document.addEventListener("keydown", lambda e: jump() if e.key == " " else None)

# ---------- GAME LOOP ----------
def game_loop(ts):
    global bird_y, velocity, pipe_x

    ctx.clearRect(0, 0, WIDTH, HEIGHT)

    if game_started:
        velocity += gravity
        bird_y += velocity
        pipe_x -= pipe_speed

        if pipe_x < -pipe_width:
            reset_pipe()

    # ---------- DRAW BIRD ----------
    if bird_img:
        ctx.drawImage(bird_img, bird_x - 18, bird_y - 18, 36, 36)
    else:
        ctx.beginPath()
        ctx.arc(bird_x, bird_y, 15, 0, math.pi * 2)
        ctx.fillStyle = "yellow"
        ctx.fill()

    # ---------- DRAW PIPES ----------
    if pipe_img:
        ctx.drawImage(pipe_img, pipe_x, pipe_height - 400, 60, 400)
        ctx.drawImage(pipe_img, pipe_x, pipe_height + pipe_gap, 60, 400)
    else:
        ctx.fillStyle = "green"
        ctx.fillRect(pipe_x, 0, 60, pipe_height)
        ctx.fillRect(pipe_x, pipe_height + pipe_gap, 60, HEIGHT)

    if not game_started:
        ctx.fillStyle = "black"
        ctx.font = "20px Arial"
        ctx.fillText("Tap to Start", 140, HEIGHT // 2)

    requestAnimationFrame(game_loop)

requestAnimationFrame(game_loop)
