
# need to pack truck 2 with all truck 2 packages
# group packages that have to be delivered
# prioritize delivery_deadlines



class Truck:

    def __init__(self):
        self.max_packages = 16
        self.average_speed = 18
        self.packages = []
        self.location = ""


class Package:

    def __init__(self, packageID, delivery_address, delivery_deadline, delivery_city, delivery_zip_code, weight, status):
        self.packageID = packageID
        self.delivery_address = delivery_address
        self.delivery_deadline = delivery_deadline
        self.delivery_city = delivery_city
        self.delivery_zip_code = delivery_zip_code
        self.weight = weight
        self.status = status



class Delivery_Distribution:

    def __init__(self):
        self.packages = []


    def add_package(self, packageID, delivery_address, delivery_deadline, delivery_city, delivery_zip_code, weight, status):
        self.packages.append(Package(packageID, delivery_address, delivery_deadline, delivery_city, delivery_zip_code, weight, status))


    def lookup_package(self, packageID=None, delivery_address=None, delivery_deadline=None, delivery_city=None, delivery_zip_code=None, weight=None, status=None):
        packages = []

        for package in self.packages:
            if package.packageID == packageID:
                packages.append(package)
                return packages
            elif package.delivery_address == delivery_address:
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







if __name__ == "__main__":
    pass
