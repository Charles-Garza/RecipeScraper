#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import time
import csv
import re
import sys

title = ' '
rows = []
i = 1
count = 0
url = "https://www.allrecipes.com/recipes/17562/dinner/?page="

while (title != ''): 
    response = requests.get(url + str(i))
    html = response.content

    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all(class_='fixed-recipe-card'):
        recipeLink = link.find('a')
        recipeLink = recipeLink['href']
        recipeResponse = requests.get(recipeLink)
        recipeHtml = recipeResponse.content
        recipeSoup = BeautifulSoup(recipeHtml, 'html.parser')
         
        #print(recipeLink)
        img = link.find(class_='fixed-recipe-card__img')['data-original-src']
        title = link.find(class_='fixed-recipe-card__title-link').get_text().strip() 
        description = link.find(class_='fixed-recipe-card__description')
        #stars = recipeSoup.find(class_='stars stars-5')
        #rating = stars["data-ratingstars"]
         
        ingredients = re.sub(r'\n\s*\n', r'\n', recipeSoup.find(class_="checklist dropdownwrapper list-ingredients-1").get_text().strip(), flags=re.M)
        img = re.sub(r'\/media*\/', r'', img) 
        
        sys.stdout.write("INSERT INTO food_recipe_recipe (recipe_image, recipe_name, ")
        sys.stdout.write("recipe_content, date_posted, recipe_author_id) VALUES (")
        sys.stdout.write("\'" + str(img) + "\',\'" + title + "\',\'")
        sys.stdout.write(str(description.get_text()) + ingredients + "\'")
        sys.stdout.write(", \'2019-04-16 00:00:00\', \'2\');\n")
        #print(ingredients) 

        ''' 
        img = link.find(class_='fixed-recipe-card__img')
        if img:
            img = img['data-original-src']
        else:
            img = ''
        name = link.find('h3').get_text().strip()
        title = str(name)
        description = link.find(class_='fixed-recipe-card__description')
        description = description.get_text().strip()
        rows.append([name, description, rating, img])
        '''

    if not soup.find_all(class_='fixed-recipe-card'):
        break
        
    i = i + 1
    print(title)
    time.sleep(3)

with open("recipes.csv", "w+") as outfile:
    writer = csv.writer(outfile)
    headers = ['Title', 'Description', 'Img']
    writer.writerow(headers)
    for row in rows:
        writer.writerows([row])

