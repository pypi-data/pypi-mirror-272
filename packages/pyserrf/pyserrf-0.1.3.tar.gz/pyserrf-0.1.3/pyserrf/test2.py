
corrs_target.loc['MET_204']
corrs_qc.loc['MET_204']

cta=pd.read_table("test_data/corrs_train_A.tsv")
ctga=pd.read_table("test_data/corrs_target_A.tsv")

result = main(10, corrs_qc, corrs_target)

g=pd.concat([corrs_target.loc[result],corrs_qc.loc[result]], axis=1).sort_index()
f=pd.concat([c,d], axis=1).sort_index()

result


g.merge(f)


def intersect(arr1, arr2):
    # Function to find the intersection of two arrays
    return list(set(arr1) & set(arr2))

def main(num, corr_train_order, corr_target_order):
    sel_var = []
    l = num
    while len(sel_var) < num:
        print(sel_var)
        sel_var = intersect(corr_train_order.index[0:l], corr_target_order.index[0:l])
        #sel_var = [var for var in sel_var if var != j]
        l += 1
    return sel_var


c=corrs_qc.loc[a._get_top_metabolites_in_both_correlations(corrs_qc, corrs_target, 10)]
d=corrs_target.loc[a._get_top_metabolites_in_both_correlations(corrs_qc, corrs_target, 10)]


a._get_top_metabolites_in_both_correlations(corrs_qc, corrs_target, 10)
met='MET_216'
corrs_qc=a._corrs_qc['A'][met].drop(met).abs().sort_values(ascending=False)
corrs_target=a._corrs_target['A'][met].drop(met).abs().sort_values(ascending=False)

a._get_sorted_correlation(a.)
