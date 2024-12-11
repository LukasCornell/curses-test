'''
main.py: en meny man navigerar med piltangenterna. 

__author__  = "Lukas Cornell"
__version__ = "2.0.0"
__email__   = "lukas.cornell@elev.ga.ntig.se"
'''



import curses
import csv
import os
from time import sleep
import uuid
import locale
import random

text1 = """ ____            _      _    _             _                          
|  _ \ _ __ ___ (_) ___| | _| |_          | |    __ _  __ _  ___ _ __ 
| |_) | '__/ _ \| |/ _ \ |/ / __|  _____  | |   / _` |/ _` |/ _ \ '__|
|  __/| | | (_) | |  __/   <| |_  |_____| | |__| (_| | (_| |  __/ |   
|_|   |_|  \___// |\___|_|\_\\__|          |_____\__,_|\__, |\___|_|   
              |__/                                    |___/           """


text2 = """  _ \              _)        |     |              
 |   |   __|  _ \   |   _ \  |  /  __|            
 ___/   |    (   |  |   __/    <   |        _____|
_|     _|   \___/   | \___| _|\_\ \__|            
 |              ___/                              
 |       _` |   _` |   _ \   __|                  
 |      (   |  (   |   __/  |                     
_____| \__,_| \__, | \___| _|                     
              |___/     """


text3 = """
██████╗ ██████╗  ██████╗      ██╗███████╗██╗  ██╗████████╗          
██╔══██╗██╔══██╗██╔═══██╗     ██║██╔════╝██║ ██╔╝╚══██╔══╝          
██████╔╝██████╔╝██║   ██║     ██║█████╗  █████╔╝    ██║       █████╗
██╔═══╝ ██╔══██╗██║   ██║██   ██║██╔══╝  ██╔═██╗    ██║       ╚════╝
██║     ██║  ██║╚██████╔╝╚█████╔╝███████╗██║  ██╗   ██║             
╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝             
                                                                    
██╗      █████╗  ██████╗ ███████╗██████╗                            
██║     ██╔══██╗██╔════╝ ██╔════╝██╔══██╗                           
██║     ███████║██║  ███╗█████╗  ██████╔╝                           
██║     ██╔══██║██║   ██║██╔══╝  ██╔══██╗                           
███████╗██║  ██║╚██████╔╝███████╗██║  ██║                           
╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝                           
"""
# Set the locale to a supported one, e.g., 'en_US.UTF-8'
try:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')  # or another suitable locale
except locale.Error:
    print("Locale not supported, using default format.")

texts = [text1, text2, text3]
text = random.choice(texts)



def start_screen():
  

  lines = text.splitlines()
  num_layers = len(lines)

  for layer in range(num_layers):
        print(lines[layer])
        sleep(0.2)

  sleep(1)





class bcolors:
    #ANSI escape sequences for terminal text formatting.

    RED = '\033[91m'
    ORANGE = '\033[48'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    DEFAULT = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



def load_data(filename): 
    products = [] 
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                id = int(row['id'])
                name = row['name'][:35] 
                desc = row['desc'][:70]
                price = float(row['price'])
                quantity = int(row['quantity'])

                products.append(        #list
                    {                    #dictionary
                        "id": id,       
                        "name": name,
                        "desc": desc,
                        "price": price,
                        "quantity": quantity
                    }
                )
    except ValueError:
        print("Kan inte hitta filen")
        sleep(1)
    
    return products




start_screen()  #startar animationen i början

os.system('cls')



def create_inventory(products):
    # skapa sidhuvudet av tabellen:
    header = (f"{'#':<6} {'NAMN':<35} {'BESKRIVNING':<70} {'PRIS':<14} {'KVANTITET':<10}")  #avstånd mellan delarna i header
    # rader för varje produkt:
    rows = []
    rows.append(header) #lägger till header i listan

    for index, product in enumerate(products, 1):
        name = product['name'][:35] #så de inte blir för långa
        desc = product['desc'][:70]
        price = product['price']
        quantity = product['quantity']
        
        price = locale.currency(price, grouping=True)
        row = f"{index:<6} {name:<35} {desc:<70} {price:<14} {quantity:<10}"

        rows.append(row)

    
    
    return rows 

products = load_data('test.csv')    #laddar in info från csv-filen


def save_info(products):    #sparar informationen och updaterar listan
    csv_file_path = "test.csv"

        # skriv produkterna till csv-filen
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["id", "name", "desc", "price", "quantity"])
        writer.writeheader()  
        writer.writerows(products)
    
    print(f"Data successfully saved to {csv_file_path}")
    sleep(1)

    os.system('cls')


def delete_product(current_index):  #ta bort-funktionen 
    temp_product = None

    for product in products:
        if product["id"] == current_index:
            temp_product = product
            break  # Avsluta loopen så snart produkten hittas

    if temp_product:
        products.remove(temp_product)
        return f"Product: {current_index} {temp_product['name']} was removed"
    else:
        return f"Product with id {current_index} not found"
    




