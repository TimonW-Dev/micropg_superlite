# micropg_superlite V3

This README contains the most important things you need to know about micropg_superlite. You can find detailed documentation in the [wiki of this repository](https://github.com/TimonW-Dev/micropg_superlite/wiki).

If there are any problems, questions, bugs or suggestions for improvement, please open an [issue](https://github.com/TimonW-Dev/micropg_superlite/issues) on this Github repository or write an email to the email address linked in [my profile](https://github.com/TimonW-Dev). We are happy to provide the necessary free support to help you with your micropg_superlite requests.

## About micropg_superlite
### Difference between [micropg_superlite](https://github.com/TimonW-Dev/micropg_superlite) and [micropg](https://github.com/nakagami/micropg)

[micropg_superlite](https://github.com/TimonW-Dev/micropg_superlite) is a lightweight version based on [micropg](https://github.com/nakagami/micropg) by [
nakagami](https://github.com/nakagami). If you have RAM/memory issues with [micropg](https://github.com/nakagami/micropg) than this library might solve this issue.

micropg_superlite has been specially optimised for the ESP8266 microchip and other microchips that have little RAM. micopg_lite works on any microchip that runs micropyhton.

### Major changes in micropg_superlite V3
Those who have already worked with micropg_superlite V2 know that the micropg_superlite V2 driver has some limitations in terms of functionality. Therefore, micropg_superlite V3 was optimized from scratch to bring back the functionality that is present in [Nakagami's](https://github.com/nakagami) [micropg](https://github.com/nakagami/micropg).

## Installation

1. Download the `micropg_superlite.py` file from this repository to your local computer.

2. Copy the `micropg_superlite.py` file to the "/lib" folder on the microcontroller using the Thonny IDE or another program. If there is no "lib" folder in the root directory, you have to create it.

    **Hint** for the Thony IDE:
    
    Open in the top bar the "View" menu and make sure that the entry "Files" has a "✓", if not then click on "Files". Now you can directly download and upload files from your computer to the microcontroller. You also can create folders on the microcontroller.

3. Now you should be able to import the library to your microcontroller in a MicroPython file.

````python
import micropg_superlite
````

## microcontroller file tree
````
/
├─ example.py
└─ lib/
    └─ micropg_superlite.py
````

## Examples
You need to establish a network connection before executing micropg_superlite code. The [SELECT example](#select-example-with-wifi-connection) inclueds the wifi template. All other examples do not include the wifi template.

### examples/ folder
The [examples](https://github.com/TimonW-Dev/micropg_superlite/tree/main/examples) folder has a [docker-postgres-container-setup.sh](https://github.com/TimonW-Dev/micropg_superlite/blob/main/examples/docker-postgres-container-setup.sh) script to create an empty PostgreSQL container and an [exampleDatabase.sql](https://github.com/TimonW-Dev/micropg_superlite/blob/main/examples/exampleDatabase.sql) file which contains the database used in the examples. You will also find complete test scripts with WLAN connection templates and examples for CREATE/DROP TABLE and DATABASE in the examples folder.

### SELECT example with wifi connection:
````python
import time
import network   # Handles the wifi connection
import micropg_superlite

### To Do: Fill in your wifi connection data and change the server data
ssid = 'wifissid'
password = 'secret'

# Connect to network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected():
    print("Wifi Status: ", wlan.status())
    time.sleep(1)


print("Wifi connected")

conn = micropg_superlite.connect(host='127.0.0.1', # To Do: Replace this string with the IP address of your server
                    user='postgres',
                    password='123456',
                    database='exampledatabase')
cur = conn.cursor()

cur.execute('select * from customers')
selectresult = cur.fetchall()
conn.close()

# EXAMPLE: Print raw data
print(selectresult)

# EXAMPLE: Print data table
for r1 in selectresult:
    for r2 in r1:
        print(r2, end="\t")
    print()
````

### INSERT example
````python
conn = micropg_superlite.connect(host='127.0.0.1', # To Do: Replace this string with the IP address of your server
                    user='postgres',
                    password='123456',
                    database='exampledatabase')
cur = conn.cursor()

cur.execute('INSERT INTO customers (id, firstName, lastName, email) values (%s, %s, %s, %s)', ['5', 'David', 'Wilson', 'david.wilson@example.com'])
conn.commit()
conn.close()

````

### UPDATE example
```` python
conn = micropg_superlite.connect(host='127.0.0.1', # To Do: Replace this string with the IP address of your server
                    user='postgres',
                    password='123456',
                    database='exampledatabase')
cur = conn.cursor()

cur.execute("update customers set firstName='UpdatedFirstName' where id=2;")
conn.commit()
conn.close()
````

### DELETE example
```` python
conn = micropg_superlite.connect(host='127.0.0.1', # To Do: Replace this string with the IP address of your server
                    user='postgres',
                    password='123456',
                    database='exampledatabase')
cur = conn.cursor()

cur.execute("delete from customers where id=1;")
conn.commit()
conn.close()

````

## micropg_superlite limitations
- reduced error handling
- no MD5 auth method support
- No native support for the so-called "executemany" function