import requests
import json
import time
from dotenv import load_dotenv
import os

load_dotenv()

api_token = os.environ["api_token"]

pin_url = "https://api.web3.storage/upload"

headers = {
  'accept': 'application/json',
  'Authorization': 'Bearer ' + api_token
#   'Content-Type': 'multipart/form-data'
}


def mints(address):
    query = """query mints ($address: [String!]!) {
    mints(where: {minterAddresses: $address, recipientAddresses: $address}, sort: {sortKey: TIME, sortDirection: DESC}) {
        nodes {
        mint {
            originatorAddress
            toAddress
            collectionAddress
            tokenId
        }
        }
    }
    }"""

    variables = {
    "address": address
    }

    url = 'https://api.zora.co/graphql'
    r = requests.post(url, json={'query': query, 'variables': variables})
    # print(r.status_code)
    # print(r.text)
    mints = r.json()['data']['mints']['nodes']
    # print(r.json()['data']['mints']['nodes'][0]['mint'])
    # print('The most recent mints for ' + address + ' are: ')
    mint_list = []
    for mint in mints:
        collection_address = mint['mint']['collectionAddress']
        token_id = mint['mint']['tokenId']
        # url = "https://api.opensea.io/api/v1/asset_contract/" + str(collection_address)
        # headers = {"X-API-KEY": "051d1a31d15343cab4c4a4fdb123dd56"}
        # response = requests.get(url, headers=headers)
        # slug = response.json()['collection']['slug']
        # print('https://opensea.io/collection/' + slug + '/' + token_id)
        url_show = 'https://opensea.io/assets/ethereum/' + collection_address + '/' + token_id
        url = 'https://opensea.io/assets/ethereum/' + collection_address + '/' + token_id + '>' + url_show + '</a><br>'
        # print(url_show)
        mint_list.append(url)
        # time.sleep(0.5)
    return mint_list

def buys(address):
    query = """query buys ($address: [String!]!) {
    sales(sort: {sortKey: TIME, sortDirection: DESC}, where: {buyerAddresses: $address}) {
        nodes {
        sale {
            buyerAddress
            collectionAddress
            tokenId
        }
        }
    }
    }"""

    variables = {
    "address": address
    }

    url = 'https://api.zora.co/graphql'
    r = requests.post(url, json={'query': query, 'variables': variables})
    # print(r.status_code)
    # print(r.text)

    sales = r.json()['data']['sales']['nodes']
    # print(mints)
    # print(r.json()['data']['mints']['nodes'][0]['mint'])
    # print('The most recent purchases for ' + address + ' are: ')
    buy_list = []
    for sale in sales:
        collection_address = sale['sale']['collectionAddress']
        token_id = sale['sale']['tokenId']
        # url = "https://api.opensea.io/api/v1/asset_contract/" + str(collection_address)
        # headers = {"X-API-KEY": "051d1a31d15343cab4c4a4fdb123dd56"}
        # response = requests.get(url, headers=headers)
        # slug = response.json()['collection']['slug']
        # print('https://opensea.io/collection/' + slug + '/' + token_id)
        url_show = 'https://opensea.io/assets/ethereum/' + collection_address + '/' + token_id
        url = 'https://opensea.io/assets/ethereum/' + collection_address + '/' + token_id + '>' + url_show + '</a><br>'
        buy_list.append(url)
        # print(url_show)
        # time.sleep(0.5)
    return buy_list


def bot(website):
    name = time.time()
    address = website
    mints_list = mints(address)
    mints_url = '<a href=' + ('<a href='.join(str(e) for e in mints_list)) + '<br></a>'
    buys_list = buys(address)
    buys_url = '<a href=' + ('<a href='.join(str(e) for e in buys_list)) + '<br></a>'
    f = open('templates/' + 'return.html', 'w')
    html_template = """<html>
    <head>
    <link rel= "stylesheet" type= "text/css" href="/static/mainpage.css">
    <title>DevTeam Project</title>
    </head>
    <body>
    <h2>Welcome to The DevTeam Project</h2>
    
    <p>The most recent mints from {address} are: <br><br>{mints}<br><br></p>
    <p>The most recent purchases from {address} are: <br><br>{buys}<br><br></p>
    </body>
    </html>
    """.format(address=address, mints=mints_url, buys=buys_url)
    f.write(html_template)
    f.close()
    filename = 'templates/' + 'return.html'
    payload={}
    files=[
    ('file',(filename,open(filename,'rb')))
    ]
    response = requests.request("POST", pin_url, headers=headers, data=payload, files=files)
    # print(response.text)
    # ipfs_hash = response.json()['IpfsHash']
    ipfs_hash = response.json()['cid']
    link = 'https://aifrens.mypinata.cloud/ipfs/' + ipfs_hash
    # print(link)
    return link, name
    # link = ipfs_hash + '/' + filename


