from PIL import Image
import tkinter as tk
import json
import sys

class Crosshair:

    def __init__(self, crosshair_color="(0, 0, 255, 255)", settings=(2, 8, 4)):
        self.crosshair_color = eval(crosshair_color)
        self.filename = "crosshair.png"
        self.transparent_color = (255, 255, 255, 0)
        self.line_width = settings[0]
        self.line_length = settings[1]
        self.line_offset = settings[2]

        self.width = (self.line_length * 2) + self.line_width + (self.line_offset * 2)
        self.matrix = []

    def create_crosshair_matrix(self):
        for y in range(self.width):
            row = []
            for x in range(self.width):
                append_flag = False
                if x >= (self.width / 2) - (self.line_width / 2) and x < self.line_length + self.line_offset + self.line_width:
                    if y < self.line_length:
                        row.append(self.crosshair_color)
                        append_flag = True
                    elif y >= self.line_length + (self.line_offset * 2) + self.line_width:
                        row.append(self.crosshair_color)
                        append_flag = True

                if y >= (self.width / 2) - (self.line_width / 2) and y < self.line_length + self.line_offset + self.line_width:
                    if x < self.line_length:
                        row.append(self.crosshair_color)
                        append_flag = True
                    elif x >= self.line_length + (self.line_offset * 2) + self.line_width:
                        row.append(self.crosshair_color)
                        append_flag = True

                if not append_flag:
                    row.append(self.transparent_color)
            self.matrix.append(row)

    def save_crosshair_png(self):
        im = Image.new("RGBA", (self.width, self.width))
        for y in range(self.width):
            for x in range(self.width):
                im.putpixel((x, y), self.matrix[x][y])
        im.save(self.filename)

    def print_crosshair(self):
        for y in range(self.width):
            for x in range(self.width):
                if self.matrix[y][x] == self.crosshair_color:
                    sys.stdout.write("1")
                else:
                    sys.stdout.write("0")
            sys.stdout.write("\n")

    def display_crosshair(self):

        def center(toplevel):
            toplevel.update_idletasks()
            w = toplevel.winfo_screenwidth()
            h = toplevel.winfo_screenheight()
            x = int(w / 2 - self.width / 2)
            y = int(h / 2 - self.width / 2)
            toplevel.geometry("{}x{}+{}+{}".format(self.width, self.width, x, y))

        root = tk.Tk()
        w = tk.Toplevel(root)
        w.title("Crosshair")
        w.geometry("250x80")
        button = tk.Button(w, text="Quit", command=root.destroy, height = 80, width = 250)
        button.pack()

        center(root)
        root.image = tk.PhotoImage(file=self.filename)
        label = tk.Label(root, image=root.image, bg='white')
        root.overrideredirect(True)
        root.geometry("{}x{}".format(self.width, self.width))
        root.lift()
        root.wm_attributes("-topmost", True)
        root.wm_attributes("-disabled", True)
        root.wm_attributes("-transparentcolor", "white")
        label.pack()
        w.grab_set()
        label.configure(state="disable")
        label.mainloop()

def main():
    with open("config.json", "r") as f:
        config = json.loads(f.read())

    try:
        c = Crosshair(config["crosshair_color"], (config["line_width"], config["line_length"], config["line_offset"]))
    except Exception as e:
        print("Missing {}. Using default settings.".format(e))
        c = Crosshair()

    c.create_crosshair_matrix()
    c.save_crosshair_png()
    c.display_crosshair()

if __name__ == "__main__":
    main()
