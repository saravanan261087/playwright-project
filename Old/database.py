import psycopg2

conn = psycopg2.connect(
    host="10.0.117.69",
    port="5432",
    database="cirrusdb",
    user="cirrusdevicetest",
    password="cirrusdevicetestpass123"
)
print("Connected to PostgreSQL successfully")

cursor = conn.cursor()

cursor.execute("""
select create_dt_ts,* from cirrus.cirrus_operations 
where guid= '88-73-84-53-00-01-1D-A6' order by create_dt_ts desc
""")

row = cursor.fetchone()

#print("Columns:")
#print([d[0] for d in cursor.description])

print("\nOutput:", row)

with open("DB output.txt", "w") as file:
    file.write("Output:\n")
    file.write(str(row))

cursor.close()
conn.close()