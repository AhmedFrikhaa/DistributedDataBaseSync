import tkinter as tk
from tkinter import ttk
import mysql.connector
from HO import handle_sales_data

class HOInterface(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("HO Interface")
        self.pack(fill='both', expand=True)

        # Create the Treeview table to display sales data
        self.table_columns = ('id', 'Product', 'price', 'quantity', 'sale_date')
        self.treeview = ttk.Treeview(self, columns=self.table_columns, show='headings')
        self.treeview.column('id', width=100, anchor='center')
        self.treeview.column('Product', width=200, anchor='center')
        self.treeview.column('price', width=120, anchor='center')
        self.treeview.column('quantity', width=120, anchor='center')
        self.treeview.column('sale_date', width=120, anchor='center')

        self.treeview.heading('id', text='id')
        self.treeview.heading('Product', text='Product')
        self.treeview.heading('price', text='price')
        self.treeview.heading('quantity', text='quantity')
        self.treeview.heading('sale_date', text='sale_date')

        self.treeview.pack(pady=10)


        # Connect to the BO database
        HO_db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ho_sales"
        )

        cursor = HO_db.cursor()
        query = "SELECT * FROM sales ORDER BY sale_date DESC LIMIT 10"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()


        # Populate the table with the sales data
        for row in rows:
            self.treeview.insert("", tk.END, values=row)

        # Close the database connection
        HO_db.close()



if __name__ == '__main__':
    root = tk.Tk()
    app = HOInterface(master=root)
    app.mainloop()
