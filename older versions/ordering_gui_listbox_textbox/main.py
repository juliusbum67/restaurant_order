import tkinter as tk
import data as data


class Gui:
    def __init__(self, master, model):
        self.master = master
        self.model = model
        master.title("Shop")
        master.geometry(f"600x{180 + len(self.model.products) * 15}")
        # print(f"600x{180 + len(self.model.products)*15}")

        # Label für Produktliste
        self.product_label = tk.Label(master, text="Produkte")
        self.product_label.place(x=10, y=10)

        # Label für Rechnung
        self.invoice_label = tk.Label(master, text="Rechnung")
        self.invoice_label.place(x=150, y=10)

        # Listbox für Produktliste
        self.products_listbox = tk.Listbox(master, height=len(self.model.products))
        for product, price in self.model.products.items():
            self.products_listbox.insert(tk.END, f"{product} - {price}€")
        self.products_listbox.place(x=10, y=35)
        self.products_listbox.bind("<<ListboxSelect>>", self.chosen_product)

        # Textfeld für die Rechnung
        self.invoice_text = tk.Text(master, height=(len(self.model.products) + 2), width=30, exportselection=False)
        self.invoice_text.place(x=150, y=35)

        # Bezahl-Button
        self.pay_button = tk.Button(master, text="Bezahlt", width=10, height=4, command=self.reset_invoice)
        self.pay_button.place(x=410, y=35)

    def chosen_product(self, event):
        index = self.products_listbox.curselection()[0]
        product = list(self.model.products.keys())[index]
        self.model.add_to_invoice(product)
        self.update_invoice()

    def update_invoice(self):
        self.invoice_text.delete(1.0, tk.END) # Textfeld leeren
        price_sum = 0
        for product, amount in self.model.invoice.items():
            price_sum += self.model.products[product] * amount
            self.invoice_text.insert(tk.END, f"{amount} x {product}: {self.model.products[product]:.2f} EUR\n")
        self.invoice_text.insert(tk.END, f"\nSumme: {price_sum:.2f} EUR")

    def reset_invoice(self):
        self.model.reset_invoice()
        self.update_invoice()


class Model:
    def __init__(self, product):
        self.products = product
        self.invoice = {}

    def add_to_invoice(self, product):
        if product in self.invoice:
            self.invoice[product] += 1
        else:
            self.invoice[product] = 1

    def reset_invoice(self):
        self.invoice = {}


model_object = Model(data.produkte)

root = tk.Tk()

gui = Gui(root, model_object)
root.mainloop()
