from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json
WHITE = "#ffffff"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    pw_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    web_details = web_entry.get().title()
    email_details = email_entry.get()
    pw_details = pw_entry.get()
    new_data = {
        web_details: {
            "email": email_details,
            "password": pw_details,
        }
    }

    if web_details == "" or pw_details == "":
        messagebox.showwarning(title="Oops",message="Please don't leave any field empty")
    else:
        is_ok = messagebox.askokcancel(title=web_details, message=f"These are the details entered: \nEmail: {email_details}"
                                                          f"\n Password: {pw_details} \nIs it ok to save?")
        if is_ok:
                try:
                    # Reading old data
                    with open("data.json", "r") as data_file:
                        data = json.load(data_file)

                except FileNotFoundError:
                    with open("data.json", "w") as data_file:
                        #Saving updated data
                        json.dump(new_data, data_file, indent=4)

                except ValueError:
                    with open("data.json", "w") as data_file:
                        #Saving updated data
                        json.dump(new_data, data_file, indent=4)
                else:
                    # Updating old data with new data
                    data.update(new_data)
                    with open("data.json", "w") as data_file:
                        json.dump(data, data_file, indent=4)
                finally:
                    web_entry.delete(0, END)
                    pw_entry.delete(0, END)


#-----------------------------Search Password------------------------------------#
def find_password():
    website = web_entry.get().title()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showwarning(title="Error", message="No data file found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\n"
                                                       f"Password: {password}")
        else:
            messagebox.showwarning(title="Error", message=f"No details for {website} exists")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg=WHITE)

canvas = Canvas(height=200, width=200, bg=WHITE, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# labels
web_label = Label(text="Website:", bg=WHITE)
web_label.grid(column=0, row=1)

email_label = Label(text="Email/Username:", bg=WHITE)
email_label.grid(column=0, row=2)

pw_label = Label(text="Password:", bg=WHITE)
pw_label.grid(column=0, row=3)

# entries
web_entry = Entry(width=21, highlightthickness=0)
web_entry.grid(column=1, row=1)
web_entry.focus()

email_entry = Entry(width=38, highlightthickness=0)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, "saurav.shaw10@gmail.com")

pw_entry = Entry(width=21, highlightthickness=0)
pw_entry.grid(column=1, row=3)

# buttons
gen_pw_button = Button(text="Generate Password", highlightbackground=WHITE, command=generate_password)
gen_pw_button.grid(column=2, row=3)

add_button = Button(text="Add", width=35, highlightbackground=WHITE, command=save)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search",width=13, highlightbackground=WHITE, command=find_password)
search_button.grid(column=2, row=1)


window.mainloop()