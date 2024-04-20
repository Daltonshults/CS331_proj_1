from math import radians, cos, sin, asin, sqrt

class DistanceChecker:
    def decimal_degrees(self, point):
        lat = point[0]
        long = point[1]

        d_degrees_lat = lat[0] + lat[1]/60 + lat[2]/3600
        d_degrees_long = long[0] + long[1]/60 + long[2]/3600
        
        if lat[3] == "S":
            d_degrees_lat = -d_degrees_lat

        if long[3] == "W":
            d_degrees_long = -d_degrees_long        

        return d_degrees_lat, d_degrees_long

    def convert_to_radians(self, lat_1, long_1, lat_2, long_2):
        lat_1 = radians(lat_1)
        long_1 = radians(long_1)
        lat_2 = radians(lat_2)
        long_2 = radians(long_2)

        return lat_1, long_1, lat_2, long_2
    
class HaversineDistance(DistanceChecker):

    def compute_c(self, alpha):
        return 2 * asin(sqrt(alpha))

    def compute_distance(self, c, r):
        return c * r

    def haversine(self, point_1, point_2):
        r = 6371
        lat_1, long_1 = self.decimal_degrees(point_1)
        lat_2, long_2 = self.decimal_degrees(point_2) 

        lat_1, long_1, lat_2, long_2 = self.convert_to_radians(lat_1,
                                                        long_1,
                                                        lat_2,
                                                        long_2)     


        dlat = lat_2 - lat_1
        dlong = long_2 - long_1

        alpha = (sin(dlat/2)**2) + cos(lat_1) * cos(lat_2) * (sin(dlong/2)**2)

        return self.compute_distance(self.compute_c(alpha), r)
    
class EuclideanDistance(DistanceChecker):

    def euclidean(self, point_1, point_2):
        lat_1, long_1 = self.decimal_degrees(point_1)
        lat_2, long_2 = self.decimal_degrees(point_2)

        print(f"X_1: {long_1}")
        print(f"Y_1: {lat_1}")
        print(f"X_2: {long_2}")
        print(f"Y_2: {lat_2}")

        y = (lat_2 - lat_1)** 2
        x = (long_2 - long_1)** 2

        total = sqrt(x + y)
        # One degree of latitude is equal to 25,000/360 
        #                                   = 69.4 miles 
        #                                   = 111.2 kilometers
        return total * 111.2
    