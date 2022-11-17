from math import*

def Distance1(lat1,lng1,lat2,lng2):# 第二種計算方法
    radlat1 = radians(lat1)  
    radlat2 = radians(lat2)  
    a = radlat1-radlat2  
    b = radians(lng1)-radians(lng2)  
    s = 2*asin(sqrt(pow(sin(a/2),2)+cos(radlat1)*cos(radlat2)*pow(sin(b/2),2)))  
    earth_radius = 6378.137  
    s = s*earth_radius  
    if s < 0:  
        return -s  
    else:  
        return s


Lat_A = 25.05430; Lng_A=121.52221 # ntub

Lat_B=39.904211; Lng_B=116.407395 # 北京
distance=Distance1(Lat_A,Lng_A,Lat_B,Lng_B)
print('(Lat_A, Lng_A)=({0:.6f},{1:.6f})'.format(Lat_A,Lng_A))
print('(Lat_B, Lng_B)=({0:.6f},{1:.6f})'.format(Lat_B,Lng_B))
print('Distance1={0:.3f} km'.format(Distance1(Lat_A,Lng_A,Lat_B,Lng_B)))