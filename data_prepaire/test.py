import unittest
import datetime

import prepaire


class Test(unittest.TestCase):
    def test_bsearch_trivial(self):
        arr = [10, 20, 30, 40, 50]
        indx = prepaire.bsearch(arr, 35, 0, len(arr)-1)
        self.assertEqual(2, indx)

    def test_bsearch_duplicate(self):
        arr = [10, 20, 30, 40, 50]
        indx = prepaire.bsearch(arr, 30, 0, len(arr)-1)
        self.assertEqual(2, indx)

    def test_bsearch_extract(self):
        arr = [(10, 'a'), (20, 'a'), (30, 'a'), (40, 'a'), (50, 'a')]
        indx = prepaire.bsearch(arr, 35, 0, len(arr)-1, lambda v: v[0])
        self.assertEqual(2, indx)

    def test_bsearch_corner_more(self):
        arr = [10, 20, 30, 40, 50]
        indx = prepaire.bsearch(arr, 100, 0, len(arr)-1)
        self.assertEqual(4, indx)

    def test_bsearch_corner_less(self):
        arr = [10, 20, 30, 40, 50]
        self.assertRaises(ValueError, prepaire.bsearch, arr, 0, 0, len(arr)-1)

    def test_bsearch_interval(self):
        arr = [10, 20, 30, 40, 50]
        indx = prepaire.bsearch(arr, 35, 0, 1)
        self.assertEqual(1, indx)

    def test_interpolate_more(self):
        arr = [2, 3, 4, 5, 6]
        result = prepaire.interpolate_array(arr, 5)
        etalon_array = [2, 3, 4, 5, 6]
        for i in xrange(len(etalon_array)):
            self.assertAlmostEqual(etalon_array[i], result[i])

    def test_interpolate_more_2(self):
        arr = [-5, 5]
        result = prepaire.interpolate_array(arr, 11)
        etalon_array = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
        for i in xrange(len(etalon_array)):
            self.assertAlmostEqual(etalon_array[i], result[i])

    def test_interpolate_less(self):
        arr = [3, 6, 9, 12, 15]
        result = prepaire.interpolate_array(arr, 3)
        etalon_array = [3, 9, 15]
        for i in xrange(len(etalon_array)):
            self.assertAlmostEqual(etalon_array[i], result[i])

    def test_interpolate_big_not_raises(self):
        arr = [0.02, 0.028, -0.069, -0.067, -0.019, -0.051, 0.028, -0.038, 0.03, 0.042, 0.063, 0.013, 0.026, 0.066,
               0.105, 0.173, 0.184, 0.223, 0.241, 0.259, 0.313, 0.369, 0.435, 0.394, 0.454, 0.458, 0.465, 0.438, 0.442,
               0.454, 0.465, 0.466, 0.501, 0.396, 0.372, 0.414, 0.506, 0.508, 0.349, 0.339, 0.392, 0.38, 0.387, 0.223,
               0.203, 0.214, 0.13, 0.096, 0.105, 0.074, 0.024, 0.022, 0.074]

        prepaire.interpolate_array(arr, 100)
        # if it does not raise anything, it's ok


    def test_interpolate_mixed(self):
        arr = [1, -1, 1]
        result = prepaire.interpolate_array(arr, 5)
        etalon_array = [1, 0, -1, 0, 1]
        for i in xrange(len(etalon_array)):
            self.assertAlmostEqual(etalon_array[i], result[i])

    def test_interpolate_less_two(self):
        arr = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
        result = prepaire.interpolate_array(arr, 3)
        etalon_array = [-5, 0, 5]
        for i in xrange(len(etalon_array)):
            self.assertAlmostEqual(etalon_array[i], result[i])

    def test_interpolate_empty_array(self):
        arr = []
        result = prepaire.interpolate_array(arr, 3)
        etalon_array = [0, 0, 0]
        for i in xrange(len(etalon_array)):
            self.assertAlmostEqual(etalon_array[i], result[i])

    def test_event_overlap(self):
        events = [{
            "type": 5,
            "direction": 1,
            "start": datetime.datetime.strptime("11:10:09", '%H:%M:%S'),
            "end": datetime.datetime.strptime("11:10:17", '%H:%M:%S')
        },
        {
            "type": 5,
            "direction": 1,
            "start": datetime.datetime.strptime("11:11:10", '%H:%M:%S'),
            "end": datetime.datetime.strptime("11:11:20", '%H:%M:%S')
        }]

        start_time = datetime.datetime.strptime("11:10:01", '%H:%M:%S')
        end_time = datetime.datetime.strptime("11:10:04", '%H:%M:%S')
        is_overlapped = prepaire.is_event_overlapped(events, start_time, end_time)

        self.assertFalse(is_overlapped)

        start_time = datetime.datetime.strptime("11:10:18", '%H:%M:%S')
        end_time = datetime.datetime.strptime("11:10:20", '%H:%M:%S')
        is_overlapped = prepaire.is_event_overlapped(events, start_time, end_time)

        self.assertFalse(is_overlapped)

        start_time = datetime.datetime.strptime("11:10:10", '%H:%M:%S')
        end_time = datetime.datetime.strptime("11:10:12", '%H:%M:%S')
        is_overlapped = prepaire.is_event_overlapped(events, start_time, end_time)

        self.assertTrue(is_overlapped)

        start_time = datetime.datetime.strptime("11:10:08", '%H:%M:%S')
        end_time = datetime.datetime.strptime("11:10:09", '%H:%M:%S')
        is_overlapped = prepaire.is_event_overlapped(events, start_time, end_time)

        self.assertTrue(is_overlapped)

        start_time = datetime.datetime.strptime("11:11:13", '%H:%M:%S')
        end_time = datetime.datetime.strptime("11:11:14", '%H:%M:%S')
        is_overlapped = prepaire.is_event_overlapped(events, start_time, end_time)

        self.assertTrue(is_overlapped)



if __name__ == '__main__':
    unittest.main()