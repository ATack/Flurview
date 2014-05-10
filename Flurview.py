# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        flurview
# Purpose:     create an info screen for my hallway
#
# Author:      Achim Tack
#
# Created:     10.05.2014
# Copyright:   (c) Achim Tack 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python


def main():
    pass


if __name__ == '__main__':
    main()

##################################################################################################################################
#Funktionen


def url_to_string(url):
    # function cycles randomly through different user agents simulate more natural queries
    import gc

    gc.collect()
    try:
        import urllib2
        import time
        from random import choice

        agents = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17',
            'Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0',
            'Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02',
            'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
            'Mozilla/3.0',
            'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543a Safari/419.3',
            'Mozilla/5.0 (Linux; U; Android 0.5; en-us) AppleWebKit/522+ (KHTML, like Gecko) Safari/419.3',
            'Opera/9.00 (Windows NT 5.1; U; en)']

        agent = choice(agents)
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', agent)]
        html = opener.open(url).read()
        sleep(1)

    except Exception as e:
        print "error in url_to_string"
        print e
        html = ""
        gc.collect()

    return html


def retrieve_weather_data(city):
    url = 'http://de.windfinder.com/weatherforecast/' + city

    html = url_to_string(url)

    #get precipitation
    precipitation = []
    precipitation_html = html.split(
        '<th class="rowname">Niederschlag (<a href="/settings"><span class="units-desc-pr">mm</span>/3h</a>)</th>')[
        1].split('<th class="rowname">Luftdruck (hPa)</th>')[0].split(' units-pr">')
    for e in precipitation_html:
        e = e.split('</div>')[0]
        e = e.replace('\n', '').replace('\t', '')
        try:
            precipitation.append(float(e))
        except:
            pass

    del precipitation[0:4]  # delete night hours from 0 to 4 o clock for better diagram readability

    print precipitation

    max_daily_precipitation = round(max(precipitation), 1)
    sum_daily_precipitation = sum(precipitation)

    try:
        drosselfaktor_kachelfarbe = int(round(sum_daily_precipitation / max_daily_precipitation))
    except:
        drosselfaktor_kachelfarbe = 0

    #get temperature
    temperature = []
    temperature_html = html.split('(<a href="/settings">&deg;<span class="units-desc-at">C</span></a>)</th>')[1].split(
        '<th class="rowname">')[0].split('units-at')
    for e in temperature_html:
        e = e.split('">')[1]
        e = e.split('</div>')[0]
        e = e.replace('\n', '').replace('\t', '')
        try:
            temperature.append(float(e))
        except:
            pass

    del temperature[0:4]  # delete night hours from 0 to 4 o clock for better diagram readability

    max_daily_temperature = int(max(temperature))

    #define tile colour
    temp_farberstellung = max_daily_temperature - drosselfaktor_kachelfarbe

    if temp_farberstellung <= 0:
        weather_tile_colour = "#9600fe"
        graphcolor = "#ffffff"
    elif 1 <= temp_farberstellung <= 5:
        weather_tile_colour = "#00e600"
        graphcolor = "#ffffff"
    elif 6 <= temp_farberstellung <= 10:
        weather_tile_colour = "#b8ff61"
        graphcolor = "#313131"
    elif 11 <= temp_farberstellung <= 15:
        weather_tile_colour = "#fec800"
        graphcolor = "#313131"
    elif 16 <= temp_farberstellung <= 20:
        weather_tile_colour = "#feae00"
        graphcolor = "#ffffff"
    elif 21 <= temp_farberstellung <= 25:
        weather_tile_colour = "#dc4a1d"
        graphcolor = "#ffffff"
    elif 26 <= temp_farberstellung <= 30:
        weather_tile_colour = "#b41419"
        graphcolor = "#ffffff"
    else:
        weather_tile_colour = "#b41419"
        graphcolor = "#ffffff"

    X_TempfarbeSchrift = graphcolor

    # create graph
    fig = plt.figure(frameon=False)
    fig.set_size_inches(9, 3)

    ax1 = fig.add_subplot(111)
    ax1.plot(precipitation, color=graphcolor, linestyle='dashed', linewidth=4.0)
    ax1.set_xlabel('', color=graphcolor, weight='bold')  #Uhrzeit
    ax1.tick_params(axis='x', colors=graphcolor)

    # Make the y-axis label and tick labels match the line color.
    #Niederschlag
    ax1.set_ylabel('', color=graphcolor, weight='bold')  #Niederschlag
    ax1.set_ylim(0, (max(precipitation) + 1.5))
    ax1.tick_params(axis='y', colors=graphcolor)
    for tl in ax1.get_yticklabels():
        tl.set_color(graphcolor)
        tl.set_weight('bold')

    #Temperatur
    ax2 = ax1.twinx()
    ax2.plot(temperature, color=graphcolor, linewidth=4.0)
    ax2.set_ylabel('', color=graphcolor, weight='bold')  #Temperatur
    ax2.set_ylim(0, (max(temperature) + 5))
    ax2.tick_params(axis='y', colors=graphcolor)

    for tl in ax2.get_yticklabels():
        tl.set_color(graphcolor)
        tl.set_weight('bold')

    for child in ax2.get_children():
        if isinstance(child, matplotlib.spines.Spine):
            child.set_color(graphcolor)

    xticks = ["6", "9", "12", "15", "18", "21", "24"]
    x = [1, 4, 7, 10, 13, 16, 19]
    plt.xticks(x, xticks)

    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_visible(False)
    ax1.spines['bottom'].set_visible(False)
    ax1.xaxis.set_ticks_position('none')

    savefig('images/wetter.png', transparent=True, dpi=300)

    gc.collect()
    return max_daily_temperature, max_daily_precipitation, weather_tile_colour, X_TempfarbeSchrift


