# TypesOfEnglish.py
# Author: Luis Briones

import requests
import sys
import os
import re


# Connect to  API end point and get product data
def get_product(query, productids):
    request = requests.post('https://www.teacherspayteachers.com/graph/graphql', json={'query': query, 'variables': productids})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


# Download list of words from gist
def get_words():
    try:
        americanrequest = requests.get(
            'https://gist.githubusercontent.com/mdg/aa4c9070ff3dbeaa5d4613cba05c2faf/raw/c9f1795048a9d7f841079aca2a66f14ef3e7002b/american-words.txt')
        britishrequest = requests.get(
            'https://gist.githubusercontent.com/mdg/aa4c9070ff3dbeaa5d4613cba05c2faf/raw/c9f1795048a9d7f841079aca2a66f14ef3e7002b/british-words.txt')

        if americanrequest.status_code == 200 and britishrequest.status_code == 200:
            # Remove blank lines and split list by new lines
            americanwords = list(filter(None, (americanrequest.text).split('\n')))
            britishwords = list(filter(None, (britishrequest.text).split('\n')))
        else:
            raise Exception("Failed to get word list \n americanrequest: {} \n britishrequest: {}".
                            format(americanrequest.status_code, britishrequest.status_code))

        return {'americanwords': americanwords, 'britishwords': britishwords}
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)


# Determine type of English
def check_type_of_english(productstring, wordlist):
    americancount = 0
    britishcount = 0

    try:
        productstring = str(productstring)

        # Regular expressions below check word boundaries and plurals

        # American check
        for aword in wordlist.get('americanwords', ''):  # regular expresison checks word boundaries and plural
            amer_regex = re.findall(r'\b' + re.escape(aword) + r's?\b', productstring, re.IGNORECASE)
            if amer_regex:
                americancount += 1

        # British check
        for bword in wordlist.get('britishwords', ''):
            brit_regex = re.findall(r'\b' + re.escape(bword) + r's?\b', productstring, re.IGNORECASE)
            if brit_regex:
                britishcount += 1

        if americancount > 0 and britishcount == 0:
            return 'American English'
        elif britishcount > 0 and americancount == 0:
            return 'British English'
        elif americancount > 0 and britishcount > 0:
            return 'Mixed British and American English'
        else:
            return 'Unknown'

    except ValueError as e:
        print('Variable provided was not a string. Error: {0}'.format(e))


def main():
    currentpath = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    # Open product id list from file
    with open(os.path.join(currentpath, 'products.txt'), 'r') as f:
        productidimport = [line.rstrip('\n') for line in f]

    # GraphQL Variables
    productids = {"productIds": productidimport}

    # GraphQL query
    query = """
    query productText($productIds: [ID]!) {
        products(ids: $productIds) {
            id
            name
            description
        }
    }
    """

    # Get product information
    product = get_product(query, productids)
    productinfo = product.get('data', {}).get('products', {})

    productoutput= []

    # Get lists of american and british words
    wordlist = get_words()

    for product in productinfo:
        # productoutput dictionary will hold ids mapped to type of english
        productoutput.append({
                            "productid": product.get('id', ''),
                            "englishtype": check_type_of_english(product.get('name', '') + ' ' +
                                                                 product.get('description', ''), wordlist)
                            })

    # Output dictionary content
    [print('{0} - {1}'.format(product.get('productid', ''), product.get('englishtype', ''))) for product in
     productoutput]


if __name__ == "__main__":
    main()
