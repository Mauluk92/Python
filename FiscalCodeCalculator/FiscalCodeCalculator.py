from calendar import monthrange
import re
import Levenshtein as lev
import unidecode
import datetime

class FiscalCodeCalculator():
    def __init__(self, list_inputs):
        self.fiscal_code = self.code_calc(list_inputs)
    # Necessary attributes for fiscal code calculation 
    
    fiscal_code = ""
    
    month_list =("Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
"Luglio", "Agosto", "Settembre", "Ottombre", "Novembre", "Dicembre")
    current_date_time = datetime.datetime.now()
    current_year = int(current_date_time.strftime("%Y"))
    
    month_id = ["A", "B", "C", "D", "E", "H", "L", "M", "P", "R", "S", "T"]

    numbers_month = [1,2,3,4,5,6,7,8,9,10,11,12]

    month_list_upper_case = list(map(lambda x:x.upper(), month_list))

    dict_month_to_numbers = dict(zip(month_list_upper_case, numbers_month))
    
    # Error log dictionary:

    error_log= {True: "",
                False: "Alcuni campi sono vuoti!",
                "NomeERR": "Il nome è digitato incorrettamente!\n",
                "CognomeERR": "Il cognome è digitato incorrettamente!\n",
                "DayERR": "Il giorno è digitato incorrettamente!\n",
                "YearERR": "L'anno è digitato incorrettamente!\n",
                "LocalityERR": "La località è digitata incorrettamente!\n",
                "DayOUT_OF_RANGE_ERR": "Il giorno non è compreso nel mese!\n",
                "MonthERR": "Il mese è digitato incorrettamente!\n",
                "LocalityNOTFOUND_ERR": "La località non è stata trovata!\n",}

    # Attributes for the control character of fiscal code
    control_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    keys = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    value_odd = [1,0,5,7,9,13,15,17,19,21,1,0,5,7,9,13,15,17,19,21,2,4,18,20,11,3,6,8,12,14,16,10,22,25,24,23]
    value_even =[0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
    dict_odd = dict(zip(keys, value_odd))
    dict_even = dict(zip(keys, value_even))
    # Methods
    ## Method of preformatting inputs:

    def pre_formatting_name(self, aName):
        return aName.strip().replace(" ", "").replace("'","").upper()
    def pre_formatting_date(self, aDate):
        return aDate.strip().replace(" ", "")
    def pre_formatting_locality(self, aLocality):
        return aLocality.strip().upper().replace(" ", "")
    def is_empty(self, input_fiscal):
        if not input_fiscal:
            return False
        else:
            return True

    ## Methods of validating inputs against regexp:

    def is_name_correct(self,aName):
        aName = self.pre_formatting_name(aName)
        pattern_aName = "^([A-Z]|\'|[ÀÈÌÒÙY])+$"
        if re.match(pattern_aName, aName):
            return True
        else:
            return "NomeERR"
    def is_surname_correct(self,aSurname):
        aSurname = self.pre_formatting_name(aSurname)
        pattern_aSurname = "^([A-Z]|\'|[ÀÈÌÒÙY])+$"
        if re.match(pattern_aSurname, aSurname):
            return True
        else:
            return "CognomeERR"

    def is_day_correct(self,aDay):
        aDay = self.pre_formatting_date(aDay)
        pattern_aDay ="^\d\d$"   
        if re.match(pattern_aDay, aDay):
            return True
        else:
            return "DayERR"
    def is_year_correct(self,aYear):
        aYear=self.pre_formatting_date(aYear)
        pattern_aYear ="^\d\d\d\d$"   
        if re.match(pattern_aYear, aYear):
            return True
        else:
            return "YearERR"
    def is_locality_correct(self,aLocality):
        aLocality = self.pre_formatting_locality(aLocality)
        pattern_aLocality="^([A-Z]|\D|\')+$"
        aLocality_code = ""
        if re.match(pattern_aLocality, aLocality):
            return True
        else:
            return "LocalityERR"
    def is_month_correct(self, aMonth):
        if aMonth.upper() in self.month_list_upper_case:
            return True
        else:
            return "MonthERR"
    # Check for day within range

    def is_day_within_range(self, aDay, aMonth, aYear):
        aMonth_number = self.dict_month_to_numbers[aMonth.upper()]
        if 1 <= int(aDay) <= monthrange(int(aYear), aMonth_number)[1]: 
            return True
        else:
            return "DayOUT_OF_RANGE_ERR"

    # Method for best-match locality

    def best_match_locality(self, aLocality):
        aLocality = self.pre_formatting_locality(aLocality)
        file = open("codice_catastale.txt", "r")
        best_match=""
        match=""
        codex=""
        while True:
            line = file.readline().strip()
            if not line:
                break
            loc_code = line.split(";")
            match = loc_code[0]
            distance_match = lev.jaro_winkler(aLocality, match)
            best = lev.jaro_winkler(best_match, aLocality)
            if distance_match > 0.8 and distance_match >best:
                best_match = match
                codex = loc_code[1]
        if not best_match:
            return "LocalityNOTFOUND_ERR"
        else:
            return best_match, codex

    # Methods of fiscal code characters processing

    def is_double_letter(self, aName):
        aName = self.pre_formatting_name(aName)
        double_letters = []
        for index_char in range(len(aName)-1):
            if aName[index_char] == aName[index_char +1]:
                double_letters.append(aName[index_char])
        return double_letters

    def name_surname_code(self, aName):
        aName_code = ""
        aName = self.pre_formatting_name(aName)
        aName = unidecode.unidecode(aName)
        vowel_list = ["A", "E", "I", "O", "U", "Y"]
        vowels = []
        consonants = []
        double_letters = self.is_double_letter(aName)
        for char in aName:
            if char not in vowel_list:
                consonants.append(char)
            else:
                vowels.append(char)
        vowels = vowels + ["X", "X"]
        consonants_vowels = consonants + vowels
        while len(aName_code) < 3:
            if (consonants_vowels[0] in double_letters) and len(set(consonants))>2:
                consonants_vowels.pop(0)
            aName_code += consonants_vowels[0]
            consonants_vowels.pop(0)
        return aName_code


    def month_code(self,aMonth):
        aMonth = aMonth.upper()
        return self.month_id[self.dict_month_to_numbers[aMonth]-1]
    def day_code(self,aDay):
        return aDay
    def year_code(self, aYear):
        return aYear[-2:]
    def locality_code(self, aLocality):
        return self.best_match_locality(aLocality)[1]
        
    # Actual method for calculating the characters of the fiscal code

    def code_calc(self, list_inputs ):   # list_inputs= [aSurname, aName,aYear, aMonth, aDay, aLocality, aGender]
        func_errors = [self.is_surname_correct, self.is_name_correct,self.is_year_correct, self.is_month_correct, self.is_day_correct, self.is_locality_correct]
    # list of functions to calculate fiscal code:
        errors = "" 
        func_calc = [self.name_surname_code, self.name_surname_code,self.year_code, self.month_code, self.day_code, self.locality_code]

        resulting_code = ""
        control_number = 0
        for elements in list_inputs[:-1]:
            if not self.is_empty(elements):
                return self.error_log[self.is_empty(elements)]
        # Checking for errors:
        for elements, func in zip(list_inputs[:-1], func_errors):
            errors += self.error_log[func(elements)]
        # Checking for secondary errors:
        if not errors:
            errors += self.error_log[self.is_day_within_range(list_inputs[4], list_inputs[3], list_inputs[2])]
            if self.best_match_locality(list_inputs[5]) == "LocalityNOTFOUND_ERR":
                errors += self.error_log["LocalityNOTFOUND_ERR"]
        if errors:
            return errors
        else:
            if list_inputs[-1] == 40:
                    list_inputs[4] = str(int(list_inputs[4] + 40))
            for elements, func in zip(list_inputs[:-1], func_calc):
                resulting_code += func(elements)
            for char_index in range(len(resulting_code)):
                if char_index %2 == 0:
                    control_number += self.dict_odd[resulting_code[char_index]]
                else:
                    control_number += self.dict_even[resulting_code[char_index]]
            resulting_code += str(self.control_letters[control_number%26])
            return resulting_code

