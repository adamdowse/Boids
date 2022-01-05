
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

def rule1(boids,pos_coff,perception_limit):
    #rule1
    #the below can be imporved by minusing the current location from the center of mass calc
    v1 = []
    for b in boids:
        com = np.array([0,0])
        i = 0
        for other in boids:
            if b[0] != other[0] and b[1] != other[1]:
                if np.linalg.norm(b[0:2] - other[0:2]) < perception_limit: 
                    i += 1 
                    com = com + other[0:2] 
        if i > 0:
            com = com / i
            com = (com - b[0:2]) / pos_coff 
        v1.append(com)
    return np.array(v1)

def rule2(boids,num_of_boids,repulce_limit):  
    v2 = np.zeros((num_of_boids,2))
    for i,b in enumerate(boids):
        j = 0
        for other in boids:
            if b[0] != other[0] and b[1] != other[1]:
                if np.linalg.norm(b[0:2] - other[0:2]) < repulce_limit:
                    v2[i,:] = v2[i,:] + (b[0:2] - other[0:2]) / np.linalg.norm(b[0:2] - other[0:2])
                    j+= 1
        if j > 0:
            v2[i,:] /= j
    return v2

def rule2_5(boids,num_of_boids,window,repulce_factor):
    v = np.zeros((num_of_boids,2))
    for i,b in enumerate(boids):
        if b[0] > window.width:
            v[i,0] = - repulce_factor
        elif b[0] < 0:
            v[i,0] =  repulce_factor
        
        if b[1] > window.height:
            v[i,1] = -repulce_factor
        elif b[1] < 0:
            v[i,1] = repulce_factor
    return v

def rule3(boids,vel_coff,perception_limit):
    v3 = []
    for b in boids:
        cov = np.array([0,0])
        i = 0
        for other in boids:
            if b[2] != other[2] and b[3] != other[3]:
                if np.linalg.norm(b[0:2] - other[0:2]) < perception_limit:
                    i += 1
                    cov = cov + other[2:4]
        if i > 0:
            cov = cov / i
            cov = (cov - b[2:4]) / vel_coff
        v3.append(cov)
    return np.array(v3)

perception_limit = 300

def calc_new_positions(boids,num_of_boids,window):
    pos_coff = 80
    vel_coff = 0.5
    global perception_limit
    repulce_limit = 30
    repulce_factor = 10
    vel_limit = 10

    v1 = rule1(boids,pos_coff=pos_coff,perception_limit=perception_limit)
    v2 = rule2(boids,num_of_boids,repulce_limit=repulce_limit)
    v2_5 = rule2_5(boids,num_of_boids,window,repulce_factor)
    v3 = rule3(boids,vel_coff=vel_coff,perception_limit=perception_limit)

    #update vel
    boids[:,2:] = boids[:,2:] + v1 + v2 + v3 #+ v2_5

    #limit vel Unsure if this works
    
    for b in boids:
        if np.linalg.norm(b[2:4]) > vel_limit:
            b[2:4] = b[2:4] / np.linalg.norm(b[2:4]) * vel_limit
        
    #update pos
    boids[:,0:2] = boids[:,0:2] + boids[:,2:]

    #loop the screen
    for b in boids:
        if b[0] > window.width:
            b[0] = 0
        elif b[0] < 0:
            b[0] = window.width

        if b[1] > window.height:
            b[1] = 0
        elif b[1] < 0:
            b[1] = window.height

    return boids


window = pyglet.window.Window(fullscreen=True)

batch = pyglet.graphics.Batch()
batch2 = pyglet.graphics.Batch()

sprites = []
circles = []
num_of_boids = 50
boids = init_positions(num_of_boids,window.width,window.height,-10,10)
for i in range(num_of_boids):
    circle = pyglet.shapes.Circle(boids[i][0],boids[i][1],perception_limit,batch=batch2)
    circles.append(circle)
    # temporary sprite object
    temp = pyglet.shapes.Circle(boids[i][0], boids[i][1], 5, color= (255,0,0),batch = batch)
     
    # append the sprite object to the list
    sprites.append(temp)

@window.event
def on_draw():
    window.clear()

    #batch2.draw()
    batch.draw()

def update(dt,boids,num_of_boids,window):
    calc_new_positions(boids,num_of_boids,window)
    for i,b in enumerate(boids):
        sprites[i].x = b[0]
        sprites[i].y = b[1]
        circles[i].x = b[0]
        circles[i].y = b[1]

pyglet.clock.schedule_interval(update, 1/60.,boids=boids,num_of_boids=num_of_boids,window=window)

pyglet.app.run()