import csv
import copy
import numpy as np
import pandas as pd

from py_lopa.calcs.thermo_pio import nbp_deg_K
from py_lopa.calcs import helpers

df = pd.read_csv('data/cheminfo.csv')
cheminfo = helpers.get_cheminfo()
completed_chems = pd.NA
dippr_consts = pd.read_csv('data/dippr_consts.csv')

try:
    completed_chems = pd.read_csv('data/cheminfo_with_nbp.csv')
except:
    pass

def get_nbp_from_dippr_consts(cas):
    nbp_k = pd.NA
    try:
        row = dippr_consts[(dippr_consts['cas_no'] == cas) & (dippr_consts['property_id'] == 'NBP')]
        nbp_k = helpers.get_data_from_pandas_series_element(row['const_value'])
    except:
        pass
    return nbp_k

# def nbp_deg_K(chems = None, x0 = 298.15, mixture_cas_nos = [], mixture_molfs = [], cheminfo = None):

# cas_no,chem_name,pws_name,mat_comp_id,mw,vp_a,vp_b,vp_c,vp_d,vp_e,tmin,tmax,pac_1,pac_2,pac_3,pac_units,erpg_1,erpg_2,erpg_3,erpg_unit,erpg_1_base,erpg_2_base,erpg_3_base,erpg_unit_base,loc_1,loc_2,loc_3,loc_unit,loc_n,loc_dose,tox_data,min_conc_for_60_min_loc_dose__ppm_,min_conc_for_60_min_1_pct_sev_inj,gamma_estimate,lel,idlh,aegl_1_60_min,aegl_2_60_min,aegl_3_60_min,aegl_1_60_min_base,aegl_2_60_min_base,aegl_3_60_min_base,olivier_tc_1,olivier_tc_2,olivier_tc_3,doe_tc_1,doe_tc_2,doe_tc_3,flash_point__deg_c_,lc50,idlh_1,idlh_2,idlh_3,erpg_more_conservative_than_aegl,t_low_deg_c,t_high_deg_c,only_pacs_or_doe,SLOT_ppm_n_min,SLOT_n,Probit_A,Probit_B,Probit_n

buffer = []
for idx, row in df.iterrows():
    if not pd.isna(completed_chems):
        if row['cas_no'] in completed_chems['cas_no']:
            continue
    cas_no = row['cas_no']
    row_out = copy.deepcopy(row)
    row_out['nbp_k'] = None
    nbp_k = pd.NA
    try:
        nbp_k = get_nbp_from_dippr_consts(cas=cas_no)
        if pd.isna(nbp_k):
            nbp_k = nbp_deg_K(mixture_cas_nos=[cas_no], mixture_molfs=[1], cheminfo=cheminfo)
        if pd.isna(nbp_k):
             print(f'***********\n\n\ncould not get nbp for cas: {cas_no}\n\n')
        row_out['nbp_k'] = nbp_k
        buffer.append(row_out)
        with open('data/cheminfo_with_nbp.csv', 'a', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(buffer)
            buffer = []
    except Exception as e:
        print(f'**********could not write to file. currently in buffer:\n{buffer}\n\n\n')