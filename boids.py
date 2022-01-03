
import pyglet
import random
import statistics as stat
import numpy as np

#class boid:
#    def __init__(self,idx,x,y):
#        self.idx = idx
#        self.x = x
#        self.y = y

#calculating boids
def init_positions(num_of_boids,max_width,max_height,min_vel,max_vel):
    boids = []
    for i in range(num_of_boids):
        boids.append([random.randint(1,max_width), random.randint(1,max_height),
            random.randint(min_vel,max_vel), random.randint(min_vel,max_vel)])
    boids = np.array(boids)
    return boids


def rule1(boids,num_of_boids,pos_coff=100):
    #rule1
    #the below can be imporved by minusing the current location from the center of mass calc
    v1 = []
    for b in boids:
        com = np.array([0,0])
        for other in boids:
            if b[0] != other[0] and b[1] != other[1]:
                com = com + b[0:1]
        com = com / (num_of_boids-1)
        com = com - b[0:1]
        v1.append(com)
    return np.array(v1)

def rule2(boids,num_of_boids,repulce_limit):
    v2 = [[0,0]]*num_of_boids  
    for i,b in enumerate(boids):
        for other in boids:
            if b[0] != other[0] and b[1] != other[1]:
                if abs(b[0:1] - other[0:1]) < repulce_limit:
                    v2[i][:] = v2[i][:] - (b[0:1] - other[0:1])
    return np.array(v2)

def rule3(boids,vel_coff=8):
    v3 = []
    for b in boids:
        cov = np.array([0,0])
        for other in boids:
            if b[2] != other[2] and b[3] != other[3]:
                cov = cov + b[2:3]
        cov = cov / (num_of_boids-1)
        cov = cov - b[2:3]
        v3.append(cov)
    return np.array(v3)

def calc_new_positions(boids):
    v1 = rule1(boids,30,pos_coff=50)
    v2 = rule2(boids,30,1)
    v3 = rule3(boids,vel_coff=8)

    #update vel
    boids[:,2:] = boids[:,2:] + v1 + v2 + v3
    #boids[:][3] = boids[:][3] + v1 + v2 + v3

    #update pos
    boids[:,0:2] = boids[:,0:2] + boids[:,2:]
    #boids[:][1] = boids[:][1] + boids[:][3]

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
num_of_boids = 30
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

def update(dt,boids):
    calc_new_positions(boids)
    for i,b in enumerate(boids):
        sprites[i].x = b[0]
        sprites[i].y = b[1]

pyglet.clock.schedule_interval(update, 1/60.,boids=boids)

pyglet.app.run()