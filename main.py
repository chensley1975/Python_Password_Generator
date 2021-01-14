from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from datetime import date
from password_generator import Create_Password
import sqlite3
import csv

conn = sqlite3.connect('passwords.db')
c = conn.cursor()

class GUI_Password:

    def __init__(self, master):
        header = ['Date Created', 'Site Name', 'Website', 'Username', 'No. of Characters', 'Password']

        def Create_Table():
            c.execute('CREATE TABLE IF NOT EXISTS passwordtbl (date TEXT, name TEXT, website TEXT, username TEXT, characters TEXT, password TEXT)')

        def Table_Entry():
            characters = self.characters.get()
            password = Create_Password(int(characters))
            site_name = self.site.get()
            website = self.web_address.get()
            username = self.username.get()
            today = date.today()
            curr_date = today.strftime("%m/%d/%Y")
            
            c.execute('SELECT * FROM passwordtbl')
            counts = c.fetchall()
            if len(counts) > 0:
                for row in counts:
                    name = row[1]
                    username = row[3]
                    if name == self.site.get() and username == self.username.get():
                        c.execute("UPDATE passwordtbl SET password=? WHERE name=? AND username=?", (password, site_name, username))
                        conn.commit()
                        return Load_Data()
                c.execute("INSERT INTO passwordtbl (date, name, website, username, characters, password) VALUES (?, ?, ?, ?, ?, ?)", (curr_date, site_name, website, username, characters, password))
                conn.commit()
            else:
                c.execute("INSERT INTO passwordtbl (date, name, website, username, characters, password) VALUES (?, ?, ?, ?, ?, ?)", (curr_date, site_name, website, username, characters, password))
                conn.commit()

            Load_Data()

        def Read_Table():
            conn = sqlite3.connect('passwords.db')
            c = conn.cursor()
            data = c.execute('SELECT * FROM passwordtbl')
            counts = c.fetchall()
            scounts = sorted(counts, key=lambda x: (x[1], x[3]))
            if len(counts) > 0:
                i = 1
                for row in scounts:
                    ttk.Label(self.frame_grid_view, text = row[0]).grid(row = i, column = 0, padx = 10, pady = 10)
                    ttk.Label(self.frame_grid_view, text = row[1]).grid(row = i, column = 1, padx = 10, pady = 10)
                    ttk.Label(self.frame_grid_view, text = row[2]).grid(row = i, column = 2, padx = 10, pady = 10)
                    ttk.Label(self.frame_grid_view, text = row[3]).grid(row = i, column = 3, padx = 10, pady = 10)
                    ttk.Label(self.frame_grid_view, text = row[4]).grid(row = i, column = 4, padx = 10, pady = 10)
                    ttk.Label(self.frame_grid_view, text = row[5]).grid(row = i, column = 5, padx = 10, pady = 10)
                    i += 1

        def Main_Form():
            master.title('Password Generation Program')
            master.iconbitmap('pass.ico')
            master.resizable(False, False)

            self.style = ttk.Style()
            self.style.configure('TButton', font = ('Cambria', 11))
            self.style.configure('TLabel', font = ('Cambria', 11))

            self.frame_header = ttk.Frame(master)
            self.frame_header.pack()

            ttk.Label(self.frame_header, text = 'Password Generation Software', font = ('Cambria', 16, 'bold'))

            Entry_Fields()
            Grid_View()
            Button_View()

        def Entry_Fields():
            self.frame_entry = ttk.Frame(master)
            self.frame_entry.pack()
            
            ttk.Label(self.frame_entry, text = 'Name of site:').grid(row = 0, column = 0, padx = 5, pady = 5, sticky = E)
            self.site = Entry(self.frame_entry, width = 25)
            self.site.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = W)
            ttk.Label(self.frame_entry, text = 'Web Address:').grid(row = 1, column = 0, padx = 5, pady = 5, sticky = E)
            self.web_address = Entry(self.frame_entry, width = 50)
            self.web_address.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = W)
            ttk.Label(self.frame_entry, text = 'Username:').grid(row = 2, column = 0, padx = 5, pady = 5, sticky = E)
            self.username = Entry(self.frame_entry, width = 25)
            self.username.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = W)
            ttk.Label(self.frame_entry, text = 'Number of Characters:').grid(row = 3, column = 0, padx = 5, pady = 5, sticky = E)
            self.characters = Entry(self.frame_entry, width = 5)
            self.characters.grid(row = 3, column = 1, padx = 5, pady = 5, sticky = W)

        def Clear_Fields():
            self.site.delete(0, 'end')
            self.web_address.delete(0, 'end')
            self.username.delete(0, 'end')
            self.characters.delete(0, 'end')

        def Grid_View():
            self.frame_grid_view = ttk.Frame(master)
            self.frame_grid_view.pack()

            ttk.Label(self.frame_grid_view, text = header[0]).grid(row = 0, column = 0, padx = 10, pady = 10)
            ttk.Label(self.frame_grid_view, text = header[1]).grid(row = 0, column = 1, padx = 10, pady = 10)
            ttk.Label(self.frame_grid_view, text = header[2]).grid(row = 0, column = 2, padx = 10, pady = 10)
            ttk.Label(self.frame_grid_view, text = header[3]).grid(row = 0, column = 3, padx = 10, pady = 10)
            ttk.Label(self.frame_grid_view, text = header[4]).grid(row = 0, column = 4, padx = 10, pady = 10)
            ttk.Label(self.frame_grid_view, text = header[5]).grid(row = 0, column = 5, padx = 10, pady = 10)

            Read_Table()

        def Load_Data():
            self.frame_header.destroy()
            self.frame_entry.destroy()
            self.frame_grid_view.destroy()
            self.frame_buttons.destroy()
            Main_Form()

        def Export_Table():
            data = []
            row_data = []
            data.append(header)
            folder_name = filedialog.askdirectory()
            file_name = folder_name + '/' + 'password_export.csv'
            c.execute('SELECT * FROM passwordtbl')
            table_data = c.fetchall()
            for row in table_data:
                for i in range(6):
                    row_data.append(row[i])
                data.append(row_data)
                row_data = []
            with open(file_name, 'w', newline='') as pass_file:
                pass_write = csv.writer(pass_file)
                pass_write.writerows(data)
            messagebox.showinfo("File Saved!", "The file has been saved.")

        def Button_View():
            self.frame_buttons = ttk.Frame(master)
            self.frame_buttons.pack()

            ttk.Button(self.frame_buttons, text = 'Create Password', command = Table_Entry).grid(row = 0, column = 0, padx = 10, pady = 10)
            ttk.Button(self.frame_buttons, text = 'Export Passwords', command = Export_Table).grid(row = 0, column = 1, padx = 10, pady = 10)
            ttk.Button(self.frame_buttons, text = 'Clear', command = Clear_Fields).grid(row = 0, column = 2, padx = 10, pady = 10)
            ttk.Button(self.frame_buttons, text = 'Exit', command = master.destroy).grid(row = 0, column = 3, padx = 10, pady = 10)

        Create_Table()
        Main_Form()

def main():
    root = Tk()
    passwords = GUI_Password(root)
    root.mainloop()
    c.close()
    conn.close()

if __name__ == "__main__": main()
