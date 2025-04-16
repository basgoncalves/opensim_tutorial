tested_leg = 'r'
non_tested_leg = 'l'

muscles_to_plot = [
    'glut_med1' + tested_leg, 'glut_med2' + tested_leg, 'glut_med3' + tested_leg, 'glut_min1' + tested_leg, 'glut_min2' + tested_leg, 'glut_min3' + tested_leg, 
    'semimem' + tested_leg, 'semiten' + tested_leg, 'bifemlh' + tested_leg, 'bifemsh' + tested_leg, 'sar' + tested_leg, 'add_long' + tested_leg, 'add_brev' + tested_leg, 
    'add_mag1' + tested_leg, 'add_mag2' + tested_leg, 'add_mag3' + tested_leg, 'tfl' + tested_leg, 'pect' + tested_leg, 'grac' + tested_leg, 'glut_max1' + tested_leg, 
    'glut_max2' + tested_leg, 'glut_max3' + tested_leg, 'iliacus' + tested_leg, 'psoas' + tested_leg, 'quad_fem' + tested_leg, 'gem' + tested_leg, 'peri' + tested_leg, 
    'rect_fem' + tested_leg, 'vas_med' + tested_leg, 'vas_int' + tested_leg, 'vas_lat' + tested_leg, 'med_gas' + tested_leg, 'lat_gas' + tested_leg, 'soleus' + tested_leg, 
    'tib_post' + tested_leg, 'flex_dig' + tested_leg, 'flex_hal' + tested_leg, 'tib_ant' + tested_leg, 'per_brev' + tested_leg, 'per_long' + tested_leg, 'per_tert' + tested_leg, 
    'ercspn' + tested_leg, 'intobl' + tested_leg,  'extobl' + tested_leg,
    'ext_dig' + tested_leg, 'ext_hal' + tested_leg, 
    
    'glut_med1' + non_tested_leg, 'glut_med2' + non_tested_leg, 'glut_med3' + non_tested_leg, 'glut_min1' + non_tested_leg, 'glut_min2' + non_tested_leg, 
    'glut_min3' + non_tested_leg, 'semimem' + non_tested_leg, 'semiten' + non_tested_leg, 'bifemlh' + non_tested_leg, 'bifemsh' + non_tested_leg, 'sar' + non_tested_leg, 'add_long' + non_tested_leg, 'add_brev' + non_tested_leg, 
    'add_mag1' + non_tested_leg, 'add_mag2' + non_tested_leg, 'add_mag3' + non_tested_leg, 'tfl' + non_tested_leg, 'pect' + non_tested_leg, 'grac' + non_tested_leg, 'glut_max1' + non_tested_leg, 'glut_max2' + non_tested_leg, 
    'glut_max3' + non_tested_leg, 'iliacus' + non_tested_leg, 'psoas' + non_tested_leg, 'quad_fem' + non_tested_leg, 'gem' + non_tested_leg, 'peri' + non_tested_leg, 'rect_fem' + non_tested_leg, 'vas_med' + non_tested_leg, 
    'vas_int' + non_tested_leg, 'vas_lat' + non_tested_leg,non_tested_leg, 'med_gas' + non_tested_leg, 'lat_gas' + non_tested_leg, 'soleus' + non_tested_leg, 'tib_post' + non_tested_leg, 'flex_dig' + non_tested_leg, 'flex_hal' + non_tested_leg, 
    'tib_ant' + non_tested_leg, 'per_brev' + non_tested_leg, 'per_long' + non_tested_leg,non_tested_leg, 'per_tert' + non_tested_leg, 'ext_dig' + non_tested_leg, 'ext_hal' + non_tested_leg, 
    'ercspn' + non_tested_leg, 'extobl' + non_tested_leg, 'intobl' + non_tested_leg,
]

emg_mappings = {
    'glut_med1_' + tested_leg: tested_leg.upper() + 'GLTMED',
    'glut_med2_' + tested_leg: tested_leg.upper() + 'GLTMED',
    'glut_med3_' + tested_leg: tested_leg.upper() + 'GLTMED',
    'glut_min1_' + tested_leg: tested_leg.upper() + 'GLTMED',
    'glut_min2_' + tested_leg: tested_leg.upper() + 'GLTMED',
    'glut_min3_' + tested_leg: tested_leg.upper() + 'GLTMED',
    'glut_max1_' + tested_leg: tested_leg.upper() + 'GLTMED',
    'glut_max2_' + tested_leg: tested_leg.upper() + 'GLTMED',
    'glut_max3_' + tested_leg: tested_leg.upper() + 'GLTMED',
    'add_brev_' + tested_leg: tested_leg.upper() + 'RADDLONG',
    'add_long_' + tested_leg: tested_leg.upper() + 'RADDLONG',
    'grac_' + tested_leg: tested_leg.upper() + 'RADDLONG',
    'bifemlh_' + tested_leg: tested_leg.upper() + 'RBF',
    'bifemsh_' + tested_leg: tested_leg.upper() + 'RBF',
    'semimem_' + tested_leg: tested_leg.upper() + 'RBF',
    'semiten_' + tested_leg: tested_leg.upper() + 'RBF',
    'tib_ant_' + tested_leg: tested_leg.upper() + 'RTA',
    'ext_dig_' + tested_leg: tested_leg.upper() + 'RTA',
    'ext_hal_' + tested_leg: tested_leg.upper() + 'RTA',
    'vas_med_' + tested_leg: tested_leg.upper() + 'RRF',
    'vas_int_' + tested_leg: tested_leg.upper() + 'RRF',
    'vas_lat_' + tested_leg: tested_leg.upper() + 'RRF',
    'pect_' + tested_leg: tested_leg.upper() + 'RRF',
    'med_gas_' + tested_leg: tested_leg.upper() + 'RGM',
    'lat_gas_' + tested_leg: tested_leg.upper() + 'RGM',
    'soleus_' + tested_leg: tested_leg.upper() + 'RGM'
}

muscles_groups_tetsted_leg = {
    'glut_med': ['glut_med1' + tested_leg, 'glut_med2' + tested_leg, 'glut_med3' + tested_leg],
    'glut_min': ['glut_min1' + tested_leg, 'glut_min2' + tested_leg, 'glut_min3' + tested_leg],
    'glut_max': ['glut_max1' + tested_leg, 'glut_max2' + tested_leg, 'glut_max3' + tested_leg],
    'hamstrings': ['semimem' + tested_leg, 'semiten' + tested_leg, 'bifemlh' + tested_leg, 'bifemsh' + tested_leg],
    'adductors': ['add_long' + tested_leg, 'add_brev' + tested_leg, 'add_mag1' + tested_leg, 'add_mag2' + tested_leg, 'add_mag3' + tested_leg, 'pect' + tested_leg, 'grac' + tested_leg],
    'quadriceps': ['rect_fem' + tested_leg, 'vas_med' + tested_leg, 'vas_int' + tested_leg, 'vas_lat' + tested_leg],
    'calf': ['med_gas' + tested_leg, 'lat_gas' + tested_leg, 'soleus' + tested_leg],
    'tibialis': ['tib_ant' + tested_leg, 'tib_post' + tested_leg],
    'peroneals': ['per_brev' + tested_leg, 'per_long' + tested_leg, 'per_tert' + tested_leg],
    'extensors': ['ext_dig' + tested_leg, 'ext_hal' + tested_leg],
    'core': ['ercspn' + tested_leg, 'intobl' + tested_leg, 'extobl' + tested_leg]
}