def retrieve_bus_departures():
    import gc

    url = 'http://mobile.bahn.de/bin/mobil/bhftafel.exe/dox?evaId=694865&bt=dep&max=20&rt=1&disableEquivs=yes&p=1111111111&start=1&'
    html = url_to_string(url)

    departures = \
    html.split('<div class="haupt rline">')[1].split('<div class="formular">')[0].split('<ul class="neben">')[1].split(
        '<div class="clicktable">')[1].split('<div class="sqdetailsDep trow">')

    departure_list = []

    for departure in departures:
        if len(departure) >= 5:
            nummer = departure.split('<span class="bold">')[1].split('</span>')[0].replace('  ', ' ')
            zeit = departure.split('<span class="bold">')[2].split('</span>')[0]
            ziel = departure.split('&gt;&gt;')[1].split('<br />')[0].replace('\n', '')

            if ziel == 'Hauptbahnhof/ZOB, Hamburg':
                departure_list.append([nummer, zeit, ziel])

            if ziel == 'Trabrennbahn Bahrenfeld, Hamburg':
                departure_list.append([nummer, zeit, ziel])

            if ziel == 'Schenefelder Platz, Schenefeld (Bz Hamburg)':
                departure_list.append([nummer, zeit, ziel[0:18]])

    sorted(departure_list)

    try:
        bus1 = departure_list[0]
        bus1 = bus1[1] + " " + bus1[2]

    except:
        bus1 = ''

    try:
        bus2 = departure_list[1]
        bus2 = bus2[1] + " " + bus2[2]
    except:
        bus2 = ''

    try:
        bus3 = departure_list[2]
        bus3 = bus3[1] + " " + bus3[2]
    except:
        bus3 = ''

    try:
        bus4 = departure_list[3]
        bus4 = bus4[1] + " " + bus4[2]
    except:
        bus4 = ''

    gc.collect()
    return bus1, bus2, bus3, bus4


def create_bus_ticker(bus1, bus2, bus3):
    # get current time
    lt = localtime()
    date = strftime("%d.%m.%Y", lt)
    timestamp = strftime("%H:%M", lt)

    nextbus_1 = date + " " + bus1.split(' ')[0]
    nextbus_2 = date + " " + bus2.split(' ')[0]
    nextbus_3 = date + " " + bus3.split(' ')[0]

    nextbus1_time = datetime.datetime.strptime(nextbus_1, "%d.%m.%Y %H:%M")
    nextbus2_time = datetime.datetime.strptime(nextbus_2, "%d.%m.%Y %H:%M")
    nextbus3_time = datetime.datetime.strptime(nextbus_3, "%d.%m.%Y %H:%M")

    current_time = date + " " + timestamp

    # Parse the time strings
    current_time = datetime.datetime.strptime(current_time, "%d.%m.%Y %H:%M")
    nextbus1_time = datetime.datetime.strptime(nextbus_1, "%d.%m.%Y %H:%M")
    nextbus2_time = datetime.datetime.strptime(nextbus_2, "%d.%m.%Y %H:%M")
    nextbus3_time = datetime.datetime.strptime(nextbus_3, "%d.%m.%Y %H:%M")

    # Do the math, the result is a timedelta object
    delta_1 = nextbus1_time - current_time
    delta_2 = nextbus2_time - current_time
    delta_3 = nextbus3_time - current_time

    restzeit_1 = delta_1.seconds / 60
    restzeit_2 = delta_2.seconds / 60
    restzeit_3 = delta_3.seconds / 60

    restzeit_anzeige = restzeit_1

    if restzeit_1 > 10:
        bus_farbe = '#313131'
    elif 6 <= restzeit_1 <= 10:
        bus_farbe = '#029418'
    elif 4 <= restzeit_1 <= 5:
        bus_farbe = '#d99623'
    else:
        bus_farbe = '#b61b43'

    gc.collect()
    return date, timestamp, restzeit_anzeige, bus_farbe


