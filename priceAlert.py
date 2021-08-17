#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By : Fred Cozzi
# Created Date: Tue August 17 17:27:00 GMT 2021
# Version : 1.0
# Python Version : 3.9.4
# =============================================================================
"""Python source file using the twilio API and Oilprice API. The application
retrives the price of oil and sends texts alerts to the users phone."""
# =============================================================================
# Imports
import os
import datetime
import time
import requests
from twilio.rest import Client
# =============================================================================

url = 'https://api.oilpriceapi.com/v1/prices/latest' 
headers = {
  'Authorization': 'Oil Price Token Here',
  'Content-Type': 'application/json'
}
AUTH_SID = "Twilio SID" # Needs to be put in env variable for additional security
AUTH_TOK = "Twilio Token" # Needs to be put in env variable for additional security

def getData(): # Makes the GET request to Oilprice API 
    response = requests.get(url=url, headers=headers) 
    data = response.json() # Put in JSON format
    return data # Return data for future use

def sendText(key1, key2, s): # Uses twilio to send a text to the users phone

    data = getData() # Function to get data in JSON format

    client = Client(AUTH_SID, AUTH_TOK)
    s = s + str(data[key1][key2]) # Message that will be sent to user

    message = client.messages.create( # Sends message to phone
        body=s, # Message to be sent
        from_="+447429895135", # Sending phone number
        to="+447935906799" # Recieving phone number
    )

    now = time.localtime() 
    print("Message sent at: ", time.asctime(now)) # Prints to the CLI the time which the message was sent

def timeAlert(hour, minute): # Function that alerts the user at a desired time
    alarmTime = datetime.time(hour, minute, 0) # Time the user wants to be alerted

    while True: # Infinite loop
        if alarmTime == datetime.datetime.now().time(): # If alarm time is the same as the time now, send SMS
            sendText('data', 'formatted', 'The price of oil is ') 


def priceAlert(difference): # Price alert function that alerts user of price spikes or falls
    while True: # Infinite loop

        firstData = getData() 
        firstPrice = firstData['data']['price'] # The initial price

        time.sleep(120) # Wait for the next price

        secondData = getData() 
        secondPrice = secondData['data']['price'] # The final price
        compare = abs(firstPrice - secondPrice)

        if compare > difference: # If compare is bigger than the difference specified by the user
            sendText('data', 'formatted', 'The price has dropped to ')