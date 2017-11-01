# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 15:07:41 2017

@author: pyang
"""
import math
import pandas
import os
import numpy
WorkspaceRoot = os.getcwd()
csvfile = os.path.join(WorkspaceRoot, 'coordinatelFile.csv')
csvfile = os.path.join(WorkspaceRoot, 'ALLcoordinatelFile.txt')
#def Distance(series):
#    return 100*(math.exp((17.625* series['dewpoint_c'])/(243.04 + series['dewpoint_c']))/math.exp((17.625*series['temp_c'])/(243.04+series['temp_c'])))

from math import cos, asin, sqrt
def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295     #Pi/180
    a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))*1000 #2*R*asin..


# def deg2rad(deg):
#   return deg * (math.pi/180)
#
# def getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2):
#   R = 6371; # Radius of the earth in km
#   dLat = deg2rad(lat2-lat1) #deg2rad below
#   dLon = deg2rad(lon2-lon1)
#   a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2)) * math.sin(dLon/2) * math.sin(dLon/2)
#   c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
#   d = R * c # Distance in km
#   return d



def calc_dist(series):
    #print(series.loc["Lon_OpenLayer"])
    #print(len(series))
    #print(series.iloc[0],series.iloc[1],series.iloc[2],series.iloc[3])
    (lat1,lon1) = (series.iloc[0],series.iloc[1])
    (lat2,lon2) = (series.iloc[2],series.iloc[3])
    #print(x1,y1,x2,y2)
    if lat1 == -999.0:
        return -9999
    else:
        #return getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2)*1000 #multiply 1000 (1KM) for meters
        return distance(lat1,lon1,lat2,lon2)
    #Probabaly need to projected to get the real world distance
    #return math.sqrt(((y2 - y1)*(y2 - y1))  + ((x2 - x1)*(x2 - x1)))


def calc_confidence(series):
    # assump there are three levels 1,2,3 the higher the closer
    #have to consider the no data value (-9999) use 0 for the -9999
    if -9999 in (series.loc["disOpenLayer"],series.loc["disGoogle"],series.loc["disTamu"]):
        print("there are 0s ")
    return  (1,2,3)

def calc_confidence(series):
    # oc = series.iloc[0]
    # gc = series.iloc[1]
    # tc = series.iloc[2]
    oc, gc, tc = 0,0,0
    VL = [series.iloc[0],series.iloc[1],series.iloc[2]]
    if -9999 in VL:
        #print(VL)
        #put the -9999 with value -1
        if series.iloc[0] == -9999:
            oc = -1
            if series.iloc[1] == -9999:
                gc = -1
                tc = 3
            elif series.iloc[2] == -9999:
                tc = -1
                gc = 3
            else:
                if series.iloc[1] < series[2]:
                    gc,tc = (3,2)
                else:
                    gc,tc = (2,3)
        elif series.iloc[1] == -9999:
            gc = -1
            if series.iloc[0] == -9999:
                oc = -1
                tc = 3
            elif series.iloc[2] == -9999:
                tc = -1
                gc = 3
            else:
                if series.iloc[0] < series[2]:
                    oc,tc = (3,2)
                else:
                    oc,tc = (2,3)
        elif series.iloc[2] == -9999:
            tc = -1
            if series.iloc[0] == -9999:
                oc = -1
                gc = 3
            elif series.iloc[1] == -9999:
                tc = -1
                oc = 3
            else:
                if series.iloc[0] < series[1]:
                    oc,tc = (3,2)
                else:
                    oc,tc = (2,3)
    else:
        if max(VL) == series.iloc[0]:
            oc = 3
            if series.iloc[1] < series.iloc[2]:
                gc,tc = (2,1)
            else:
                gc,tc = (1,2)

        if max(VL) == series.iloc[1]:
            gc = 3
            if series.iloc[0] < series.iloc[2]:
                oc, tc = (2, 1)
            else:
                oc, tc = (1, 2)
        if max(VL) == series.iloc[2]:
            tc = 3
            if series.iloc[0] < series.iloc[1]:
                oc, gc = (2, 1)
            else:
                oc, gc = (1, 2)
    #print(oc,gc,tc)

    return pandas.Series({'ConfidenceOpenLayer' : oc, 'ConfidenceGoogle' : gc,'ConfidenceTamu' : tc,'GUID':series['GUID']})

#Examples
#https://stackoverflow.com/questions/16236684/apply-pandas-function-to-column-to-create-multiple-new-columns
#https://stackoverflow.com/questions/15118111/apply-function-to-each-row-of-pandas-dataframe-to-create-two-new-columns
pandas.set_option('display.float_format', lambda x: '%.3f' % x)
with open(csvfile) as csv:
    df = pandas.read_csv(csv)#,sep=' ')
    #print(df)
    #'GUID', 'Lat_OpenLayer', 'Lon_OpenLayer', 'Lat_Google', 'Lon_Google','Lat_Tamu', 'Lon_Tamu', 'Lat_Ref', 'Lon_Ref'
    #'GUID', 'OpenLayer', 'Google', 'Tamu', 'Ref'
    #df.loc[:,'CoorOpenLayer'] = '(' + df.loc[:,'Lat_OpenLayer'] + ',' + df.loc[:,'Lon_OpenLayer'] +')'
    #df.loc[:,'dicOpenLayer'] = df.apply(calc_dist)
    print(df.columns)
    df.loc[:,'disOpenLayer'] = df.loc[:,['Lat_OpenLayer', 'Lon_OpenLayer','Lat_Ref', 'Lon_Ref']].apply(calc_dist,axis=1)
    df.loc[:,'disGoogle'] = df.loc[:, ['Lat_Google', 'Lon_Google', 'Lat_Ref', 'Lon_Ref']].apply(calc_dist,axis=1)
    df.loc[:,'disTamu'] = df.loc[:, ['Lat_Tamu', 'Lon_Tamu', 'Lat_Ref', 'Lon_Ref']].apply(calc_dist, axis=1)
    #Here do a little bit of statistic analyses
    des_OpenLayer = df.loc[:,'disOpenLayer'].describe()
    des_Google = df.loc[:,'disGoogle'].describe()
    des_Tamu = df.loc[:,'disTamu'].describe()
    print des_OpenLayer,des_Google,des_Tamu
    g = numpy.array(df.loc[:,'disGoogle'])
    p93_g = numpy.percentile(g,93)
    t = numpy.array(df.loc[:,'disTamu'])
    p93_t = numpy.percentile(t,93)
    print p93_g,p93_t
"""
    df_conf = df.loc[:, ['disOpenLayer', 'disGoogle', 'disTamu','GUID']].apply(calc_confidence, axis=1)
    #print(df.loc[:,('disOpenLayer','disGoogle','disTamu')])
    # df.loc[:, 'ConfidenceOpenLayer'] = df.loc[:, ['disOpenLayer', 'disGoogle', 'disTamu']].apply(calc_confidence, axis=1)
    # df.loc[:, 'ConfidenceGoogle']    = df.loc[:, ['disOpenLayer', 'disGoogle','disTamu']].apply(calc_confidence, axis=1)
    # df.loc[:, 'ConfidenceTamu'] = df.loc[:, ['disOpenLayer', 'disGoogle','disTamu']].apply(calc_confidence, axis=1)
    df = pandas.merge(df,df_conf,on = 'GUID')

    df = pandas.concat([df, pandas.DataFrame(df.sum(axis=0), columns=['Total']).T])
    print(df)
    #print(df.iloc[:, {'ConfidenceOpenLayer','ConfidenceGoogle','ConfidenceTamu'}])
    ##create confidence level from the existing three service based on spatial distance

    df.to_csv("ConfidenceLevel_3.csv")
    #df.loc[:,'dicOpenLayer'] = df.loc[:,['Lat_OpenLayer', 'Lon_OpenLayer','Lat_Ref', 'Lon_Ref']].apply(calc_dist)

    #s = df.ix[:,['Lat_OpenLayer', 'Lon_OpenLayer','Lat_Ref', 'Lon_Ref']]
    #df.loc[:,'DisOpenLayer'] = df.apply(calc_dist,axis = 1)
