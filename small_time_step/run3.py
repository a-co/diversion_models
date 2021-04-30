SIMULATION = {'simulation': {'control': {'duration': '365', 'startmonth': '1', 'startyear': '2021', 'decay': 'never', 'explicit_inventory': 'true'}, 'archetypes': {'spec': [{'lib': 'cycamore', 'name': 'Enrichment'}, {'lib': 'cycamore', 'name': 'Reactor'}, {'lib': 'cycamore', 'name': 'Source'}, {'lib': 'cycamore', 'name': 'Sink'}, {'lib': 'agents', 'name': 'NullRegion'}, {'lib': 'agents', 'name': 'NullInst'}, {'lib': 'cycamore', 'name': 'Reactor'}, {'lib': 'cycamore', 'name': 'Separations'}]}, 'facility': [{'name': 'UraniumMine', 'config': {'Source': {'outcommod': 'c_uore', 'outrecipe': 'r_nat_u', 'throughput': '87.86422566185702'}}}, {'name': 'LEUEnrichmentFacility', 'config': {'Enrichment': {'feed_commod': 'c_uore', 'feed_recipe': 'r_nat_u', 'product_commod': 'c_leu', 'tails_commod': 'c_spent_leu', 'swu_capacity': '1000', 'max_feed_inventory': '100', 'max_enrich': '0.041', 'initial_feed': '0'}}}, {'name': 'LWR', 'config': {'Reactor': {'fuel_incommods': {'val': 'c_leu'}, 'fuel_inrecipes': {'val': 'r_leu'}, 'fuel_outcommods': {'val': 'c_spent_leu'}, 'fuel_outrecipes': {'val': 'r_leu_spent'}, 'cycle_time': '94', 'refuel_time': '14', 'assem_size': '295', 'n_assem_core': '3', 'n_assem_batch': '1', 'power_cap': '90'}}}, {'name': 'SpentFuelSink', 'config': {'Sink': {'in_commods': {'val': 'c_spent_leu'}}}}], 'region': {'name': 'MyRegion', 'config': {'NullRegion': None}, 'institution': {'name': 'inst', 'initialfacilitylist': {'entry': [{'number': 1, 'prototype': 'UraniumMine'}, {'number': 1, 'prototype': 'LEUEnrichmentFacility'}, {'number': 1, 'prototype': 'LWR'}, {'number': 1, 'prototype': 'SpentFuelSink'}]}, 'config': {'NullInst': None}}}, 'recipe': [{'name': 'r_nat_u', 'basis': 'mass', 'nuclide': [{'id': '92235', 'comp': '0.00711'}, {'id': '92238', 'comp': '0.99289'}]}, {'name': 'r_heu', 'basis': 'mass', 'nuclide': [{'id': '92235', 'comp': '0.9'}, {'id': '92238', 'comp': '0.1'}]}, {'name': 'r_leu', 'basis': 'mass', 'nuclide': [{'id': '92235', 'comp': '0.04'}, {'id': '92238', 'comp': '0.96'}]}, {'name': 'r_leu_spent', 'basis': 'mass', 'nuclide': [{'id': '92235', 'comp': '0.01'}, {'id': '92238', 'comp': '0.94'}, {'id': '94239', 'comp': '0.01'}, {'id': '55135', 'comp': '0.3'}]}]}}