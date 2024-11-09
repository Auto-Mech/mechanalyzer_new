""" functions for managing creck classes and dictionaries
"""

import pandas as pd

R = ['R', 'H', 'OH', 'O2', 'O', 'CH3', 'HO2', 'HCO', 'C2H3']
RSR = ['C5H5', 'C7H7', 'C6H5CH2', 'C6H5O', 'A1O']


def build_creckclass_fromdct(rxn_creckclass_dct, classtype_dct = {}):
    """ build a dataframe with reactiontype, classtype, speciestype, bimoltype for each reaction

    Args:
        rxn_creckclass_dct (dict{rxn: {'speciestype':speciestype, 
        'reactiontype':reactiontype}}): assigned species and reaction type
        classtype_dct (dict{reactiontype(str): classtype(str)}, optional): _description_. Defaults to None.
    
    return creckclass_df: dataframe[['classtype','speciestype','reactiontype','bimoltype'][rxn]]
    """
    
    creckclass_df = pd.DataFrame.from_dict(rxn_creckclass_dct, orient='index')
    # add info on bimolecular type
    for speciestype, df_sptype in creckclass_df.groupby('speciestype'):
        for idx, reactiontype in df_sptype['reactiontype'].items():
            bimoltype = set_bimol_type(idx, speciestype, reactiontype)
            creckclass_df.loc[idx, ['bimoltype']] = bimoltype
    for reactiontype, df_rxntype in creckclass_df.groupby('reactiontype'):
        rxns = df_rxntype.index
        if reactiontype in classtype_dct.keys():
            cltype = classtype_dct[reactiontype]
        else:
            cltype = 'UNSORTED'
        creckclass_df.loc[rxns, 'classtype'] = cltype
    
    return creckclass_df
        
def set_bimol_type(rxn, speciestype, reactiontype):
    """
    check if a bimolecular reaction is of type M+M, RSR+M, R+M, R+R, RSR+RSR
    from speciestype A-M/R/RSR and reactiontype
    NB for now, relies on rudimental classification. can be upgraded
    by analysing radical character in autochem.
    suggestion: check if molecule or radical, then for rsr check presence of multiple rad structures
    risk: for aromatics, resonance will always be detected
    """
    # return unimol for unimolecular reactions
    if len(rxn[0]) == 1:
        return 'UNIMOL'
    # CHECK SPECIES TYPE 1 - CLASSIFIED ACCORDING TO THE SPECIES TYPE FROM THE USER
    try:
        species_type_1 = speciestype.split('-')[-1]
    except AttributeError:
        return 'UNSORTED'

    # CHECK SPECIES TYPE 2
    try:
        species_type_2 = reactiontype.split('_')[1]
    except AttributeError:
        return 'UNSORTED'
    
    if species_type_2 in R:
        species_type_2 = 'R'
    elif species_type_2 in RSR:
        species_type_2 = 'RSR'
    elif '-' in species_type_2:
        species_type_2 = species_type_2.split('-')[1]
    else:
        species_type_2 = 'NA'

    type_list = [species_type_1, species_type_2]
    type_list.sort()

    return '+'.join(type_list)

