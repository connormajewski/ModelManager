import json
import urllib.parse
import base64
import requests
import webbrowser
import socketserver
import http.server
import time

import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

from tkinter import Tk
from tkinter.filedialog import askopenfilenames
from urllib.parse import unquote

from config import client_id, dev_id, client_secret, runame, refresh_token, access_token, config_file_data, config_file_path


def generate_tokens_initial():
    
    url_scopes = "https://api.ebay.com/oauth/api_scope/sell.inventory https://api.ebay.com/oauth/api_scope/sell.account https://api.ebay.com/oauth/api_scope/sell.fulfillment"

    oauth_url = (

        f"https://auth.ebay.com/oauth2/authorize?"
        f"client_id={client_id}&response_type=code&redirect_uri={runame}&scope={urllib.parse.quote(url_scopes, safe='/')}&prompt=login"
    )

    authorization_code = None

    webbrowser.open(oauth_url)

    authorization_code = input("INPUT CODE: ")

    authorization_code = unquote(authorization_code)
            
    token_url = "https://api.ebay.com/identity/v1/oauth2/token"

    authorization_header = f"{client_id}:{client_secret}".encode()
    authorization_header_b64 = base64.b64encode(authorization_header)
    authorization_header_b64_decoded = authorization_header_b64.decode()

    headers = {

        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {authorization_header_b64_decoded}"

    }

    body = {

        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri" : runame

    }

    body_encoded = urllib.parse.urlencode(body)

    response = requests.post(token_url, headers=headers, data=body_encoded)

    if response.status_code == 200:
        tokens = response.json()
        
        print("SUCCESS.")
        
        config_file_data["access_token"] = tokens["access_token"]
        config_file_data["refresh_token"] = tokens["refresh_token"]
        
        config_file = open(config_file_path, "w")
        
        json.dump(config_file_data, config_file, indent=2)
        
        config_file.close()

    else:

        print(f"FAILURE. ERROR CODE {response.status_code}")
        print(response.text)

def get_policy_ids():
    
    fulfillment_endpoint = f"https://api.ebay.com/sell/account/v1/fulfillment_policy?marketplace_id=EBAY_US"
    payment_endpoint = f"https://api.ebay.com/sell/account/v1/payment_policy?marketplace_id=EBAY_US"
    return_endpoint = f"https://api.ebay.com/sell/account/v1/return_policy?marketplace_id=EBAY_US"

    policyIds = {}

    endpoints = {"fulfillment" : fulfillment_endpoint, "payment" : payment_endpoint, "return" : return_endpoint}

    headers = {
    
        "Authorization" : f"Bearer {access_token}",
        "Content-Type" : "application/json"
    
    }
    
    for attribute, endpoint in endpoints.items():
        
        response = requests.get(endpoint, headers=headers)
        
        if response.status_code  == 200:
              
            data = response.json()
            
            policy = attribute + "PolicyId"
                
            policyId = data[attribute + "Policies"][0][policy]
            
            #print(f"{attribute} ID: {policyId}")
            
            policyIds[policy] = policyId
        
        else:
            
            print(response.text)
            
    return policyIds

def set_policy_ids():
    
    payment_endpoint = f"https://api.ebay.com/sell/account/v1/payment_policy"
    shipping_endpoint = f"https://api.ebay.com/sell/account/v1/shipping_policy"
    return_endpoint = f"https://api.ebay.com/sell/account/v1/return_policy"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payment_policy = {
    
        "name" : "Sandbox_Payment_Policy",
        "marketplaceId" : "EBAY_US",
        "categoryTypes" : [
            {
                "name" : "ALL_EXCLUDING_MOTORS_VEHICLES"
            }
        ],
    
        "immediatePay" : True
    
    }
    
    shipping_policy = {
        "name": "Sandbox Shipping Policy",
        "marketplaceId": "EBAY_US",
        "categoryTypes": [
            {
                "name": "ALL_EXCLUDING_MOTORS_VEHICLES"
            }
        ],
        "handlingTime": {
            "unit": "DAY",
            "value": 1
        },
        "shippingOptions": [
            {
                "optionType": "DOMESTIC",
                "shippingServices": [
                    {
                        "shippingServiceCode": "USPSFirstClass",
                        "sortOrderId": 1,
                        "shippingCost": {
                            "currency": "USD",
                            "value": "0.00"
                        }
                    }
                ]
            }
        ]
    }
    
    return_policy = {
        "name": "Sandbox Return Policy",
        "marketplaceId": "EBAY_US",
        "categoryTypes": [
            {
                "name": "ALL_EXCLUDING_MOTORS_VEHICLES"
            }
        ],
        "returnsAccepted": True,
        "returnPeriod": {
            "value": 30,
            "unit": "DAY"
        },
        "refundMethod": "MONEY_BACK",
        "returnShippingCostPayer": "BUYER"
    }
    
    payment_response = requests.post(payment_endpoint, headers=headers, data=json.dumps(payment_policy))
    shipping_response = requests.post(shipping_endpoint, headers=headers, data=json.dumps(shipping_policy))
    return_response = requests.post(return_endpoint, headers=headers, data=json.dumps(return_policy))
    
    print(f"{payment_response}\n{payment_response.text}\n\n")
    print(f"{shipping_response}\n{shipping_response.text}\n\n")
    print(f"{return_response}\n{return_response.text}\n\n")
   
