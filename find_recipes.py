import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import concurrent.futures

class RecipeFinder():
    def __init__(self, **kwargs):
        self.search = kwargs.values()
        self.all_titles = []
        self.all_links = []
        self.all_ranks = []
        self.all_num_of_comments = []
        self.links_filtered = []
        self.all_ingredients = []
        self.urls = []
        self.all_content = []
        self.recipes = None
        self.base = "https://www.kwestiasmaku.com"
        self.max_threads = 100
        self.search_url = "/szukaj?search_api_views_fulltext="
        self.session_object = requests.Session()


    def check_ingredients(self, source):
        page = self.session_object.get(source)
        soup = BeautifulSoup(page.text, 'lxml')
        content = soup.find('div', class_='field field-name-field-skladniki field-type-text-long field-label-hidden')
        # print(content)
        if content != None:
            ingredients = [r.get_text() for r in content.select('li')]
            found_ingredient = True
            temp = ';'.join(ingredients)
            temp = temp.replace("\n","")
            combined_ingredients = temp.replace("\t","")
            # print(combined_ingredients)
            if ingredients:
                for s in self.search:
                    if s in combined_ingredients:
                        self.links_filtered.append(source)
                        self.all_ingredients.append(combined_ingredients)
                        # print(self.links_filtered


    def check_url(self, i):
        if i == 0:
            source = self.base + self.search_url
        else:
            source = self.base + self.search_url + "&page=" + str(i)
        page = self.session_object.get(source)
        # page = requests.get(source)
        soup = BeautifulSoup(page.text, 'lxml')
        content = soup.find('div', class_='view-content')
        if content != None:
            self.urls.append(source) 
            self.all_content.append(content)


    def download_urls(self):
        # i = 0
        for index, item in enumerate(self.search):
            if index == 0:
                self.search_url += item
            else:
                break

        numbers = [x for x in range(100)]

        threads = len(numbers)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(self.check_url, numbers)

        all_urls = pd.DataFrame({
           "links": self.urls
        })

        file_name = "URLs.xlsx"
        all_urls.to_excel(file_name)


    def find_recipes_in_url(self, content):
        titles = [r.get_text() for r in content.select('.field-name-title a')]
        links = [self.base + r['href'] for r in content.select('.field-type-image a')]
        # ranks = [r["data-average-stars"] for r in content.select('.fivestar-static-item .fivestar-widget-wrapper')]
        # num_of_comments = [r.get_text() for r in content.select('.fivestar-summary-wrapper .fivestar_votes_count')]

        for i in range(len(titles)):
            self.all_titles.append(titles[i])
            self.all_links.append(links[i])
            # self.all_ranks.append(ranks[i])
            # self.all_num_of_comments.append(num_of_comments[i])


    def download_recipes(self):
        threads = min(self.max_threads, len(self.all_content))

        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(self.find_recipes_in_url, self.all_content)


    def download_ingredients(self):
        threads = len(self.all_links)

        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(self.check_ingredients, self.all_links)


    def main(self):

        t0 = time.time()
        self.download_urls()
        t1 = time.time()
        self.download_recipes()
        t2 = time.time()
        self.download_ingredients()
        t3 = time.time()

        recipes = pd.DataFrame({
            "title": self.all_titles,
            "link": self.all_links,
            # "rank": self.all_ranks,
            # "num_of_comments": self.all_num_of_comments
        })

        ingredients = pd.DataFrame({
            "link": self.links_filtered,
            "ingredients": self.all_ingredients,
        })

        file_name = "Recipes.xlsx"
        recipes.to_excel(file_name)
        file_name = "Ingredients.xlsx"
        ingredients.to_excel(file_name)
        print("Done")
        print(t1-t0)
        print(t2-t1)
        print(t3-t2)
        # [title, link, rank, num_of_comments]

k = RecipeFinder(main="makaron", additional1="śmietanka")
k.main()