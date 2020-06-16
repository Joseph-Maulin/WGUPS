

# Initiate:
  > initialize Distances object from data.py
  > initialize 2 Truck objects
  > initialize Delivery_Distribution object
  > initialize Package objects from packages dict in data.py
  > start set_truck_routes()


```
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


  dd.set_truck_routes()
```



#  Delivery_Distribution flow

  > all functionality is run through the Delivery_Distribution object
    Truck and Package are used as data storage objects

  > set_truck_routes
      > increments by delivery time and calls find_and_deliver(truck) whichever truck is   available
      > when all packages are delivered. checks are run to see if all package deadlines are met
      and adjust truck routes if necessary
      > finally prints routing results print_route_results

  > find_and_deliver
      > updates information about packages being currently delivered if currently_delivering
      > gets delivery_time of next found route from get_truck_routes()
      > sets trucks next delivery_time
      > moves truck to HUB if no next location found or package limit reached
      > marks truck as done if at HUB and no packages are left to deliver

  >