def create_welcome_message():
    d = datetime.datetime.now()
    weekday = datetime.datetime.today().weekday()

    if weekday == 5:
        if 0 <= d.hour <= 7:
            m = "Weiter <br>schlafen!"
        elif 7 <= d.hour <= 9:
            m = "Frueh auf<br>heute..."
        elif 10 <= d.hour <= 19:
            m = "Wochenende!"
        elif 20 <= d.hour <= 20:
            m = "Nabend!"
        elif 22 <= d.hour <= 24:
            m = "Schlaft gut!"
        else:
            m = 'Hallo!'

    if weekday == 6:
        if 0 <= d.hour <= 7:
            m = "Weiter <br>schlafen!"
        elif 7 <= d.hour <= 9:
            m = "Frueh auf<br>heute..."
        elif 10 <= d.hour <= 19:
            m = "Wochenende!"
        elif 20 <= d.hour <= 20:
            m = "Nabend!"
        elif 22 <= d.hour <= 24:
            m = "Schlaft gut!"
        else:
            m = 'Hallo!'

    if weekday == 4:
        if 0 <= d.hour <= 4:
            m = "Weiter <br>schlafen!"
        elif 5 <= d.hour <= 9:
            m = "Viel Spass <br>heute!"
        elif 10 <= d.hour <= 11:
            m = "Moin!"
        elif 12 <= d.hour <= 22:
            m = "Wochenende!"
        elif 23 <= d.hour <= 24:
            m = "Ab ins<br>Bett!"
        else:
            m = 'Hallo!'

    else:
        if 0 <= d.hour <= 4:
            m = "Weiter <br>schlafen!"
        elif 5 <= d.hour <= 9:
            m = "Viel Spass <br>heute!"
        elif 10 <= d.hour <= 15:
            m = "Moin!"
        elif 16 <= d.hour <= 20:
            m = "Home!"
        elif 21 <= d.hour <= 22:
            m = "Schlaft gut!"
        elif 23 <= d.hour <= 24:
            m = "Ab ins<br>Bett!"
        else:
            m = 'Hallo!'

    gc.collect()
    return m


def retrieve_google_calendar_entries(url):
    import gc

    terminliste = {}
    terminliste_list = []

    html = url_to_string(url)

    entries = html.split("BEGIN:VEVENT")

    for entry in entries:

        try:
            entry_name = entry.split('SUMMARY:')[1].split('TRANSP:')[0].replace('\n', '').replace('\r', '')

            max = 25
            if len(entry_name) >= max:
                entry_name = entry_name[0:max] + '<br>' + entry_name[max:max * 2] + '<br>' + entry_name[max * 2:max * 3]
            else:
                pass

            entry_time = entry.split('DTSTART:')[1].split('DTEND:')[0].replace('\n', '').replace('\r', '')

            begin_date = entry_time[0:8]
            begin_date = datetime.datetime.strptime(begin_date, "%Y%m%d")

            begin_time = entry_time[9:13]

            if begin_date.date() == datetime.datetime.today().date():
                terminliste[begin_time] = entry_name

        except Exception as e:
            #print e
            pass

    for element in sorted(terminliste.iterkeys()):
        zeit = str(int(element) + 200)
        terminliste_list.append("%s: %s" % (zeit, terminliste[element]))  # Zeitumstellung + 200

    terminstring = str(terminliste_list).replace("', '", '<br><br>').replace("['", '<strong>').replace("']",'').replace(': ','</strong><br>').replace('[]', '<strong>keine Termine</strong>')

    gc.collect()
    return terminstring


