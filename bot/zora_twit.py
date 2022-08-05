import requests
import json
import time
from dotenv import load_dotenv
import os
import typing as tp

load_dotenv()

api_key = os.environ["api_key"]
api_secret = os.environ["api_secret"]
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
    mint_list = []
    for mint in mints:
        collection_address = mint['mint']['collectionAddress']
        token_id = mint['mint']['tokenId']
        url_show = 'https://opensea.io/assets/ethereum/' + collection_address + '/' + token_id
        url = 'https://opensea.io/assets/ethereum/' + collection_address + '/' + token_id + '>' + url_show + '</a><br>'
        mint_list.append(url)
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
    buy_list = []
    for sale in sales:
        collection_address = sale['sale']['collectionAddress']
        token_id = sale['sale']['tokenId']
        url_show = 'https://opensea.io/assets/ethereum/' + collection_address + '/' + token_id
        url = 'https://opensea.io/assets/ethereum/' + collection_address + '/' + token_id + '>' + url_show + '</a><br>'
        buy_list.append(url)
    return buy_list

def get_all_files(directory: str) -> tp.List[str]:
    paths: tp.List[str] = []
    for root, dirs, files_ in os.walk(directory):        
        for file in files_:            
             paths.append(os.path.join(root, file))
    return paths

def bot(website):
    # name = time.time()
    address = website
    mints_list = mints(address)
    mints_url = '<a href=' + ('<a href='.join(str(e) for e in mints_list)) + '<br></a>'
    buys_list = buys(address)
    buys_url = '<a href=' + ('<a href='.join(str(e) for e in buys_list)) + '<br></a>'
    f = open('build/' + 'index.html', 'w')
    html_template = """<html>
    <head>
    <link rel= "stylesheet" type= "text/css" href="static/mainpage.css">
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
    filename1 = 'build/' + 'index.html'
    filename2 = 'build/static/' + 'mainpage.css'
    payload={}
    all_files: tp.List[str] = get_all_files('./build')            
    files = [('file', (file, open(file, "rb"))) for file in all_files]
    response = requests.request("POST", pin_url, headers=headers, data=payload, files=files)
    # print(response.text)
    # ipfs_hash = response.json()['IpfsHash']
    ipfs_hash = response.json()['cid']
    link = 'https://aifrens.mypinata.cloud/ipfs/' + ipfs_hash + '/build/'
    print(link)
    return link


# bot('oscode.eth')