# Written by Rob Brodin, rbrodin@wpi.edu, for Quantcast Programming Challenge. September-October 2021
from csv import reader

class CookieCount:
    # CookieCount(string csvFilePath, string specifiedDate)
    # initialize CookieCount, takes a file path linking to the csv,
    # and the specified date where we want to find the most common occurance of a cooke.
    def __init__(self, csvFilePath, specifiedDate):
        self.csvFilePath = csvFilePath
        # Assuming the date is of the format: 2018-12-08T21:30:00+00:00, split when there is a T.
        self.specifiedDate, other = specifiedDate.split('T')

        # Dictionary which will keep track of cookies and count for each. {'cookieKey': numOccurances, 'cookieKey2': numOccurances}
        self.cookieDictionary = {}

        # maxCookieStrings stores the cookie(s) with the highest number of occurances.
        # if there are multiple then the list will be of format: ["cookie1", "cookie2", ...]
        self.maxCookieStrings = []
        # maxCookieOccurances keeps track of the largest number of occurances of a single cookie string for all cookie strings given a certain timestamp.
        self.maxCookieOccurances = 0

    # updateCookieDictionary(string cookieString) : void
    # takes a string of a cookie and updates the count of the number of occurances of that cookie in self.cookieDictionary
    def updateCookieDictionary(self, cookieString):
        # if the cookie already exists, update the current number of occurances by one.
        if cookieString in self.cookieDictionary:
            self.cookieDictionary[cookieString] += 1
        # Otherwise, initialize as one.
        else:
            self.cookieDictionary[cookieString] = 1

    # updateCookieCount(string cookieString) : void
    # takes a string of a cookie and updates the maximum cookie (self.maxCookieOccurances (int) and self.maxCookieStrings (list))
    # if the occurances of cookieString given are greater than the current maximum.
    def updateCookieCount(self, cookieString):
        currentCookieCount = self.cookieDictionary[cookieString]
        # if the number of occurances for the current cookie (cookieString) is
        if currentCookieCount > self.maxCookieOccurances:
            self.maxCookie = [cookieString, currentCookieCount]
            self.maxCookieOccurances = currentCookieCount
            self.maxCookieStrings = [cookieString]
        elif currentCookieCount == self.maxCookieOccurances:
            self.maxCookieStrings.append(cookieString)

    # splitDate(string timestamp) : string timestamp (of format: 2016-10-20)
    def splitDate(self, string):
        dateSearchingFor, other = string.split("T")
        return dateSearchingFor

    # binarySearch(list listOfRows, int low, int high, string date) : int index
    # Modified binary search function which returns the index of the first occurance of a date in a given array
    # Returns -1 if given date not found
    def binarySearch(self, listOfRows, low, high, date):
        if high >= low:
            center = (high + low) // 2
            dateSearchingFor = self.splitDate(date)
            dateFound = listOfRows[center][1]

            # Need to check if there is another occurance of a given timestamp at a lower index.
            if dateSearchingFor in dateFound and center != 0 and dateSearchingFor in listOfRows[center - 1][1]:
                return self.binarySearch(listOfRows, low, center - 1, date)
            elif dateSearchingFor in dateFound:
                return center
            elif date < dateFound:
                return self.binarySearch(listOfRows, low, center - 1, date)
            else:
                return self.binarySearch(listOfRows, center + 1, high, date)
        else:
            return -1


    # iterateThroughCookies(void) : void
    # finds cookie and timestamp in a csv file by binary search and updates a dictionary containing the number of occurances
    # of each cookie string (of format: cookieString, timestamp)
    def iterateThroughCookies(self):
        with open(self.csvFilePath, 'r') as csvFile:
            # split the cookies and timestamps into separate lists
            csv_reader = reader(csvFile)
            listOfRows = list(csv_reader)
            if(len(listOfRows) == 0):
                print("Read file incorrectly or no cookies and timestamps given!")
            listOfRows.pop(0)

            # Get the starting index of the timestamp (ie the first time a timestamp shows up), and start from there instead of iterating through the entire list.
            # Binary search makes it O(logn) !
            # Also gives timestamp as format DATE + "T00:00:00+00" (ie 12:00am)
            startingIndex = self.binarySearch(listOfRows, 0, (len(listOfRows) - 1), (self.specifiedDate + "T00:00:00+00:00"))

            # if the startingIndex -1, then the date was not found in the list!
            if(startingIndex == -1):
                print("The date you're searching for does not exist!")
            else:
                # iterate through the cookies on a certain day until a new day is found (more efficient than iterating through all of them)
                for index in range(startingIndex, len(listOfRows)):
                    # cookieString keeps the timestamp frmo the current index in listOfRows
                    cookieString = listOfRows[index][0]
                    # accessDate keeps the timestamp from the current index in listOfRows
                    accessDate = listOfRows[index][1]

                    # if the date read from the current file is in the specified date (ie a substring),
                    # add it to the cookieDictionary, update the number of occurances in the dictionary,
                    # and update the max number of occurances (if applicable)
                    if self.specifiedDate in accessDate:
                        self.updateCookieDictionary(cookieString)
                        self.updateCookieCount(cookieString)
                    # no need to keep looping if we hit another day
                    else:
                        break

    # displayMaxCookie(void)
    # void function that prints the string of the cookie with the largest number of occurances
    def displayMaxCookie(self):
        for cookie in self.maxCookieStrings:
            print(cookie)


    # run(void) : void
    # takes no arguments and runs iterateThroughCookies() and displayMaxCookie() to calculate and show the cookie with the largest number of occurances.
    def run(self):
        self.iterateThroughCookies()
        self.displayMaxCookie()


# ./most_active_cookie cookie_log.csv -d 2018-12-08
# CLI conditional statements.
import sys
if(len(sys.argv) != 4):
    print("Please specify: fileName.csv -d timestamp")
else:
    if(not sys.argv[1].endswith(".csv")):
        print("Please specify: fileName.csv -d timestamp")
        print("You specified a non-csv file!")
    elif (sys.argv[2] != "-d"):
        print("Please specify: fileName.csv -d timestamp")
        print("Please specify -d and a timestamp (string) !")
    else:
        newCookieCount = CookieCount(sys.argv[1], sys.argv[3])
        newCookieCount.run()