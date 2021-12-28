from typing import Sequence
import requests
from bs4 import BeautifulSoup
import pandas as pd
from difflib import SequenceMatcher

class FoodManager():
    def __init__(self):
        self.session_object = requests.Session()
        self.food_type_source = "https://bonavita.pl/charakterystyka-12-grup-produktow-spozywczych-i-ich-znaczenie-dla-organizmu"
        self.food_macro_source = ["https://kalkulatorkalorii.net/tabela-kalorii/1/q-","item","?query=","item","&sc=Produkty"]
        self.food_categories = None
        self.category_components = None

    def get_food_type(self):
        foodtest = "szpinak"
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


    def get_food_macro(self):

        foodtest = input("Wprowadź produkt:")
        source = "https://potrafiszschudnac.pl/diety/tabele-kalorycznosci-produktow/"
        page = self.session_object.get(source)
        soup = BeautifulSoup(page.text, 'lxml')
        content = soup.find('table', class_='prods_table')
        # print(content)
        if content != None:
            macro_table = [r.get_text() for r in content.select('tbody tr td')]
        counter = 0
        macro_dictionary = {}
        for item in macro_table:
            if counter == 0:
                temp_key = str(item)
                macro_dictionary[temp_key] = []
            elif 0 < counter < 4:
                macro_dictionary[temp_key].append(str(item))
            elif counter == 4:
                macro_dictionary[temp_key].append(str(item))
                counter = -1
            counter += 1
        # [kcal, białka, tłuszcze, węglowodany]
        keys_list = list(macro_dictionary)
        similarity = []
        user_satisfied = False
        try:
            print(macro_dictionary[foodtest])
        except:
            max_ratio_index = 0
            for key in macro_dictionary.keys():
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
                    print(f"kcal: {macro_dictionary[item][0]} | białko: {macro_dictionary[item][1]} | tłuszcz: {macro_dictionary[item][2]} | węglowodany {macro_dictionary[item][3]}")
                else:
                    max_ratio_index += 1


    def get_user_food_preference(self):
        pass

    def create_shopping_list(self):
        pass

    def divide_food(self, category):
        pass


# food that requires refrigeration
class Fridge():
    def __init__(self, food_list = []):
        self.food_list = food_list

    def __str__(self):
        pass

    def find_product(self, name):
        pass

# food that doesn't require refrigeration
class Cupboard():
    def __init__(self, food_list = []):
        self.food_list = food_list

    def __str__(self):
        pass

    def find_product(self, name):
        pass


## TESTING

f1 = FoodManager()
# f1.get_food_type()
f1.get_food_macro()