import tkinter as tk
from tkinter import ttk
import mysql.connector
from HO import run as run

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

        self.add_btn = ttk.Button(self, text="Refresh", command=self.refresh)
        self.add_btn.pack()

        self.treeview.pack(pady=10)


        # Connect to the BO database
        self.HO_db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ho_sales"
        )

        self.cursor = self.HO_db.cursor()
        query = "SELECT * FROM sales ORDER BY sale_date DESC LIMIT 10"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        # Populate the table with the sales data
        for row in rows:
            self.treeview.insert("", tk.END, values=row)

        self.cursor.close()
        # Close the database connection
        self.HO_db.close()
    def mainloop(self, run):
        run()
        self.master.mainloop()

    def refresh(self):
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        self.HO_db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ho_sales"
        )

        self.cursor = self.HO_db.cursor()
        query = "SELECT * FROM sales ORDER BY sale_date DESC LIMIT 10"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        # Populate the table with the sales data
        for row in rows:
            self.treeview.insert("", tk.END, values=row)

        self.cursor.close()
        # Close the database connection
        self.HO_db.close()






if __name__ == '__main__':
    root = tk.Tk()
    app = HOInterface(master=root)
    app.mainloop(run)
