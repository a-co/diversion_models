SIMULATION = {'simulation': {'agent': [{'name': 'deployer_military', 'prototype': 'military_deployer'}, {'name': 'deployer_civilian', 'prototype': 'civilian_deployer'}, {'name': 'deployer_shared', 'prototype': 'shared_deployer'}], 'archetypes': {'spec': [{'lib': 'cycamore', 'name': 'DeployInst'}, {'lib': 'cycamore', 'name': 'Source'}, {'lib': 'cycamore', 'name': 'Sink'}, {'lib': 'cycamore', 'name': 'Storage'}, {'lib': 'cycamore', 'name': 'Reactor'}, {'lib': 'cycamore', 'name': 'Separations'}, {'lib': 'cycamore', 'name': 'Enrichment'}]}, 'control': {'duration': '144', 'explicit_inventory': 'true', 'startmonth': '1', 'startyear': '2020'}, 'prototype': [{'config': {'Source': {'inventory_size': '1e30', 'outcommod': 'u_ore', 'outrecipe': 'r_u_ore', 'throughput': '1e10'}}, 'name': 'mine'}, {'config': {'Separations': {'feed_commod_prefs': {'val': ['1.0', '10.0', '100.0']}, 'feed_commods': {'val': ['u_ore', 'u_ore1', 'u_ore2']}, 'feedbuf_size': '2e8', 'leftover_commod': 'waste', 'streams': {'item': {'commod': 'u_nat', 'info': {'buf_size': '150000', 'efficiencies': {'item': [{'comp': 'U', 'eff': '.99'}, {'comp': 'O', 'eff': '.99'}]}}}}, 'throughput': '2e8'}}, 'name': 'milling'}, {'config': {'Separations': {'feed_commod_prefs': {'val': '1.0'}, 'feed_commods': {'val': 'u_nat'}, 'feedbuf_size': '200000', 'leftover_commod': 'waste', 'streams': {'item': {'commod': 'uf6', 'info': {'buf_size': '200000', 'efficiencies': {'item': {'comp': 'U', 'eff': '.99'}}}}}, 'throughput': '200000'}}, 'name': 'conversion'}, {'config': {'Enrichment': {'feed_commod_prefs': {'val': '1'}, 'feed_commods': {'val': 'uf6'}, 'feed_recipe': 'r_uox', 'max_feed_inventory': '20000', 'product_commod': 'mil_fiss', 'swu_capacity': '15069.031412187223', 'tails_assay': '0.003', 'tails_commod': 'mil_u_dep'}}, 'name': 'mil_enrichment'}, {'config': {'Storage': {'in_commods': {'val': 'mil_u_dep'}, 'out_commods': {'val': 'mil_u_dep_str'}, 'residence_time': '0'}}, 'name': 'mil_str_u_dep'}, {'config': {'Storage': {'in_commod_prefs': {'val': '1'}, 'in_commods': {'val': 'uf6'}, 'in_recipe': 'r_mil_uox', 'max_inv_size': '30000', 'out_commods': {'val': 'mil_uox'}, 'residence_time': '0'}}, 'name': 'mil_uox_fabrication'}, {'config': {'Reactor': {'assem_size': '14000', 'cycle_time': '2', 'fuel_incommods': {'val': 'mil_uox'}, 'fuel_inrecipes': {'val': 'r_mil_uox'}, 'fuel_outcommods': {'val': 'mil_uox_spent'}, 'fuel_outrecipes': {'val': 'r_mil_uox_spent'}, 'fuel_prefs': {'val': '1'}, 'n_assem_batch': '1', 'n_assem_core': '1', 'power_cap': '0.15', 'refuel_time': '0'}}, 'lifetime': '960', 'name': 'mil_lwr'}, {'config': {'Storage': {'in_commods': {'val': 'mil_mox_spent'}, 'out_commods': {'val': 'mil_mox_spent_str'}, 'residence_time': '60'}}, 'name': 'mil_str_mox_spent'}, {'config': {'Separations': {'feed_commod_prefs': {'val': '1.0'}, 'feed_commods': {'val': 'mil_uox_spent'}, 'feedbuf_size': '30000000000', 'leftover_commod': 'waste', 'streams': {'item': {'commod': 'mil_fiss', 'info': {'buf_size': '3000000000', 'efficiencies': {'item': {'comp': 'Pu', 'eff': '.95'}}}}}, 'throughput': '1e100'}}, 'name': 'reprocessing'}, {'config': {'Storage': {'in_commod_prefs': {'val': '10'}, 'in_commods': {'val': 'mil_fiss'}, 'in_recipe': 'r_mil_heu', 'max_inv_size': '1e100', 'out_commods': {'val': 'mil_heu'}, 'residence_time': '0'}}, 'name': 'mil_str_fiss'}, {'config': {'Enrichment': {'feed_commod_prefs': {'val': ['1', '20']}, 'feed_commods': {'val': ['uf6', 'mil_uf6']}, 'feed_recipe': 'r_natl_u', 'max_feed_inventory': '100000', 'product_commod': 'civ_leu', 'swu_capacity': '35000', 'tails_assay': '0.003', 'tails_commod': 'u_dep'}}, 'name': 'civ_enrichment'}, {'config': {'Storage': {'in_commods': {'val': 'u_dep'}, 'out_commods': {'val': 'u_dep_str'}, 'residence_time': '0'}}, 'name': 'civ_str_u_dep'}, {'config': {'Storage': {'in_commod_prefs': {'val': '1000'}, 'in_commods': {'val': 'civ_leu'}, 'in_recipe': 'r_uox', 'max_inv_size': '30000', 'out_commods': {'val': 'uox'}, 'residence_time': '1'}}, 'name': 'civ_fabrication'}, {'config': {'Reactor': {'assem_size': '29565', 'cycle_time': '18', 'fuel_incommods': {'val': 'uox'}, 'fuel_inrecipes': {'val': 'r_uox'}, 'fuel_outcommods': {'val': 'uox_spent'}, 'fuel_outrecipes': {'val': 'r_uox_spent'}, 'n_assem_batch': '1', 'n_assem_core': '3', 'power_cap': '900', 'refuel_time': '0'}}, 'lifetime': '960', 'name': 'civ_lwr'}, {'config': {'Storage': {'in_commods': {'val': 'uox_spent'}, 'out_commods': {'val': 'uox_spent_str'}, 'residence_time': '60'}}, 'name': 'civ_str_uox_spent'}, {'config': {'DeployInst': {'build_times': {'val': ['37', '37', '61', '73']}, 'n_build': {'val': ['1', '1', '1', '1']}, 'prototypes': {'val': ['mil_enrichment', 'mil_str_u_dep', 'mil_uox_fabrication', 'mil_str_fiss']}}}, 'name': 'military_deployer'}, {'config': {'DeployInst': {'build_times': {'val': ['121', '121', '121', '145', '157', '169']}, 'n_build': {'val': ['1', '1', '1', '1', '1', '1']}, 'prototypes': {'val': ['civ_enrichment', 'civ_str_u_dep', 'civ_fabrication', 'civ_lwr', 'civ_str_uox_spent', 'civ_lwr']}}}, 'name': 'civilian_deployer'}, {'config': {'DeployInst': {'build_times': {'val': ['1', '1', '1']}, 'n_build': {'val': ['1', '1', '1']}, 'prototypes': {'val': ['mine', 'milling', 'conversion']}}}, 'name': 'shared_deployer'}], 'recipe': [{'basis': 'mass', 'name': 'r_u_ore', 'nuclide': [{'comp': '0.0071', 'id': '922350000'}, {'comp': '0.9929', 'id': '922380000'}, {'comp': '999', 'id': '120240000'}]}, {'basis': 'mass', 'name': 'r_natl_u', 'nuclide': [{'comp': '0.0071', 'id': '922350000'}, {'comp': '0.9929', 'id': '922380000'}]}, {'basis': 'mass', 'name': 'r_uox', 'nuclide': [{'comp': '0.05', 'id': '922350000'}, {'comp': '0.95', 'id': '922380000'}]}, {'basis': 'mass', 'name': 'r_uox_spent', 'nuclide': [{'comp': '0.01', 'id': '922350000'}, {'comp': '0.94', 'id': '922380000'}, {'comp': '0.01', 'id': '942390000'}, {'comp': '0.001', 'id': '952410000'}, {'comp': '0.03', 'id': '551350000'}]}, {'basis': 'mass', 'name': 'r_mil_uox', 'nuclide': [{'comp': '0.0071', 'id': '922350000'}, {'comp': '0.9929', 'id': '922380000'}]}, {'basis': 'mass', 'name': 'r_mil_uox_spent', 'nuclide': [{'comp': '0.0071', 'id': '922350000'}, {'comp': '0.9919', 'id': '922380000'}, {'comp': '0.001', 'id': '942390000'}]}, {'basis': 'mass', 'name': 'r_mil_heu', 'nuclide': [{'comp': '0.90', 'id': '922350000'}, {'comp': '0.10', 'id': '922380000'}]}]}}