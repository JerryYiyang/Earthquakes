from io import StringIO
import unittest

import quake_funcs


class TestCases(unittest.TestCase):
    def test_earthquake_init(self):
        # Test that when we create an Earthquake, all the attributes are
        # correct.
        quake = quake_funcs.Earthquake(
            '12km SSW of Idyllwild, CA', 0.97, -116.7551651, 33.6391678,
            1488177290)

        self.assertEqual(quake.place, '12km SSW of Idyllwild, CA')
        self.assertAlmostEqual(quake.mag, 0.97)
        self.assertAlmostEqual(quake.longitude, -116.7551651)
        self.assertAlmostEqual(quake.latitude, 33.6391678)
        self.assertEqual(quake.time, 1488177290)

    def test_earthquakes_equal_0(self):
        # Two earthquakes with the same attributes should be equal.
        quake1 = quake_funcs.Earthquake(
            '12km SSW of Idyllwild, CA', 0.97, -116.7551651, 33.6391678,
            1488177290)
        quake2 = quake_funcs.Earthquake(
            '12km SSW of Idyllwild, CA', 0.97, -116.7551651, 33.6391678,
            1488177290)
        self.assertEqual(quake1, quake2)

    def test_earthquakes_equal_1(self):
        # Two earthquakes with different attributes (e.g. the place)
        # should not be equal.
        quake1 = quake_funcs.Earthquake(
            '12km SSW of Idyllwild, CA', 0.97, -116.7551651, 33.6391678,
            1488177290)
        quake2 = quake_funcs.Earthquake(
            '13km SSW of Idyllwild, CA', 0.97, -116.7551651, 33.6391678,
            1488177290)
        self.assertNotEqual(quake1, quake2)

    def test_read_file_0(self):
        # We can create a fake file that can be used for testing.
        in_file = StringIO(
            '0.97 -116.7551651 33.6391678 1488177290 12km SSW of Idyllwild, '
            'CA\n2.19 -121.5801697 36.9580002 1488173538 5km S of Gilroy, '
            'California\n'
        )

        quakes = quake_funcs.read_quakes_from_file(in_file)

        # We should close it when we're done.
        in_file.close()

        expected_quakes = [
            quake_funcs.Earthquake(
                '12km SSW of Idyllwild, CA', 0.97, -116.7551651, 33.6391678,
                1488177290),
            quake_funcs.Earthquake(
                '5km S of Gilroy, California', 2.19, -121.5801697, 36.9580002,
                1488173538)
        ]

        self.assertEqual(quakes, expected_quakes)

    def test_filter_by_mag_0(self):
        quakes = [
            quake_funcs.Earthquake(
                '12km SSW of Idyllwild, CA', 0.97, -116.7551651, 33.6391678,
                1488177290),
            quake_funcs.Earthquake(
                '5km S of Gilroy, California', 2.19, -121.5801697, 36.9580002,
                1488173538),
            quake_funcs.Earthquake(
                '100km SE of King Salmon, Alaska', 1.9, -155.2835, 58.1548,
                1488219604)
        ]

        filtered = [
            quake_funcs.Earthquake(
                '5km S of Gilroy, California', 2.19, -121.5801697, 36.9580002,
                1488173538),
            quake_funcs.Earthquake(
                '100km SE of King Salmon, Alaska', 1.9, -155.2835, 58.1548,
                1488219604)
        ]

        self.assertEqual(quake_funcs.filter_by_mag(quakes, 1, 3), filtered)

    def test_filter_by_place_0(self):
        quakes = [
            quake_funcs.Earthquake(
                '12km SSW of Idyllwild, CA', 0.97, -116.7551651, 33.6391678,
                1488177290),
            quake_funcs.Earthquake(
                '5km S of Gilroy, California', 2.19, -121.5801697, 36.9580002,
                1488173538),
            quake_funcs.Earthquake(
                '100km SE of King Salmon, Alaska', 1.9, -155.2835, 58.1548,
                1488219604)
        ]

        filtered = [
            quake_funcs.Earthquake(
                '12km SSW of Idyllwild, CA', 0.97, -116.7551651, 33.6391678,
                1488177290),
            quake_funcs.Earthquake(
                '5km S of Gilroy, California', 2.19, -121.5801697, 36.9580002,
                1488173538)
        ]

        self.assertEqual(quake_funcs.filter_by_place(quakes, 'ca'), filtered)

    # TODO: Remove the quotation marks once you're ready to test working
    # with JSON data.
    def test_quake_from_feature(self):
        feature = {
            'geometry': {
                'coordinates': [
                    -117.4906667,
                    33.9131667,
                    0.25
                ],
                'type': 'Point'
            },
            'id': 'ci37814000',
            'properties': {
                'code': '37814000',
                'detail': ('http://earthquake.usgs.gov/'
                           'earthquakes/feed/v1.0/detail/ci37814000.geojson'),
                'dmin': 0.2836,
                'gap': 87,
                'ids': ',ci37814000,',
                'mag': 1.24,
                'magType': 'ml',
                'net': 'ci',
                'nst': 8,
                'place': '5km NE of Home Gardens, CA',
                'rms': 0.27,
                'sig': 24,
                'sources': ',ci,',
                'status': 'automatic',
                'time': 1488179250520,
                'title': 'M 1.2 - 5km NE of Home Gardens, CA',
                'tsunami': 0,
                'type': 'earthquake',
                'types': (',geoserve,nearby-cities,origin,phase-data,'
                          'scitech-link,'),
                'tz': -480,
                'updated': 1488179487273,
                'url': ('http://earthquake.usgs.gov/'
                        'earthquakes/eventpage/ci37814000')
            },
            'type': 'Feature'
        }

        quake = quake_funcs.quake_from_feature(feature)
        expected_quake = quake_funcs.Earthquake(
            '5km NE of Home Gardens, CA', 1.24, -117.4906667, 33.9131667,
            1488179250)
        self.assertEqual(quake, expected_quake)

    def test_get_mag(self):
        quake = quake_funcs.Earthquake('5km NW of Foothill Ranch, CA', 1.22,
                                       -100.232, 100.123, 123123123)
        self.assertEqual(quake_funcs.get_mag(quake), 1.22)

    def test_get_long(self):
        quake = quake_funcs.Earthquake('5km NW of Foothill Ranch, CA', 1.22,
                                       -100.232, 100.123, 123123123)
        self.assertEqual(quake_funcs.get_long(quake), -100.232)

    def test_get_lat(self):
        quake = quake_funcs.Earthquake('5km NW of Foothill Ranch, CA', 1.22,
                                       -100.232, 100.123, 123123123)
        self.assertEqual(quake_funcs.get_lat(quake), 100.123)

    def test_get_time(self):
        quake = quake_funcs.Earthquake('5km NW of Foothill Ranch, CA', 1.22,
                                       -100.232, 100.123, 123123123)
        self.assertEqual(quake_funcs.get_time(quake), 123123123)

    def test_sort_mag(self):
        quakes = [quake_funcs.Earthquake('5km NW of Foothill Ranch, CA', 1.22,
                                         -100.232, 100.123, 123123123),
                  quake_funcs.Earthquake('7km NE of Irvine, CA', 2.34,
                                         -123.123, 123.123, 123123123)]
        self.assertEqual(quake_funcs.sort_mag(quakes), None)

    def test_sort_time(self):
        quakes = [quake_funcs.Earthquake('5km NW of Foothill Ranch, CA', 1.22,
                                         -100.232, 100.123, 123123123),
                  quake_funcs.Earthquake('7km NE of Irvine, CA', 2.34,
                                         -123.123, 123.123, 123123123)]
        self.assertEqual(quake_funcs.sort_time(quakes), None)

    def test_sort_long(self):
        quakes = [quake_funcs.Earthquake('5km NW of Foothill Ranch, CA', 1.22,
                                         -100.232, 100.123, 123123123),
                  quake_funcs.Earthquake('7km NE of Irvine, CA', 2.34,
                                         -123.123, 123.123, 123123123)]
        self.assertEqual(quake_funcs.sort_long(quakes), None)

    def test_sort_lat(self):
        quakes = [quake_funcs.Earthquake('5km NW of Foothill Ranch, CA', 1.22,
                                         -100.232, 100.123, 123123123),
                  quake_funcs.Earthquake('7km NE of Irvine, CA', 2.34,
                                         -123.123, 123.123, 123123123)]
        self.assertEqual(quake_funcs.sort_lat(quakes), None)


# Run the unit tests.
if __name__ == '__main__':
    unittest.main()