def refresh_access_token():
    
    authorization_header = f"{client_id}:{client_secret}".encode()
    authorization_header_b64 = base64.b64encode(authorization_header)
    authorization_header_b64_decoded = authorization_header_b64.decode()
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {authorization_header_b64_decoded}"
    }
    
    body = {
    
        "grant_type" : "refresh_token",
        "refresh_token" : refresh_token,
    
    }
    
    body_encoded = urllib.parse.urlencode(body)
    
    token_url = "https://api.ebay.com/identity/v1/oauth2/token"

    refresh_access_response = requests.post(token_url, headers=headers, data=body_encoded)
    
    if refresh_access_response.status_code == 400:
        
        print("REFRESH TOKEN INVALID. MUST REVALIDATE OAUTH.")
        
        generate_tokens_initial()
    
    if refresh_access_response.status_code == 200:
        
        tokens = refresh_access_response.json()
    
        config_file_data["access_token"] = tokens["access_token"]
        
        config_file = open(config_file_path, "w")
        
        json.dump(config_file_data, config_file, indent=2)
        
        config_file.close()
        
        print("ACCESS CODE REFRESHED.")
    
    else:
        
        print(refresh_access_response.status_code)
        print(refresh_access_response.text)
    
def create_inventory_body():
    
    body = {
      "sku" : f"{sku}",
      "condition": "NEW",
      "locale" : "en_US",
      "availability": {
        "shipToLocationAvailability": {
          "quantity": 1,
        }
      },
      "product": {
        "title": "Aoshima 1:35 Japan History Figures, Factory Sealed.",
        "description": "Vintage, never opened, factory seal.",
        "aspects": {
          "Brand": ["Aoshima"],
          "Scale": ["1:35"],
          "Type": ["Figure Kit"]
        },
        "imageUrls": hosted_image_urls
      },
    }

    return None
 
def get_condition_id(categoryID):
    
    endpoint = f"https://api.ebay.com/sell/metadata/v1/marketplace/EBAY_US/get_item_condition_policies?category_ids=262320"
    
    headers = {
    
        "Authorization" : f"Bearer {access_token}",
        "Content-Type" : "application/json",
        "Content-Language" : "en-US"
    
    }
    
    inventory_response = requests.get(endpoint, headers=headers)
    
    if inventory_response.status_code == 200:
        
        print("INVENTORY SUCCESSFULLY.")
        
        inventory_data = inventory_response.json()
        
        print(inventory_data)
        
    else:
        
        print("INVENTORY FAILED.")
 
def create_test_inventory_item(image_urls, model_obj):
    
    if len(image_urls) < 1:
        
        print("INVENTORY CREATION FAILED: NO PHOTOS")
        
        return None
    
    hosted_image_urls = []
    
    image_counter = 1
    
    for image_url in image_urls:
        
        hosted_image_urls.append(upload_listing_photo(image_url, f"image_{image_counter}"))
        
        image_counter += 1
    
    endpoint = f"https://api.ebay.com/sell/inventory/v1/inventory_item/{model_obj.model_sku}"
    
    headers = {
    
        "Authorization" : f"Bearer {access_token}",
        "Content-Type" : "application/json",
        "Content-Language" : "en-US"
    
    }
    
    body = {
      "sku" : f"{model_obj.model_sku}",
      "condition": "NEW",
      "locale" : "en_US",
      "availability": {
        "shipToLocationAvailability": {
          "quantity": model_obj.model_quantity,
        }
      },
      "product": {
        "title": f"{model_obj.model_title}",
        "description": f'{"Never opened, factory seal." if model_obj.model_condition == "sealed" else "Opened, parts in box."}',
        "aspects": {
          "Brand": [f"{model_obj.model_manufacturer.title()}"],
          "Scale": [f"{model_obj.model_scale}"],
          "Type": ["Model Kit"]
        },
        "imageUrls": hosted_image_urls
      },
      "packageWeightAndSize": {
        "dimensions": {
          "length": f"{model_obj.model_dimensions[0]:.2f}",
          "width": f"{model_obj.model_dimensions[1]:.2f}",
          "height": f"{model_obj.model_dimensions[2]:.2f}",
          "unit": "INCH"
          },
        "weight": {"value": f"{model_obj.model_weight:.2f}", "unit": "POUND"}
      },
    }
    
    print(body)
    
    inventory_response = requests.put(endpoint, headers=headers, json=body)
    
    print(inventory_response.status_code)
    print(inventory_response.text)
    
    if inventory_response.status_code == 204 or inventory_response.status_code == 200:
        
        print("INVENTORY ADDED SUCCESSFULLY.")
        
        return inventory_response.status_code
        
    else:
        
        print("INVENTORY FAILED.")
        
        return None
    
