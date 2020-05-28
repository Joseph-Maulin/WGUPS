
# need to pack truck 2 with all truck 2 packages
# group packages that have to be delivered
# prioritize delivery_deadlines
from data import packages, Distances


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

    def __init__(self):
        self.packages = []


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


    def find_route(self, current_location, distances, route_length=16):

        route_length = 100000
        shortest_route = []
        location_visited = [current_location]

        # start at current_location
        # go through status not delivered

        temp_route = []
        temp_route_length = 0
        packages = 0
        locations = self.get_available_locations()

        for location in locations:
            while packages < 16:
                available_locations = [loc for loc in locations if loc not in location_visited]
                for loc in available_locations:
                    temp_route.append(loc)
                    temp_route_length


    def find_best_route(self, location, visited, available, package):
        if not available:
            return 0

        elif package == 16:
            return 0

        else:

            for loc in available:
                visited.append(location)
                package+=get_num_packages(loc)
                loc = self.get_available_locations()
                available_locations = [l for l in loc if l not in visited]
                self.find_best_route(loc, visited, available, package)


    def get_num_packages(self, location):
        n = 0
        for pacakage in self.packages:
            if package.address_Name == "location":
                n+=1

        return n


    def get_available_locations(self):
        available = []
        for package in self.packages:
            if package.status != "Delivered":
                available.append(package.address_Name)

        return list(set(available))



if __name__ == "__main__":
    dd = Delivery_Distribution()
    Distances = Distances()
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

    dd.find_route("HUB", Distances)
