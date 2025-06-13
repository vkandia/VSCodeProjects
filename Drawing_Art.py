# Import required libraries
import tkinter as tk
from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import ttk

"""
Build the drawing feature

We need to create functions for knowing:
- when the drawing/erasing is starting
- when is actually happening
- when the drawing/erasing is finished

How to keep track of whether the user is drawing or not?
use of a boolean is_drawing
similar for the erasing action
"""


def start_drawing(event):
    """
    Start a new drawing when the user presses their left mouse button on the canvas

    event: mouse press event

    """
    # we need to modify variables defined out of the scope of the function
    global is_drawing, prev_x, prev_y, is_erasing
    is_drawing = True  # the drawing has started
    is_erasing = False
    # even.x, event.y current mouse coordinates
    prev_x, prev_y = event.x, event.y


def draw_or_erase(event):
    """
    This is the function that will be repeatedly called when the user moves the mouse
    in order to draw a continuous line, or to erase a drawing or part of it

    """
    global is_drawing, prev_x, prev_y, is_erasing
    if is_drawing:
        x, y = event.x, event.y
        canvas.create_line(prev_x, prev_y, x, y,
                           fill=drawing_color,
                           width=line_width,
                           capstyle='round',
                           smooth=True)
        prev_x, prev_y = x, y  # update the start coordinates of the next line segment
    elif is_erasing:
        x, y = event.x, event.y
        items = canvas.find_overlapping(x - line_width / 2, y - line_width / 2, x + line_width / 2, y + line_width / 2)
        for item in items:
            canvas.delete(item)


def stop_drawing(event):
    """
    This function helps us detect when the user stops drawing when release the mouse button
    event: mouse release event

    """
    global is_drawing, is_erasing
    is_drawing = False  # current drawing stopped but the user can still move the mouse around without drawing anything
    is_erasing = True


# Erase action definition
def start_erasing(event):
    """
    Start to erase a drawing when the user double-click their left mouse button on the canvas

    event: mouse press event

    """
    # we need to modify variables defined out of the scope of the function
    global is_erasing, prev_x, prev_y, is_drawing
    is_erasing = True  # the erasing act has started
    is_drawing = False
    # even.x, event.y current mouse coordinates
    prev_x, prev_y = event.x, event.y


def stop_erasing(event):
    """
    This function helps us detect when the user stops erasing when release the mouse button
    event: mouse release event

    """
    global is_drawing, is_erasing
    is_drawing = True  # current erasing action stopped but the user can still move the mouse around without drawing/erasing anything
    is_erasing = False


"""
Choose the drawing colour and the line width
"""


def choose_line_color():
    """
    this function brings up the colour chooser and let the user choose the line colour
    in hex code format

    """
    global drawing_color  # defined outside of this function with a default value
    color = askcolor(color=drawing_color)[1]  # [0] of the tuple the RGB code, [1] the hex code of the chosen colour
    if color:  # check that the user has actually chosen something (pressed 'Ok' instead of 'Cancel')
        drawing_color = color


def choose_line_width(value):
    """
    this function updates the line_width variable

    """
    global line_width
    line_width = int(value)

# Creating the main window
root = Tk()
root.title("Drawing Canvas")
root.geometry('800x400')
root.configure(bg='IndianRed')

# Create a canvas and set its background color that expands with the main window 'root'
canvas = tk.Canvas(root, bg='white')
canvas.pack(fill="both", expand=True, padx=10, pady=10)

# Defining some variables
is_drawing = False
is_erasing = False
drawing_color = "black"
line_width = 2
prev_x, prev_y = 0, 0

# Add a frame to put the buttons on (widgets)
controls_frame = tk.Frame(canvas, width=800, height=50, bg='RosyBrown')
controls_frame.pack(side='bottom', fill="x", padx=5, pady=5)

#Style
# Create a style
style = ttk.Style(controls_frame)

# Set the theme with the theme_use method
style.theme_use('default')  # put the theme name here, that you want to use

# Add button for choosing the colour
color_button = ttk.Button(controls_frame, text="Change Color", command=choose_line_color)
color_button.pack(side="left", padx=10, pady=5)

# Add a button for clearing the entire canvas
clear_button = ttk.Button(controls_frame, text="Clear Canvas", command=lambda: canvas.delete("all"))
clear_button.pack(side="left", padx=10, pady=5)

# Add a button for erase a part of the drawing
erase_button = ttk.Button(controls_frame, text="Eraser", command=lambda: start_erasing)
erase_button.pack(side="left", padx=10, pady=5)

#  Add a slider in order to choose the width of the user's line
line_width_label = ttk.Label(controls_frame, text="Line Width:")
line_width_label.pack(side="left", padx=5, pady=5)

# Add an integer var to connect the slider with a label
scale_int = tk.IntVar(value=line_width)

line_width_slider = ttk.Scale(controls_frame, from_=1, to=10, orient="horizontal",
                              command=lambda value:choose_line_width(scale_int.get()),
                              variable=scale_int)

line_width_slider.pack(side="left", padx=5, pady=5)

# Add a label for the value of the line width
line_value_label = ttk.Label(controls_frame, textvariable=scale_int)
line_value_label.pack(side="left", padx=5, pady=5)


"""
line_width_labelled_scale = ttk.LabeledScale(controls_frame, from_=1, to=10, variable=scale_int)
line_width_labelled_scale.pack(side="left", padx=5, pady=5)
"""

# Link the buttons with actions

canvas.bind("<Button-1>", start_drawing) # single left click on mouse
canvas.bind("<Double-1>", start_erasing) # double left click on mouse
canvas.bind("<B1-Motion>", draw_or_erase) # hold down the left mouse button and grad the mouse on the canvas

canvas.bind("<ButtonRelease-1>", stop_drawing)
canvas.bind("<ButtonRelease-1>", stop_erasing)

# Run the program
root.mainloop()
