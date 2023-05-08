# Testing second ListBox instead of textbox to allow deletion of items
import tkinter as tk
import data as data


class Gui:
    def __init__(self, master, model):
        self.master = master
        self.model = model
        master.title("Shop")
        master.geometry(f"600x{180 + len(self.model.products) * 15}")
        # master.state("zoomed")
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

        # Listbox für die Rechnung
        self.invoice_listbox = tk.Listbox(master, height=(len(self.model.products)), width=30, exportselection=False)
        self.invoice_listbox.place(x=150, y=35)
        self.invoice_listbox.bind("<<ListboxSelect>>", self.delete_item)

        # Summen Label
        self.total_label = tk.Label(master, text="Summe: 0.00 EUR", justify="right")
        self.total_label.place(x=230, y=10)

        # Bezahl-Button
        self.pay_button = tk.Button(master, text="Bezahlen", width=10, height=4, command=self.reset_invoice)
        self.pay_button.place(x=410, y=35)

    def chosen_product(self, event):
        index = self.products_listbox.curselection()[0]
        product = list(self.model.products.keys())[index]
        self.model.add_to_invoice(product)
        self.update_invoice()

    def update_invoice(self):
        self.invoice_listbox.delete(0, tk.END)  # Empty invoice
        price_sum = 0
        for product, amount in self.model.invoice.items():
            price_sum += self.model.products[product] * amount
            self.invoice_listbox.insert(tk.END, f"{amount} x {product}: {self.model.products[product]:.2f} EUR\n")
        self.total_label.configure(text=f"Summe: {price_sum:.2f} EUR", justify="right")

    def delete_item(self, event):
        index = self.invoice_listbox.curselection()
        if index:
            product_text = self.invoice_listbox.get(index[0])
            if "Summe" not in product_text:
                product = product_text.split(" x ")[1].split(":")[0].strip()
                self.model.remove_from_invoice(product)
                self.update_invoice()

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

    def remove_from_invoice(self, product):
        if product in self.invoice:
            if self.invoice[product] > 1:
                self.invoice[product] -= 1
            else:
                del self.invoice[product]

    def reset_invoice(self):
        self.invoice = {}


model_object = Model(data.products)

root = tk.Tk()

gui = Gui(root, model_object)
root.mainloop()
