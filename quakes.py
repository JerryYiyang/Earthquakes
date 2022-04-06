import quake_funcs
import sys
from utils import time_to_str, get_json


def main():
    nfile = open(sys.argv[1], "r")
    quakes = quake_funcs.read_quakes_from_file(nfile)
    print_quakes(quakes)
    choice = None
    sorted_ = quakes

    while choice != 'q':
        choice = get_choice()
        if choice.lower() == 's':
            sort_choice = input('Sort by (m)agnitude, (t)ime, (l)ongitude,'
                                'or l(a)titude? ')
            sorting(sort_choice, quakes, sorted_)
        elif choice.lower() == 'f':
            filter_choice = input('Filter by (m)agnitude or (p)lace? ')
            filtering(filter_choice, quakes, sorted_)
        elif choice.lower() == 'n':
            new_quakes = get_new_quake(quakes)
            if new_quakes[1]:
                print('\nNew quakes found!!!\n')
                print_quakes(quakes)
            elif new_quakes[1] is False:
                print()
                print_quakes(quakes)
        elif choice.lower() == 'q':
            write_to_file(sys.argv[1], quakes)
        elif choice.lower() != ('s' or 'f' or 'n' or 'q'):
            print('You must input "s", "f", "n", or "q"!')
            choice = get_choice()
        elif choice == 'q':
            print_quakes(quakes)
    nfile.close()


def print_quakes(quakes):
    print('Earthquakes:\n------------')
    for quake in quakes:
        mag = float(quake.mag)
        place = quake.place
        time = time_to_str(int(quake.time))
        long_ = quake.longitude
        lat = quake.latitude
        print('(%.2f) %40s at %s (%4.3f, %.3f)'
              % (mag, place, time, long_, lat))
    print()


def get_choice():
    return input('Options:\n  (s)ort\n  (f)ilter\n  (n)ew quakes'
                 '\n  (q)uit\n\nChoice: ')


def sorting(sort_choice, quakes, sorted_):
    if sort_choice.lower() == 'm':
        quake_funcs.sort_mag(quakes)
        quake_funcs.sort_mag(sorted_)
        print()
        print_quakes(quakes)
    elif sort_choice.lower() == 't':
        quake_funcs.sort_time(quakes)
        quake_funcs.sort_time(sorted_)
        print()
        print_quakes(quakes)
    elif sort_choice.lower() == 'l':
        quake_funcs.sort_long(quakes)
        quake_funcs.sort_long(sorted_)
        print()
        print_quakes(quakes)
    elif sort_choice.lower() == 'a':
        quake_funcs.sort_lat(quakes)
        quake_funcs.sort_lat(sorted_)
        print()
        print_quakes(quakes)
    elif sort_choice.lower() != ('m' or 't' != 'l' != 'a'):
        print('You must input "m", "t", "l", or "a"!')
        sort_choice = input('Sort by (m)agnitude, (t)ime, (l)ongitude,'
                            'or l(a)titude? ')


def filtering(filter_choice, quakes, sorted_):
    if filter_choice.lower() == 'm':
        low = float(input('Lower bound: '))
        high = float(input('Upper bound: '))
        filtered = quake_funcs.filter_by_mag(sorted_, low, high)
        print()
        print_quakes(filtered)
    elif filter_choice.lower() == 'p':
        word = input('Search for what string? ')
        filtered = quake_funcs.filter_by_place(sorted_, word)
        print()
        print_quakes(filtered)


def get_new_quake(quakes):
    new_quakes = get_json(
            'http://earthquake.usgs.gov/earthquakes/feed'
            '/v1.0/summary/1.0_hour.geojson')
    features = new_quakes['features']
    count = 0
    new_quake_check = False
    for i in range(len(features)):
        new_quake = quake_funcs.quake_from_feature(features[i])
        for i in range(len(quakes)):
            if quakes[i] == new_quake:
                count += 1
        if count == 0:
            quakes.append(new_quake)
            new_quake_check = True

    return (quakes, new_quake_check)


def write_to_file(filex, quakes):
    file_out = open(filex, "w")
    for quake in quakes:
        place = quake.place
        mag = quake.mag
        long_ = quake.longitude
        lat = quake.latitude
        time = int(quake.time)
        file_out.write("%s %s %s %s %s\n" % (mag, long_, lat, time, place))

    file_out.close


if __name__ == '__main__':
    main()