def retrieve_driving_times():
    import gc

    trip_list = [('http://goo.gl/maps/nHbsb', 'Schuetzenstrasse Mitte', 20),
                 ('http://goo.gl/maps/1yi0a', 'Hauptbahnhof', 4),
                 ('http://goo.gl/maps/k3u7r', 'EDEKA Wilhelmsburg', 11),
                 ('http://goo.gl/maps/QVMQC', 'MVZ Meckelfeld', 22)]

    output_string_list = []

    for trip in trip_list:
        trip_url = trip[0]
        trip_name = trip[1]
        driving_time_nominal = trip[2]

        try:
            html = url_to_string(trip_url)
            driving_time_current = float(
                html.split('<span>Bei aktueller Verkehrslage: ')[1].split(' Minuten</span>')[0].replace('\n', ''))
        except Exception as e:
            driving_time_current = driving_time_nominal

        driving_time_deviation = driving_time_current - driving_time_nominal

        if driving_time_deviation == 1:
            output_string = "<strong>" + trip_name + ":</strong><br>" + str(driving_time_deviation).replace(".0","") + " Minute langsamer"
        elif driving_time_deviation > 1:
            output_string = "<strong>" + trip_name + ":</strong><br>" + str(driving_time_deviation).replace(".0","") + " Minuten langsamer"
        else:
            output_string = "<strong>" + trip_name + ":</strong><br>" + "keine Staumeldungen"

        output_string_list.append(output_string)

    driving_time_output = output_string_list[0] + "<p>" + output_string_list[1] + "<p>" + output_string_list[
        2] + "<p>" + output_string_list[3]

    gc.collect()
    return driving_time_output


def retrieve_water_level(url):
    import gc

    try:
        html = url_to_string(url)

        water_level_html = html.split('"eng">Measurement (Raw Data)')[1].split('</TABLE>')[0]

        current_water_level = int(
            water_level_html.split('</TR>')[2].split('<TD headers="pn" align="center">')[1].split('</TD>')[0])
        previous_water_level = int(
            water_level_html.split('</TR>')[3].split('<TD headers="pn" align="center">')[1].split('</TD>')[0])
        change_water_level = current_water_level - previous_water_level

        if change_water_level >= 5:
            message = " steigend"
        elif change_water_level <= -5:
            message = " fallend"
        else:
            message = " gleichbleibend"

        message = str(current_water_level).replace('.0', '') + "cm, " + message

        gc.collect()

    except:
        message = "keine Werte"
        gc.collect()

    gc.collect()
    return message


def create_fleisssternchen(fleiss_url):
    import gc

    html = url_to_string(fleiss_url)

    An_Curr = float(html.split("An_Curr")[1].split("\n")[0].replace(',', '.'))
    Ac_Curr = float(html.split("Ac_Curr")[1].split("\n")[0].replace(',', '.'))
    An_Prev = float(html.split("An_Prev")[1].split("\n")[0].replace(',', '.'))
    Ac_Prev = float(html.split("Ac_Prev")[1].split("\n")[0].replace(',', '.'))
    An_Curr_W = float(html.split("An_Curr_W")[1].split("\n")[0].replace(',', '.'))
    Ac_Curr_W = float(html.split("Ac_Curr_W")[1].split("\n")[0].replace(',', '.'))

    if An_Curr_W > Ac_Curr_W:
        X_Fleissfarbe = "#ff6699"
    elif An_Curr_W < Ac_Curr_W:
        X_Fleissfarbe = "#6699ff"
    else:
        X_Fleissfarbe = "#d99623"

    if An_Prev > Ac_Prev:
        X_Sieger = "Anne"
    else:
        X_Sieger = "Achim"

    gc.collect()
    return An_Curr, Ac_Curr, An_Prev, Ac_Prev, X_Fleissfarbe, An_Curr_W, Ac_Curr_W, X_Sieger


##################################################################################################################################
# main program

#import modules
import gc
import csv
from time import *

from pylab import *
import matplotlib.pyplot as plt


#import variables from external csv
variable_list = []
reader = csv.reader(open("variables.csv", "rb"))
for row in reader:
    variable_list.append(row)

calendar_url_person_1 = str(variable_list[0][0])
calendar_url_person_2 = str(variable_list[1][0])
fleiss_url = str(variable_list[2][0])
weather_location = str(variable_list[3][0])


# generate values before first run
welcome_message_string = create_welcome_message()
weather_data = retrieve_weather_data(weather_location)
calendar_string_person_1 = retrieve_google_calendar_entries(calendar_url_person_1)
calendar_string_person_2 = retrieve_google_calendar_entries(calendar_url_person_2)

