# color_evolution_v5.py
# Austin Pursley
# 5/6/2017
# An idea I had using the concept of genetic algorithms with user feedback.

# This program is a simple app/toy that allows user to select favorite colors
# from a set. The program will use simple 'genetic' computations to turn the
# selected colors into a set of new colors that might be closer to the users
# favorite color(s). This can continue for however many generations the user
# wants to go through.

import tkinter as tk
import colorgenetics_v2 as cg
import random

class ColorEvolution(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.canvas = tk.Canvas(self, width=800, height=500, borderwidth=0,
                                highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")
        # Height and width of the canvas for reference when displaying objects.
        self.height = self.canvas.winfo_reqheight()
        self.width = self.canvas.winfo_reqwidth()
        self.num_colors = 1  # Number of colors on palette.
        self.num_palettes = 5  # Number of palettes in generation.
        self.crnt_plt_i = 0  # Number for current palette being displayed.
        self.gen_count = 0  # For keeping track of the number of generations.
        self.crnt_palette = cg.Palette()  # Current palette on display.
        self.parents = []
        # Declaring the first generation, which is randomly generated.
        self.generation = [cg.Palette() for p in range(self.num_palettes)]
        for i in range(self.num_palettes):
            self.generation[i].set_num_colors(self.num_colors)
            self.generation[i].create_palette_rand(self.num_colors)
        # rect tags are labels for each color rectangle in palettes.
        self.rect_tags = []
        for i in range(self.num_colors):
            str_i = str(i)
            self.rect_tags.append("rect_tag_" + str_i)

        # Start the first generation.
        self.new_gen_set()

    def new_gen_set(self):
        if self.gen_count != 0:
            if len(self.parents) == 0:
                child_list = [cg.Palette() for p in
                                   range(self.num_palettes)]
                for i in range(self.num_palettes):
                    child_list[i].set_num_colors(self.num_colors)
                    child_list[i].create_palette_rand(self.num_colors)
            else:
                self.parents.append(self.parents[0])
                child_list = cg.palette_child_comb(self.parents,
                                                   self.num_palettes)
            for i in range(self.num_palettes):
                self.generation.append(random.choice(child_list))
                child_list.remove(self.generation[i])
        self.gen_count += 1
        # Setting current generation and palette
        self.generation = list(self.generation)
        self.crnt_palette = self.generation[self.crnt_plt_i]
        # Reset things
        self.parents.clear()
        self.crnt_plt_i = 0
        self.canvas.delete("all")
        # Display palette and control panel.
        self.display_main()
        self.set_palette_colors()

    def set_palette_colors(self):
        for i in range(0, self.num_colors):
            color = self.crnt_palette.palette[i]
            self.canvas.itemconfig(self.rect_tags[i], fill=color)
        self.canvas.itemconfig(self.pltnum_text, text=str(self.crnt_plt_i+1))

    def bckfwd_button(self, fwd_or_bck):
        if fwd_or_bck == 'f':
            self.crnt_plt_i += 1
            if self.crnt_plt_i >= len(self.generation):
                self.crnt_plt_i = 0
        elif fwd_or_bck == 'b':
            self.crnt_plt_i -= 1
            if self.crnt_plt_i < 0:
                self.crnt_plt_i = len(self.generation)-1
        self.crnt_palette = self.generation[self.crnt_plt_i]
        self.set_palette_colors()

    def acprjt_button(self, acp_rjt):
        self.generation.remove(self.generation[self.crnt_plt_i])
        if len(self.generation) > 0:
            if acp_rjt == 'a':
                self.parents.append(self.crnt_palette)
            self.bckfwd_button('f')
        else:
            if acp_rjt == 'a':
                self.parents.append(self.crnt_palette)
            self.new_gen_notice()

    def new_gen_notice(self):
        self.canvas.delete("all")
        y = self.height / 2
        x = self.width / 2 - 50
        next_gen_button = tk.Button(self, text="NEXT GENERATION",
                                    command=lambda: self.new_gen_set(),
                                    anchor="w")
        next_gen_button.configure(width=25, activebackground="white",
                                  relief="flat")
        self.canvas.create_window(x, y, anchor="nw", window=next_gen_button)

    def display_main(self):
        # Display the palette.
        for i in range(0, self.num_colors):
            x1 = i * (self.width / self.num_colors)
            y1 = self.height - 50
            x0 = (self.width / self.num_colors) * (i + 1)
            y0 = 0
            self.rect_tags[i] = (self.canvas.create_rectangle(
                x1, y1, x0, y0, width=0, tag="fart"))
        # The following displayed objects make-up  the control panel.
        # Black rectangle background
        self.canvas.create_rectangle(0, self.height - 50, self.width,
                                     self.height, fill="black", width=0)
        # Text for Palette Number
        self.pltnum_text = self.canvas.create_text(self.width / 2,
                                                   self.height - 25)
        self.canvas.itemconfig(self.pltnum_text, text=str(self.crnt_plt_i + 1),
                               fill="white")
        self.canvas.itemconfig(self.pltnum_text, font=("Arial", 20))
        # Defining the button location parameters.
        y = self.height - 35
        bx = 10
        fx = self.width - 100
        ax = self.width - (self.width / 2) + 60
        rx = self.width - (self.width / 2) - 90
        # Back and forward buttons
        bck_button = tk.Button(self, text="<-",
                               command=lambda: self.bckfwd_button('b'),
                               anchor="w")
        bck_button.configure(width=10, activebackground="white", relief="flat")
        self.canvas.create_window(bx, y, anchor="nw", window=bck_button)
        fwd_button = tk.Button(self, text="                ->",
                               command=lambda: self.bckfwd_button('f'),
                               anchor="w")
        fwd_button.configure(width=10, activebackground="white", relief="flat")
        self.canvas.create_window(fx, y, anchor="nw", window=fwd_button)
        # Accept and reject buttons
        accept_button = tk.Button(self, text="Accept",
                                  command=lambda: self.acprjt_button('a'),
                                  anchor="w")
        accept_button.configure(width=5, background="green",
                                activebackground="white", relief="flat")
        self.canvas.create_window(ax, y, anchor="nw", window=accept_button)
        reject_button = tk.Button(self, text="Reject",
                                  command=lambda: self.acprjt_button('r'),
                                  anchor="w")
        reject_button.configure(width=5, background="red",
                                activebackground="white", relief="flat")
        self.canvas.create_window(rx, y, anchor="nw", window=reject_button)

if __name__ == "__main__":
    app = ColorEvolution()
    app.mainloop()
