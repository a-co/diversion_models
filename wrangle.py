import cymetric as cym
import pandas as pd
import math

import numpy as np
import random

from cymetric import graphs as cgr
from cymetric import timeseries as tm
from cymetric import filters as fl

from collections import Counter

# extract data from sqlite file 
def tidy_df(file):
    db = cym.dbopen(file)
    ev = cym.Evaluator(db=db, write=True)
    
    agentTable = ev.eval("AgentEntry")
    try: 
        agents = agentTable.loc[:, ["AgentId", "Prototype"]]
    except: 
        print("there was an agent issue with " + file)
    
    transTable = ev.eval("Transactions")
    try: 
        transactions = transTable.loc[:, ["SenderId", "ReceiverId", "ResourceId", "Commodity", "Time"]]
    except: 
        print("there was an transactions issue with " + file)
    
    resourceTable = ev.eval("Resources")
    try: 
        resources = resourceTable.loc[:, ["ResourceId", "Quantity"]]
    except:
        print("there was a resources issue with " + file)
    
    reactorTable= ev.eval("ReactorEvents")
    try: 
        reactor_events = reactorTable.loc[:, ["Time", "Event"]]
        emissions = reactor_events.loc[reactor_events["Event"] == "DISCHARGE"]
        print("EMISSIONS", emissions)
    except: 
        print("there was a reactor issue with " + file)
    
    #merge agents, transactions, and resources
    int1 = pd.merge(transactions, resources, on='ResourceId', how='inner')

    #rename AgentId column to facilitate merge 
    send = agents.rename(columns = {"AgentId": "SenderId"})
    receive = agents.rename(columns = {"AgentId": "ReceiverId"})

    for i in range(len(int1)):
        for j in range(len(send)):
            if int1.loc[i,"SenderId"] == send.loc[j, "SenderId"]:
                int1.loc[i,"SenderId"] = send.loc[j, "Prototype"]
                
    for i in range(len(int1)):
        for j in range(len(receive)):
            if int1.loc[i,"ReceiverId"] == receive.loc[j, "ReceiverId"]:
                int1.loc[i,"ReceiverId"] = receive.loc[j, "Prototype"]

    return int1

# trim resource-identifying columns 

def trim_data(df):
    trimmed = df[["SenderId", "ReceiverId", "Time", "Quantity"]]
    trimmed["fraction"] = pd.Series(0, index = range(316)) #modular? 
    trimmed["truck"] = pd.Series(0, index = range(316))
    
    #assume leu and heu enrichment happens in the same physical facility
    #drop rows with transactions between enrichment facilities
    short = trimmed.loc[(trimmed['SenderId'] != "LEUenrich") & (trimmed['ReceiverId'] != "LEUtoHEUenrich")]
    
    #change the name of enrichment facilites 
    short["SenderId"] = short['SenderId'].replace({'LEUenrich': 'enrichment', 'LEUtoHEUenrich': 'enrichment'})
    short['ReceiverId'] = short['ReceiverId'].replace({'LEUenrich': 'enrichment', 'LEUtoHEUenrich': 'enrichment'})
    
    return short

# define truck 

def send_trucks(truck_df, truck_size): 
    truck_df["fraction"] = truck_df["Quantity"] / truck_size
    
    #collect set of all transaction types: 
    transaction_pairs = Counter()
    for i in range(len(truck_df)): 
        sender = truck_df.iloc[i, 0]
        receiver = truck_df.iloc[i, 1]
        transaction_pairs.update({(sender, receiver): truck_df.iloc[i, 3]})
        stored_material = transaction_pairs[(sender, receiver)]
        if stored_material >= truck_size: 
            trucks = stored_material // truck_size
            truck_df.at[i, "truck"] = trucks
            transaction_pairs[(sender, receiver)] -= trucks * truck_size
        else: 
            truck_df.at[i, "truck"] = 0
        
            
    print(transaction_pairs)
    print(truck_df)
        
    return truck_df

# define isotope signal 

