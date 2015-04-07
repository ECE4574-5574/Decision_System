

class TemporaryHolding:
    def __init__(self):
        self.lat = " "
        self.longi = " "
        self.alt = " "
        self.time = " "
    def storeLocation(self, lat, longi, alt, time):
        self.lat = lat;
        self.longi = longi;
        self.alt = alt;
        self.time = time;
    def getLat(self):
        return self.lat
    def getLongi(self):
        return self.longi
    def getAlt(self):
        return self.alt
    def getTime(self):
        return self.time

