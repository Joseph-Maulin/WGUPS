
# need to pack truck 2 with all truck 2 packages
# group packages that have to be delivered
# prioritize delivery_deadlines
from data import packages, Distances
import time
from datetime import timedelta, time, datetime

class Truck:

    def __init__(self):
        self.max_packages = 16
        self.average_speed = 18
        self.packages = []
        self.location = ""


class Package:
    # packageID : {"Address", "City", "Zip", "Delivery_Deadline", "Weight", "Truck", "Available", "Packaged With"}

    def __init__(self, packageID, delivery_address, address_Name, delivery_deadline, delivery_city, delivery_zip_code, weight, status, truck=0, available="8:00", packaged_with=[]):
        self.packageID = packageID
        self.delivery_address = delivery_address
        self.address_Name = address_Name
        self.delivery_deadline = delivery_deadline
        self.delivery_city = delivery_city
        self.delivery_zip_code = delivery_zip_code
        self.weight = weight
        self.status = status
        self.truck = truck
        self.available = available
        self.packaged_with = packaged_with


class Delivery_Distribution:

    def __init__(self, distances):
        self.packages = []
        self.distances = distances


    def add_package(self, packageID, delivery_address, address_Name, delivery_deadline, delivery_city, delivery_zip_code, weight, status, truck=0, available="8:00", packaged_with=[]):
        self.packages.append(Package(packageID, delivery_address, address_Name, delivery_deadline, delivery_city, delivery_zip_code, weight, status, truck=truck, available=available, packaged_with=packaged_with))


    def lookup_package(self, packageID=None, delivery_address=None, address_Name=None, delivery_deadline=None, delivery_city=None, delivery_zip_code=None, weight=None, status=None):
        packages = []

        for package in self.packages:
            if package.packageID == packageID:
                packages.append(package)
                return packages
            elif package.delivery_address == delivery_address:
                packages.append(package)
            elif package.address_Name == address_Name:
                packages.append(package)
            elif package.delivery_deadline == delivery_deadline:
                packages.append(package)
            elif package.delivery_city == delivery_city:
                packages.append(package)
            elif package.delivery_zip_code == delivery_zip_code:
                packages.append(package)
            elif package.weight == weight:
                packages.append(package)
            elif package.status == status:
                packages.append(package)
            else:
                continue

        return packages


    def lookup_status(self, packageID):
        return self.lookup_package(packageID=packageID)[0].status


    def find_route(self, current_location, route_length=16):

        # need to add delivery_deadline checks/lookaheads

        # [[route], packages/distance]
        shortest_route = [[current_location], 0]
        location_visited = [current_location]

        locations = self.get_available_locations()
        if current_location in locations:
            locations.remove(current_location)
        packages = 0

        while locations and packages<route_length:
            best_location = None
            best_ppd = 0
            for location in locations:
                new_route = shortest_route[0] + [location]
                route_packages = sum(self.get_num_packages(l) for l in new_route)
                route_distance = self.get_route_distance(new_route)
                # need to adjust taking final return to hub
                if len(locations) < 2:
                    route_distance += self.distances.distances["HUB"][location]

                total_ppd = route_packages / route_distance

                if total_ppd > best_ppd:
                    best_ppd = total_ppd
                    best_location = location

            shortest_route[0].append(best_location)
            shortest_route[1] = best_ppd

            packages += self.get_num_packages(best_location)
            current_location = best_location
            locations.remove(current_location)
            best_location = None
            best_ppd = None

            yield shortest_route[0][-2:]

        # print(shortest_route)
        shortest_route[0].append("HUB")
        return shortest_route[0]+["HUB"]

    def get_num_packages(self, location):
        n = 0
        for package in self.packages:
            if package.address_Name == location:
                n+=1

        return n

    def get_route_distance(self, route):

        #[a,b,c]
        #distances.distances[a][b] + distances.distances[b][c]
        distance = 0
        for i in range(len(route)-1):
            distance += self.distances.distances[route[i]][route[i+1]]

        return distance


    def get_available_locations(self):
        available = []
        for package in self.packages:
            if package.status != "Delivered":
                available.append(package.address_Name)

        return list(set(available))


    def route_time(self, route):
        distance_miles = self.get_route_distance(route)

        # miles / miles/hour
        # hours * 60 * 60
        distance_time = (distance_miles / 18) * 60 * 60

        return distance_time



if __name__ == "__main__":
    Distances = Distances()
    dd = Delivery_Distribution(Distances)
    for packageID, package_vars in packages.items():
        truck = 0
        available = "8:00"
        packaged_with = []

        if "Truck" in package_vars.keys():
            truck = package_vars["Truck"]
        if "Available" in package_vars.keys():
            available = package_vars["Available"]
        if "Packaged With" in package_vars.keys():
            packaged_with = package_vars["Packaged With"]

        dd.add_package(packageID,
                       package_vars["Address"],
                       Distances.address_to_place[package_vars["Address"]],
                       package_vars["Delivery_Deadline"],
                       package_vars["City"],
                       package_vars["Zip"],
                       package_vars["Weight"],
                       "Not Delivered",
                       truck=truck,
                       available=available,
                       packaged_with=packaged_with)

    delivery_time = datetime(2020,5,29,8,0,0)
    end_time = delivery_time + timedelta(hours=2)
    while delivery_time < end_time:
        for route in dd.find_route("HUB"):
            delivered_time = delivery_time + timedelta(seconds=dd.route_time(route))
            while delivery_time < delivered_time:
                print(route[0], delivery_time.strftime("%H:%M:%S"))
                delivery_time += timedelta(seconds=1)
        else:
            print("HUB", delivery_time.strftime("%H:%M:%S"))
            break

    # print(sum(dd.route_time(x) for x in dd.find_route('HUB')))









        ########
