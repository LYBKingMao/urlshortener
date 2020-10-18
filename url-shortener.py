import json
import time
import urllib
import hashlib
import boto3 #library for accessing Dynamodb
from urllib import parse
from random import randint, choice
from string import ascii_letters, digits

dynamodb = boto3.resource('dynamodb', region_name = '***').Table('***') #dynamodb instance
string_map = ascii_letters + digits

def generate_random(start, end):  #linear congruential method
    a = 32310901
    b = 1729
    rOld = time.time()
    m = end - start
    rNew = (a * rOld + b)%m
    return rNew
    

def generate_suffix():  #generate short url
    strval = "".join(string_map[int(generate_random(0,61))] for x in range(randint(8, 16)))
    strval = validate(strval)
    return strval
    
def validate(suffix):    #validate repetition
    if suffix in dynamodb.get_item(Key={'short_id': suffix}):
        new_url = generate_id()
    else:
        return suffix

def lambda_handler(event, context):
    base_url = "***"
    suffix = generate_suffix()
    new_url = base_url + suffix
    original_url = event["original_url"]
    dynamodb.put_item(Item = {  #store data to database
        "short_id": suffix,
        "new_url": new_url,
        "original_url": original_url
    })
    
    
    return {
        'statusCode': 200,
        'body': new_url
    }
