import cairo
import math

# Set up surface
surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 1050, 1200)
context = cairo.Context(surface)
context.set_source_rgb(1,1,1)
context.paint()

#House Shape
context.move_to(100, 500)
context.line_to(950,500)
context.line_to(950,600)
context.line_to(850,600)
context.line_to(850,1050)
context.line_to(200,1050)
context.line_to(200,600)
context.line_to(100,600)
context.line_to(100,500)
context.set_line_width(3)
context.set_source_rgb(0,0,1)
context.stroke()

#Door
context.move_to(450,1050)
context.line_to(450,700)
context.line_to(600,700)
context.line_to(600,1050)
context.close_path()
context.set_source_rgb(0.4, 0.8, 0)
context.set_line_width(5)
context.stroke()

#Window 1
context.move_to(250,700)
context.line_to(400,700)
context.line_to(400,850)
context.line_to(250,850)
context.close_path()
context.set_line_width(5)
context.set_source_rgb(0.4, 0.8, 0)
context.stroke()
context.move_to(325,700)
context.line_to(325,850)
context.move_to(250,775)
context.line_to(400,775)
context.set_line_width(3)
context.set_source_rgb(0,0,1)
context.stroke()

#Window 2
context.move_to(650,700)
context.line_to(800,700)
context.line_to(800,850)
context.line_to(650,850)
context.close_path()
context.set_line_width(5)
context.set_source_rgb(0.4, 0.8, 0)
context.stroke()
context.move_to(725,700)
context.line_to(725,850)
context.move_to(650,775)
context.line_to(800,775)
context.set_line_width(3)
context.set_source_rgb(0,0,1)
context.stroke()

#Doorknob
# Small circle
context.arc(575, 850, 12.5, 0, 2*math.pi)
context.set_source_rgb(0,0.5,1)
context.fill_preserve()
context.set_line_width(5)
context.set_source_rgb(0,0,0.8)
context.stroke()

#Semicircle
context.arc(525, 500,250, math.pi, 0)
context.set_source_rgb(0,0,0)
context.set_line_width(3)
context.set_source_rgb(0,0,1)
context.stroke()

# Crescent
context.arc(900, 150, 80, 0, 2*math.pi)
r2 = cairo.LinearGradient(900, 150, 1050, 400)
r2.add_color_stop_rgb(0, 1, 1, 0)
r2.add_color_stop_rgb(0.8, 0, 0, 0)
context.set_source(r2)
context.fill()

context.set_source_rgb(1,1,1)
context.arc(1000,50, 170, 0, 2*math.pi)
context.fill()

surface.write_to_png("House.png")