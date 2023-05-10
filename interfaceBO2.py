import tkinter as tk
from tkinter import ttk
import mysql.connector
from BO2 import send_sales_data


class BO2Interface(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("BO2 Interface")
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

        self.add_btn = ttk.Button(self.add_frame, text="Add Sale", command=self.add_sale)
        self.add_btn.grid(row=2, column=1, padx=5, pady=5)

        # Connect to the BO database
        bo2_db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bo2_sales"
        )

        # Fetch the all sales data from the BO database
        cursor = bo2_db.cursor()
        query = "SELECT * FROM sales ORDER BY sale_date DESC LIMIT 10"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()

        # Populate the table with the sales data
        for row in rows:
            self.treeview.insert("", tk.END, values=row)

        # Close the database connection
        bo2_db.close()

    def send_sales_data(self):
        # Call the send_sales_data() function from BO2_server.py
        send_sales_data()
        print('Sales data sent from BO2')

    def add_sale(self):
        # Get the product and date from the form
        product = self.product_entry.get()
        date = self.date_entry.get()

        # Connect to the BO database
        bo2_db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bo2_sales"
        )

        # Insert the new sale into the database
        cursor = bo2_db.cursor()
        query = "INSERT INTO sales (product_name, sale_date, synced) VALUES (%s, %s, %s)"
        values = (product, date, 0)
        cursor.execute(query, values)
        bo2_db.commit()
        cursor.close()

        self.product_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        print('Sale added to BO2 database')


if __name__ == '__main__':
    root = tk.Tk()
    app = BO2Interface(master=root)
    app.mainloop()