busse = retrieve_bus_departures()

bus_0 = busse[0].replace(', Hamburg', '')
bus_1 = busse[1].replace(', Hamburg', '')
bus_2 = busse[2].replace(', Hamburg', '')
bus_3 = busse[3].replace(', Hamburg', '')

busticker_daten = create_bus_ticker(bus_0, bus_1, bus_2)

driving_time_increase = retrieve_driving_times()

water_level_stpauli = retrieve_water_level('http://www.bsh.de/aktdat/wvd/StPauli_pgl.htm')
water_level_zollenspieker = retrieve_water_level('http://www.bsh.de/aktdat/wvd/Zollenspieker_pgl.htm')
water_level_schulau = retrieve_water_level('http://www.bsh.de/aktdat/wvd/Schulau_pgl.htm')

fleiss_person2_curr = str(create_fleisssternchen(fleiss_url)[0])
fleiss_person1_curr = str(create_fleisssternchen(fleiss_url)[1])
fleiss_person2_prev = str(create_fleisssternchen(fleiss_url)[2])
fleiss_person1_prev = str(create_fleisssternchen(fleiss_url)[3])
X_Fleissfarbe = str(create_fleisssternchen(fleiss_url)[4])
fleiss_person2_curr_w = str(create_fleisssternchen(fleiss_url)[5])
fleiss_person1_curr_w = str(create_fleisssternchen(fleiss_url)[6])
fleiss_sieger = str(create_fleisssternchen(fleiss_url)[7])

gc.collect()

