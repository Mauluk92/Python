from tkinter import *
from tkinter.ttk import *
from calendar import monthrange
import re
import Levenshtein as lev
import unidecode
import datetime

################################################################################
# Variabili Globali
################################################################################



# Month List verrà mostrato nel menu a tendina
month_list = ("Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
"Luglio", "Agosto", "Settembre", "Ottombre", "Novembre", "Dicembre")
currentDateTime = datetime.datetime.now()
date = currentDateTime.date()
current_year = int(date.strftime("%Y"))


numbers_month = [1,2,3,4,5,6,7,8,9,10,11,12]
month_list_upper_case = map(lambda x: x.upper(), month_list) # Mette tutti i mesi in uppercase

dict_month_to_numbers = dict(zip(month_list_upper_case, numbers_month))

# 1.1 Queste variabili servono per il calcolo delle cifre associate ai primi 15 caratteri del codice fiscale per il carattere di controllo

control_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]  # Sequenza dei caratteri di controllo (alfabetico)
keys = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
value_odd = [1,0,5,7,9,13,15,17,19,21,1,0,5,7,9,13,15,17,19,21,2,4,18,20,11,3,6,8,12,14,16,10,22,25,24,23]
value_even =[0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]

# 1.2 Dizionari per il calcolo del carattere di controllo

dict_odd = dict(zip(keys, value_odd))
dict_even = dict(zip(keys, value_even))

#



################################################################################
# Funzioni di analisi degli input testuali: restituiscono True se corretti
################################################################################

def is_name_correct(aName):
    aName = aName.strip().replace(" ", "").upper()
    pattern_aName = "^([A-Z]|\'|[ÀÈÌÒÙY])+$"  # Il nome, cognome deve avere solo lettere o al più apostrofi
    return re.match(pattern_aName, aName)
def is_day_correct(aDay):
    aDay = aDay.strip().replace(" ", "")
    pattern_aDay = "^\d\d$"                # Il giorno deve avere esattamente due cifre
    return re.match(pattern_aDay, aDay)
def is_year_correct(aYear):
    aYear = aYear.strip().replace(" ", "")
    pattern_aYear = "^\d\d\d\d$"              # L'anno deve contenere esattamente quattro cifre
    return re.match(pattern_aYear, aYear)
def is_locality_correct(aLocality):           # La località deve essere nel codice catastale e non deve contenere numeri
    aLocality = aLocality.strip().upper().replace(" ", "")
    pattern_aLocality = "^([A-Z]|\D|\')+$"
    aLocality_codice = ""
    aLocality_correctness = re.match(pattern_aLocality, aLocality)
    file = open("codice_catastale.txt", "r")
    while 1:
        LINEA = file.readline().strip()
        if not LINEA:
            return [False, ""]
        c = LINEA.split(";")
        if c[0].replace(" ", "") == aLocality:
            return [aLocality_correctness, c[1]]
def is_month_correct(aMonth):                # Il mese deve essere compreso nella month_list
    upper_case_month_list = map(lambda x : x.upper(), month_list)
    if aMonth.upper() in upper_case_month_list:
        return True

def is_day_within_range(aDay, aMonth, aYear):      # Restituisce True se il numero di giorni in un dato mese di un dato anno è corretto
    if 1 <= aDay <= int(monthrange(aYear, aMonth)[1]):
        return True
    else:
        return False




#######################################################
# Funzione di best-match: restituisce il comune più vicino all'input utente
#######################################################

def best_match_locality(aLocality):
    aLocality = aLocality.upper().strip().replace(" ", "")
    file = open("codice_catastale.txt", "r")
    best_match = ""
    while 1:
        LINEA = file.readline().strip()
        if not LINEA:
            break
        c = LINEA.split(";")             # Si ottiene una lista del tipo [Comune, Codice_Comune]
        match = c[0].replace(" ", "")    # Questo è il comune con cui andremo a confrontare l'input utente errato
        k = lev.jaro_winkler(aLocality, c[0]) # Questa funzione calcola il "grado" di scostamento tra la stringa input e quella match
        best = lev.jaro_winkler(best_match, aLocality) # Questo è il valore migliore della precedente funzione
        if k > 0.8 and k > best:                       # Se il comune si discosta di meno dalla stringa input rispetto al nostro best_match, sostituirlo
            best_match = c[0]
    return best_match                                  # A fine processo abbiamo una stringa che si discosta di meno da tutte da quella utente

################################################################################
# Funzioni di elaborazione delle cifre del codice fiscale: restituiscono le varie parti del codice
################################################################################

# 1 Questa funzione elabora le consonanti/vocali del nome e del cognome.
# 1.1 Se mancano sufficienti consonanti e/o vocali si aggiunge una X al codice (fino ad un massimo di due)


