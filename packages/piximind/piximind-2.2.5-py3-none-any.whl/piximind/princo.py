import requests
def princo(apikey, userId, ticket):
    url = 'http://localhost:3000/impression'
    body = {
        'apiKey': apikey,
        'userId': userId,
        'pdfBase64': ticket
    }
    try:
        response = requests.post(url, json=body)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        print('Error:', err)
        raise


def print_pdf(ticket):
    url = 'http://localhost:3000/impression/pdf'
    body = {
        'pdfBase64': ticket
    }
    try:
        response = requests.post(url, json=body)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        print('Error:', err)
        raise