def isotope_signal(filename): #parameters: duration, dt, some transaction table (check for reactor refueling)
    #converted to seconds:
    half131m = (11.9*24*60*60) #days
    half133 = (5.25*24*60*60) #days
    half133m = (2.19*24*60*60) #days
    half135 = (9.10*60*60) #hours
    time_step = (24*60*60)
    
    l131m = -np.log(2) / half131m
    l133 = -np.log(2) / half133
    l133m = -np.log(2) / half133m
    l135 = -np.log(2) / half135
    
    tidydf = tidy_df(filename)

    #find all of the reactor cycle starts 
    #calculate ratios for each t in cycle
    isotope_rows = []
    duration = int(tidydf["Time"].max())
    print(duration)
    cycle_ends = tidydf[tidydf["SenderId"] == "LWR"]["Time"].to_list()
    print(cycle_ends)
    print(type(cycle_ends[0]))
    
    for i, t in enumerate(range(duration+1)): 
        row = {"135/133m": 0, "135/133": 0, "135/131m": 0, \
               "133m/133": 0, "133m/131m": 0, "133/131m": 0}
        
        if t >= cycle_ends[0]: #every time the reactor sends material elsewhere
            previous_row = isotope_rows[i-1]
            row["135/133m"] = previous_row["135/133m"] * np.exp(-(l135-l133m)*t)
            row["135/133"] = previous_row["135/133"] * np.exp(-(l135-l133)*t)
            row["135/131m"] = previous_row["135/131m"] * np.exp(-(l135-l131m)*t)
            row["133m/133"] = previous_row["133m/133"] * np.exp(-(l133m-l133)*t)
            row["133m/131m"] = previous_row["133m/131m"] * np.exp(-(l133m-l131m)*t)
            row["133/131m"] = previous_row["133/131m"] * np.exp(-(l133-l131m)*t)
    
            if t in cycle_ends: #first isotopes released after first cycle
                #multiply each by random variable
                row["135/133m"]  += 607
                row["135/133"]   += 66.4
                row["135/131m"]  += 220000
                row["133m/133"]  += 0.109
                row["133m/131m"] += 363
                row["133/131m"]  += 3320

        isotope_rows.append(row)  
        
    isotope_columns = []
    
    for t in range(144): 
        for key, value in isotope_rows[t].items(): 
            isotope_columns.append({f'{key}_t{t}': value})

    isotope_df = pd.DataFrame(isotope_columns)
    long_row = isotope_df.sum().to_frame().T
    
    return long_row

# assemble columns and rows 

def make_cols(max_time):
    col_names = ["diversion"]
    transactions = {
          ('civ_enrichment', 'civ_str_u_dep'), ('mine', 'milling'), ('milling', 'conversion'), 
          ('civ_enrichment', 'civ_fabrication'), ('conversion', 'civ_enrichment')
    }
    
    for t in range(max_time):
        for trans in sorted(transactions): 
            col_names.append(trans[0] + "--" + trans[1] + "|time" + str(t))
    return col_names
 
def make_row(truckdf, max_time):
    long_row = []
    
    long_row.append("mil_enrichment" in truckdf["ReceiverId"].tolist())
    transactions = {
           ('civ_enrichment', 'civ_str_u_dep'), ('mine', 'milling'), ('milling', 'conversion'), 
           ('civ_enrichment', 'civ_fabrication'), ('conversion', 'civ_enrichment')
    }
    sorted_trans = sorted(transactions)
    for t in range(max_time):
        #subset rows with this timestep
        subset = truckdf.loc[truckdf['Time'] == t]
        sub_row = [0] * len(transactions)
        
        for index, row in subset.iterrows():
            #check each possible transaction
            for t in range(len(transactions)): 
                if row["SenderId"] == sorted_trans[t][0] and row["ReceiverId"] == sorted_trans[t][1]:    
                    sub_row[t] = truckdf.loc[index, "truck"]

        long_row.extend(sub_row)
    return long_row

# assemble dataframe 

def file_to_line(filename, truck_size, max_time):
    return make_row(send_trucks(trim_data(tidy_df(filename)), truck_size), max_time)
    
def simulation_data(files, truck_size, max_time):
    columns = make_cols(max_time)
    print(len(columns))
    rows = []
    for file in files: 
        
        rows.append(file_to_line(file, truck_size, max_time))
    
    isotope_rows = []
    for file in files: 
        print(file)
        isotopes = isotope_signal(file)
        isotope_rows.append(isotopes.iloc[0].values.tolist())
        if file == files[0]: 
            isotope_columns = isotopes.columns.to_list()
        
    return pd.concat([pd.DataFrame(data = rows, columns = columns), pd.DataFrame(data=isotope_rows, columns=isotope_columns)], axis=1)

if __name__ == "__main__": 
    cyclus_files = [f"small_time_step/run{i}.sqlite" for i in range(10)]
    df = simulation_data(cyclus_files, 12000, 365)
    with open ("simulation_data.py", "w") as outfile: 
        outfile.write(df)
    outfile.close()





