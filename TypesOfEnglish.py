# TypesOfEnglish.py
# Author: Luis Briones

import requests
import re

class Request:
    '''
        Class returns response from request. Split into two methods because one uses get and the other post
        depending on the type of request
    '''
    def __init__ (self):
        # Class variable
        self.query_items = {}
        pass

    def get_items_to_query(self, url, requestType):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                item_list = list(filter(None, (response.text).split('\n')))
                self.query_items[requestType] = item_list
            else:
                raise Exception('Failed to get word list \n {}: {}'.format(requestType, response.status_code))
        except requests.exceptions.RequestException as e:
            print(e)
    
    
    # Connect to  API end point and get product data
    def get_product_info(self, url, query, productids):
        try:
            response = requests.post(url, json={'query': query, 'variables': productids})
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))
        except requests.exceptions.RequestException as e:
            print(e)


# Determine type of English
def check_type_of_english(productstring, word_dict):
    americancount = 0
    britishcount = 0

    productstring = str(productstring)

    # Loop through  hash map keys to check if word's in the product string
    for word in word_dict.keys():
        # Regular expression checks word boundaries and plurals
        word_found = re.findall(r'\b' + re.escape(word) + r's?\b', productstring, re.IGNORECASE)
        
        # Keep count of american and british words found
        if word_found:
            if word_dict[word] == 'american':
                americancount += 1
            else:
                britishcount += 1

    if americancount > 0 and britishcount == 0:
        return 'American English'
    elif britishcount > 0 and americancount == 0:
        return 'British English'
    elif americancount > 0 and britishcount > 0:
        return 'Mixed British and American English'
    else:
        return 'Unknown'


def main():

    # Dictionary with all the URLS used throughout program
    url = {'americanwords': 'https://raw.githubusercontent.com/brionesl/typesofenglish/master/american-words.txt',
           'britishwords': 'https://raw.githubusercontent.com/brionesl/typesofenglish/master/british-words.txt',
           'products': 'https://raw.githubusercontent.com/brionesl/typesofenglish/master/products.txt',
           'product_api_url':  'https://www.teacherspayteachers.com/graph/graphql'}

    # Instantiate Request Class
    request = Request()

    # Response from calls to urls, are added to class variable "query_items"
    for requestType, link in url.items():
        if 'product_api_url' not in requestType:
            request.get_items_to_query(link, requestType=requestType)
    
    # Create hash map for words and the types of english
    ''' Example:
        {
            'color': 'american',
            'colour': 'british'
        }
    '''
    american_dict = {}
    british_dict = {}
    for word in request.query_items['americanwords']:
        american_dict[word] = 'american'

    for word in request.query_items['britishwords']:
        british_dict[word] = 'british'

    # Combine hash maps
    word_dict = {**american_dict, **british_dict}

    # GraphQL Variables
    productids = {"productIds": request.query_items['products']}

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
    productoutput= []
    product_list = request.get_product_info(url['product_api_url'], query, productids)
    productinfo = product_list['data']['products']

    for product in productinfo:
        # productoutput dictionary will hold ids mapped to type of english
        productoutput.append({
                            "productid": product['id'],
                            "englishtype": check_type_of_english(product['name'] + ' ' +
                                                                 product['description'], word_dict)
                            })

    # Output dictionary content
    [print('{0} - {1}'.format(product['productid'], product['englishtype'])) for product in productoutput]


if __name__ == "__main__":
    main()
