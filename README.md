
## Created by
  Joseph Maulin


# Algorithm overview

  To solve the routing system requirement goals I adapted Dijkstra's Algorithm. Since each location is a node and they are already weighted
  by the distance to travel to them, this algorithm seemed to fit well (Dijkstra's Algorithm, Programiz). The strength of this algorithm is that it is
  an undirected solution, which is ideal since I don't have a end goal target node (Dijkstra's Algorithm, Programiz). Another is that I can
  easily weight each location node and search through the tree iteratively, choosing an ideal next location without having to project too far
  in advance (Dijkstra's Algorithm, Programiz). I have an object oriented setup with Truck, Package, and Delivery_Distribution classes.
  This way each object can easily contain all the variables they need to throughout the program execution. For a data structure I used python dictionaries
  to hold the package data subdivided into "Delivered" and "Undelivered" sections for package searches.

  Packages are read from the data.py file, initialized, and loaded into the Delivery_Distribution object. The data variables are in a Delivery_Data object with
  json formated package and distance data.

  The main code flow is as follows. I have opted for a greedy version of Dijkstra's Algorithm. The purpose being that the two trucks are operating simultaneously.
  The truck with the next available open time searches for the next package delivery location. The available locations are filtered by whether they are eligible for delivery.
  This is based on whether the location has non-delivered or in route packages, packaged with packages responsibility, truck number requirements,
  and package availability. I then use a greedy approach where the locations are nodes on a tree and it chooses the best packages delivered per mile as the node number.
  The location is then added to the truck route. The route is then checked to see if any deadlines would not be met and rearranges the route if necessary.
  When the truck routes are finalized, the times when a delivery has occurred and the delivery status of the packages at that time are displayed. I have included
  travel times back to the delivery "HUB" during routing. Delivery times themselves are tracked in each package object. Finally, I go into a user interface where
  individual package details can be examined or package statuses can be seen at selected times.


# Alternative Algorithms

  Other algorithms that I could have used would be A* search and D*.

  An A* search would be slower to implement since it needs to generate routes for all possibilities to the end, dropping the worst or invalid one.
  This would be complicated to generate for two trucks simultaneously. A benefit would be ideally fitted routes, but it would be a lot more costly
  to implement. (A* Search Algorithm, Geeks for Geeks)

  A D* search would involve searching from a goal node and expanding back to the "HUB". Since there is no target to go towards, it is not adaptable to this
  situation. It also causes problems due to package carrying restrictions and having to return the "HUB". This, like A*, would also be heavier on the search
  side of the solution. (D* Search Algorithm, Wikipedia)

# Discuss the ability of your solution to adapt to a changing market and to scalability.

  This solution is fairly adaptable. The distance and package data can be easily swapped with another set. The package data variables and distances to locations
  used in this adaption are in json format. It seems reasonable that data would be collected to use in that form for a different city mapping. This would be passed
  in the form of a json object with the keys "packages", "distances", and "address_to_place". The Data class in data.py is a hard coded version of this.

  The data structure I have set up is object oriented based. Package data is read from the Data object, initialized into package objects, and stored in a python dictionary
  in the Delivery_Distribution object. Truck objects are also stored with the Delivery_Distribution object in an array. This keeps the process object oriented so that data is easily
  organized, flexible, and access time is fast during execution.

  The solution is adaptable to changes that can occur during daily execution since it is finding the next route location one by one instead of locking into a set route.
  I have also included route rearrangements if deadlines are not met. Finally, I believe it can be scaled without issue since any additions are just additions
  to the json input and the memory requirements to extend a dictionary or create new object are small. Thinking about scalability as well, I have reductions in location searches based on truck eligibility. Also there is a reduction in the O(N) of package location searches during the execution of program as packages delivered are moved into a separate dictionary key.

# Discuss the efficiency and maintainability of the software.

  The efficiency is quadratic, but N's scale down as packages are delivered due to the dictionary access of self.packages. Also some worst case scenarios are factored
  in such as all packages having deadlines before end of day.

  The code set should be easy to maintain due to the object oriented design. Functionality can be added or adjusted to certain methods without drastically effecting other method processes.


# Discuss the self-adjusting data structures chosen and their strengths and weaknesses based on the scenario.

  Locations are added to truck routes in cycles. The self-adjusting aspect in this solution checks if any package delivery deadlines would be missed by a route addition.
  If so, I have written a code segment to reorder that truck route, shuffle_for_deadlines, to the most efficient rearrangement that meets all deadlines. Packages are moved from
  a "Not Delivered" subset of the packages dictionary to the "Delivered" reducing location search times throughout execution.

  The strength is that a location can be moved around to meet delivery deadlines without adding a lot of time complexity to the solution. Otherwise, routing would have to have
  simulated lookaheads on each cycle. These would be exponential since you are also looking for the least amount of distance travelled. So you would essentially have to simulate all
  possibilities, check if deadlines are met, and look for the most efficient. The strength of this algorithm is that it is an undirected solution, which is ideal since I don't have an
  end goal target node. Another is that I can easily weight each location node and search through the tree iteratively choosing an ideal next location without having to project too
  far in advance. This seems like a reasonable less intensive middle ground solution.

  A weaknesses of this solution are that the solution's time complexity is based on the length of the current route of locations. So rearrangements later in the day become
  more intensive. However, each truck route length is lowered with each other truck in service. Another weakness is that if this was to become a real time live service. Package delivery times
  would need to be calculated from "HUB" to "HUB" to get accurate delivery times for packages beforehand.

  For expansion into other cities/markets, I think this structure is advantageous since different objects can be initialized to run in different cities. In other words, the operations can be separated into different instances of the program and be tuned to any specialized needs. For adding trucks, the set_truck_routes method would need to be slightly adjusted to move through a list of trucks. The rest of the methods are passed instances of trucks and wouldn't need any adjustment.

  Finally, the data in this execution is hard coded in data.py. Ideally, instead of providing .xlsx, the data could be provided in a standard json format which is what I have
  translated the provided docs into. The Data_Delivery class is just a container to hold the information. In a production capacity an API could be set to collect GET requests
  passed in json format with "packages", "distances", and "address_to_place" keys or they could be loaded from a database at execution. The program would then execute the same
  way and the return would be the route information jsonified.

# Memory and Bandwidth

  The memory requirements for this example are 2240 bytes for all the packages or 56 bytes per package object instance. The dictionary container uses 1184 bytes to hold the package data. Each truck is also 56 bytes per object instance as well as the delivery distribution object. So overall, the amount of memory and bandwidth needed to execute this program is fairly small and highly scalable.

# Alternative data structures

  I used a key-value pair dictionary for the containers for packages. It is O(1) for package lookups and O(p) for searching for package locations. Since each package has an autoincrement
  packageID, a hash table with a key of packageID would also function the same as the python dictionary. This would not have any collision issues due to the packageID being a primary key identifier. It might cause issues when trying to pop delivered packages, so I might have longer searches to see if a package has been delivered or not. I could also just use an array/list to hold the package objects. This data structure would function but would always be O(n) for searches through the array. I could still pop packages from a "Not Delivered" array which would reduce O(N) searches through the execution
  of the program. So while this data structure would not be fully ideal, it is a viable option.

  Also, I might reorganize the data structure as it is currently to make the locations the keys in self.packages. This would result in grouping packages by location. I think that would reduce the runtime by removing some location search times. It would reduce the available locations search because there wouldn't be duplicate locations found by searching packages. I think overall that would make a slightly more efficient program since there will most likely always be more packages than locations.


# Initiate:
  - initialize Distances object from data.py
  - initialize 2 Truck objects
  - initialize Delivery_Distribution object
  - initialize Package objects from in data.py
  - start set_truck_routes()


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



#  Delivery_Distribution Flow

  - all functionality is run through the Delivery_Distribution object
    Truck and Package are used as data storage objects

  - add_package
      - add_package into Delivery_Distribution object
      - sets delivery_deadline and availability information

  - set_truck_routes
      - increments by delivery time and calls find_and_deliver(truck) for whichever truck is available
      - when all packages are delivered. checks are run to see if all package deadlines are met
      and adjust truck routes if necessary
      - finally prints routing results print_route_results

  - find_and_deliver
      - updates information about packages being currently delivered if currently_delivering
      - gets delivery_time of next found route from get_truck_routes()
      - sets trucks next delivery_time
      - moves truck to HUB if no next location found or package limit reached
      - marks truck as done if at HUB and no packages are left to deliver

        - get_truck_routes
            - find available locations, find truck route, add_route if route found

                - get_available_locations
                    - get available locations to search for truck route
                    - prioritize filling packaged_with packages

                - find_route
                    - find most efficient next location to add to route
                    - weight locations by package per distance (location_packages / route_distance)
                    - adds "HUB" travel to the route if necessary

                - add_route
                    - update truck data, add packages/locations to route, return projected delivery_time
                    - if "HUB" in route add "HUB" distance and location to the route and reset packages
                      carried away from hub
                    - mark packages time of delivery

  - check_if_met_deadlines
      - loops through delivered packages and checks if delivery_deadline < delivered_time
      - shuffle_for_deadlines if package deadlines are not met

  - shuffle_for_deadlines
      - rearrange routes so that all package deadlines are made
      - insert route location into truck.shortest_route and run route_is_valid check
      - updates truck.shortest_route to the most efficient rearrangement

          - adjust_delivery_times
              - recalculates package delivery times for shuffled route

          - route_is_valid
              - checks if route meets all constraints
              - deadlines met, packged_with, max_packages

  - print_route_results
      - prints package status at delivery_times via print_status method
      - prints each trucks final route distance, route, and number of packages
      - finally prints total distance travelled for both trucks

          - print_status
              - prints the delivery status of all packages at each delivery time chronologically


  - helper_methods
      - lookup_package
          - lookup package by any package class variables

      - lookup_status
          - lookup status by packageID

      - get_packages_with_deadlines
          - return all packages with deadlines other than end of day

      - get_deadline
          - get time to meet for deadline_packages passed

      - get_packages
          - get packages for given location and truck

      - get_deadline_locations
          - get all locations for passed deadline_packages

      - get_route_distance
          - get distance of passed route based on data.Distances

      - route_time
          - get time to complete route in seconds. Based of distance/truck speed


## Evaluate space-time complexity using Big O notation throughout the coding and for the entire program.

  Source for learning more about time complexity :
  (Big O Notation, HackerRank, https://www.youtube.com/watch?v=v4cd1O4zkGw)

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



# Sources

Dijkstra's Algorithm
https://www.programiz.com/dsa/dijkstra-algorithm
https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm

A* search algorithm
https://en.wikipedia.org/wiki/A*_search_algorithm
https://www.geeksforgeeks.org/a-search-algorithm
D* search algorithm
https://en.wikipedia.org/wiki/D*

Time complexity
https://www.youtube.com/watch?v=v4cd1O4zkGw
