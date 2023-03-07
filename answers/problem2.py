import os
import sqlite3
import datetime

def check_dup_station(station_id, cursor):
    sql_str = "SELECT COUNT(id) FROM station_info WHERE id = {};".format(station_id)
    res = cursor.execute(sql_str).fetchall()
    return res[0][0] > 0

def check_dup_wheather(station_id, date, cursor):
    # Function to avoid duplicate entry
    sql_str = "SELECT COUNT(id) FROM wheather_record WHERE station_id = {} AND date = {};".format(station_id, date)
    res = cursor.execute(sql_str).fetchall()
    return res[0][0] > 0


def ingestion(cursor):
    num_record_station = 0
    num_record_whether = 0

    directory_path = "./wx_data"

    # Loop through each file in the directory
    for filename in os.listdir(directory_path):
        # Check if the current file is a file (not a directory)
        # print(filename)
        if os.path.isfile(os.path.join(directory_path, filename)):
            # insert data to station_info
            station_id = int(filename.split(".")[0].lstrip("USC"))
            station_info_data = [station_id, filename, ""]

            if not check_dup_station(station_id, cursor):
            

                # Execute the SQL command to insert the data
                cursor.execute("INSERT INTO station_info (id, station_name, state_loc) VALUES (?, ?, ?)", station_info_data)

                # Commit the changes to the database
                conn.commit()
                num_record_station += 1
            else:
                print("{} station_id record already exists.".format(station_id))

            with open(os.path.join(directory_path, filename), "r") as file:
                for line in file:
                    content = line.strip().split()
                    # print(content)
                    content[0] = datetime.datetime.strptime(content[0], "%Y%m%d").date()
                    # Convert temperature values from tenths of a degree Celsius to Celsius
                    content[1] = float(content[1]) / 10
                    content[2] = float(content[2]) / 10
                    content[3] = float(content[3]) / 10
                    # Define the data to insert
                    wheather_record_data = [station_id] + content
                    
                    if not check_dup_wheather(wheather_record_data[0], wheather_record_data[1], cursor):

                        # Execute the SQL command to insert the data
                        cursor.execute("INSERT INTO wheather_record (station_id, date, max_temperature, min_temperature, precipitation_amount) VALUES (?, ?, ?, ?, ?)", wheather_record_data)
                        
                        # Commit the changes to the database
                        conn.commit()
                        num_record_whether += 1
                    else:
                        print("{} station_id {} date record already exists.".format(station_id, wheather_record_data[1])) 
        # print("This file is ingested ", station_id)
    res = [num_record_station, num_record_whether]
    return res


# Open a connection to the SQLite database
conn = sqlite3.connect('Wheather.db')
# Get a cursor object
cursor = conn.cursor()
# sql_str = "SELECT COUNT(*) FROM station_info"
# cur_res = cursor.execute(sql_str).fetchall()
# print(cur_res)

# Print the start time
start_time = datetime.datetime.now()
print("Start time: ", start_time)

num_records = ingestion(cursor)

end_time = datetime.datetime.now()
print("End time: ", end_time)

print("Time spend: ", end_time - start_time)

print("number of records ingested: ", num_records)

# Close the connection to the database
conn.close()