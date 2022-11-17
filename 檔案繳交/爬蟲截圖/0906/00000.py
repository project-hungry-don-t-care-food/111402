from math import*
def Distance1(Lat_A,Lng_A,Lat_B,Lng_B): #第一種計算方法
    ra=6378.140 #赤道半徑
    rb=6356.755 #極半徑 （km）
    flatten=(ra-rb)/ra  #地球偏率
    rad_lat_A=radians(Lat_A)
    rad_lng_A=radians(Lng_A)
    rad_lat_B=radians(Lat_B)
    rad_lng_B=radians(Lng_B)
    pA=atan(rb/ra*tan(rad_lat_A))
    pB=atan(rb/ra*tan(rad_lat_B))
    xx=acos(sin(pA)*sin(pB)+cos(pA)*cos(pB)*cos(rad_lng_A-rad_lng_B))
    c1=(sin(xx)-xx)*(sin(pA)+sin(pB))**2/cos(xx/2)**2
    c2=(sin(xx)+xx)*(sin(pA)-sin(pB))**2/sin(xx/2)**2
    dr=flatten/8*(c1-c2)
    distance=ra*(xx+dr)
    return distance

def Distance2(lat1,lng1,lat2,lng2):# 第二種計算方法
    radlat1=radians(lat1)  
    radlat2=radians(lat2)  
    a=radlat1-radlat2  
    b=radians(lng1)-radians(lng2)  
    s=2*asin(sqrt(pow(sin(a/2),2)+cos(radlat1)*cos(radlat2)*pow(sin(b/2),2)))  
    earth_radius=6378.137  
    s=s*earth_radius  
    if s<0:  
        return -s  
    else:  
        return s

Lat_A=25.04193588943503; Lng_A=121.52562935866969 # 南京
Lat_B=25.04384; Lng_B=121.52198 # 北京
distance=Distance1(Lat_A,Lng_A,Lat_B,Lng_B)
print('(Lat_A, Lng_A)=({0:.6f},{1:.6f})'.format(Lat_A,Lng_A))
print('(Lat_B, Lng_B)=({0:.6f},{1:.6f})'.format(Lat_B,Lng_B))
print('Distance1={0:.3f} km'.format(distance))
print('Distance2={0:.3f} km'.format(Distance2(Lat_A,Lng_A,Lat_B,Lng_B)))

25.043073836541968, 121.52481112120324