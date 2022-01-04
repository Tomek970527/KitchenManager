from typing import Sequence
import requests
from bs4 import BeautifulSoup
import pandas as pd
from difflib import SequenceMatcher
import datetime

class FoodManager():
    def __init__(self, *storages):
        self.session_object = requests.Session()
        self.food_type_source = "https://bonavita.pl/charakterystyka-12-grup-produktow-spozywczych-i-ich-znaczenie-dla-organizmu"
        self.food_macro_source = ["https://kalkulatorkalorii.net/tabela-kalorii/1/q-","item","?query=","item","&sc=Produkty"]
        self.food_categories = None
        self.category_components = None
        self.macro_dictionary = {}
        self.storages = storages

    def get_food_type(self):
        foodtest = input("Wprowadź produkt:")
        page = self.session_object.get(self.food_type_source)
        soup = BeautifulSoup(page.text, 'lxml')
        content = soup.find('div', itemprop='description')
        # print(content)
        if content != None:
            self.food_categories = [r.get_text() for r in content.select('h4')]
            all_components = [r.get_text() for r in content.select('ul li span')]
            self.category_components = {
                self.food_categories[0]: all_components[:2], 
                self.food_categories[1]: all_components[2:5], 
                self.food_categories[2]: all_components[5:11], 
                self.food_categories[3]: all_components[11:13],
                self.food_categories[4]: all_components[13:14],
                self.food_categories[5]: all_components[14:17],
                self.food_categories[6]: all_components[17:18],
                self.food_categories[7]: all_components[18:20],
                self.food_categories[8]: all_components[20:22],
                self.food_categories[9]: all_components[22:23],
                self.food_categories[10]: all_components[23:25],
                self.food_categories[11]: all_components[25:27]
            }

        for category, components in self.category_components.items():
            components_combined = ';'.join(components)
            if foodtest in components_combined:
                print(f'{foodtest.upper()} należy do grupy: {category}')


    def all_food_macro(self):
        source = "https://potrafiszschudnac.pl/diety/tabele-kalorycznosci-produktow/"
        page = self.session_object.get(source)
        soup = BeautifulSoup(page.text, 'lxml')
        content = soup.find('table', class_='prods_table')
        # print(content)
        if content != None:
            macro_table = [r.get_text() for r in content.select('tbody tr td')]
        counter = 0
        for item in macro_table:
            if counter == 0:
                temp_key = str(item)
                self.macro_dictionary[temp_key] = []
            elif 0 < counter < 4:
                self.macro_dictionary[temp_key].append(str(item))
            elif counter == 4:
                self.macro_dictionary[temp_key].append(str(item))
                counter = -1
            counter += 1
        # [kcal, białka, tłuszcze, węglowodany]
    
    def get_food_macro(self):
        foodtest = input("Wprowadź produkt:")
        keys_list = list(self.macro_dictionary)
        similarity = []
        user_satisfied = False
        try:
            print(self.macro_dictionary[foodtest])
        except:
            max_ratio_index = 0
            for key in self.macro_dictionary.keys():
                similarity.append(SequenceMatcher(a=foodtest, b=key).ratio())
                similarity_sorted = list(similarity)
                similarity_sorted.sort(reverse=True)  
            while not user_satisfied:
                print(f'Miałeś/Miałaś na myśli: {keys_list[similarity.index(similarity_sorted[max_ratio_index])]}')
                item = keys_list[similarity.index(similarity_sorted[max_ratio_index])]
                user_input = input("[TAK/NIE]: ")
                if user_input.lower() == "tak":
                    user_satisfied = True
                    print(f"\nWartości odżywcze (100g):\n")
                    print(f"kcal: {self.macro_dictionary[item][0]} | białko: {self.macro_dictionary[item][1]} | tłuszcz: {self.macro_dictionary[item][2]} | węglowodany {self.macro_dictionary[item][3]}")
                else:
                    max_ratio_index += 1

    # NEXT STEP AFTER ADDING FOOD DATA
    # AFTER EVERY "FOOD ADD" TO EACH STORAGE, RUN THIS FUNCTION TO GET NEW FOOD PRODUCTS
    def update_user_food_preference(self):
        storage_items_names = []
        updated_items = []
        for s in self.storages:
            storage_items = None
            storage_items = pd.read_excel(s)
            for i in range(storage_items.shape[0]):
                storage_items_names.append(storage_items.at[i, 'name'])
        try:
            food_list = pd.read_excel("FoodList.xlsx")
            for i in range(food_list.shape[0]):
                updated_items.append(food_list.at[i, 'name'])
            for item in storage_items_names:
                found = False
                for i in range(food_list.shape[0]):
                    if food_list.at[i, 'name'] == item:
                        found = True
                if not found:
                    updated_items.append(item)
            food_items = pd.DataFrame({
                "name": updated_items,
            })
            file_name = "FoodList.xlsx"
            food_items.to_excel(file_name)
        except FileNotFoundError:
            s = set(storage_items_names)
            food_items = pd.DataFrame({
                "name": list(s),
            })
            file_name = "FoodList.xlsx"
            food_items.to_excel(file_name)
        
        

    def create_shopping_list(self):
        pass

    def divide_food(self, category):
        # RELAYS ON THE get_food_type() AND (Fridge.food_list OR Cupboard.food_list)
        pass

    def main(self):
        pass