def get_test_inventory_item(sku):
    
    #endpoint = f"https://api.ebay.com/sell/metadata/v1/marketplace/{marketplace_id}/get_item_condition_policies?category_id={categoryID}"
    endpoint = f"https://api.ebay.com/sell/inventory/v1/inventory_item/"
    
    headers = {
    
        "Authorization" : f"Bearer {access_token}",
        "Content-Language" : "en-US"
    
    }
    
    inventory_response = requests.get(endpoint, headers=headers)
    
    if inventory_response.status_code == 200:
        
        print("INVENTORY SUCCESSFULLY.")
        
        inventory_data = inventory_response.json()
        
        print(inventory_data)
        
    else:
        
        print("INVENTORY FAILED.")
        
def get_condition():
    
    endpoint = f"https://api.ebay.com/commerce/taxonomy/v1"
    #endpoint = f"https://api.ebay.com/sell/inventory/v1/inventory_item/"
    
    headers = {
    
        "Authorization" : f"Bearer {access_token}",
        "Content-Language" : "en-US"
    
    }
    
    inventory_response = requests.get(endpoint, headers=headers)
    
    if inventory_response.status_code == 200:
        
        print("INVENTORY SUCCESSFULLY.")
        
        inventory_data = inventory_response.json()
        
        print(inventory_data)
        
    else:
        
        print("INVENTORY FAILED.")

def clear_inventory():
    
    skus = []
    
    endpoint = f"https://api.ebay.com/sell/inventory/v1/inventory_item/"
    
    headers = {
    
        "Authorization" : f"Bearer {access_token}",
        "Content-Type" : "application/json"
    
    }
    
    inventory_response = requests.get(endpoint, headers=headers)
    
    data = inventory_response.json()
    
    print(data)
    
    if not data["total"] and not data["size"]:
        
        print("No inventory items have been created.")
        
    else:            
    
        for item in data["inventoryItems"]:
            
            if "sku" in item:
                
                delete_inventory(item["sku"])

def delete_inventory(sku):
    
    endpoint = f"https://api.ebay.com/sell/inventory/v1/inventory_item/{sku}"
    
    headers = {
    
        "Authorization" : f"Bearer {access_token}",
        "Content-Type" : "application/json"
    
    }
    
    delete_response = requests.delete(endpoint, headers=headers)
    
    success_codes = [200,204,202]
    
    if delete_response.status_code in success_codes:
        
        print("DELETION SUCCESSFUL.")
    
    else:
        
        print("DELETION FAILED.")
    