def add_product(products, name, desc, price, quantity): #lägg till
    #få rätt nummer
    max_id = max(products, key = lambda x: x['id'])

    new_id = max_id['id'] + 1

    #skapar den nya produkten
    new_product = {                    
        "id": new_id,       
        "name": name,
        "desc": desc,
        "price": price,
        "quantity": quantity
    }
    products.append(new_product)

    with open('test.csv','a') as fd:
        fd.write(f"\n{new_id},{name},{desc},{price},{quantity}")

    return f"Du lade till {name}, id = {new_id}"






def change_product(products, current_index, new_id, new_name, new_desc, new_price, new_quantity):   #förändra
    #Listar ut vilken produkt som ska ändras
    product_to_edit = next((product for product in products if product['id'] == current_index), None)

    #ändrar all info
    if product_to_edit:
        product_to_edit['id'] = new_id
        product_to_edit['name'] = new_name
        product_to_edit['desc'] = new_desc
        product_to_edit['price'] = new_price
        product_to_edit['quantity'] = new_quantity
        return f"Product with ID {current_index} has been updated successfully."
    else:
        return f"Error: Product with ID {current_index} not found."




def product_menu(curses_rows, current_index, stdscr):#many för produkten
    curses.curs_set(0)
    stdscr.keypad(True)
    def print_product_menu():
        stdscr.addstr(f"{current_index}")
        stdscr.addstr(0,0,f" ← Edit, ↑ Add product , → Delete, ↓ Exit\n\n[Use Arrow Keys]") #meny
    while True:
        print_product_menu()
        key = stdscr.getch()

        if key == 450:
            choice = "Add"
            break
        elif key == 452:
            choice = "Edit"
            break
        elif key == 454:
            choice = "Delete"
            break
        elif key == 456:
            choice = "Exit"
            break
           
    stdscr.clear()
    stdscr.addstr(0, 0, f"You selected {choice}\nPRESS ANY KEY TO CONTINUE")
    stdscr.refresh()
    stdscr.getch()  # Wait for another key press to continue
    stdscr.clear()

    if choice == 'Add':
        stdscr.refresh()
        stdscr.keypad(False)
        curses.endwin() 
        try:
            name = input("Namn: ")
            desc = input("Beskrivning: ")
            price = float(input("Pris: "))
            quantity = int(input("Kvantitet: "))
            print(add_product(products, name, desc, price, quantity))
            curses.curs_set(0)
            stdscr.keypad(True)
        except ValueError:
            print("Invalid input. Please try again.")
            sleep(1)

    elif choice == 'Edit':
        stdscr.refresh()
        stdscr.keypad(False)
        curses.endwin() 

        try:
            new_id = current_index
            new_name = input("Nytt namn: ")
            new_desc = input("Ny beskrivning: ")
            new_price = float(input("Nytt pris: "))
            new_quantity = int(input("Ny kvantitet: "))
            print(change_product(products, current_index, new_id, new_name, new_desc, new_price, new_quantity))
            save_info(products)
            curses.curs_set(0)
            stdscr.keypad(True)
        except ValueError:
            print("Invalid input. Please try again.")
            sleep(1)


    elif choice == 'Delete':
        stdscr.addstr(delete_product(current_index))
        stdscr.refresh()
        save_info(products)

    

    
    



    
curses_rows = create_inventory(products)
chosen_product = ""
# current_id = 0


def draw_menu(stdscr):

    curses.curs_set(0)  
    stdscr.keypad(True) #startar curses

    current_index = 1  # så att den börjar vid första produkten och inte headern

    def print_menu():   #Skapar menyn med rätt dimensioner
        curses_rows = create_inventory(products)
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        for idx, item in enumerate(curses_rows):    #skapar nummer för alla produkter
            x = w // 2 - len(item) // 2 #ser till att raderna blir rätt längder
            y = idx
            if idx == current_index:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, item)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, item)
        stdscr.refresh()

    #Fixar färgerna
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Loopen som kollar vilka tangenter man trycker på
    while True:
        print_menu()
        key = stdscr.getch()

        if key == 450 and current_index > 1:  # ser till att man inte kan gå utanför listan
            current_index -= 1
        elif key == 456 and current_index < len(curses_rows) - 1:
            current_index += 1
        elif key == ord('\n'):  # "Enter" tangenten
            if current_index == 0:  # Om man väljer header så händer inget
                continue
           
            stdscr.clear()
            stdscr.addstr(0, 0, f"You selected {curses_rows[current_index]}\nPRESS ANY KEY TO CONTINUE")
            stdscr.refresh()
            stdscr.getch()  # vänta på nästa tryck
            stdscr.clear()
            product_menu(curses_rows, current_index, stdscr)    #skickar all info till produktmenyn

curses.wrapper(draw_menu)

