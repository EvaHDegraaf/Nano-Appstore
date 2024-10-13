import datetime
import random
import json
import os
from datetime import datetime

def Menu():
        print("\nWelkom bij het dagboek en nummerraadspel!")
        print("1: Dagboek openen")
        print("2: Nummerraadspel spelen")
        print("3: Afsluiten")
        
        keuze = input("Uw keuze: ").strip()

        match keuze:
            case "1":
                account()
            case "2":
                Nummerspel()
            case "3":
                print("Afsluiten, tot ziens!")
                return  
            case _:
                print("Ongeldige keuze, probeer opnieuw.")

def lees_dagboek():#r als in read om het dagboek te kunnen lezen
    with open('dagboek.json', 'r') as f:
        return json.load(f)
            
def schrijf_dagboek(dagboek):#opend het file om in te schrijven
    with open('dagboek.json', 'w') as f:
        json.dump(dagboek, f, indent=4)

def is_date_free(dagboek, datum):#check of de dag al bezet is
    return datum not in dagboek

def account():
    while True:
        print("\nHeeft u al een account? (type 1 of 2)")
        print("1. Ik heb al een account")
        print("2. Ik wil een account aanmaken")

        keuze = input("Uw keuze: ").strip()

        match keuze:#matched de input aan de cases waardoor je dingen kan doen
            case "1":
                login()
            case "2":
                registreren()
            case _:
                print("Ongeldige keuze, probeer opnieuw.")

def dagboek_keuze():
    while True:
        print("\nWilt u uw dagboek lezen of erin schrijven? (type 1 of 2)")
        print("1. Lezen")
        print("2. Schrijven")

        keuze = input("Uw keuze: ").strip()

        match keuze:
            case "1":
                dagboek = lees_dagboek()
                print(dagboek)  # Display the diary entries
            case "2":
                dagboek_entry()
            case _:
                print("Ongeldige keuze, probeer opnieuw.")

def login():#opend het passwordfile om te kijken of de gebruikersnaam en wachtwoord combinatie klopt door 'r'
    username = input("Voer je gebruikersnaam in: ")
    password = input("Voer je wachtwoord in: ")
    with open('password.txt', 'r') as f:
            users = f.readlines()

    for user in users:
        stored_username, stored_password = user.strip().split(':')
        if stored_username == username and stored_password == password:
            print("Login succesvol!")
            dagboek_keuze()
            return 

    print("Ongeldige gebruikersnaam of wachtwoord.")

def registreren():#zet de combienatie van gebruikersnaam en wachtwoord in het txtfile
    username = input("Voer je gebruikersnaam in: ")
    password = input("Voer je wachtwoord in: ")
    
    with open('password.txt', 'a') as f:
        f.write(f'{username}:{password}\n')
    print("Gebruiker succesvol geregistreerd!")
    login()

def dagboek_entry():
    dagboek = lees_dagboek()

    while True:
        vandaag = input("Wil je de tekst voor vandaag of een andere datum toevoegen? (vandaag/andere datum): ").strip().lower()
        if vandaag == 'vandaag':
            datum = datetime.now().strftime('%d-%m-%Y')
            break
        else:
            datum_input = input("Voer de datum in (DD-MM-yyyy): ")
            try:
                datum = datetime.strptime(datum_input, '%d-%m-%Y').strftime('%d-%m-%Y')
                break
            except ValueError:
                print("Ongeldige datum. Probeer het opnieuw.")

    if is_date_free(dagboek, datum):
        tekst = input("Voer je tekst in: ")
        dagboek[datum] = tekst
        print("Tekst toegevoegd.")
    else:
        print(f"Deze datum is al bezet. Huidige tekst: {dagboek[datum]}")
        keuze = input("Wil je de tekst herschrijven (h) of toevoegen (a)? (h/a): ").strip().lower()
        if keuze == 'h':
            tekst = input("Voer je nieuwe tekst in: ")
            dagboek[datum] = tekst
            print("Tekst herschreven.")
        elif keuze == 'a':
            tekst = input("Voer de extra tekst in: ")
            dagboek[datum] += "\n" + tekst
            print("Extra tekst toegevoegd.")
        else:
            print("Ongeldige keuze.")

    schrijf_dagboek(dagboek)

def Nummerspel():
    lower_bound = 1 
    upper_bound = 200
    max_attempts = 4
    num = random.randint(lower_bound, upper_bound) # het nummer dat geggenereerd word zit tussen het laagste en hoogste getal in

    for attempt in range(max_attempts):
        guess = input(f"Kies een nummer tussen de {lower_bound} en {upper_bound}: ")
        try:
            guess = int(guess)
            if guess == num:
                print("Goedzo, dat was je nummer! :D")
                return
            else:
                print("Nope, dat is fout")
        except ValueError:
            print("Voer een geldig nummer in.")
        
        remaining_attempts = max_attempts - attempt - 1
        print(f"{remaining_attempts} kansen over")

    print(f"Geen kansen meer over. Het juiste nummer was {num}.")
    
Menu()
