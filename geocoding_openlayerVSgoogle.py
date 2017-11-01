#-------------------------------------------------------------------------------
# Name:
# Purpose: Python Script to check the differences of the geocoding service from
#            OpenLayer, Google, Bing and others
# Author:      pyang
# Created:     10/08/2017
# Copyright:   (c) pyang 2017
#-------------------------------------------------------------------------------

import urllib
import time
import xml.etree.ElementTree as ET
import math
#Google geocoding API key: AIzaSyDg94OOra8C9JBiwUHUUPACdO5bGep6Fkc

#==============================================================================
# fn = r'C:\Users\pyang\Dropbox\Programming\Python\CitingMapLocation.txt'
serviceurl = 'http://maps.googleapis.com/maps/api/geocode/xml?'
#
# f = open(fn)
#==============================================================================

#with open
#==============================================================================
# for line in f:
#     #line = line.rstrip().upper()
#     #print line
#     time.sleep(3)  # Delay for 3 seconds to avoid time out
#
#
#     address = line # raw_input('Enter location: ')
#
#
#     if len(address) < 1 : break
#
#     url = serviceurl + urllib.urlencode({'sensor':'false', 'address': address})
#     #print 'Retrieving', url
#     uh = urllib.urlopen(url)
#     data = uh.read()
#     #print 'Retrieved',len(data),'characters'
#     #print data
#     tree = ET.fromstring(data)
#
#
#     results = tree.findall('result')
#     lat = results[0].find('geometry').find('location').find('lat').text
#     lng = results[0].find('geometry').find('location').find('lng').text
#     location = results[0].find('formatted_address').text
#
#     #print 'lat',lat,'lng',lng
#     print lat,',',lng
#==============================================================================

    #printabs



#==============================================================================
# Lisbon, Portugal
# Palisades, New York, USA
# Wrocław, Poland
# Fargo, ND, USA
# Palmerston North, New Zealand
# Potenza , Italy
# McGill University, Canada
# University of Kentucky
# Eldoret, Kenya
# Orlando, Florida
# Zhengzhou, China
# Rolla, MO 65401, United States
# Lisbon,Portugal
# Tainan City, Taiwan
# Brno, Czech Republic
# Nanjing , China
#  Beijing, China
# Austin, TX, USA
#==============================================================================

import pandas
import geopy
import os
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
geolocator = Nominatim()
serviceurl = 'http://maps.googleapis.com/maps/api/geocode/xml?'
def do_geocode(address):
    try:
        return geopy.geocode(address)
    except GeocoderTimedOut:
        return do_geocode(address)


# from geopy import geocoders
#
# g = geocoders.GoogleV3()  #https://geopy.readthedocs.io/en/latest/#geopy.geocoders.GoogleV3
#
# for x in xrange(1,10000):
#     print x
#     a = g.geocode("AV JOAO NAVES DE AVILA " + str(x) + " UBERLANDIA MG BRASIL")
#     print a


#function for getting geocoding from different sources
def geocodingDif(address,ADDRESS, CITY, STATE, ZIPCODE):

    location = geolocator.geocode(address)
    if location != None:
    #print(location.address)
        print('OpenLayer:', (location.latitude, location.longitude))
        OpenLayerstring = "%f,%f" % (location.latitude, location.longitude)
    else:
        print('not found!')
        OpenLayerstring = "%f,%f" % (-999, -999)

    #using the geopy api to do it
    g = geopy.geocoders.GoogleV3(api_key='AIzaSyDg94OOra8C9JBiwUHUUPACdO5bGep6Fkc')
    a = g.geocode(address,timeout=10)
    if a != None:
        print("Google: ",(a.latitude, a.longitude))
        Googlestring = "%f,%f" % (a.latitude, a.longitude)
    else:
        print('not found!')
        Googlestring = "%f,%f" % (-999, -999)

    # url = serviceurl + urllib.parse.urlencode({'sensor': 'false', 'address': address})
    # print(url)
    # uh = urllib.request.urlopen(url)
    # data = uh.read()
    # tree = ET.fromstring(data)
    # results = tree.findall('result')
    # if results:
    #     lat = float(results[0].find('geometry').find('location').find('lat').text)
    #     lng = float(results[0].find('geometry').find('location').find('lng').text)
    #     location = results[0].find('formatted_address').text
    #     print('Google Map:', (lat, lng))
    #     Googlestring = "%f,%f" % (lat, lng)
    # else:
    #     print('not found!')
    #     Googlestring = "%f,%f" % (-999, -999)

    url = "http://geoservices.tamu.edu/Services/Geocode/WebService/GeocoderWebServiceHttpNonParsed_V04_01.aspx?streetAddress=%s&city=%s&state=%s&zip=%s&apikey=demo&format=XML&allowTies=false&TieBreakingStrategy=flipACoin&notStore=false&version=4.01" % (ADDRESS, CITY, STATE, ZIPCODE)
    uh = urllib.request.urlopen(url)
    data = uh.read()
    tree = ET.fromstring(data)
    results = tree.findall('OutputGeocodes')
    if results :
        lat = float(results[0].find('OutputGeocode').find('Latitude').text)
        lng = float(results[0].find('OutputGeocode').find('Longitude').text)
        print('Texas A&M Geocoding:', (lat, lng))
        TexasAMstring = "%f,%f" % (lat, lng)
    else:
        print('not found!')
        TexasAMstring = "%f,%f" % (-999, -999)
        
    return OpenLayerstring + ',' + Googlestring + ',' + TexasAMstring

