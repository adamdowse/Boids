
import pyglet
import random
import statistics as stat
import numpy as np


#calculating boids
def init_positions(num_of_boids,max_width,max_height,min_vel,max_vel):
    boids = []
    for i in range(num_of_boids):
        boids.append([random.randint(1,max_width), random.randint(1,max_height),
            random.randint(min_vel,max_vel), random.randint(min_vel,max_vel)])
    boids = np.array(boids)
    return boids


def rule1(boids,num_of_boids,pos_coff=100,perception_limit=100):
    #rule1
    #the below can be imporved by minusing the current location from the center of mass calc
    v1 = []
    for b in boids:
        com = np.array([0,0])
        i = 1
        for other in boids:
            if b[0] != other[0] and b[1] != other[1]:
                if np.linalg.norm(b[0:2] - other[0:2]) < perception_limit: 
                    i += 1 
                    com = com + other[0:2] 
        com = com / i
        com = (com - b[0:2]) / pos_coff 
        v1.append(com)
    return np.array(v1)

def rule2(boids,num_of_boids,repulce_limit=100):  
    v2 = np.zeros((num_of_boids,2))
    for i,b in enumerate(boids):
        for other in boids:
            if b[0] != other[0] and b[1] != other[1]:
                if abs(b[0] - other[0]) < repulce_limit and abs(b[1] - other[1]) < repulce_limit:
                    v2[i,:] = v2[i,:] - (b[0:2] - other[0:2])
    return v2

def rule2_5(boids,num_of_boids,window,repulce_limit):
    v2_5 = np.zeros((num_of_boids,2))
    for i,b in enumerate(boids):
        if b[0] > window.width - repulce_limit or b[1] < window.height - repulce_limit:
            v2_5[i,0:2] = v2_5[i,0:2] - b[2:4]
        if b[0] < repulce_limit or b[1] < repulce_limit:
            v2_5[i,0:2] = v2_5[i,0:2] + b[2:4]        
    return v2_5

def rule3(boids,vel_coff=8):
    v3 = []
    for b in boids:
        cov = np.array([0,0])
        for other in boids:
            if b[2] != other[2] and b[3] != other[3]:
                cov = cov + other[2:4]
        cov = cov / (num_of_boids-1)
        cov = (cov - b[2:4]) / vel_coff
        v3.append(cov)
    return np.array(v3)

def calc_new_positions(boids,num_of_boids,window):
    v1 = rule1(boids,num_of_boids,pos_coff=100)
    v2 = rule2(boids,num_of_boids,repulce_limit=20)
    #v2_5 = rule2_5(boids,num_of_boids,window,2)
    v3 = rule3(boids,vel_coff=8)

    #update vel
    boids[:,2:] = boids[:,2:] + v1 + v2 + v3 #+ v2_5

    #update pos
    boids[:,0:2] = boids[:,0:2] + boids[:,2:]

    #loop the screen
    for b in boids:
        if b[0] > window.width:
            b[0] = b[0] - window.width
        elif b[0] < 0:
            b[0] = window.width + b[0]

        if b[1] > window.height:
            b[1] = b[1] - window.height
        elif b[1] < 0:
            b[1] = window.height + b[1]

    return boids


window = pyglet.window.Window()




#Draw some text in the center of the screen
label = pyglet.text.Label('Hello World',
    font_name='Times New Roman',
    font_size=36,
    x=window.width//2, y=window.height//2,
    anchor_x='center', anchor_y='center')

batch = pyglet.graphics.Batch()

image = pyglet.image.load('project/pixil-frame-0.png')

sprites = []
num_of_boids = 10
boids = init_positions(num_of_boids,window.width,window.height,1,10)
for i in range(num_of_boids):
    
    # temporary sprite object
    temp = pyglet.sprite.Sprite(image, boids[i][0], boids[i][1], batch = batch)
     
    # append the sprite object to the list
    sprites.append(temp)

@window.event
def on_draw():
    window.clear()
    label.draw()
    batch.draw()

def update(dt,boids,num_of_boids,window):
    calc_new_positions(boids,num_of_boids,window)
    for i,b in enumerate(boids):
        sprites[i].x = b[0]
        sprites[i].y = b[1]

pyglet.clock.schedule_interval(update, 1/30.,boids=boids,num_of_boids=num_of_boids,window=window)

pyglet.app.run()