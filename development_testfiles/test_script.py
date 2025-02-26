# This script is made to test the functionality of micropg_superlite after making changes to the source

import network   # Handles the wifi connection
import micropg_superlite
import time

### To Do: Fill in your wifi connection data and change the server data
ssid = 'ssid'
password = 'secret'


### To Do: Fill in your server connection data
db_host = '127.0.0.1'
db_user = 'postgres'
db_password = '123456'
db_database = 'postgres'

# Connect to network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected():
    print("Wifi Status: ", wlan.status())
    time.sleep(1)

print("Wifi connected")
print("---")

start_time = time.time()

conn = micropg_superlite.connect(host=db_host,
                    user=db_user,
                    password=db_password,
                    database=db_database)
cur = conn.cursor()

successCount = 0

### SELECT test
cur.execute("SELECT c.firstName || ' ' || c.lastName AS customer_name, c.email, c.birthDate, o.orderDate, o.status, p.name AS product_name, p.price, oi.quantity, cat.name AS category_name, i.lastRestockDate, COALESCE(p.description, 'No description available') AS product_description, CASE WHEN c.loyaltyPoints > 500 THEN 'VIP' WHEN c.loyaltyPoints > 100 THEN 'Regular' ELSE 'New' END AS customer_status, c.birthDate AS customer_birth_date FROM customers c LEFT JOIN orders o ON c.id = o.customerId LEFT JOIN order_items oi ON o.id = oi.orderId LEFT JOIN products p ON oi.productId = p.id LEFT JOIN categories cat ON p.categoryId = cat.id RIGHT JOIN inventory i ON p.id = i.productId WHERE o.orderDate >= '2024-03-20' AND i.quantity > 0 ORDER BY o.orderDate DESC LIMIT 5;")
selectresult = cur.fetchall()

print(selectresult)

expectedresult = "[('Emily* %Brown', 'emily.brown@example.com', '1995-02-28', '2024-03-30 15:30:00', 'Completed', 'Smart Watch', '199.99', 1, 'Smartphones', '2024-03-08', 'Fitness tracking and notifications', 'New', '1995-02-28'), ('Emily* %Brown', 'emily.brown@example.com', '1995-02-28', '2024-03-30 15:30:00', 'Completed', 'External Hard Drive', '89.99', 1, 'Computers', '2024-03-11', '2TB storage capacity', 'New', '1995-02-28'), ('Emma-Hans 0Clark$', 'emma.clark@example.com', '1998-08-08', '2024-03-29 13:20:00', 'Processing', 'Coffee Maker', '79.99', 1, 'Home & Kitchen', '2024-03-09', '12-cup programmable coffee maker', 'New', '1998-08-08'), ('Mich!?l# Lee@LeeTestChar=?{}()', 'michael.lee@example.com', '1987-03-25', '2024-03-28 10:00:00', 'Pending', 'Laptop Pro X', '1299.99', 1, 'Computers', '2024-03-01', 'High-performance laptop with 16GB RAM', 'Regular', '1987-03-25'), ('Jane Smith', 'jane.smith@example.com', '1985-12-03', '2024-03-26 11:15:00', 'Completed', 'Wireless Mouse', '39.99', 1, 'Accessories', '2024-03-12', 'Ergonomic design with long battery life', 'Regular', '1985-12-03')]"

if expectedresult == str(selectresult):
    print("SELECT ok")
else:
    print("SELECT !!!failed!!!")
    successCount = successCount + 1

print("---")

### INSERT test
cur.execute("INSERT INTO customers (firstName, lastName, email, birthDate, specialNote, loyaltyPoints) VALUES ('Jörg@', 'Müller-Schmïdt#', 'joerg.mueller-schmidt@täst.com', '1976-09-13', 'VIP & allergisch gegen Laktose; bevorzugt Bio-Produkte!', 666)")

cur.execute('select count(Id) from customers')
selectresult = cur.fetchall()

if (selectresult[0][0] == 13):
    print("INSERT ok")
else:
    print("INSERT !!!failed!!!")
    successCount = successCount + 1

print("---")

### UPDATE test
cur.execute("UPDATE customers SET firstName = 'Jörg-Ülrîch™', lastName = 'Müllèr-van der Schmïdt§', email = 'joerg.ueli+mueller-schmidt_123@tæst.çøm', specialNote = CONCAT(specialNote, ' | Achtung: Name geändert! (ツ)_/¯'), loyaltyPoints = loyaltyPoints + 42 WHERE firstName = 'Jörg@' AND lastName = 'Müller-Schmïdt#'")

cur.execute("select firstname from customers WHERE firstName = 'Jörg-Ülrîch™' AND lastName = 'Müllèr-van der Schmïdt§'")
selectresult = cur.fetchall()

if(selectresult[0][0] == "Jörg-Ülrîch™"):
    print("UPDATE ok")
else:
    print("UPDATE !!!failed!!!")

print("---")

### DELETE test
cur.execute("DELETE FROM customers WHERE firstName = 'Jörg-Ülrîch™' AND lastName = 'Müllèr-van der Schmïdt§'")

cur.execute("select count(Id) from customers")
selectresult = cur.fetchall()

if (selectresult[0][0] == 12):
    print("DELETE ok")
else:
    print("DELETE !!!failed!!!")
    successCount = successCount + 1

print("---")

### CREATE TABLE test
cur.execute('CREATE TABLE testTable (testChar varchar(45), testInt Int, testDate date);')

cur.execute("SELECT count(schemaname) FROM pg_catalog.pg_tables WHERE schemaname like 'public'")
selectresult = cur.fetchall()

if (selectresult[0][0] == 7):
    print("CREATE TABLE ok")
else:
    print("CREATE TABLE !!!failed!!!")
    successCount = successCount + 1

print("---")

### DROP TABLE test
cur.execute('DROP TABLE testTable;')

cur.execute("SELECT count(schemaname) FROM pg_catalog.pg_tables WHERE schemaname like 'public'")
selectresult = cur.fetchall()

if (selectresult[0][0] == 6):
    print("DROP TABLE ok")
else:
    print("DROP TABLE !!!failed!!!")
    successCount = successCount + 1

print("---")

### Data types handling test
cur.execute("CREATE TABLE data_types_test (char_col CHAR(1), int_col INT, float_col FLOAT, bool_col BOOLEAN, date_col DATE, null_col VARCHAR(45));")
cur.execute("INSERT INTO data_types_test (char_col, int_col, float_col, bool_col, date_col, null_col) VALUES ('a', 1, 1.1, TRUE, '2024-12-31', NULL);")
cur.execute("SELECT * FROM data_types_test;")
selectresult = cur.fetchall()
print(selectresult)
if (selectresult == [('a', 1, 1.1, True, '2024-12-31', None)]):
    print("DATA TYPES ok")
else:
    print("DATA TYPES !!!failed!!!")
    successCount = successCount + 1
cur.execute('DROP TABLE data_types_test;')

print("---")

### Close connection - prepeare for next step
conn.close()

### Test end. Finish script
print("\n---")

if (successCount == 0):
    print("All tests completed SUCCESSFULLY")
else:
    print("!!! At least one test failed !!!")

print("\n")

end_time = time.time()
duration = end_time - start_time
print(f"Script duration: {duration:.3f} Sekunden")

print("---")