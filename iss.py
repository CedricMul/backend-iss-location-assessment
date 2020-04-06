#!/usr/bin/env python
import turtle
import requests
import time


__author__ = 'Cedric Mulvihill, Madar tutorial'


def get_crew():
    r = requests.get('http://api.open-notify.org/astros.json')
    r.raise_for_status()
    return r.json()['people']

def get_iss_location():
    r = requests.get('http://api.open-notify.org/iss-now.json')
    r.raise_for_status()
    position = r.json()['iss_position']
    lat = float(position['latitude'])
    lon = float(position['longitude'])
    return lat, lon

def map_iss(lat,lon):
    screen = turtle.Screen()
    screen.setup(720,360)
    screen.bgpic('map.gif')
    screen.setworldcoordinates(-180, -90, 180, 90)
    screen.register_shape('iss.gif')
    iss = turtle.Turtle()
    iss.shape('iss.gif')
    iss.setheading(90)
    iss.penup()
    iss.goto(lon, lat)
    return screen

def get_rise_time(lat, lon):
    param = {'lat': lat, 'lon': lon}
    r = requests.get('http://api.open-notify.org/iss-pass.json',
            params=param)
    r.raise_for_status()
    passover = r.json()['response'][1]['risetime']
    return time.ctime(passover)


def main():
    crew_dict = get_crew()
    print('Current people in space: {}'.format(len(crew_dict)))
    for i in crew_dict:
        print("- {} in {}".format(i['name'], i['craft']))
    
    lat, lon = get_iss_location()
    print('ISS coordinates: lat {:.02f}, lon {:.02f}'.format(lat, lon))

    print('Next Rise Time for Indy: {}'.format(get_rise_time(39.768403, -86.158068)))
    screen = None
    screen = map_iss(lat, lon)

    indy_lat = 39.768403
    indy_lon = -86.158068
    location = turtle.Turtle()
    location.penup()
    location.color('yellow')
    location.goto(indy_lon, indy_lat)
    location.dot(5)
    location.hideturtle()
    if screen is not None:
        screen.exitonclick()



if __name__ == '__main__':
    main()