def is_double_letter(aName):
    double_letters= []
    for index_char in range(len(aName)-1):
        if aName[index_char] == aName[index_char +1]:
            double_letters.append(aName[index_char])
    return double_letters
            



def name_surname_code(aName):
    aName_codice = ""
    aName = unidecode.unidecode(aName)
    lista_vocali = ["A", "E", "I", "O", "Y"]
    vocali = []
    consonanti = []
    double_letters = is_double_letter(aName.upper().replace("'", "").strip().replace(" ", ""))
    for lettera in aName.upper().replace("'", "").strip().replace(" ", ""):
        if lettera not in lista_vocali:
            consonanti.append(lettera)
        else:
            vocali.append(lettera)
    vocali = vocali + ["X","X"]
    consonanti_vocali = consonanti + vocali # Lista delle lettere ordinate per priorità
    while len(aName_codice) < 3:   
        if (consonanti_vocali[0] in double_letters ) and len(set(consonanti))>1:
            consonanti_vocali.pop(0)
        aName_codice = aName_codice + consonanti_vocali[0]
        consonanti_vocali.pop(0)
            
    return aName_codice



        
# 2 Questa funzione elabora il mese di nascita e restituisce l'ID corretto corrispondente 
def month_code(aMonth):
    # Lista delle lettere identificative dei mesi corrispondenti
    aMonth = aMonth.upper()
    month_id = ["A", "B", "C", "D", "E", "H", "L", "M", "P", "R", "S", "T"]
    return month_id[dict_month_to_numbers[aMonth]-1]

################################################################################
# Calcolo delle cifre del codice Fiscale
################################################################################
n = 0
def calcola_codice():
    easter_egg2 = ""
    easter_egg =""
    risultato_codice_fiscale = ""
    errori = ""
    control_number = 0 # Somma dei numeri associati ad ogni carattere (pari o dispari): utilizzato per il calcolo del carattere di controllo finale

    # Test degli input

    if not is_name_correct(surname.get()):
        errori += "Il cognome è digitato incorrettamente!\n"
    if not is_name_correct(name.get()):
        errori += "Il nome è digitato incorrettamente!\n"
    if not is_year_correct(year.get()):
        errori +=  "L'anno è digitato incorrettamente!\n"
    if not is_day_correct(day.get()):
        errori += "Il giorno è digitato incorrettamente!\n"
    if not is_month_correct(month_option.get()):
        errori += "Il mese è digitato incorrettamente!\n"
    if is_month_correct(month_option.get()) and is_day_correct(day.get()) and is_year_correct(year.get()):
        if not is_day_within_range(int(day.get()),dict_month_to_numbers[month_option.get().upper()], int(year.get())):
            errori += "Il giorno non è compreso nel mese!\n"

# Se la località non è stata trovata, tentare una migliore corrispondenza. Se trovata, mostrarla.

    if not is_locality_correct(locality.get())[0]:
        errori += "La località non è stata trovata!\n"
        if best_match_locality(locality.get()):
            errori += "Forse intendevi " + best_match_locality(locality.get()) + "?"

# Sezione Easter Egg 1

    if int(year.get()) < current_year - 100 and num_tentativi.get() > 0:
        easter_egg = ""
        easter_egg2 = "Va bene ti credo ;)"
    if int(year.get()) < current_year - 100 and num_tentativi.get() == 0:
        easter_egg = "Dai frà fai il serio!" if gender.get() == 0 else "Dai soré fai la seria!"
        num_tentativi.set(1)

# Se sono presenti errori, mostrarli, altrimenti si procede con il calcolo del codice fiscale

    if errori:
        code.set(errori)
    elif easter_egg:
        code.set(easter_egg)
    else:
        risultato_codice_fiscale += name_surname_code(surname.get())
        risultato_codice_fiscale += name_surname_code(name.get())
        risultato_codice_fiscale += year.get()[-2:]
        risultato_codice_fiscale += month_code(month_option.get())
        if gender.get() == 0:    # Se il genere è maschile non sommare niente ai giorni, altrimenti se femmina si somma 40
            risultato_codice_fiscale += day.get()
        else:
            risultato_codice_fiscale += str(int(day.get()) + 40)
        risultato_codice_fiscale += is_locality_correct(locality.get())[1]
        for carattere_codice in range(0, len(risultato_codice_fiscale)):
            if carattere_codice % 2 == 0:
                control_number += dict_odd[risultato_codice_fiscale[carattere_codice]]
            else:
                control_number += dict_even[risultato_codice_fiscale[carattere_codice]]
        risultato_codice_fiscale+=str(control_letters[control_number%26])

