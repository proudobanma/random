from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
window.fullscreen = True
window.exit_button.visible = False
window.color = color.black50

ground = Entity(
    model='plane',
    texture='white_cube',
    color=color.brown,
    collider='mesh',
    scale=(8, 1, 3)
)

player = FirstPersonController(
    collider='box', jump_duration=0.35)
player.cursor.visible = False

# Calculate the highest point based on player's starting position and ground scale
highest_point = player.y + ground.scale.y / 2

roof = Entity(
    model='plane',
    texture='white_cube',
    color=color.brown,
    collider='mesh',
    scale=(8, 1, 3),  # Adjusted scale to fit the scene better
    y=highest_point + 5  # Adjusted position to be above the highest point
)

pill1 = Entity(
    model='cube',
    color=color.magenta,
    scale=(0.4, 0.1, 53),
    z=28, x=-0.7
)
pill2 = duplicate(pill1,
                  x=-3.7)
pill3 = duplicate(pill1,
                  x=0.6)
pill4 = duplicate(pill1,
                  x=3.6)

from random import randint

blocks = []
for i in range(12):
    block = Entity(
        model='cube', collider='box',
        color=color.white33,
        position=(2, 0.1, 3 + i * 4),
        scale=(3, 0.1, 2.5)
    )
    block2 = duplicate(block,
                       x=-2.2)
    blocks.append(
        (block, block2, randint(0, 10) > 7,
         randint(0, 10) > 7)
    )

goal = Entity(
    color=color.dark_gray,
    model='cube',
    collider='box',
    z=55,
    scale=(10, 1, 10),
)

pillar = Entity(
    color=color.azure,
    model='cube',
    z=58,
    scale=(1, 15, 1), y=8
)

fallen = False
fall_timer = 0

def update():
    global fallen, fall_timer

    if not fallen and player.y < -5:  # Check if player falls
        fallen = True

    if fallen:
        fall_timer += time.dt  # Add time since last frame to the fall_timer

        if fall_timer >= 7:  # If 7 seconds passed since fall
            application.quit()  # Quit the application
    if fallen and fall_timer >= 5:  # If 5 seconds passed since fall
        display_you_died_text()  # Display "You Died" text

    for block1, block2, k, n in blocks:
        for x, y in [(block1, k),
                     (block2, n)]:
            if x.intersects() and y:
                invoke(destroy, x,
                       delay=0.5)
                x.fade_out(duration=0.5)
                fallen = True  # Set fallen to True when player intersects with block
                break

def display_you_died_text():
    you_died_text = Text('You Died', origin=(0, 0), scale=3, color=color.white)
    you_died_text.scale *= 3
    you_died_text.x = -you_died_text.width / 2  # Center the text horizontally
    you_died_text.y = -you_died_text.height / 2  # Center the text vertically
    invoke(destroy, you_died_text, delay=3)  # Remove the "You Died" text after 3 seconds

def input(key):
    if key == 'escape':
        quit()

app.run()