# food that requires refrigeration
class Fridge():
    def __init__(self, food_names = [], food_expire_dates = [], food_quantity = []):
        self.food_names = food_names
        self.food_expire_dates = food_expire_dates
        self.food_quantity = food_quantity
        self.done_adding = False
        self.file_updated = False
        self.food_items = None

    def __str__(self):
        return f'{self.food_list}'

    def add_food(self):
        result = lambda x: True if x.upper() == "TAK" else False
        if not self.done_adding and not self.file_updated:
            print("Dodaj produkt z Twojej lodówki.")
            self.food_names.append(input("Nazwa: "))
            temp_quantity = input("Ilość: ")
            self.food_quantity.append(temp_quantity)
            temp_expire_date = []
            for i in range(int(temp_quantity)):
                temp_expire_date.append(input(f"Data ważności {i + 1}: "))
            self.food_expire_dates.append(';'.join(temp_expire_date))
            self.done_adding = result(input("Kończymy na dziś? [TAK/NIE]: "))
        elif self.done_adding and not self.file_updated:
            self.food_items = pd.DataFrame({
                "name": self.food_names,
                "quantity": self.food_quantity,
                "expire_date": self.food_expire_dates,
            })
            # get item form pd.DataFrame
            # print(food_items.at[0, 'name'])
            file_name = "Fridge.xlsx"
            self.food_items.to_excel(file_name)
            self.file_updated = True

    def find_product(self, name):
        # Find particualar item in your fridge...
        # Didn't find anything? Check your cupboard...
        self.food_items = None
        self.food_items = pd.read_excel('Fridge.xlsx')
        for i in range(self.food_items.shape[0]):
            if name in self.food_items.at[i, 'name']:
                print(f"Aktualnie w Twojej lodówce znajduję/ą się {self.food_items.at[i, 'quantity']} sztuka/i.")
            else:
                print("Niestety w Twojej lodówce nie ma takiego produktu.")

    def check_expire_date(self):
        # 2 categories:
        # - expired
        # - equal or less than 3 days to expire
        pass

    def main(self):
        # while not self.file_updated:
        #     self.add_food()
        self.find_product("masło")

# food that doesn't require refrigeration
class Cupboard():
    def __init__(self, food_names = [], food_expire_dates = [], food_quantity = []):
        self.food_names = food_names
        self.food_expire_dates = food_expire_dates
        self.food_quantity = food_quantity
        self.done_adding = False
        self.file_updated = False
        self.food_items = None

    def __str__(self):
        return f'{self.food_list}'

    def add_food(self):
        result = lambda x: True if x == "TAK" else False
        if not self.done_adding and not self.file_updated:
            print("Dodaj produkt z poza Twojej lodówki.")
            self.food_names.append(input("Nazwa: "))
            self.food_expire_dates.append(input("Data ważności: "))
            self.done_adding = result(input("Kończymy na dziś? [TAK/NIE]: "))
        elif self.done_adding and not self.file_updated:
            self.food_items = pd.DataFrame({
                "name": self.food_names,
                "quantity": self.food_quantity,
                "expire_date": self.food_expire_dates,
            })
            file_name = "Cupboard.xlsx"
            self.food_items.to_excel(file_name)
            self.file_updated = True
        

    def find_product(self, name):
        self.food_items = None
        self.food_items = pd.read_excel('Fridge.xlsx')
        for i in range(self.food_items.shape[0]):
            if name in self.food_items.at[i, 'name']:
                print(f"Aktualnie w Twojej lodówce znajduję/ą się {self.food_items.at[i, 'quantity']} sztuka/i.")
            else:
                print("Niestety w Twojej lodówce nie ma takiego produktu.")

    def check_expire_date(self):
        pass

    def main(self):
        while not self.file_updated:
            self.add_food()


class ShoppingCosts():
    def __init__(self):
        pass

    def read_receipt_photo(self):
        pass

    def enter_prices_manually(self):
        pass

    def main(self):
        pass


## TESTING

f1 = FoodManager("Cupboard.xlsx", "Fridge.xlsx")
# f1.get_food_type()
# f1.get_food_macro()
f1.update_user_food_preference()

# c1 = Cupboard()
# c1.main()

# fr1 = Fridge()
# fr1.main()
