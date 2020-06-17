

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

  > add_package
      > add_package into Delivery_Distribution object
      > sets delivery_deadline and availability information

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

        > get_truck_routes
            > find available locations, find truck route, add_route if route found

                > get_available_locations
                    > get available locations to search for truck route
                    > prioritize filling packaged_with packages

                > find_route
                    > find most efficient next location to add to route
                    > weight locations by package per distance (location_packages / route_distance)
                    > adds "HUB" travel to the route if necessary

                > add_route
                    > update truck data, add packages/locations to route, return projected delivery_time
                    > if "HUB" in route add "HUB" distance and location to the route and reset packages
                      carried away from hub
                    > mark packages time of delivery

  > check_if_met_deadlines
      > loops through delivered packages and checks if delivery_deadline < delivered_time
      > shuffle_for_deadlines if package deadlines are not met

  > shuffle_for_deadlines
      > rearrange routes so that all package deadlines are made
      > insert route location into truck.shortest_route and run route_is_valid check
      > updates truck.shortest_route to the most efficient rearrangement

          > route_is_valid
              > checks if route meets all constraints
              > deadlines met, packged_with, max_packages

  > print_route_results
      > prints package status at delivery_times via print_status method
      > prints each trucks final route distance, route, and number of packages
      > finally prints total distance travelled for both trucks

          > print_status
              > prints the delivery status of all packages at each delivery time chronologically


  > helper_functions
      > lookup_package
          > lookup package by any package class variables

      > lookup_status
          > lookup status by packageID

      > get_packages_with_deadlines
          > return all packages with deadlines other than end of day

      > get_deadline
          > get minimum time to meet for deadline_packages passed

      > get_packages
          > get packages for given location and truck

      > get_deadline_locations
          > get all locations for passed deadline_packages

      > get_route_distance
          > get distance of passed route based on data.Distances

      > route_time
          > get time to complete route in seconds. Based of distance/truck speed