def create_test_listing(image_urls, model_obj):
    
    print(type(model_obj.model_dimensions[0]))
    print(model_obj.model_weight)
    
    categoryIds = {
        "car" : "262320", 
        "truck" : "262320",
        "plane" : "262319",
        "helicopter" : "262319",
        "balloon": "262319",
        "rocket" : "262325", 
        "ship" : "262321", 
        "submarine" : "262321", 
        "figurine" : "262324", 
        "miscellaneous" : "262335", 
        "motorcycle" : "165777", 
        "tank" : "165756",
        "army": "165756",
        "slotcar" : "776"
        }
        
    
    
    model_type = model_obj.model_type
    
    categoryId = categoryIds[model_type]
    
    get_condition_id(categoryId)
            
    print(f"{model_type} : {categoryId}")
    
    print(model_obj.model_sku)
        
    inventory_created = create_test_inventory_item(image_urls, model_obj)
    
    if inventory_created is None:
        
        print("ERROR CREATING INVENTORY.")
        
        return None
        
    print("PASSED.")
    
    endpoint = f"https://api.ebay.com/sell/inventory/v1/offer/"
    
    policyIds = get_policy_ids()
    
    headers = {
    
        "Authorization" : f"Bearer {access_token}",
        "Content-Type" : "application/json",
        "Accept" : "application/json",
        "Content-Language" : "en-US"
    
    }
    
    body = {
        "sku": f"{model_obj.model_sku}",
        "categoryId": f"{categoryId}",
        "marketplaceId": "EBAY_US",
        "format": "FIXED_PRICE",
        "listingPolicies": {
            "fulfillmentPolicyId": f"{policyIds["fulfillmentPolicyId"]}",
            "returnPolicyId": f"{policyIds["returnPolicyId"]}",
            "paymentPolicyId": f"{policyIds["paymentPolicyId"]}"
        },
        "pricingSummary": {
           "price": {
               "value": f"{model_obj.model_price}",
               "currency": "USD"
           }
        },
        "itemLocation": {
            "country": "US",
            "postalCode": "14895",
            "stateOrProvince": "NY",
            "city": "Wellsville"
        },

        "availableQuantity": 1,
        "merchantLocationKey": "Wellsville_Key",
        "listingDescription": f"{'New in box, complete with factory seal.' if model_obj.model_condition == 'sealed' else 'Complete box with parts included.'}"
    }
    
    offer_id = check_offerId_exists(model_obj.model_sku)
    
    print(offer_id)
    
    if offer_id is None:
        
        inventory_response = requests.post(endpoint, headers=headers, json=body)
    
        if inventory_response.status_code == 204 or inventory_response.status_code == 200 or inventory_response.status_code == 201:
            
            offer_id = inventory_response.json()["offerId"]
            
            print("INVENTORY ADDED SUCCESSFULLY.")
            
            print(offer_id)
            
        else:
            
            print("LISTING FAILED.")
            
            return None
    
        print(inventory_response.status_code)
        print(inventory_response.text)

    publish_endpoint = f"https://api.ebay.com/sell/inventory/v1/offer/{offer_id}/publish"
            
    publish_response = requests.post(publish_endpoint, headers=headers)
    
    print(publish_response.status_code)
    print(publish_response.text)  
    
    if publish_response.status_code == 204 or publish_response.status_code == 200 or publish_response.status_code == 201:
    
        print("LISTING LIVE")
    
        return publish_response.status_code
        
    else:
        
        return None
 
def view_listing(item_id):
        
    url = f"https://api.ebay.com/buy/browse/v1/item/v1|{item_id}"

    headers = {
        "Authorization": f"Bearer {access_token}",  # Token must include buy.browse scope
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    print(response.status_code)
    print(response.json())
 
def check_offerId_exists(sku):
    
    #check_endpoint = f"https://api.ebay.com/sell/inventory/v1/offer?sku={sku}"
    check_endpoint = f"https://api.ebay.com/sell/inventory/v1/offer"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    check_response = requests.get(check_endpoint, headers=headers)
    
    if check_response.status_code == 200:
        
        check_data = check_response.json()
        
        if "offers" in check_data and len(check_data["offers"]) > 0:
        
            print("OFfer id found.")
            
            print(check_response.text)
        
            offer_id = check_data["offers"][0]["offerId"]
            
            return offer_id
            
        else:
            
            return None
            
    else:
        
        print(f"Failed to find offer id for SKU {sku}")
        
def set_location(merchant_location_key):
    
    headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
    }

    endpoint = f"https://api.ebay.com/sell/inventory/v1/location/{merchant_location_key}"

    body = {
      "location": {
        "address": {
          "city": "Wellsville",
          "stateOrProvince": "NY",
          "postalCode": "14895",
          "country": "US"
        }
      },
      "name": f"{merchant_location_key}",
      "merchantLocationStatus": "ENABLED",
      "locationTypes": ["WAREHOUSE"]
    }

    response = requests.post(endpoint, headers=headers, json=body)

    print("LOCATRION FINSIHED")

    print(response.status_code)
    print(response.text)

# Uploads an image to EPS (Ebay image hosting) to allow it to be linked to an inventory/listing. Cannot create a listing through REST API if there is no image.
# Had to use Trading XML, could not find a way to use REST API to do this.

