I corrected the last part for the code  of WEBSCRAPING to get the df but it didnt save, here it is the code:
launch_dict= dict.fromkeys(column_names)

# Remove an irrelvant column
del launch_dict['Date and time ( )']

# Let's initial the launch_dict with each value to be an empty list
launch_dict['Flight No.'] = []
launch_dict['Launch site'] = []
launch_dict['Payload'] = []
launch_dict['Payload mass'] = []
launch_dict['Orbit'] = []
launch_dict['Customer'] = []
launch_dict['Launch outcome'] = []
# Added some new columns
launch_dict['Version Booster']=[]
launch_dict['Booster landing']=[]
launch_dict['Date']=[]
launch_dict['Time']=[]

for table_number, table in enumerate(soup.find_all('table', "wikitable plainrowheaders collapsible")):
    # get table row 
    for rows in table.find_all("tr"):
        # check to see if the first table heading is a number corresponding to launch a number 
        if rows.th:
            if rows.th.string:
                flight_number = rows.th.string.strip()
                flag = flight_number.isdigit()
        else:
            flag = False
        # get table element 
        row = rows.find_all('td')
        # if it is a number, save cells in a dictionary 
        if flag:
            extracted_row += 1
            # Flight Number value
            launch_dict['Flight No.'].append(flight_number)

            datatimelist = date_time(row[0])
            # Date value
            launch_dict['Date'].append(datatimelist[0].strip(','))

            # Time value
            launch_dict['Time'].append(datatimelist[1])

            # Booster version
            bv = booster_version(row[1])
            if not (bv):
                bv = row[1].a.string
            launch_dict['Version Booster'].append(bv)

            # Launch Site
            launch_site = row[2].a.string if row[2].a else None
            launch_dict['Launch Site'].append(launch_site)

            # Payload
            payload = row[3].a.string if row[3].a else None
            launch_dict['Payload'].append(payload)

            # Payload Mass
            payload_mass = get_mass(row[4])
            launch_dict['Payload mass'].append(payload_mass)

            # Orbit
            orbit = row[5].a.string if row[5].a else None
            launch_dict['Orbit'].append(orbit)

            # Customer
            customer = row[6].a.string if row[6].a else None
            launch_dict['Customer'].append(customer)

            # Launch outcome
            launch_outcome = list(row[7].strings)[0] if row[7].a else None
            launch_dict['Launch outcome'].append(launch_outcome)

            # Booster landing
            booster_landing = landing_status(row[8]) if row[8].a else None
            launch_dict['Booster landing'].append(booster_landing)

# Display the first few rows of the launch_dict
for key, value in launch_dict.items():
    print(f"{key}: {value[:5]}")
