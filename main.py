import tkinter as tk
import data as data


class Gui:
    def __init__(self, master, model):
        self.master = master
        self.model = model
        master.title("Shop")
        # master.geometry(f"1900x{180 + len(self.model.products) * 35}")
        # master.state("zoomed")
        # print(f"600x{180 + len(self.model.products)*15}")
        master.geometry("1000x600")
        # master.configure(bg="honeydew")

        # Label for product list
        self.product_label = tk.Label(master, text="Produkte", font=("Arial", 16))
        self.product_label.place(x=55, y=40)

        # Label for invoice
        self.invoice_label = tk.Label(master, text="Rechnung", font=("Arial", 16))
        self.invoice_label.place(x=577, y=40)

        # Label for total
        self.total_label = tk.Label(master, text="Summe: 0.00 EUR", font=("Arial", 16))
        self.total_label.place(x=577, y=70)

        # Listbox for product list
        self.products_listbox = tk.Listbox(master, height=19, width=30, borderwidth=0, exportselection=False,
                                           font=("Arial", 16), selectbackground="lightblue", selectforeground="black")
        for product, price in self.model.products.items():      # Add Items to Listbox
            self.products_listbox.insert(tk.END, f"{product} - {price}€")
        self.products_listbox.place(x=55, y=70)
        self.products_listbox.bind("<<ListboxSelect>>", self.chosen_product)

        # Listbox for invoice
        self.invoice_listbox = tk.Listbox(master, height=15, width=30, borderwidth=0, exportselection=False,
                                          font=("Arial", 16))
        self.invoice_listbox.place(x=577, y=105)
        self.invoice_listbox.bind("<<ListboxSelect>>", self.delete_item)

        # Button to pay
        self.pay_button = tk.Button(master, text="Bezahlen", width=30, height=2, borderwidth=0,
                                    command=self.reset_invoice, font=("Arial", 16))
        self.pay_button.place(x=577, y=490)

    def chosen_product(self, event):
        index = self.products_listbox.curselection()[0]
        product = list(self.model.products.keys())[index]
        self.model.add_to_invoice(product)
        self.update_invoice()

    def update_invoice(self):
        self.invoice_listbox.delete(0, tk.END)      # Empty invoice
        price_sum = 0
        for product, amount in self.model.invoice.items():
            price_sum += self.model.products[product] * amount
            self.invoice_listbox.insert(tk.END, f"{amount} x {product}: {self.model.products[product]:.2f} EUR\n")
        self.total_label.configure(text=f"Summe: {price_sum:.2f} EUR")

    def delete_item(self, event):
        index = self.invoice_listbox.curselection()
        if index:
            product_text = self.invoice_listbox.get(index[0])
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
