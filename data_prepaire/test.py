import unittest
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

if __name__ == '__main__':
    unittest.main()