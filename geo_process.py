import buildGraph as bg
import feature as f
import urllib as ul
import googlemaps as gmaps
import time
import os


def get_geocode(address):
    """obtain a geocode of an address by using google map api"""
    client = gmaps.Client(key='AIzaSyBCOzFObKjRYYXE6OQQrwHqKBo_u3Ryb4o')
    tmp = client.geocode(address)
    print(tmp)
    print(address)
    if len(tmp)<=0:
        return ("","")
    for component in tmp:
        
        lat = float(component['geometry']['location']['lat'])
        lng = float(component['geometry']['location']['lng'])

        if lat > 0:
            break
    
    return (lat, lng)

def geoProcess(hometown_list):
    
    filename = "../output/HT_geo_info.txt"
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    fr = open(filename, mode='r')
    skip = len(fr.readlines())
    fr.close()
    
    print("Skip ="+str(skip))
    fw = open(filename, mode='a')
    i =0
    for spot in hometown_list:
        
        if i < skip:
            i=i+1
            continue
        geo = get_geocode(spot)
        fw.write(spot+"\t"+str(geo[0])+"\t"+str(geo[1])+"\n")
        print(geo)
        print("==========")
        fw.flush()
        time.sleep(1)
        
        
        
    fw.close()
    

graph,hometown_list= bg.build_graph()
print(hometown_list)
print("how much ht:"+str(len(hometown_list)))
geoProcess(hometown_list)

