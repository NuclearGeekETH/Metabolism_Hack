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
    mints_url = '<a target="_blank" href=' + ('<a target="_blank" href='.join(str(e) for e in mints_list)) + '<br></a>'
    buys_list = buys(address)
    buys_url = '<a target="_blank" href=' + ('<a target="_blank" href='.join(str(e) for e in buys_list)) + '<br></a>'
    f = open('build/' + 'index.html', 'w')
    html_template = """<html>
    <head>
    <link rel="apple-touch-icon" sizes="180x180" href="/static/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/static/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/static/favicon-16x16.png">
    <link rel="manifest" href="/static/site.webmanifest">
    <link rel="mask-icon" href="/static/safari-pinned-tab.svg" color="#5bbad5">
    <link rel= "stylesheet" type= "text/css" href="/static/mainpage.css">
    <title>MintHound</title>
    <script src="https://cdn.tailwindcss.com"></script>  
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap" rel="stylesheet">

    </head>
    <body>
            <section class="flex bg-teal-700">
            <div class="w-full items-center content-center justify-center container mx-auto px-8 pt-10">
              <div class="text-center">
                <!-- <img src="/static/MintHound.png" alt="" /> -->
                <img class="max-w-2xl mx-auto" src="/static/MintHound.png" alt="" />
                <p class="-mt-8 lg:text-2xl text-white thanks">Thanks furry much for using MintHound!</p>
                <div class="mt-8 mb-12 bg-white/50 mx-auto backdrop-blur-sm py-12 rounded-2xl max-w-5xl visited:text-purple-500">
    
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