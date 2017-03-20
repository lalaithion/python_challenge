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
