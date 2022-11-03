# Immigrant-counter

The program executes a simulation of an immigration counter at an airport. The airport is operational 24 hours a day.
International flights arrive at the airport as a poisson distribution at an average rate of 1 per hour.
Each flight carries anywhere between 100-200 passengers. All of the arriving passengers are
required to queue up at the immigration counter and get their passports stamped before they
can exit the airport. About two-thirds of the arriving passengers are local citizens, while one-third are foreign nationals.
Each passenger takes about 5-10 minutes to walk from the arrival gate to the immingration counter. There are
'm' counters for local citizens and 'n' counters for foreigners. Each passenger joins one of the two queues for the counters
based on their nationality(local or foreigner). 
Local citizens need to spend about 0.5-1 minutes at the counter, whereas foreign nationals spend 2-3 minutes at the counter since a thorough scrutiny of their visa/passport is required.

The program takes 'm' and 'n' values as input and also the number of times the simulation must run(say x). Next, the program initially simulates 1 simulation for given m,n and plots two graphs; one for the number of passengers in local queue and the other for the number of passengers in the foreigners queue in a time period of 1440 minutes (24 hours).
Next it runs the simulation 'x' number of times and returns the average waiting period for any particular passenger (i.e., time taken between arriving at the airport to completing their immigration check).
