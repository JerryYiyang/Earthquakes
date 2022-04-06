from math import isclose


class Earthquake:
    """A class to represent an Earthquake."""
    def __init__(self, place, mag, longitude, latitude, time):
        self.place = place
        self.mag = mag
        self.longitude = longitude
        self.latitude = latitude
        self.time = time

    def __eq__(self, other):
        return(
                self.place == other.place and
                isclose(self.mag, other.mag) and
                isclose(self.longitude, other.longitude) and
                isclose(self.latitude, other.latitude) and
                isclose(self.time, other.time)
                )


def quake_from_feature(feature):
    place = feature['properties']['place']
    mag = float(feature['properties']['mag'])
    long_ = float(feature['geometry']['coordinates'][0])
    lat = float(feature['geometry']['coordinates'][1])
    time = int(feature['properties']['time']) / 1000
    quake = Earthquake(place, mag, long_, lat, time)

    return quake


# NOTE: This function takes an already open file as input.  You *will not*
# be opening anything in this function.
def read_quakes_from_file(file):
    nfile = file
    quakes = []

    for line in nfile:
        location = []
        indv_data = line.split()
        location = indv_data[4:]
        place = ' '.join(location)

        mag = float(indv_data[0])
        longitude = float(indv_data[1])
        latitude = float(indv_data[2])
        time = float(indv_data[3])

        data = Earthquake(place, mag, longitude, latitude,
                          int(time))
        quakes.append(data)

    return quakes


def filter_by_mag(quakes, low, high):
    mag_list = []

    for quake in quakes:
        if quake.mag >= float(low) and quake.mag <= float(high):
            mag_list.append(quake)

    return mag_list


def filter_by_place(quakes, word):
    quakes_list = []

    for quake in quakes:
        loc = quake.place
        if word.lower() in loc.lower():
            quakes_list.append(quake)

    return quakes_list


def get_mag(quake):
    return quake.mag


def get_long(quake):
    return quake.longitude


def get_lat(quake):
    return quake.latitude


def get_time(quake):
    return quake.time


def sort_mag(quakes):
    quakes.sort(key=get_mag, reverse=True)


def sort_time(quakes):
    quakes.sort(key=get_time, reverse=True)


def sort_long(quakes):
    quakes.sort(key=get_long)


def sort_lat(quakes):
    quakes.sort(key=get_lat)