# Copia il codice fiscale nella clipboard e lo mostra

        main_window.clipboard_clear()
        main_window.clipboard_append(risultato_codice_fiscale)


        risultato_codice_fiscale+=" Codice copiato! :)\n"
        risultato_codice_fiscale+= easter_egg2
        code.set(risultato_codice_fiscale)


#######################################################
# Creazione della finestra principale
#######################################################

main_window = Tk()
main_window.title("Calcolatore Codice Fiscale")



#######################################################
# Variabili dati anagrafici + risultato finale (code)
#######################################################

name = StringVar(main_window)
surname = StringVar(main_window)
locality = StringVar(main_window)
gender = IntVar(main_window)
year = StringVar(main_window)
month = StringVar(main_window)
day = StringVar(main_window)
code = StringVar(main_window)
num_tentativi = IntVar(main_window)
num_tentativi.set(0)
# Lista dei mesi




# Stile del layout

style_label = Style()
style_button = Style()
font_label =("Courier", 11, "bold")
font_button =("Courier", 11, "bold")
font_entry =("Courier", 11, "bold")
background_primary ="#c4e7f0"
color_button_active = ("active", "#5ba8d3")
color_button_inactive = ('!active','#5ba8d3')


# Configurazione dello stile dei vari elementi

style_label.configure('My.TLabel',background =background_primary, font = font_label)
style_button.configure('My.TButton', font = font_button, background ="#5ba8d3" )
style_button.map('My.TButton', background=[color_button_active, color_button_inactive])
main_window.configure(background=background_primary)

# Creazione dei Label per ogni campo da riempire

name_label = Label(main_window, text = "Nome:", style = 'My.TLabel')
surname_label = Label(main_window, text = "Cognome:", style = 'My.TLabel')
locality_label = Label(main_window, text = "Luogo di nascita:", style = 'My.TLabel')
gender_label = Label(main_window, text = "Genere:",  style = 'My.TLabel')
data_label = Label(main_window, text ="Data di nascita:", style = 'My.TLabel')

# Creazione del label per mostrare il codice fiscale risultante e/o messaggi di errore

code_label = Label(main_window, textvariable = code, style='My.TLabel')
code_label.configure(anchor="center")


# I campi veri e propri da riemprie

# 1 I campi testuali

name_entry = Entry(main_window, textvariable = name)
surname_entry = Entry(main_window, textvariable = surname)
locality_entry = Entry(main_window, textvariable = locality)
year_entry = Entry(main_window, textvariable = year, width=4)
day_entry = Entry(main_window, textvariable = day, width=2)

# 2 I campi a scelta (genere)

gender_M_radio = Radiobutton(main_window, text="M", variable = gender, value =0 )
gender_F_radio = Radiobutton(main_window, text="F", variable = gender, value =40)

# 3 I campi a tendina (mesi)

month_option = Combobox(main_window, values =month_list)

# 4 Il pulsante di calcolo

code_button = Button(main_window, text="Calcola", command=calcola_codice, style='My.TButton')

#######################################################
# Posizionamento dei vari campi e widget mediante una griglia
#######################################################

name_label.grid(row=0, column = 0, sticky=("WE"))
surname_label.grid(row=1, column = 0, sticky=("WE"))
locality_label.grid(row=2, column = 0, sticky=("WE"))
gender_label.grid(row=5, column = 0, sticky=("WE"))
data_label.grid(row=3, column = 0, sticky=("WE"))

#######################################################
# Posizionamento dei vari campi testuali
#######################################################

name_entry.grid(row=0, column = 2, columnspan=2, sticky="WE")
surname_entry.grid(row=1, column = 2, columnspan=2, sticky="WE")
locality_entry.grid(row=2, column = 2, columnspan=2, sticky="WE")
day_entry.grid(row =3, column = 1, sticky="W")
year_entry.grid(row = 3, column =3, sticky="W")

#######################################################
# Posizionamento del drop down menu dei mesi
#######################################################

month_option.grid(row= 3, column = 2, sticky="W")

#######################################################
# Posizionamento dei pulsanti per il genere
#######################################################

gender_M_radio.grid(row= 5, column = 1, sticky="E")
gender_F_radio.grid(row= 5, column = 2, sticky="W")

#######################################################
# Posizionamento del display di codice fiscale (o messaggi di errore)
#######################################################

code_label.grid(row = 8, column = 0, sticky="EW", columnspan = 4)

# Posizionamento del pulsante di calcolo del codice fiscale

code_button.grid(row = 6, column = 0, sticky="EW", columnspan = 4)

# Avvio del main loop della finestra principale: il processo ha inizio

main_window.mainloop()


