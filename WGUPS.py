
# need to pack truck 2 with all truck 2 packages
# group packages that have to be delivered
# prioritize delivery_deadlines
from data import packages, Distances
import time
from datetime import timedelta, time, datetime

class Truck:

    def __init__(self, truckNum):
        self.max_packages = 16
        self.average_speed = 18
        self.truckNum = truckNum
        self.packages = []
        self.locations = []
        self.current_location = "HUB"
        self.visited_hub = True
        self.shortest_route = ["HUB"]
        self.location_visited = []
        self.route_time = 0
        self.time_of_next_delivered = None
        self.currently_delivering = []

    def print_packages(self):
        for package in self.packages:
            print(package)


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
        self.delivery_time = None

    def __repr__(self):
        return str({"packageID" : self.packageID,
                "delivery_address" : self.delivery_address,
                "address_Name" : self.address_Name,
                "delivery_deadline" : self.delivery_deadline,
                "delivery_city" : self.delivery_city,
                "delivery_zip_code" : self.delivery_zip_code,
                "weight" : self.weight,
                "status" : self.status,
                "truck" : self.truck,
                "available" : self.available,
                "packaged_with" : self.packaged_with
                })


class Delivery_Distribution:

    def __init__(self, distances, trucks=[]):
        self.packages = []
        self.distances = distances
        self.trucks = trucks
        self.delivery_time = datetime(2020,5,29,8,0,0)
        self.end_time = self.delivery_time + timedelta(hours=9)

    def add_package(self, packageID, delivery_address, address_Name, delivery_deadline, delivery_city, delivery_zip_code, weight, status, truck=0, available="8:00", packaged_with=[]):
        self.packages.append(Package(packageID, delivery_address, address_Name, delivery_deadline, delivery_city, delivery_zip_code, weight, status, truck=truck,
                                     available=available, packaged_with=packaged_with))


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

    # self.delivery_time = datetime(2020,5,29,8,0,0)
    # self.end_time = delivery_time + timedelta(hours=9)
    # while delivery_time < end_time:
    #     for route in dd.find_route('Deker Lake'):
    #         delivered_time = delivery_time + timedelta(seconds=dd.route_time(route))
    #         print(route[0], delivery_time.strftime("%H:%M:%S"))
    #         while delivery_time < delivered_time:
    #             delivery_time += timedelta(seconds=1)
    #     else:
    #         print("HUB", delivery_time.strftime("%H:%M:%S"))
    #         break

    # print(sum(dd.route_time(x) for x in dd.find_route('HUB')))
    def cycle_timer(self):
        truck1 = self.trucks[0]
        truck2 = self.trucks[1]

        truck1.time_of_next_delivered = self.delivery_time
        truck2.time_of_next_delivered = self.delivery_time

        while self.delivery_time < self.end_time:

            print(self.delivery_time)

            if truck1.time_of_next_delivered <= self.delivery_time:
                if truck1.packages:
                    packages_delivered = self.get_packages(truck1.currently_delivering, truck1)
                    for package in packages_delivered:
                        package.delivery_time = self.delivery_time
                        truck1.packages.remove(package)
                route = self.get_truck_routes(truck1)
                if route:
                    truck1.time_of_next_delivered = self.delivery_time + timedelta(seconds=self.route_time(route))
                    print(truck1.time_of_next_delivered, truck1.packages[-1])

            if truck2.time_of_next_delivered <= self.delivery_time:
                if truck2.packages:
                    packages_delivered = self.get_packages(truck2.currently_delivering, truck2)
                    for package in packages_delivered:
                        package.delivery_time = self.delivery_time
                        truck2.packages.remove(package)
                route = self.get_truck_routes(truck2)
                if route:
                    truck2.time_of_next_delivered = self.delivery_time + timedelta(seconds=self.route_time(route))
                    print(truck1.time_of_next_delivered, truck2.packages[-1])

            self.delivery_time += timedelta(seconds=1)

        not_delivered_count = 0
        for package in self.packages:
            if package.status == "Not Delivered":
                not_delivered_count += 1

        print(f"not_delivered_count: {not_delivered_count}")

        delivery_time = datetime(2020,5,29,8,0,0)

        print("\ntruck1")
        print(self.get_route_distance(truck1.shortest_route))
        print(delivery_time + timedelta(seconds=truck1.route_time))

        print("\ntruck2")
        print(self.get_route_distance(truck2.shortest_route))
        print(truck2.shortest_route, )
        print(delivery_time + timedelta(seconds=truck2.route_time))


    def get_truck_routes(self, truck):

        if len(truck.packages) == 16:
            return None

        truck.locations = self.get_available_locations(truck)

        truck_route = self.find_route(truck)

        if truck_route:
            self.add_route(truck, truck_route)
            return truck.locations[-2:]

        else:
            return None




    # def get_truck_routes(self):
    #
    #     truck1 = self.trucks[0]
    #     truck2 = self.trucks[1]
    #
    #     while True:
    #         truck1.locations = self.get_available_locations(truck1)
    #         truck2.locations = self.get_available_locations(truck2)
    #
    #         truck1_route = self.find_route(truck1)
    #         truck2_route = self.find_route(truck2)
    #
    #         if truck1_route:
    #             if truck1_route[1] >= truck2_route[1]:
    #                 self.add_route(truck1, truck1_route)
    #         if truck2_route:
    #             if not truck1_route:
    #                 self.add_route(truck2, truck2_route)
    #             elif truck1_route[1] < truck2_route[1]:
    #                 self.add_route(truck2, truck2_route)
    #
    #         print(self.delivery_time + timedelta(seconds=truck1.route_time))
    #
    #         not_delivered_count = 0
    #         for package in self.packages:
    #             if package.status == "Not Delivered":
    #                 not_delivered_count += 1
    #
    #         if not_delivered_count == 0:
    #             break
    #
    #         if len(truck1.packages) == 16 and len(truck2.packages) == 16:
    #             print("maxed out trucks")
    #             break
    #
    #     not_delivered_count = 0
    #     for package in self.packages:
    #         if package.status == "Not Delivered":
    #             print(package)
    #             not_delivered_count += 1
    #
    #     print(f"\npackages_left: {not_delivered_count}")
    #
    #     delivery_time = datetime(2020,5,29,8,0,0)
    #
    #     print("\ntruck1")
    #     print(self.get_route_distance(truck1.shortest_route))
    #     print(delivery_time + timedelta(seconds=truck1.route_time))
    #
    #     print("\ntruck2")
    #     print(self.get_route_distance(truck2.shortest_route))
    #     print(truck2.shortest_route, )
    #     print(delivery_time + timedelta(seconds=truck2.route_time))


    def add_route(self, truck, location):

        truck.current_location = location[0]
        truck.locations.remove(truck.current_location)
        truck.route_time = self.route_time(truck.shortest_route)
        truck.shortest_route.append(location[0])
        truck.currently_delivering = location[0]

        location_packages = self.get_packages(location[0], truck)
        truck.packages += location_packages
        for package in location_packages:
            package.truck = truck.truckNum
            package.status = "Delivered"
            package.delivered_time = self.delivery_time + timedelta(seconds=self.route_time(truck.shortest_route[-2:]))

    def find_route(self, truck, location_taken=None):

        # truck 2, packaged_with, delivery_deadline

        shortest_route = [[truck.current_location], 0]
        location_visited = [truck.current_location]

        if truck.locations and len(truck.packages) < truck.max_packages:
            best_location = None
            best_ppd = 0
            for location in truck.locations:
                new_route = shortest_route[0] + [location]
                packages = self.get_packages(location, truck)
                if (len(truck.packages) + len(packages) <= truck.max_packages):
                    route_distance = self.get_route_distance(new_route)

                    location_ppd = len(packages) / route_distance

                    if location_ppd > best_ppd:
                        best_ppd = location_ppd
                        best_location = location

            return (best_location, best_ppd)

        # print(shortest_route)
        # shortest_route[0].append("HUB")
        # return shortest_route[0]+["HUB"]


    def get_packages(self, location, truck):
        packages = []
        for package in self.packages:
            if package.address_Name == location:
                if package.truck == 0 or package.truck == truck.truckNum:
                    packages.append(package)

        return packages

    def get_route_distance(self, route):

        #[a,b,c]
        #distances.distances[a][b] + distances.distances[b][c]
        distance = 0
        for i in range(len(route)-1):
            distance += self.distances.distances[route[i]][route[i+1]]

        return distance


    def get_available_locations(self, truck):

        available = []
        for package in self.packages:
            if package.status == "Not Delivered":
                if int(package.truck) == 0 or int(package.truck) == int(truck.truckNum):
                    available.append(package.address_Name)

        return list(available)


    def route_time(self, route):
        distance_miles = self.get_route_distance(route)

        # miles / miles/hour
        # hours * 60 * 60
        distance_time = (distance_miles / 18) * 60 * 60

        return distance_time



if __name__ == "__main__":
    Distances = Distances()
    truck1 = Truck(1)
    truck2 = Truck(2)
    dd = Delivery_Distribution(Distances, trucks=[truck1, truck2])
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
                       truck=int(truck),
                       available=available,
                       packaged_with=packaged_with
                       )


    dd.cycle_timer()
