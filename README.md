# Python Challenge Swimlane

This is a coding interview for Swimlane.

The python library 'requests' is required for this to run.

http://docs.python-requests.org/en/latest/user/install/

### Command Line Interface

You can use the unix style philosophy and just `cat` files into this tool's stdin:

`cat <filename> <filename> | python3 main.py`

Or you can pass them in as arguments:

`python3 main.py <filename> <filename>`

By default, when run, this will create a database.json file that stores the data read from the internet.
You can customize your output filename with:

`python3 main.py <filenames> -o <output_filename>`

You can also load a database file with a command line flag:

`python3 main.py database.json -l`

Instead of opening a REPL, you can also run a single query from the command line:

`python3 main.py -l database.json -c 'show [geoip.city] where (geoip.country != US)'`

### Query Language

After loading and saving the database, it will open a shell where you can enter commands to
filter and list the IP addresses.

`show` is the simplest command; it will list all IP addresses.

`show [geoip.country, geoip.city]` will show all IP addresses as well as the city and country found in the geoip lookup.

`show where (geoip.country == US)` will show all IP addresses from the US.

`show where (geoip.country != US)` will show all IP addresses __not__ from the US.

`show [geoip.city] where (geoip.country == US)` will combine both things above.

`show where (or (geoip.country == US) (geoip.country == NL))` will or the two filters together. These can be nested, and
the keyword `and` is also available for anding two filters together.

Example:

```
 > show [geoip.city, geoip.country, geoip.org] where (or (geoip.country == US) (geoip.country == NL))
IP             	geoip.city  	geoip.country	geoip.org                                           	
99.174.36.137  	            	US           	AS7018 AT&T Services, Inc.                          	
166.141.209.233	            	US           	AS22394 Cellco Partnership DBA Verizon Wireless     	
24.197.112.182 	Asheville   	US           	AS20115 Charter Communications                      	
40.82.106.5    	Amsterdam   	NL           	AS8075 Microsoft Corporation                        	
33.238.19.104  	            	US           	                                                    	
166.188.59.37  	            	US           	AS20057 AT&T Mobility LLC                           	
20.219.138.87  	Falls Church	US           	                                                    	
33.67.141.226  	            	US           	                                                    	
4.44.97.176    	            	US           	AS3356 Level 3 Communications, Inc.                 	
208.128.240.230	Chesterfield	US           	AS3561 Savvis                                       	
3.173.155.119  	Fairfield   	US           	                                                    	
13.211.237.22  	Seattle     	US           	                                                    	
159.129.75.124 	Irving      	US           	                                                    	
139.169.190.74 	Houston     	US           	AS1202 National Aeronautics and Space Administration
64.227.30.42   	Jacksonville	US           	AS13768 Peer 1 Network (USA) Inc.                   	
174.156.164.63 	            	US           	AS3651 Sprint                                       	
32.145.242.134 	            	US           	AS2686 AT&T Global Network Services, LLC            	
184.159.117.150	            	US           	AS22561 CenturyTel Internet Holdings, Inc.          	
23.5.102.194   	Amsterdam   	NL           	AS20940 Akamai International B.V.                   	
34.142.6.33    	            	US           	                                                    	
68.211.11.74   	            	US           	AS7018 AT&T Services, Inc.                          	
216.235.211.155	Houston     	US           	AS3900 YHC Corporation                              	
35.192.211.127 	Ann Arbor   	US           	                                                    	
65.100.100.42  	Tucson      	US           	AS209 Qwest Communications Company, LLC             	
184.40.8.232   	            	US           	AS6389 BellSouth.net Inc.                           	
72.240.178.112 	Maumee      	US           	AS13490 Buckeye Cablevision, Inc.                   	
136.17.123.206 	Dearborn    	US           	                                                    	
164.242.37.96  	            	US           	                                                    	
108.65.14.158  	            	US           	AS7018 AT&T Services, Inc.                          	
40.43.195.14   	            	US           	AS4249 Eli Lilly and Company                        	
142.254.194.243	            	US           	AS11426 Time Warner Cable Internet LLC              	
33.33.53.155   	            	US           	                                                    	
107.73.246.73  	            	US           	                                                    	
3.221.25.119   	Fairfield   	US           	                                                    	
131.55.14.207  	Montgomery  	US           	AS385 754th Electronic Systems Group                	
154.54.193.133 	Washington  	US           	AS174 Cogent Communications                         	
```

### Multithreading Performance Increases

Multithreaded w/ 100 lines from list_of_ips.txt

```
real	0m16.550s
user	0m1.393s
sys	   0m0.274s
```

Singlethreaded w/ 100 lines from list_of_ips.txt

```
real	1m21.563s
user	0m2.232s
sys	   0m0.383s
```

The multithreaded version is about 5 times as fast.
