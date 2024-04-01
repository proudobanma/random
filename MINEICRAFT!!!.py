from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from tkinter import filedialog

app = Ursina()

window.frame_rate = 60
window.fullscreen = True
Sky()

# Adjust the player speed
player = FirstPersonController(speed=5)

arm = Entity(
    parent=camera.ui,
    model='cube',
    color=color.blue,
    position=(0.75, -0.6),
    rotation=(150, -10, 6),
    scale=(0.2, 0.2, 1.5)
)

shift_pressed = False

# Set the reach distance
reach_distance = 10

def update():
    global shift_pressed
    
    if held_keys['left mouse']:
        arm.position = (0.6, -0.5)
    elif held_keys['right mouse']:
        arm.position = (0.6, -0.5)
    else:
        arm.position = (0.75, -0.6)
        
    if held_keys['shift']:
        if not shift_pressed:
            shift_pressed = True
            # Reduce player speed when shift is pressed
            player.speed = 2  # Adjust the player's speed
            # Adjust player position downwards
            player.y -= 0.5
    else:
        if shift_pressed:
            shift_pressed = False
            # Restore player speed when shift is released
            player.speed = 5
            # Move player position back up
            player.y += 0.5 * (1 if held_keys['space'] else 0)

    # Set the reach distance for placing boxes
    hit_info = raycast(camera.position, camera.forward, distance=reach_distance)
    if hit_info.hit:
        print('Hit:', hit_info.entity)


boxes = []

for n in range(50):
    for k in range(50):
        box = Button(
            position=(k, 0, n),
            color=color.green,
            highlight_color=color.lime,
            model='cube',
            texture='white_cube',
            parent=scene
        )
        boxes.append(box)

def save_scene():
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if filename:
        with open(filename, 'w') as f:
            for box in boxes:
                f.write(f"{box.position} {box.color}\n")
        print("Scene saved successfully.")

def open_scene():
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if filename:
        with open(filename, 'r') as f:
            for line in f:
                position_str, color_str = line.split()
                position = eval(position_str)
                color = eval(color_str)
                box = Button(
                    position=position,
                    color=color,
                    highlight_color=color.lime,
                    model='cube',
                    texture='white_cube',
                    parent=scene
                )
                boxes.append(box)
        print("Scene opened successfully.")

def input(key):

    if held_keys['control']:
        if key == 's':
            save_scene()
        elif key == 'o':
            open_scene()
    elif  key == 'escape':
        quit() 
    for box in boxes:
        if box.hovered:
            if key == 'right mouse down':
                new_box = Button(
                    position=box.position + mouse.normal,
                    color=color.orange,
                    highlight_color=color.turquoise,
                    model='cube',
                    texture='white_cube',
                    origin_y=-0.01,
                    parent=scene
                )
                boxes.append(new_box)
            if key == 'left mouse down':
                boxes.remove(box)
                destroy(box)
            if key == '2':
                box.color = color.orange
            if key == '3': 
                box.color = color.yellow
            if key == '4': 
                box.color = color.green
            if key == '5': 
                box.color = color.azure
            if key == '6': 
                box.color = color.violet
            if key == '7': 
                box.color = color.light_gray
            if key == '8': 
                box.color = color.dark_gray
            if key == '9': 
                box.color = color.black
            if key == '1': 
                box.color = color.red
            if key == '0': 
                box.color = color.white

app.title = 'pixel block 3D'

app.run()
