import tkinter as tk
from tkinter import ttk
import mysql.connector
from BO1 import send_sales_data


class BO1Interface(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("BO1 Interface")
        self.pack(fill='both', expand=True)

        # Create the Treeview table to display sales data
        self.table_columns = ('id', 'Product', 'price', 'quantity', 'sale_date', 'synced')
        self.treeview = ttk.Treeview(self, columns=self.table_columns, show='headings')
        self.treeview.column('id', width=100, anchor='center')
        self.treeview.column('Product', width=200, anchor='center')
        self.treeview.column('price', width=120, anchor='center')
        self.treeview.column('quantity', width=120, anchor='center')
        self.treeview.column('sale_date', width=120, anchor='center')
        self.treeview.column('synced', width=120, anchor='center')

        self.treeview.heading('id', text='id')
        self.treeview.heading('Product', text='Product')
        self.treeview.heading('price', text='price')
        self.treeview.heading('quantity', text='quantity')
        self.treeview.heading('sale_date', text='sale_date')
        self.treeview.heading('synced', text='synced')

        self.treeview.pack(pady=10)

        # Create the 'Send Sales Data' button
        self.send_sales_btn = ttk.Button(self, text="Send Sales Data", command=self.send_sales_data)
        self.send_sales_btn.pack(pady=10)

        # Create the form for adding new sales data
        self.add_frame = ttk.Frame(self)
        self.add_frame.pack(pady=10)

        self.product_label = ttk.Label(self.add_frame, text="Product:")
        self.product_label.grid(row=0, column=0, padx=5, pady=5)

        self.product_entry = ttk.Entry(self.add_frame)
        self.product_entry.grid(row=0, column=1, padx=5, pady=5)

        self.date_label = ttk.Label(self.add_frame, text="Date (YYYY-MM-DD):")
        self.date_label.grid(row=1, column=0, padx=5, pady=5)

        self.date_entry = ttk.Entry(self.add_frame)
        self.date_entry.grid(row=1, column=1, padx=5, pady=5)

        self.quantity_label = ttk.Label(self.add_frame, text="Quantity:")
        self.quantity_label.grid(row=2, column=0, padx=5, pady=5)

        self.quantity_entry = ttk.Entry(self.add_frame)
        self.quantity_entry.grid(row=2, column=1, padx=5, pady=5)

        self.price_label = ttk.Label(self.add_frame, text="Price:")
        self.price_label.grid(row=3, column=0, padx=5, pady=5)

        self.price_entry = ttk.Entry(self.add_frame)
        self.price_entry.grid(row=3, column=1, padx=5, pady=5)

        self.add_btn = ttk.Button(self.add_frame, text="Add Sale", command=self.add_sale)
        self.add_btn.grid(row=4, column=1, padx=5, pady=5)


        # Connect to the BO database
        bo1_db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bo1_sales"
        )

        # Fetch the all sales data from the BO database
        cursor = bo1_db.cursor()
        query = "SELECT * FROM sales ORDER BY sale_date DESC LIMIT 10"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()

        # Populate the table with the sales data
        for row in rows:
            self.treeview.insert("", tk.END, values=row)

        # Close the database connection
        bo1_db.close()

    def send_sales_data(self):
        # Call the send_sales_data() function from BO1_server.py
        send_sales_data()
        bo1_db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bo1_sales"
        )

        # Fetch the all sales data from the BO database
        cursor = bo1_db.cursor()

        for item in self.treeview.get_children():
            self.treeview.delete(item)

        query = "SELECT * FROM sales ORDER BY sale_date DESC"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()

        # Populate the table with the sales data
        for row in rows:
            self.treeview.insert("", tk.END, values=row)
        print('Sales data sent from BO1')

    def add_sale(self):
        # Get the product and date from the form
        product = self.product_entry.get()
        date = self.date_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()

        # Connect to the BO database
        bo1_db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bo1_sales"
        )

        # Insert the new sale into the database
        cursor = bo1_db.cursor()
        query = "INSERT INTO sales (product_name, sale_date,price,quantity, synced) VALUES (%s, %s, %s,%s,%s)"
        values = (product, date, price, quantity, 0)
        cursor.execute(query, values)
        bo1_db.commit()

        # Clear the form and refresh the table
        self.product_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)

        for item in self.treeview.get_children():
            self.treeview.delete(item)

        query = "SELECT * FROM sales ORDER BY sale_date DESC"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()

        # Populate the table with the sales data
        for row in rows:
            self.treeview.insert("", tk.END, values=row)

        print('Sale added to BO1 database')
        cursor.close()


if __name__ == '__main__':
    root = tk.Tk()
    app = BO1Interface(master=root)
    app.mainloop()
