import pandas as pd
from pyserrf import SERRF

samples=pd.read_table("../metabolomics_INIA/config/samples.tsv")

pos=pd.read_table("../metabolomics_INIA/input/peak_data/positive_charge.tsv")


pos=samples[['sample','measurement_group']].merge(pos, on='sample')

pos
