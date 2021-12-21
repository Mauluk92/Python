from tkinter import *
from tkinter.ttk import *
from FiscalCodeCalculator import FiscalCodeCalculator


def calculate():
    list_inputs = [surname.get(), name.get(), year.get(), month_option.get(), day.get(), locality.get(), gender.get()]
    code.set(FiscalCodeCalculator(list_inputs).fiscal_code)


month_list =("Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
"Luglio", "Agosto", "Settembre", "Ottombre", "Novembre", "Dicembre")

main_window = Tk()
main_window.title("Calcolatore Codice Fiscale")


name = StringVar(main_window)
surname = StringVar(main_window)
locality = StringVar(main_window)
gender = IntVar(main_window)
year = StringVar(main_window)
month = StringVar(main_window)
day = StringVar(main_window)
code = StringVar(main_window)

style_label = Style()
style_button = Style()
font_label =("Courier", 11, "bold")
font_button =("Courier", 11, "bold")
font_entry =("Courier", 11, "bold")
background_primary ="#c4e7f0"
color_button_active = ("active", "#5ba8d3")
color_button_inactive = ('!active','#5ba8d3')

style_label.configure('My.TLabel',background =background_primary, font = font_label)
style_button.configure('My.TButton', font = font_button, background ="#5ba8d3" )
style_button.map('My.TButton', background=[color_button_active, color_button_inactive])
main_window.configure(background=background_primary)


name_label = Label(main_window, text = "Nome:", style = 'My.TLabel')
surname_label = Label(main_window, text = "Cognome:", style = 'My.TLabel')
locality_label = Label(main_window, text = "Luogo di nascita:", style = 'My.TLabel')
gender_label = Label(main_window, text = "Genere:",  style = 'My.TLabel')
data_label = Label(main_window, text ="Data di nascita:", style = 'My.TLabel')


code_label = Label(main_window, textvariable = code, style='My.TLabel')
code_label.configure(anchor="center")

name_entry = Entry(main_window, textvariable = name)
surname_entry = Entry(main_window, textvariable = surname)
locality_entry = Entry(main_window, textvariable = locality)
year_entry = Entry(main_window, textvariable = year, width=4)
day_entry = Entry(main_window, textvariable = day, width=2)

gender_M_radio = Radiobutton(main_window, text="M", variable = gender, value =0 )
gender_F_radio = Radiobutton(main_window, text="F", variable = gender, value =40)

month_option = Combobox(main_window, values =month_list)

code_button = Button(main_window, text="Calcola", command=calculate, style='My.TButton')

name_label.grid(row=0, column = 0, sticky=("WE"))
surname_label.grid(row=1, column = 0, sticky=("WE"))
locality_label.grid(row=2, column = 0, sticky=("WE"))
gender_label.grid(row=5, column = 0, sticky=("WE"))
data_label.grid(row=3, column = 0, sticky=("WE"))

name_entry.grid(row=0, column = 2, columnspan=2, sticky="WE")
surname_entry.grid(row=1, column = 2, columnspan=2, sticky="WE")
locality_entry.grid(row=2, column = 2, columnspan=2, sticky="WE")
day_entry.grid(row =3, column = 1, sticky="W")
year_entry.grid(row = 3, column =3, sticky="W")


month_option.grid(row= 3, column = 2, sticky="W")


gender_M_radio.grid(row= 5, column = 1, sticky="E")
gender_F_radio.grid(row= 5, column = 2, sticky="W")

code_label.grid(row = 8, column = 0, sticky="EW", columnspan = 4)

code_button.grid(row = 6, column = 0, sticky="EW", columnspan = 4)

main_window.mainloop()
