import random 
import subprocess

base_simulation = {'simulation': 
                   {'control': 
                    {'duration': '365', 'startmonth': '1', 'startyear': '2021', 'decay': 'never', 'explicit_inventory': 'true'}, 
                    'archetypes': 
                    {'spec': [{'lib': 'cycamore', 'name': 'Enrichment'}, 
                              {'lib': 'cycamore', 'name': 'Reactor'}, 
                              {'lib': 'cycamore', 'name': 'Source'}, 
                              {'lib': 'cycamore', 'name': 'Sink'}, 
                              {'lib': 'agents', 'name': 'NullRegion'}, 
                              {'lib': 'agents', 'name': 'NullInst'}, 
                              {'lib': 'cycamore', 'name': 'Reactor'}, 
                              {'lib': 'cycamore', 'name': 'Separations'}]}, 
                    'facility': [{'name': 'UraniumMine', 
                                  'config': 
                                  {'Source': {'outcommod': 'c_uore', 'outrecipe': 'r_nat_u', 'throughput': '100'}}}, 
                                 {'name': 'LEUEnrichmentFacility', 
                                  'config': 
                                  {'Enrichment': {'feed_commod': 'c_uore', 'feed_recipe': 'r_nat_u', 'product_commod': 'c_leu', 
                                                  'tails_commod': 'c_spent_leu', 'swu_capacity': '1000', 
                                                  'max_feed_inventory': '100', 'max_enrich': '0.041', 'initial_feed': '0'}}}, 
                                 {'name': 'LWR', 
                                  'config': 
                                  {'Reactor': {'fuel_incommods': {'val': 'c_leu'}, 
                                               'fuel_inrecipes': {'val': 'r_leu'}, 
                                               'fuel_outcommods': {'val': 'c_spent_leu'}, 
                                               'fuel_outrecipes': {'val': 'r_leu_spent'}, 
                                               'cycle_time': '90', 'refuel_time': '14', 
                                               'assem_size': '295', 'n_assem_core': '3', 
                                               'n_assem_batch': '1', 'power_cap': '90'}}}, 
                                 {'name': 'SpentFuelSink', 
                                  'config': 
                                  {'Sink': {'in_commods': {'val': 'c_spent_leu'}}}}, 
                                 {'name': 'HEUenrich', 
                                  'config': 
                                  {'Enrichment': {'feed_commod': 'c_uore', 'feed_recipe': 'r_nat_u',
                                                  'product_commod': 'c_heu', 'tails_commod': 'heu_tails', 
                                                  'swu_capacity': '1000', 
                                                  'max_feed_inventory': '100', 
                                                  'max_enrich': '0.9', 'initial_feed': '0'}}}, 
                                 {'name': 'LEUtoHEUenrich', 
                                  'config': 
                                  {'Enrichment': {'feed_commod': 'c_leu_spent', 'feed_recipe': 'r_leu_spent', 
                                                  'product_commod': 'c_heu', 'tails_commod': 'c_heu_tails', 
                                                  'swu_capacity': '1000', 'max_feed_inventory': '100', 
                                                  'max_enrich': '0.9', 'initial_feed': '0'}}}, 
                                 {'name': 'HEUSink', 
                                  'config': {'Sink': {'in_commods': {'val': 'c_heu'}}}}], 
                    'region': {'name': 'MyRegion', 
                               'config': 
                               {'NullRegion': None}, 
                               'institution': {'name': 'inst', 
                                               'initialfacilitylist': 
                                               {'entry': [{'number': 1, 'prototype': 'UraniumMine'}, 
                                                          {'number': 1, 'prototype': 'LEUEnrichmentFacility'}, 
                                                          {'number': 1, 'prototype': 'LWR'}, 
                                                          {'number': 1, 'prototype': 'SpentFuelSink'}, 
                                                          {'number': 1, 'prototype': 'HEUenrich'}, 
                                                          {'number': 1, 'prototype': 'LEUtoHEUenrich'}, 
                                                          {'number': 1, 'prototype': 'HEUSink'}]}, 
                                               'config': {'NullInst': None}}}, 
                    'recipe': [{'name': 'r_nat_u', 'basis': 'mass', 
                                'nuclide': [{'id': '92235', 'comp': '0.00711'}, 
                                            {'id': '92238', 'comp': '0.99289'}]}, 
                               {'name': 'r_heu', 'basis': 'mass', 
                                'nuclide': [{'id': '92235', 'comp': '0.9'}, 
                                            {'id': '92238', 'comp': '0.1'}]}, 
                               {'name': 'r_leu', 'basis': 'mass', 
                                'nuclide': [{'id': '92235', 'comp': '0.04'}, 
                                            {'id': '92238', 'comp': '0.96'}]}, 
                               {'name': 'r_leu_spent', 'basis': 'mass', 
                                'nuclide': [{'id': '92235', 'comp': '0.01'}, 
                                            {'id': '92238', 'comp': '0.94'}, 
                                            {'id': '94239', 'comp': '0.01'}, 
                                            {'id': '55135', 'comp': '0.3'}]}]}}



num_runs = 10

for n in range(num_runs): 
    print(str(n+1) + " of " + str(num_runs) + " runs")
    
    sim = base_simulation
    
    diversion = random.choice([True, False])
    if not diversion: 
        sim["simulation"]["facility"] = sim["simulation"]["facility"][0:4]
        sim["simulation"]["region"]["institution"]['initialfacilitylist']['entry'] = [{'number': 1, 'prototype': 'UraniumMine'}, 
                                                          {'number': 1, 'prototype': 'LEUEnrichmentFacility'}, 
                                                          {'number': 1, 'prototype': 'LWR'}, 
                                                          {'number': 1, 'prototype': 'SpentFuelSink'}]
    
    throughput = float(sim["simulation"]["facility"][0]["config"]["Source"]["throughput"]) * random.uniform(0.8, 1.2)
    cycletime = int(sim["simulation"]["facility"][2]["config"]["Reactor"]["cycle_time"]) + random.randint(-15, 15)
    
    sim["simulation"]["facility"][0]["config"]["Source"]["throughput"] = str(throughput)
    sim["simulation"]["facility"][2]["config"]["Reactor"]["cycle_time"] = str(cycletime)
    
    cyclus_file = "small_time_step/run" + str(n) + ".py"
    with open(cyclus_file, "w") as outfile: 
        outfile.write("SIMULATION = " + str(sim))
    outfile.close()
    


for n in range(num_runs):
    process = subprocess.run(['cyclus', f'small_time_step/run{n}.py', '-o', f'small_time_step/run{n}.sqlite'], stdout=subprocess.PIPE)

    with open(f'small_time_step/run{n}.log', 'w') as f:
        print(process.stdout.decode('utf-8'))
        f.write(process.stdout.decode('utf-8'))