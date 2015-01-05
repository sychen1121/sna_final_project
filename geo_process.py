import buildGraph as bg
import feature as f
import urllib as ul
import googlemaps as gmaps
import time
import os


def get_geocode(address):
    """obtain a geocode of an address by using google map api"""
    client = gmaps.Client(key='AIzaSyABja4kcCMTjVLYMepiO5q2MtoWuxfK7NI')
    tmp = client.geocode(address)
    print(tmp)
    print(address)
    if len(tmp)<=1:
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
        
    fw = open(filename, mode='w')
    for spot in hometown_list:
        geo = get_geocode(spot)
        fw.write(spot+"\t"+str(geo[0])+"\t"+str(geo[1])+"\n")
        print(geo)
        print("==========")
        time.sleep(2)
        
        
    fw.close()
    

graph,hometown_list= bg.build_graph()
print(hometown_list)
print("how much ht:"+str(len(hometown_list)))
geoProcess(hometown_list)