def upload_listing_photo(image_path, image_name):
    
    endpoint = "https://api.ebay.com/ws/api.dll"
    
    xml_payload = f"""<?xml version="1.0" encoding="utf-8"?>
    <UploadSiteHostedPicturesRequest xmlns="urn:ebay:apis:eBLBaseComponents">
      <RequesterCredentials>
        <eBayAuthToken>{access_token}</eBayAuthToken>
      </RequesterCredentials>
      <PictureName>{image_name}</PictureName>
      <PictureSet>Supersize</PictureSet>
      <GalleryType>Gallery</GalleryType>
      <GalleryPlus>true</GalleryPlus>
    </UploadSiteHostedPicturesRequest>
    """
    
    headers = {
        "X-EBAY-API-CALL-NAME": "UploadSiteHostedPictures",
        "X-EBAY-API-SITEID": "0",
        "X-EBAY-API-COMPATIBILITY-LEVEL": "1143",
        "X-EBAY-API-DEV-NAME": dev_id,
        "X-EBAY-API-APP-NAME": client_id,
        "X-EBAY-API-CERT-NAME":client_secret,
    }
    
    image_file = open(image_path, "rb")
    
    files = {
        "XML Payload": (None, xml_payload, "text/xml"),
        "file1": (image_path, image_file, "image/jpg")
    }
    
    response = requests.post(endpoint, headers=headers, files=files)
    
    image_file.close()
    
    if response.status_code == 200:
        
        print(response.text)
        print("\n\n\n\n")
            
        start = response.text.find("<FullURL>") + len("<FullURL>")
        end = response.text.find("</FullURL>")
        hosted_url = response.text[start:end]
        print("SUCCESS UPLOADING.")
        print("Hosted Image URL:", hosted_url) 
        
        return hosted_url
        
    else:
        print("ERROR UPLOADING.") 
 
def get_listing_categories():
    
        category_file = open("category_file.txt", "w", encoding="utf-8")

        endpoint = "https://api.ebay.com/ws/api.dll"
        
        xml_payload = f"""<?xml version="1.0" encoding="utf-8"?>
        <GetCategoriesRequest xmlns="urn:ebay:apis:eBLBaseComponents">
          <RequesterCredentials>
            <eBayAuthToken>{access_token}</eBayAuthToken>
          </RequesterCredentials>
          <DetailLevel>ReturnAll</DetailLevel>
          <LevelLimit>0</LevelLimit>
          <ViewAllNodes>true</ViewAllNodes>
          <CategorySiteID>0</CategorySiteID>
        </GetCategoriesRequest>
        """
        
        headers = {
            "X-EBAY-API-CALL-NAME": "GetCategories",
            "X-EBAY-API-SITEID": "0",
            "X-EBAY-API-COMPATIBILITY-LEVEL": "967",
            "X-EBAY-API-DEV-NAME": dev_id,
            "X-EBAY-API-APP-NAME": client_id,
            "X-EBAY-API-CERT-NAME":client_secret,
        }
        
        files = {
            "XML Payload": (None, xml_payload, "text/xml"),
        }

        response = requests.post(endpoint, headers=headers, files=files)
        
        xml_content = response.text  # your XML response string

        root = ET.fromstring(xml_content)

        namespaces = {'ebay': 'urn:ebay:apis:eBLBaseComponents'}

        # Use namespace prefix in find with the dictionary
        category_array = root.find('.//ebay:CategoryArray', namespaces)
        
        if category_array is not None:
            for category in category_array.findall('ebay:Category', namespaces):
                cat_id = category.find('ebay:CategoryID', namespaces)
                cat_name = category.find('ebay:CategoryName', namespaces)
                category_file.write(f"{cat_name.text if cat_name is not None else '' : <64} : {cat_id.text if cat_id is not None else ''}\n")
        else:
            print("No categories found in response.")
        
        category_file.close()
        
def get_listing_locations():
    
    endpoint = "https://api.ebay.com/sell/inventory/v1/location"
    
    headers = {
    
        "Authorization" : f"Bearer {access_token}",
        "Content-Language" : "en-US"
    
    }
    
    response = requests.get(endpoint, headers=headers)
    
    if response.status_code == 200:
        
        print("LISTING LOCATIONS FOUND,")
        
        data = response.json()
        
        print(data)
        
        location_names = [location["name"] for location in data["locations"]]
        
        print(location_names)
        
    else:
        
        print("ERROR FINDING LISTING LOCATIONS.")
          

def check_access_token_validity():

    endpoint = f"https://api.ebay.com/sell/account/v1/payment_policy?marketplace_id=EBAY_US"

    headers = {
    
        "Authorization" : f"Bearer {access_token}",
        "Content-Type" : "application/json"
    
    }
    
    response = requests.get(endpoint, headers=headers)
    
    if response.status_code == 401:
        
        print("ACCESS TOKEN INVALID, GENERATING NEW ONE.")
        
        refresh_access_token()
        
    if response.status_code == 200:
        
        print("ACCESS TOKEN VALID. NO ACTION REQUIRED.")
        