#
# Address = "24575 BORDER HILL RD, NOVI, MI, 48375"
# print(Address,type(Address))
# from geopy.geocoders import Nominatim
# geolocator = Nominatim()
# location = geolocator.geocode(Address)
# print(location.address)
# print('OpenLayer:',(location.latitude, location.longitude))
#
# serviceurl = 'http://maps.googleapis.com/maps/api/geocode/xml?'
# address = Address
# url = serviceurl + urllib.parse.urlencode({'sensor':'false', 'address': address})
# uh = urllib.request.urlopen(url)
# data = uh.read()
# tree = ET.fromstring(data)
# results = tree.findall('result')
# lat = float(results[0].find('geometry').find('location').find('lat').text)
# lng = float(results[0].find('geometry').find('location').find('lng').text)
# location = results[0].find('formatted_address').text
# print('Google Map:',(lat,lng))


csvfile = r"C:\Users\Peter\Dropbox\Programming\Python\Ok_parcel_example_test.csv"
WorkspaceRoot = os.getcwd()
Workspace = os.path.join(WorkspaceRoot, 'Import-Students.csv')
#Workspace = os.path.join(WorkspaceRoot, 'Import-Students-test.csv')
AddressFile = os.path.join(WorkspaceRoot, 'AddressFile.txt')
urlFile = os.path.join(WorkspaceRoot, 'urlFile.txt')
coordinatelFile = os.path.join(WorkspaceRoot, 'AddressClean_111.txt')
cleanedcsv = os.path.join(WorkspaceRoot, 'AddressClean_11.txt')

with open(Workspace) as csv, open(coordinatelFile,'a') as F9:
    pread = pandas.read_csv(csv)
    df = pread[['GUID','Address','City','State', 'Zip','Student Lng(X)','Student Lat(Y)']]
    df = df[pandas.notnull(df['Address'])]
    df = df[pandas.notnull(df['City'])]
    df = df.drop_duplicates()
    df = df.dropna(thresh=3)
    #df.to_csv(cleanedcsv,header=True,sep=" ")
    #df = df.dropna(axis=1, how='any')
    #print(df.head(5))

    for index, row in df.iterrows():
        #print(row)
        #Some address may not correct,don't know why!
        if math.isnan(row['Zip']):
            #Address = row['Address'] + ',' + row['City'] + ',' + row['State']
            Address = row['Address'] + ' ' + row['City'] + ' ' + row['State']
        #if row['Zip']:
        else:
            #Address = row['Address'] + ',' + row['City'] + ',' + row['State'] + ',' + str(int(row['Zip']))
            Address = row['Address'] + ' ' + row['City'] + ' ' + row['State'] + ' ' + str(int(row['Zip']))
            ADDRESS = row['Address'].replace(" ", "%20")
            CITY = row['City'].replace(" ", "%20")
            STATE = row['State'].replace(" ", "%20")
            ZIPCODE = str(int(row['Zip']))            
            # url = "http://geoservices.tamu.edu/Services/Geocode/WebService/GeocoderWebServiceHttpNonParsed_V04_01.aspx?streetAddress=%s&city=%s&state=%s&zip=%s&apikey=demo&format=XML&allowTies=false&TieBreakingStrategy=flipACoin&notStore=false&version=4.01" % (ADDRESS,CITY,STATE,ZIPCODE)
            # print(url)
            # uh = urllib.request.urlopen(url)
            # data = uh.read()
            # tree = ET.fromstring(data)
            # results = tree.findall('OutputGeocodes')
            # lat = float(results[0].find('OutputGeocode').find('Latitude').text)
            # lng = float(results[0].find('OutputGeocode').find('Longitude').text)
            # print('Texas A&M Geocoding:',(lat,lng))

        guid = row['GUID']
        REFLat = row['Student Lat(Y)']
        REFLon = row['Student Lng(X)']

        writestring = "%s,%s,%f,%f" % (guid, Address, REFLat, REFLon)
        F9.write(writestring + '\n')
            
#            writestring = "%s,%s,%f,%f"%(guid,geocodingDif(Address,ADDRESS,CITY,STATE,ZIPCODE),REFLat,REFLon)
#            F9.write(writestring + '\n')
#            time.sleep(3)
        

        #F9.write( Address + '\n')
        #print(Address)

'''
with open(csvfile) as csv:
    pread = pandas.read_csv(csv)
    df = pread[['SITEADDRESS','SITECITY','SITESTATE', 'SITEZIP5']]
    df = df[pandas.notnull(df['SITEADDRESS'])]
    print(df)
    #print(df.ix[0])
    df.loc[:,'SITESTATE']
    #df.groupby(level=[0, 1]).agg({"SITEADDRESS": strJoin, "value": np.sum})
    for index, row in df.iterrows():
        Address = row['SITEADDRESS'] + ' ' + row['SITECITY'] + ' ' +row['SITESTATE'] + ' ' + str(int(row['SITEZIP5']))
        print(Address,type(Address))
        #using google map
        url = serviceurl + urllib.parse.urlencode({'sensor': 'false', 'address': address})
        uh = urllib.request.urlopen(url)
        data = uh.read()
        tree = ET.fromstring(data)
        results = tree.findall('result')
        lat = float(results[0].find('geometry').find('location').find('lat').text)
        lng = float(results[0].find('geometry').find('location').find('lng').text)
        location = results[0].find('formatted_address').text
        print('Google Map:', (lat, lng))
        # using openlayer
        geolocator = Nominatim()
        location = geolocator.geocode(Address)
        print(location.address)
        print('OpenLayer:', (location.latitude, location.longitude))
        time.sleep(3)
'''


