
from customtkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageGrab
import CTkColorPicker

mouse_in_canvas = False

size = 50
sizePos = size // 2
brush = 'Circle'
color = 'black'
canvas_width = 1000
canvas_height = 600

window = CTk()



window.geometry("1300x750")
window.title("Paintoo")
set_appearance_mode("dark")
set_default_color_theme("green")
def color_popup():
    global color
    
    colorA = CTkColorPicker.AskColor()
    
    color = colorA.get()


canvas = CTkCanvas(window, width=canvas_width, height=canvas_height, bg='white', highlightthickness=0)
canvas.place(x=150, y=80)

def clear():
    canvas.delete('all')

def change_brush(choice):
    global brush
    brush = choice

def save_contents():
    filename_A = filedialog.asksaveasfilename()
    
    canvas.update_idletasks()
    x = window.winfo_rootx() + canvas.winfo_x()
    y = window.winfo_rooty() + canvas.winfo_y()
    x1 = x + canvas.winfo_width()
    y1 = y + canvas.winfo_height()
    ImageGrab.grab(bbox=(x, y, x1, y1)).save(f'{filename_A}.png')

def eraser():
    global color
    color = 'white'
 
def import_file():
    image_path = filedialog.askopenfilename(title='Open a file')
    if image_path:
        pil_image = Image.open(image_path)
        resized_image = pil_image.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)
        tk_image = ImageTk.PhotoImage(resized_image)
        canvas.image = tk_image
        canvas.create_image(0, 0, image=tk_image, anchor="nw")
        


save_as_button = CTkButton(window, text='Save as (.png)', command=save_contents)
save_as_button.place(x=0, y=20)
import_file_btn = CTkButton(window, text='Import Image', command=import_file)
import_file_btn.place(x=0,y=100)
color_pick_button = CTkButton(window, text='Color select', command=color_popup)
color_pick_button.place(x=500, y=20)

eraser_button = CTkButton(window, text='Erase', command=eraser)
eraser_button.place(x=800, y=20)

brushes = ['Circle', 'Square', 'Triangle', 'Text']
brush_selector = CTkComboBox(window, values=brushes, command=change_brush)
brush_selector.set('Circle')
brush_selector.place(x=1000, y=20)

sizeLABEL = CTkLabel(window, text=f"Size: {size}")
sizeLABEL.place(x=750, y=20)

clear_button = CTkButton(window, text='Clear', command=clear)
clear_button.place(x=880, y=700)

def changeSize(event):
    global size, sizePos
    if event.delta > 0: size += 5
    else: size -= 5
    size = max(5, size)
    sizePos = size // 2
    sizeLABEL.configure(text=f"Size: {size}")

def mouse_leave_canvas(event):
    global mouse_in_canvas
    mouse_in_canvas = False
    
def mouse_enter_canvas(event):
    global mouse_in_canvas
    mouse_in_canvas = True
    
canvas.bind("<Enter>",mouse_enter_canvas)
canvas.bind("<Leave>",mouse_leave_canvas)     
def draw(event):
    
    if mouse_in_canvas:
        if brush == 'Circle':
            canvas.create_oval(event.x-sizePos, event.y-sizePos, event.x+sizePos, event.y+sizePos, fill=color, outline=color)
        elif brush == 'Square':
            canvas.create_rectangle(event.x-sizePos, event.y-sizePos, event.x+sizePos, event.y+sizePos, fill=color, outline=color)
        elif brush == 'Triangle':
            points = [event.x, event.y-sizePos, event.x+sizePos, event.y+sizePos, event.x-sizePos, event.y+sizePos]
            canvas.create_polygon(points, fill=color, outline=color)
        elif brush == 'Text':
            dialog = CTkInputDialog(text="Type in a string (text):", title="Input Dialog")
        
        
            user_text = dialog.get_input()
            if user_text:
                canvas.create_text(event.x, event.y, text=user_text, fill=color, font=("Arial", size), anchor="nw")



window.bind('<B1-Motion>', draw)
window.bind('<Button-1>', draw)

window.bind('<MouseWheel>', changeSize)

window.mainloop()