#begin main loop
while True:

    try:
        # refresh data at specific times
        current_time = datetime.datetime.now()

        if current_time.hour == 5 and current_time.minute == 0:
            try:
                print 'Stunde 0'
                weather_data = retrieve_weather_data(weather_location)
                sleep(20)
                gc.collect()
            except:
                gc.collect()
                pass

        if current_time.hour == 12 and current_time.minute == 0:
            try:
                print 'Stunde 12'
                weather_data = retrieve_weather_data(weather_location)
                sleep(20)
                gc.collect()
            except:
                gc.collect()
                pass

        if current_time.hour == 15 and current_time.minute == 0:
            try:
                print 'Stunde 15'
                weather_data = retrieve_weather_data(weather_location)
                sleep(20)
                gc.collect()
            except:
                gc.collect()
                pass

        if current_time.minute == 0:
            try:
                print 'Minute 0'
                welcome_message_string = create_welcome_message()
                calendar_string_person_1 = retrieve_google_calendar_entries(calendar_string_person_1)
                calendar_string_person_2 = retrieve_google_calendar_entries(calendar_string_person_2)
                driving_time_increase = retrieve_driving_times()
                water_level_stpauli = retrieve_water_level('http://www.bsh.de/aktdat/wvd/StPauli_pgl.htm')
                water_level_zollenspieker = retrieve_water_level('http://www.bsh.de/aktdat/wvd/Zollenspieker_pgl.htm')
                water_level_schulau = retrieve_water_level('http://www.bsh.de/aktdat/wvd/Schulau_pgl.htm')
                fleiss_person2_curr = str(create_fleisssternchen(fleiss_url)[0])
                fleiss_person1_curr = str(create_fleisssternchen(fleiss_url)[1])
                fleiss_person2_prev = str(create_fleisssternchen(fleiss_url)[2])
                fleiss_person1_prev = str(create_fleisssternchen(fleiss_url)[3])
                X_Fleissfarbe = str(create_fleisssternchen(fleiss_url)[4])
                fleiss_person2_curr_w = str(create_fleisssternchen(fleiss_url)[5])
                fleiss_person1_curr_w = str(create_fleisssternchen(fleiss_url)[6])
                fleiss_sieger = str(create_fleisssternchen(fleiss_url)[7])
                gc.collect()
            except Exception as e:
                gc.collect()
                print e
                pass

        if current_time.minute == 15:
            try:
                print 'Minute 15'
                welcome_message_string = create_welcome_message()
                driving_time_increase = retrieve_driving_times()
                water_level_stpauli = retrieve_water_level('http://www.bsh.de/aktdat/wvd/StPauli_pgl.htm')
                water_level_zollenspieker = retrieve_water_level('http://www.bsh.de/aktdat/wvd/Zollenspieker_pgl.htm')
                water_level_schulau = retrieve_water_level('http://www.bsh.de/aktdat/wvd/Schulau_pgl.htm')
                gc.collect()
            except:
                gc.collect()
                pass

        if current_time.minute == 30:
            try:
                print 'Minute 30'
                welcome_message_string = create_welcome_message()
                calendar_string_person_1 = retrieve_google_calendar_entries(calendar_string_person_1)
                calendar_string_person_2 = retrieve_google_calendar_entries(calendar_string_person_2)
                driving_time_increase = retrieve_driving_times()
                water_level_stpauli = retrieve_water_level('http://www.bsh.de/aktdat/wvd/StPauli_pgl.htm')
                water_level_zollenspieker = retrieve_water_level('http://www.bsh.de/aktdat/wvd/Zollenspieker_pgl.htm')
                water_level_schulau = retrieve_water_level('http://www.bsh.de/aktdat/wvd/Schulau_pgl.htm')
                gc.collect()
            except:
                gc.collect()
                pass

        if current_time.minute == 45:
            try:
                print 'Minute 45'
                welcome_message_string = create_welcome_message()
                driving_time_increase = retrieve_driving_times()
                water_level_stpauli = retrieve_water_level('http://www.bsh.de/aktdat/wvd/StPauli_pgl.htm')
                water_level_zollenspieker = retrieve_water_level('http://www.bsh.de/aktdat/wvd/Zollenspieker_pgl.htm')
                water_level_schulau = retrieve_water_level('http://www.bsh.de/aktdat/wvd/Schulau_pgl.htm')
                gc.collect()
            except:
                gc.collect()
                pass


        # refresh bus information on a 45sec interval
        busse = retrieve_bus_departures()

        bus_0 = busse[0].replace(', Hamburg', '')
        bus_1 = busse[1].replace(', Hamburg', '')
        bus_2 = busse[2].replace(', Hamburg', '')
        bus_3 = busse[3].replace(', Hamburg', '')

        busticker_daten = create_bus_ticker(bus_0, bus_1, bus_2)

        current_date_string = str(busticker_daten[0])
        current_time_string = str(busticker_daten[1])
        minutes_until_next_departure = str(busticker_daten[2])
        bus_tile_colour = str(busticker_daten[3])

        # Insert data into html

        #OEPNV
        data = open("index_template.html").read()
        data = data.replace('X_BUS1', bus_1)
        data = data.replace('X_BUS2', bus_2)
        data = data.replace('X_BUS3', bus_3)
        data = data.replace('X_RESTZEIT', minutes_until_next_departure + " Min.")
        data = data.replace('X_DATUM', current_date_string)
        data = data.replace('X_UHRZEIT', current_time_string)
        data = data.replace('X_NEXTBUS', bus_0)
        data = data.replace('X_Busfarbe', bus_tile_colour)

        #VERKEHR
        data = data.replace('X_FAHRZEIT', driving_time_increase)

        #WETTER
        data = data.replace('X_TEMP', str(weather_data[0]) + "°C   ")
        data = data.replace('X_RAIN', str(weather_data[1]) + "mm ")
        data = data.replace('X_Tempfarbe', weather_data[2])
        data = data.replace('X_ColourText', weather_data[3])

        #ELBWASSERSTAND
        data = data.replace('X_PEGEL_1', water_level_stpauli)
        data = data.replace('X_PEGEL_2', water_level_zollenspieker)
        data = data.replace('X_PEGEL_3', water_level_schulau)

        #WILLKOMMEN
        data = data.replace('X_MESSAGE', welcome_message_string)

        #KALENDER
        data = data.replace('X_AchimKAL', calendar_string_person_1)
        data = data.replace('X_AnneKAL', calendar_string_person_2)

        #FLEISSSTERNCHEN
        data = data.replace('X_Akt_Anne', fleiss_person2_curr)
        data = data.replace('X_Akt_Achim', fleiss_person1_curr)
        data = data.replace('X_Akt_W_Anne', fleiss_person2_curr_w)
        data = data.replace('X_Akt_W_Achim', fleiss_person1_curr_w)
        data = data.replace('X_Sieger', fleiss_sieger)
        data = data.replace('X_Fleissfarbe', X_Fleissfarbe)

        o = open("index.html", "w")
        o.write(data)
        o.close()

        gc.collect()

    except Exception as e:
        print e
        gc.collect()

    finally:
        sleep(20)
        gc.collect()

    gc.collect()
    sleep(45)