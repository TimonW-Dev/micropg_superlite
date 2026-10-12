# micropg_superlite

**The World's Lightest PostgreSQL Driver for MicroPython, Designed for ESP8266**

`micropg_superlite` is made for MicroPython devices with very little RAM. Compare its features and memory usage with the other drivers to choose the right library for your project.

## 📚 Contents

- [About](#-about-micropg_superlite)
- [Features and comparison](#-features-and-comparison)
- [Installation](#-installation)
- [Examples](#-examples)
- [Support and acknowledgements](#-support-and-acknowledgements)

## ℹ️ About micropg_superlite

`micropg_superlite` is a compact PostgreSQL driver for MicroPython boards with limited RAM, especially the ESP8266. It is based on [`micropg`](https://github.com/nakagami/micropg) and focuses on keeping memory usage low while still supporting the common SQL operations `SELECT`, `INSERT`, `UPDATE`, and `DELETE`.

For a quick overview and help choosing the right `micropg` driver for your project, see the comparison table below.

### 📊 Features and comparison

| Feature | [micropg](https://github.com/nakagami/micropg) | [micropg_lite](https://github.com/TimonW-Dev/micropg_lite) | [micropg_superlite](https://github.com/TimonW-Dev/micropg_superlite) **(this project)** |
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

¹ RAM usage was measured on a Raspberry Pi Pico W running MicroPython firmware 1.29.0. Actual usage may vary depending on the firmware build and measurement conditions.

## 📥 Installation

### Choose a file

**We recommend `micropg_superlite.py`.** If you need to save even more RAM, you can use the precompiled `micropg_superlite.mpy` file. In most cases, this is not necessary. The `.mpy` file may be incompatible with some MicroPython firmware and cannot be edited or debugged like the `.py` file.

### Install on your microcontroller

1. Download `micropg_superlite.py` from the root of this repository.
2. Copy the file into the `/lib` folder on your microcontroller using Thonny IDE or another tool. Create the folder if it does not exist.
   - **Thonny tip:** Open **View** in the top bar and enable **Files**. You can then upload files and create folders on the microcontroller.
3. Import the library in your MicroPython script:

```python
import micropg_superlite
```

Your files should be arranged like this:

```text
/
├── example.py
└── lib/
    └── micropg_superlite.py
```

## 🚀 Examples

Establish a network connection before running any `micropg_superlite` code. The SELECT example below includes a Wi-Fi connection template; the other examples assume that the connection is already established.

### Example files

The [`examples/` folder](https://github.com/TimonW-Dev/micropg_superlite/tree/main/examples) contains:

- [`docker-postgres-container-setup.sh`](https://github.com/TimonW-Dev/micropg_superlite/blob/main/examples/docker-postgres-container-setup.sh), to create an empty PostgreSQL container.
- [`exampleDatabase.sql`](https://github.com/TimonW-Dev/micropg_superlite/blob/main/examples/exampleDatabase.sql), the database used by the examples.
- Complete test scripts with WLAN connection templates, plus examples for creating and dropping tables and databases.

### 🔍 SELECT (including Wi-Fi setup)

Replace the Wi-Fi credentials and server details with your own:

```python
import time
import network
import micropg_superlite

ssid = 'wifissid'
password = 'secret'

# Connect to the network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected():
    print("Wi-Fi status:", wlan.status())
    time.sleep(1)

print("Wi-Fi connected")

conn = micropg_superlite.connect(
    host='127.0.0.1',  # Replace with your server's IP address
    user='postgres',
    password='123456',
    database='exampledatabase'
)
cur = conn.cursor()

cur.execute('select * from customers')
selectresult = cur.fetchall()
conn.close()

# Print the raw data
print(selectresult)

# Print the data as rows
for row in selectresult:
    for value in row:
        print(value, end="\t")
    print()
```

### ➕ INSERT

```python
conn = micropg_superlite.connect(
    host='127.0.0.1',  # Replace with your server's IP address
    user='postgres',
    password='123456',
    database='exampledatabase'
)
cur = conn.cursor()

cur.execute(
    'INSERT INTO customers (id, firstName, lastName, email) values (%s, %s, %s, %s)',
    ['5', 'David', 'Wilson', 'david.wilson@example.com']
)
conn.close()
```

### ✏️ UPDATE

```python
conn = micropg_superlite.connect(
    host='127.0.0.1',  # Replace with your server's IP address
    user='postgres',
    password='123456',
    database='exampledatabase'
)
cur = conn.cursor()

cur.execute("update customers set firstName='UpdatedFirstName' where id=2;")
conn.close()
```

### 🗑️ DELETE

```python
conn = micropg_superlite.connect(
    host='127.0.0.1',  # Replace with your server's IP address
    user='postgres',
    password='123456',
    database='exampledatabase'
)
cur = conn.cursor()

cur.execute("delete from customers where id=1;")
conn.close()
```

## 💬 Support and acknowledgements

If you encounter a problem, have a question, or would like to suggest an improvement, please [open an issue](https://github.com/TimonW-Dev/micropg_superlite/issues). You can also contact me by email using the address linked in [my profile](https://github.com/TimonW-Dev). This is an open-source project maintained on a voluntary basis, so support is provided as time allows.

`micropg_superlite` is based on [micropg](https://github.com/nakagami/micropg), developed by [nakagami](https://github.com/nakagami). Many thanks to nakagami for the great work — without micropg, micropg_superlite would not exist!

Released under the MIT License.
