# TestCase class will be used to write test cases.
import unittest
from Cookie import *

class TestCase(unittest.TestCase):
    def testUpdateCookieDictionary(self):
        self.testCookie = CookieCount('cookieTest.csv', '2018-12-08T21:30:00+00:00')
        # checking if initial value when non-existing key in dictionary is added is equal to one.
        self.testCookie.updateCookieDictionary('rob')
        self.assertEqual(1, self.testCookie.cookieDictionary['rob'])

        # checking if value when initialized is incremented by one when another cookie with the same name is found.
        self.testCookie.updateCookieDictionary('rob')
        self.assertEqual(2, self.testCookie.cookieDictionary['rob'])

    def testUpdateCookieCount(self):
        # Testing MaxCookie where we have two cookies, one with 2 occurances, and one with one occurance.
        self.testCookie = CookieCount('cookieTest.csv', '2018-12-08T21:30:00+00:00')
        self.assertEqual([], self.testCookie.maxCookieStrings)
        self.assertEqual(0, self.testCookie.maxCookieOccurances)

        # Testing to make sure maxCookie is correctly updated with one value.
        self.testCookie.updateCookieDictionary('rob')
        self.testCookie.updateCookieCount('rob')
        self.assertEqual(['rob'], self.testCookie.maxCookieStrings)
        self.assertEqual(1, self.testCookie.maxCookieOccurances)

        # Case to make sure that if we have an equal number of occurances for two cookies, than maxCookie contains both of them.
        self.testCookie.updateCookieDictionary('robert')
        self.testCookie.updateCookieCount('robert')
        self.assertEqual(['rob', 'robert'], self.testCookie.maxCookieStrings)
        self.assertEqual(1, self.testCookie.maxCookieOccurances)

        # Case to make sure that maxCookie updates properly when going from list with multiple cookies to just one cookie and count.
        self.testCookie.updateCookieDictionary('rob')
        self.testCookie.updateCookieCount('rob')
        self.assertEqual(['rob'], self.testCookie.maxCookieStrings)
        self.assertEqual(2, self.testCookie.maxCookieOccurances)
        # MaxCookie should display 'rob', because there are more occurances of rob.

    # self,listOfStrings, low, high, timestamp
    def testBinarySearch(self):
        # Can define testCookie with any timestamp and still check binarySearch independently.
        timestampOne = "2018-12-08T21:30:00+00:00"
        self.testCookie = CookieCount('cookieTest.csv', timestampOne)

        timeStampList = [["a","2018-12-06T14:19:00+00:00"], ["b","2018-12-09T14:19:00+00:00"],
         ["b","2018-12-09T15:19:00+00:00"], ["c","2018-12-09T16:19:00+00:00"], ["d","2018-12-10T14:19:00+00:00"]]
        self.assertEqual(self.testCookie.binarySearch(timeStampList, 0, len(timeStampList) - 1, timestampOne), -1)

        # Checking to make sure 0th index of list works
        timestampTwo = "2018-12-06T21:30:00+00:00"
        self.assertEqual(self.testCookie.binarySearch(timeStampList, 0, len(timeStampList) - 1, timestampTwo), 0)

        # Checking to make sure final index of list works
        timestampThree = "2018-12-10T00:00:00+00:00"
        self.assertEqual(self.testCookie.binarySearch(timeStampList, 0, len(timeStampList) - 1, timestampThree), 4)

unittest.main()