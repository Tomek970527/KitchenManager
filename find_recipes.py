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

    '''
    # ALGORITHM TO FIND SIMILAR WORDS (NOT ONLY THE SAME) IN INGREDIENTS STRING
    def KMPSearch(self, pattern, txt):
        M = len(pattern)
        N = len(txt)

        lps = [0]*M
        j = 0 
        self.computeLPSArray(pattern, M, lps)
  
        i = 0 # index for txt[]
        while i < N:
            if pattern[j] == txt[i]:
                i += 1
                j += 1
    
            if j == M:
                # print "Found pattern at index " + str(i-j)
                j = lps[j-1]
    
            # mismatch after j matches
            elif i < N and pattern[j] != txt[i]:
                # Do not match lps[0..lps[j-1]] characters,
                # they will match anyway
                if j != 0:
                    j = lps[j-1]
                else:
                    i += 1

    
    def computeLPSArray(self, pattern, M, lps):
        len = 0

        lps[0] = 0
        i = 1

        while i < M:
            if pattern[i]== pattern[len]:
                len += 1
                lps[i] = len
                i += 1
            else:
                # This is tricky. Consider the example.
                # AAACAAAA and i = 7. The idea is similar 
                # to search step.
                if len != 0:
                    len = lps[len-1]
    
                    # Also, note that we do not increment i here
                else:
                    lps[i] = 0
                    i += 1
    '''


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
                # KMP Algorithm
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

    # def new_check_url(self, num):
    #     if num == 0:
    #         source = self.base + self.search_url
    #         source_plus_one = self.base + self.search_url + "&page=1"
    #     else:
    #         source = self.base + self.search_url + "&page=" + str(num)
    #         source_plus_one = self.base + self.search_url + "&page=" + str(num + 1)

    #     page = self.session_object.get(source)
    #     page_plus_one = self.session_object.get(source_plus_one)
    #     soup = BeautifulSoup(page.text, 'lxml')
    #     soup_plus_one = BeautifulSoup(page_plus_one.text, 'lxml')
    #     content = soup.find('div', class_='view-content')
    #     content_plus_one = soup_plus_one.find('div', class_='view-content')

    #     if content != None and content_plus_one == None:
    #         return num
    #     elif content == None:
    #         num -= num // 2
    #         return self.new_check_url(num)
    #     elif content != None and content_plus_one != None:
    #         num += num // 2
    #         return self.new_check_url(num)

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

        # self.last_page = self.new_check_url(100)
        # print(self.last_page)
        # self.urls = [self.base + self.search_url + "&page=" + str(i) if i != 0 else self.base + self.search_url for i in range(self.last_page + 1)]
        # print(self.urls)

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

'''
# FINDING THE LAST PAGE USING RECURSION AND SOME KIND OF BINARY SEARCH
def test(num, session_object):
        search_url = "/szukaj?search_api_views_fulltext=kurczak"
        base = "https://www.kwestiasmaku.com"

        if num == 0:
            source = base + search_url
            source_plus_one = base + search_url + "&page=1"
        else:
            source = base + search_url + "&page=" + str(num)
            source_plus_one = base + search_url + "&page=" + str(num + 1)

        page = session_object.get(source)
        page_plus_one = session_object.get(source_plus_one)
        soup = BeautifulSoup(page.text, 'lxml')
        soup_plus_one = BeautifulSoup(page_plus_one.text, 'lxml')
        content = soup.find('div', class_='view-content')
        content_plus_one = soup_plus_one.find('div', class_='view-content')

        if content != None and content_plus_one == None:
            print(f'This is the final page: {num}')
            return num
        elif content == None:
            num -= num // 2
            print('Test')
            return test(num, session_object)
        elif content != None and content_plus_one != None:
            num += num // 2
            return test(num, session_object)
    
def find_last_page():
    max_page = 100
    # found = False
    session_object = requests.Session()
    # result = test(max_page, session_object)
    print(test(max_page, session_object))
    # while not found:
    #     if test(max_page, session_object):
    #         prev_max = max_page
    #         max_page += 1.5 * max_page 
    #     else:
    #         diff = (max_page - prev_max) // 2
    #         prev_max = max_page
    #         max_page -= diff

find_last_page()
'''