#    df = pread[['SITEADDRESS','SITECITY','SITESTATE', 'SITEZIP5']]
#    df = df[pandas.notnull(df['SITEADDRESS'])]
#    print(df)
#    #print(df.ix[0])
#    df.loc[:,'SITESTATE']
#    #df.groupby(level=[0, 1]).agg({"SITEADDRESS": strJoin, "value": np.sum})
#    for index, row in df.iterrows():
#        Address = row['SITEADDRESS'] + ' ' + row['SITECITY'] + ' ' +row['SITESTATE'] + ' ' + str(int(row['SITEZIP5']))
#        print(Address,type(Address))
#        #using google map
#        url = serviceurl + urllib.parse.urlencode({'sensor': 'false', 'address': address})
#        uh = urllib.request.urlopen(url)
#        data = uh.read()
#        tree = ET.fromstring(data)
#        results = tree.findall('result')
#        lat = float(results[0].find('geometry').find('location').find('lat').text)
#        lng = float(results[0].find('geometry').find('location').find('lng').text)
#        location = results[0].find('formatted_address').text
#        print('Google Map:', (lat, lng))
#        # using openlayer
#        geolocator = Nominatim()
#        location = geolocator.geocode(Address)
#        print(location.address)
#        print('OpenLayer:', (location.latitude, location.longitude))
"""
