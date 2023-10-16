import tkinter as tk
from tkinter import Canvas, Button, PhotoImage, Label, OptionMenu, StringVar
from PIL import Image, ImageTk

from classifier import get_preds

class HandwritingRecognitionApp:
    def __init__(self, root):
        self.root = root
        root.title("Handwriting Recognition App")
        self.frame = tk.Frame(root, height=1050, width=1050)
        self.frame.pack(side="top", fill="both", expand=True)

        self.last_x, self.last_y = None, None
        self.drawing = False
        self.draw_color = "white"
        self.draw_thickness = StringVar(root, 20)

        # canvas size (internally 28x28, displayed 280x280)
        self.canvas_width = 280
        self.canvas_height = 280

        self.text1 = Label(root, text="Draw here:").place(x=50, y=30)
        self.text2 = Label(root, text="Thats the version that will be compressed:").place(x=400, y=30)
        self.text3 = Label(root, text="Image fed into the neural net (rescaled):").place(x=750, y=30)

        # create a canvas for drawing
        self.canvas = Canvas(root, width=self.canvas_width, height=self.canvas_height, bg='black')
        self.canvas.place(x=50, y=50)

        # editing descriptions
        self.text1 = Label(root, text="Thickness:").place(x=50, y=380)
        self.text2 = Label(root, text="Drawing Colors and Clear:").place(x=150, y=380)

        # editing options
        self.thickness_dropdown = OptionMenu(root, self.draw_thickness, *list(range(1, 41))).place(x=50, y=405) # dropdowns origin is a bit more at the top
        self.color_black_button = Button(root, text="Black", command=self.activate_black).place(x=150, y=400)
        self.color_white_button = Button(root, text="White", command=self.activate_white).place(x=250, y=400)
        self.clear_button = Button(root, text="Clear", command=self.clear_canvas).place(x=200, y=450)

        # image representation from draw canvas
        self.image = PhotoImage(width=self.canvas_width, height=self.canvas_width)
        self.image.put("black", to=(0, 0, self.canvas_width, self.canvas_height))
        self.image_label = Label(root, image=self.image).place(x=400, y=50)

        # image representatio that is fed into neural net
        self.create_resized_image()

        # predictions
        self.pred_headline = Label(root, text="These are the sorted predictions:").place(x=760, y=380)
        self.pred_string = StringVar()
        self.pred_string.set("Here will be the preds.")
        self.pred_text = Label(root, textvariable=self.pred_string).place(x=760, y=400)

        self.fe_description = Label(root, anchor='w', justify='left', text=
            """
            Desciption:
            In this application you can write a number on the canvas at the top left.
            When writing, the image you write is redrawn (image in the middle), 
            compressed and then fed into a neural network.
            This neural network is trained with the MNIST handwritten numbers dataset 
            and predicts the number which is written on the canvas.
            At the top right the image fed into the neural network is shown in higher resolution (original: 28x28).
            The probablities for every number are displayed at the bottom right.
            You can use the drawing options above this text.
            Dont write too fast because making a copy of the drawn image creates a small delay!
            """).place(x=10, y=500)
        
        # bind mouse events to canvas
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)

    # initiates drawing process
    def start_drawing(self, event):
        self.drawing = True
        self.last_x, self.last_y = event.x, event.y
        self.draw(event)

    # redraws the drawn image as a PhotoImage, uses rectangle of "width" to redraw
    def redraw_image(self, x, y):
        half_width = int(self.draw_thickness.get()) // 2
        for i in range(x - half_width, x + half_width + 1):
            i = 0 if i < 0 else i # ensure no values below 0
            i = 280 if i > 280 else i # ensure no values above 280
            for j in range(y - half_width, y + half_width + 1):
                j = 0 if j < 0 else j
                j = 280 if j > 280 else j
                self.image.put(self.draw_color, to=(i, j))

    # main drawing function, triggers other actions (redrawing image, saving it, show it, analyse it)
    def draw(self, event):
        if self.drawing:
            x, y = event.x, event.y
            x = 0 if x < 0 else x # ensure no values below 0
            y = 0 if y < 0 else y
            x = 285 if x > 285 else x # ensure no values above 285 (usually 280 but then border lines are not equal for x and y)
            y = 285 if y > 285 else y
            self.canvas.create_line((self.last_x, self.last_y, x, y), width=int(self.draw_thickness.get()), fill=self.draw_color, capstyle=tk.ROUND, smooth=tk.TRUE)
            self.redraw_image(x, y)
            self.last_x, self.last_y = x, y # set the current draw point as the last draw point, no delay
            self.save_image()
            self.update_nn_image()
            self.display_preds()
    
    # change color so 
    def activate_black(self):
        self.draw_color = "black"

    def activate_white(self):
        self.draw_color = "white"

    # saves redrawn image as png
    def save_image(self):
        pil_image = ImageTk.getimage(photo=self.image)
        output_image = pil_image.resize((28, 28), resample=Image.NEAREST)
        output_image.save("image.png")
    
    # updates image that is fed into neural net
    def update_nn_image(self):
        self.nn_image_rescale = Image.open("image.png")
        self.nn_image_rescale = self.nn_image_rescale.resize((280, 280))
        self.nn_image_rescale = ImageTk.PhotoImage(self.nn_image_rescale)
        self.rescaled_image.config(image=self.nn_image_rescale)

    # gets preds from neural net and displays them
    def display_preds(self):
        order, preds = get_preds()
        displayed_preds = ""

        for element in range(len(order)):
            string_line = f"{order[element]}: {preds[order[element]]:.6f}\n"
            displayed_preds = displayed_preds + string_line

        self.pred_string.set(displayed_preds)

    # clears everything
    def clear_canvas(self):
        self.canvas.delete("all")
        self.recognized_digit = None
        for x in range(self.canvas_height):
            for y in range(self.canvas_width):
                self.image.put("black", to=(x, y))
        self.create_resized_image()
        self.pred_string.set("Draw a new number to get predictions!")

    # resized image from neural is often recreated in code, making it a function suggests itself
    def create_resized_image(self):
        self.nn_image_rescale = PhotoImage(width=self.canvas_width, height=self.canvas_height)
        self.nn_image_rescale.put("black", to=(0, 0, self.canvas_width, self.canvas_height))
        self.rescaled_image = Label(root, image=self.nn_image_rescale)
        self.rescaled_image.place(x=750, y=50)

if __name__ == "__main__":
    root = tk.Tk()
    app = HandwritingRecognitionApp(root)
    root.mainloop()