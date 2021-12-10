from . import models
from django.shortcuts import render
from bs4 import BeautifulSoup
# from requests.compat import quote_plus
from urllib.parse import quote_plus

import requests

# Create your views here.

BASE_CRAIGSLIST_URL = 'https://losangeles.craigslist.org/d/for-sale/search/sss?query={}'
#'https://losangeles.craigslist.org/d/services/search/bbb?query={}'
#'https://www.jumia.co.ke/{}'
#'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw=iphone+x&_sacat=0'


def base(request):
    return render(request, 'base.html')


def new_search(request):
   #response = requests.get('https://losangeles.craigslist.ponseorg/d/services/search/bbb?query=python%20tutor')
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    print(search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    print(final_url)
    response = requests.get(final_url)
    data = response.text
    #print(data)
    soup = BeautifulSoup(data, features='html.parser')
    post_title = soup.find_all('a', {'class': 'result-title'})
    # printing every title with the link title of result-title
    #print(post_title)
    #printing only title index of zero
    #print(post_title[0].text) #this spits out the text in the title
    #getting the link
    #print(post_title[0].get('href'))
    # getting the post listings
    post_listing = soup.find_all('li', {'class': 'result-row'})
    #post_title = post_listings[0].find(class_ = 'result-title').text
    #post_url = post_listings[0].find('a').get('href')
    #post_price = post_listings[0].find(class_='result-price').text

    final_posting = []

    for post in post_listing:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'
        if post.find(class_='result-image').get('data-ids'):
            post_image = post.find(class_='result-image').get('data-ids').split(',')[0].split('3:')[1]
            print(post_image)

        final_posting.append((post_title,post_url,post_price))

    print()
    # context dictionary
    stuff_for_frontend = {
        'search': search,
        'final_posting': final_posting,
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)

