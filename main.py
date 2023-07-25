from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip3
import os
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
               't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
               'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    letter_list = [choice(letters) for _ in range(randint(8, 10))]
    symbol_list = [choice(symbols) for _ in range(randint(2, 4))]
    number_list = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = letter_list + number_list + symbol_list

    shuffle(password_list)

    password = "".join(password_list)
    password_input.delete(0, END)
    password_input.insert(0, password)

    pyperclip3.copy(password)
# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():

    website = website_input.get()
    password = password_input.get()
    email = email_input.get()

    data_dict = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any field empty!")

    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered : \nEmail : {email} "
                                                              f"\nPassword : {password} \nIs it Okay to save ?")

        if is_ok:

            try:
                open("data.json", "r")

            except FileNotFoundError:
                open("data.json", "x")

            else:
                with open("data.json", "r") as file:
                    # Reading Old Data
                    data = json.load(file)
                    # Updating New Data
                    data_dict.update(data)
                    # print(data_dict)
            finally:
                with open("data.json", "w") as file:
                    # Saving New Data
                    json.dump(data_dict, file, indent=4)

            password_input.delete(0, END)          # Deletes from 0 index character to the End of text
            website_input.delete(0, END)           # Starting Character is necessary, also can delete a specific char

            file = "notepad.exe data.json"
            os.system(file)

# ---------------------------- Search for Password ------------------------------- #


def find_password():

    website = website_input.get().title()

    try:
        with open("data.json", "r") as file:
            # Reading  Data
            data = json.load(file)

    except FileNotFoundError:
        messagebox.showerror(title="Error", message="Data file not found")

    else:

        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f' E-mail : {email}\n Password : {password}')

        else:
            messagebox.showerror(title="Error", message=f'No details for website "{website}" exists.')


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
website_input = Entry(width=40)
website_input.grid(column=1, row=1, sticky=EW)
website_input.focus()

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)
email_input = Entry(width=40)
email_input.grid(column=1, row=2, columnspan=2, sticky=EW)
email_input.insert(0, "aneeqmalik@gmail.com")

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)
password_input = Entry(width=22)
password_input.grid(column=1, row=3, sticky=EW)

gen_password_button = Button(text="Generate Password", command=generate_password)
gen_password_button.grid(column=2, row=3, sticky=EW)

add_button = Button(text="Add", width=34, command=save)
add_button.grid(column=1, row=4, columnspan=2, sticky=EW)

search_button = Button(text="Search", command=find_password)
search_button.grid(column=2, row=1, sticky=EW)

window.mainloop()
