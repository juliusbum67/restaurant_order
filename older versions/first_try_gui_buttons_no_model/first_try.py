import tkinter as tk
from collections import Counter
import tkinter.font as font


class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground


class Model:
    def __init__(self):
        self.menu = {
            "Eis": 1,
            "Kuchen": 3,
            "Kaffee": 2,
            "Wasser": 1
        }
        self.price = 0
        self.products = []
        # self.ice_count = tk.StringVar(value="0")
        self.ice_count = self.count_product("Eis")
        self.cake_count = self.count_product("Kuchen")
        self.coffee_count = self.count_product("Kaffee")
        self.water_count = self.count_product("Wasser")

    def add_product(self, product):
        """Products: Eis 1E, Kuchen 3E, Kaffee 2E, Wasser 1E
        returns self.price, useful for showing live price"""
        # idea: with dictionary call values of string products as prices, maybe self.menu
        self.products.append(product)
        print(f"{product} added.")

        return self.products

    # def refresh_product_counts(self):

    def get_price(self):
        for elements in self.products:
            self.price += self.menu[elements]
        print(f"get_price was run! Price: {self.price}")
        return self.price

    def get_product_amounts(self):
        counted_products = Counter(self.products).most_common()     # Only works with label if there are already any products.
        print(counted_products)
        return counted_products

    def count_product(self, product):
        count = 0
        for element in self.products:
            if element == product:
                count += 1
        return count

    def reset(self):
        self.products = []
        self.price = 0


# Height appears to be *20 and width *10 pixels
class GUI:
    def __init__(self, model):
        self.model = model
        # main window
        self.root = tk.Tk()
        self.root.title("Restaurant Bestellung")
        self.root.geometry("1000x600")
        self.ice_count = tk.StringVar(master=self.root, value="0")

        # Buttons
        # missing: text to be shown on button, maybe picture, coordinates
        self.order_ice_button = HoverButton(self.root, height=5, width=50, text="Eis   1€", borderwidth=0,
                                            activebackground="lightblue", command=lambda: model.add_product("Eis"))
        self.order_ice_button.place(x=20, y=80)
        # self.order_ice_button["font"] = font.Font(weight=10, size=10)

        self.order_cake_button = HoverButton(self.root, height=5, width=50, text="Kuchen   3€", borderwidth=0,
                                             activebackground="lightblue", command=lambda: model.add_product("Kuchen"))
        self.order_cake_button.place(x=20, y=180)

        self.order_coffee_button = HoverButton(self.root, height=5, width=50, text="Kaffee   2€", borderwidth=0,
                                               activebackground="lightblue", command=lambda: model.add_product("Kaffee"))
        self.order_coffee_button.place(x=20, y=280)

        self.order_water_button = HoverButton(self.root, height=5, width=50, text="Wasser   1€", borderwidth=0,
                                              activebackground="lightblue", command=lambda: model.add_product("Wasser"))
        self.order_water_button.place(x=20, y=380)

        self.order_button = HoverButton(self.root,  height=5, width=50, text="Bestellen", borderwidth=0, activebackground="lightblue",
                                        command=lambda: model.reset())
        self.order_button.place(x=480, y=380)

        # Labels for Buttons
        # self.ice_label = tk.Label(self.root, text="Eis", background="None")
        # self.ice_label.place(x=40, y=30)
        # self.ice_price_label = tk.Label(self.root, text="1€")
        # self.ice_price_label.place(x=350, y=410)

        # Labels
        self.products_label = tk.Label(self.root, text="Produkte", font=('Arial',16,'bold','underline'))
        self.products_label.place(x=150, y=20)
        # self.products_label["font"] = font.Font(size=16, underline=True, font="Arial")
        # self.ice_label = tk.Label

        # Product Labels
        # self.ice_amount_label = tk.Label(self.root, text=f"{}")
        # self.first_product_label = tk.Label(self.root, text=f"{model.get_product_amounts()[0][1]}x {main.Model.get_product_amounts()[0][0]}")     # Does not work (IndexError) because list is empty when label is initialized
        # self.first_product_label.place(x=480, y=300)

        self.first_product_label = tk.Label(self.root, textvariable=self.ice_count)
        self.first_product_label.place(x=480, y=300)
        self.first_product_label.pack()


        # start tkinter
        self.root.mainloop()

model = Model()
gui=GUI(model)