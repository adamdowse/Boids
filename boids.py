
import pyglet


window = pyglet.window.Window()

#Draw some text in the center of the screen
label = pyglet.text.Label('Hello World',
    font_name='Times New Roman',
    font_size=36,
    x=window.width//2, y=window.height//2,
    anchor_x='center', anchor_y='center')

@window.event
def on_draw():
    window.clear()
    label.draw()



pyglet.app.run()