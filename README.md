# micropg_superlite
**The world's lightest PostgreSQL driver for MicroPython, made for ESP8266**

If you encounter any problems, have questions, or would like to suggest an improvement, feel free to open an [issue](https://github.com/TimonW-Dev/micropg_superlite/issues) or contact me by email using the address linked in [my profile](https://github.com/TimonW-Dev). Please keep in mind that micropg_superlite is an open-source project released under the MIT License and maintained on a voluntary basis, so support is provided as time allows.

**micropg_superlite is based on [micropg](https://github.com/nakagami/micropg), which was developed by [nakagami](https://github.com/nakagami). Therefore very big thanks to nakagami for the great development. Without micropg there wouldn't be micropgsuper_lite!**

## About micropg_superlite
`micropg_superlite` is the smallest PostgreSQL driver for MicroPython and is best for devices with little RAM. The ESP8266 has very little RAM, so it can only run `micropg_lite` or `micropg_superlite`.

Compare the features and RAM usage of each driver to choose the right PostgreSQL library for your MicroPython project.

| Feature | [micropg](https://github.com/nakagami/micropg) | [micropg_lite](https://github.com/TimonW-Dev/micropg_lite) | [micropg_superlite](https://github.com/TimonW-Dev/micropg_superlite) **you are here** |
|---|---|---|---|
| 💾 RAM usage¹ | 27,552 bytes (26.91 KiB)<br>Reference | 8,336 bytes (8.14 KiB)<br>70% less than `micropg` | 6,928 bytes (6.77 KiB)<br>75% less than `micropg`; 17% less than `micropg_lite` |
| 🔍 `SELECT` | ✅ Supported | ✅ Supported | ✅ Supported |
| ➕ `INSERT` | ✅ Supported | ✅ Supported | ✅ Supported |
| ✏️ `UPDATE` | ✅ Supported | ✅ Supported | ✅ Supported |
| 🗑️ `DELETE` | ✅ Supported | ✅ Supported | ✅ Supported |
| 🔐 Authentication | ✅ SCRAM-SHA-256, MD5 | ⚠️ SCRAM-SHA-256 only | ⚠️ SCRAM-SHA-256 only |
| ⚠️ Detailed error handling | ✅ Full | ⚠️ Reduced | ⚠️ Reduced |
| 🔒 SSL | ✅ Supported | ✅ Supported | ❌ Not supported |
| 💾 Manual commit | ✅ Supported | ✅ Supported | ❌ Not supported (forced autocommit) |
| ↩️ `ROLLBACK` | ✅ Supported | ✅ Supported | ❌ Not supported |
| 🗄️ Create/drop database | ✅ Supported | ✅ Supported | ❌ Not supported |
| 📦 Native `executemany` support | ✅ Supported | ❌ Not supported | ❌ Not supported |
| 📖 Source code readability | ✅ Readable, clear structure | ❌ Compact and optimized for RAM | ❌ Compact and optimized for RAM |

¹ RAM usage measured on a Raspberry Pi Pico W running MicroPython firmware 1.29.0. Actual usage may vary with the firmware build and measurement conditions.

## Installation

### Which file should I use: `.py` or `.mpy`?

**We recommend using `micropg_superlite.py`.** If you need to save even more RAM, you can also use the precompiled `micropg_superlite.mpy` file, but this is not necessary in most cases. The `.mpy` file may be incompatible with some MicroPython firmware and cannot be edited or debugged like the `.py` file.

### Steps

1. Download the `micropg_superlite.py` or the precompiled `micropg_superlite.mpy` file from the root of this repository to your local computer.

2. Copy the file to the "/lib" folder on the microcontroller using the Thonny IDE or another program. If there is no "lib" folder in the root directory, you have to create it.

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
    └─ micropg_superlite.py   (or micropg_superlite.mpy)
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
conn.close()

````