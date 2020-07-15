
# Created by Joseph Maulin WGU Student ID: 001118042


# Algorithm overview

To solve this routing system requirements I adapted Dijkstra's Algorithm. I have
an object oriented setup with Truck, Package, and Delivery_Distribution classes. This way
each object can easily contain all the variables they need to throughout the execution.

Packages are read from the data.py file, initialized, and loaded into the Delivery_Distribution
object. The data variables are in a dictionary and the Distances are in a json format listing
distances between each of the locations.

The main code flow is as follows. I have opted for a greedy version of Dijkstra's Algorithm.
The purpose being that two trucks are operating simultaneously. The truck with the next available
open time searches for the next package delivery location. The available locations are
filtered by whether that truck is eligible. This is based on whether the location has non-delivered
or in route packages, packaged with packages responsibility, and truck number requirements,
and package availability. Then I use a greedy approach where the locations are the nodes and it chooses
the best packages delivered per mile as the node number. The location is then added to the truck.
The route is then checked to see if any deadlines would not be met and rearranges the route if necessary.
When the truck routes are finalized I print out the times when a delivery has occurred and the delivery status
of the packages at that time. I have included travel times back to the delivery "HUB" during routing.
Delivery times themselves are tracked in each package object. Finally I go into a user interface where
individual package details can be examined or package statuses can be seen at a certain time.


# Discuss the ability of your solution to adapt to a changing market and to scalability.

  This solution is fairly adaptable. The distance data and locations can be
  easily swapped with another set. The data variables and distances to other locations
  used in this adaption are in json format. It seems reasonable that data would be collected
  to use in that form for a different set. The solution is adaptable to changes that
  can occur during daily execution since it is finding the next route location
  one by one instead of locking in a set route. I have also included route rearrangements
  if deadlines are not met. Also Finally I believe it can be scaled
  without problem since any additions are just additions to the json input. Thinking about
  scalability as well I have reductions in location searches based on truck eligibility.
  Also there is a reduction in n of package searches during the program as packages delivered
  are moved into a separate dictionary key.

# Discuss the efficiency and maintainability of the software.

  The efficiency is quadratic, but n's scale down as packages are delivered
  due to the dictionary access of self.packages. Also some worst case
  scenarios are factored in such as all packages being deadlined before
  end of day.

  The code set should be easy to maintain due to the object oriented design.
  Functionality can be added or adjusted to certain methods without drastically effecting other method processes.


# Discuss the self-adjusting data structures chosen and their strengths and weaknesses based on the scenario.

  Locations are added to truck routes in cycles. The self-adjusting aspect in this solution
  checks if any package delivery deadlines would be missed by this addition. If so, I have
  written a code segment to reorder that truck route (shuffle_for_deadlines) to the most
  efficient rearrangement that meets all deadlines.

  The strength is that a location can be moved around to meet delivery deadlines without
  adding a lot of time complexity to the solution. Otherwise routing would have to have
  simulated lookaheads on each cycle. These would be exponential since you are also looking
  for the least amount of distance travelled. So you would essentially have to simulate all
  possibilities, check if deadlines are met, and look for the most efficient. This seems like
  a reasonable less intensive middle ground solution.

  A weaknesses of this solution are that the solution's time complexity is based on
  the length of the current route of locations. So rearrangements later in the day become
  more intensive. Each truck route length is lowered with each other truck in service though.
  Another is that if this was to become a real time live service. Package delivery times
  would need to be calculated from "HUB" to "HUB" to get accurate delivery times for packages
  beforehand.



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

          > adjust_delivery_times
              > recalculates package delivery times for shuffled route

          > route_is_valid
              > checks if route meets all constraints
              > deadlines met, packged_with, max_packages

  > print_route_results
      > prints package status at delivery_times via print_status method
      > prints each trucks final route distance, route, and number of packages
      > finally prints total distance travelled for both trucks

          > print_status
              > prints the delivery status of all packages at each delivery time chronologically


  > helper_methods
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


## Evaluate space-time complexity using Big O notation throughout the coding and for the entire program.
  p = number of packages
  r = length of truck route
  l = locations

  add_package - O(p)

  lookup_package - O(p)

  lookup_status - O(1)

  get_packages_with_deadlines - O(p)

  set_truck_routes - O(p + l*(l*2p + r + p**2 + p + r**3) + l*p + r)
                        --> O(l**2*p + p**2 + r**3 + r*p)

                     O(p) packages_with_deadlines
                     O(l*2p + r + p**2) find_and_deliver
                     O(p) check_if_met_deadlines
                     O(r**3) shuffle_for_deadlines
                     O(l*p + r) print_route_results

  check_if_met_deadlines - O(p)

  shuffle_for_deadlines - O(2r+2p+r*(r*(r*p+r*p+r+p+r*p+p)))
                            -> O(2r+2p+r*(r*(r*p)))
                            -> O(2r+2p + r**3)
                            -> O(r**3)

                          O(1) deadlines_not_met
                          O(r) index shortest_route
                          O(p) get_packages
                          O(p) get_deadline
                          O(r) for i in range(len(route)-1)
                          O(r) while best_route == None and cycles>0
                          O(r) for i in range(1, finish_index)
                          O(r*p) adjust_delivery_times
                          O(r*p) route_is_valid
                          o(r) get_route_distance

  adjust_delivery_times - O(r*p)

  route_is_valid - O(p + r*(2p)) => O(r*p)
                   O(p) get packages with deadlines
                   O(r) route length
                   O(p) get_packages
                   O(p) location_packages

  get_deadline - O(p)

  print_route_results - O(l*p + 4r) -> O(l*p + r)
                        O(l*p) for print_status
                        O(r) for get_route_distance

  print_status -  O(p + l*(2p)) -> O(l*p)

  find_and_deliver - O(16 + l*p**2 + r+2) -> O(l*p**2 + r)
                     O(16) c in currently_delivering max of 16
                     O(l*2p + r + p**2) g in get_truck_routes
                     O(2) - route_time constant size of 2

  get_truck_routes - O(p + l*2p + r + p**2)
                        -> O(l*2p + r + p**2)

                     O(p) get_available_locations
                     O(l*2p) find_route
                     O(r + p**2) add_route

  add_route - O(r + p**2)
              O(r) route_time n for n in shortest_route
              O(p) package in location_packages
              O(p) packages["Not Delivered"]

  find_route - O(l*p**2*2) -> O(l*p**2)
               O(l) location in locations
               O(p) get_packages()
               O(p) package in get_packages()
               O(2) r in get_route_distance(new_route) new_route constant 2

  get_packages - O(p)

  get_available_locations - O(p)

  get_deadline_locations - O(p)

  get_route_distance - O(r)

  route_time = O(r)
