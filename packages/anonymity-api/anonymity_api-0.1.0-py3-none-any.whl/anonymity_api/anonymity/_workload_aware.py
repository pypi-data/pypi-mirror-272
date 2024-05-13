from anonymity_api import anonymity
from anonymity_api.anonymity.utils import aux_functions
import pandas as pd

def workload_aware_k_anonymity( data, quasi_idents, k, queries, idents = [], taxonomies= None):
    '''Anonymizes based on the given workload. The goal is to preserve utility on the anonymization when having previous knowledge of the
    workload that will be done with the anonymizaed dataset
    
    :param data: dataset to anonymize
    :param quasi_idents: quasi identifiers of the dataset
    :param k: k to be used in k-anonymization
    :param queries: workload to be applied on the dataset
    :param idents: identifiers of the dataset
    :param taxonomies: hierarchy to be used for quasi-identifer generalization
    
    :returns: the anonymized dataset'''
    
    corr, queries_proc = aux_functions.check_corr( queries )
    
    query_df, rest_df = aux_functions.get_query_dataframes(data, queries_proc, quasi_idents)
    
    arg_corr = None
    
    if len(corr) != 0:
        
        arg_corr = aux_functions.process_corr(corr, quasi_idents)
        
    return pd.concat([anonymity.k_anonymity(query_df, quasi_idents, k, idents, arg_corr, taxonomies= taxonomies.copy() if taxonomies != None else taxonomies),
                    anonymity.k_anonymity(rest_df, quasi_idents, k, idents, arg_corr, taxonomies= taxonomies.copy() if taxonomies != None else taxonomies)]).reset_index(drop=True)
    
    
def workload_aware_distinct_l_diversity(data, quasi_idents, sens_atts, l, queries, idents = [], taxonomies= None): 
    '''Anonymizes based on the given workload. The goal is to preserve utility on the anonymization when having previous knowledge of the
    workload that will be done with the anonymizaed dataset
    
    :param data: dataset to anonymize
    :param quasi_idents: quasi identifiers of the dataset
    :param sens_atts: sensitive attributes of the dataset
    :param l: l to be used in distinct l-diversity
    :param queries: workload to be applied on the dataset
    :param idents: identifiers of the dataset
    :param taxonomies: hierarchy to be used for quasi-identifer generalization
    
    :returns: the anonymized dataset'''
    
    corr, queries_proc = aux_functions.check_corr( queries )
    
    query_df, rest_df = aux_functions.get_query_dataframes(data, queries_proc, quasi_idents)
    
    arg_corr = None
    
    if len(corr) != 0:
        
        arg_corr = aux_functions.process_corr(corr, quasi_idents)
        
    return pd.concat([anonymity.distinct_l_diversity(query_df, quasi_idents, sens_atts, l, idents, arg_corr, taxonomies= taxonomies.copy() if taxonomies != None else taxonomies), 
                     anonymity.distinct_l_diversity(rest_df, quasi_idents, sens_atts, l, idents, arg_corr, taxonomies= taxonomies.copy() if taxonomies != None else taxonomies)]).reset_index(drop=True)
    

def workload_aware_entropy_l_diversity(data, quasi_idents, sens_atts, l, queries, idents = [], taxonomies= None): 
    '''Anonymizes based on the given workload. The goal is to preserve utility on the anonymization when having previous knowledge of the
    workload that will be done with the anonymizaed dataset
    
    :param data: dataset to anonymize
    :param quasi_idents: quasi identifiers of the dataset
    :param sens_atts: sensitive attributes of the dataset
    :param l: l to be used in entropy l-diversity
    :param queries: workload to be applied on the dataset
    :param idents: identifiers of the dataset
    :param taxonomies: hierarchy to be used for quasi-identifer generalization
    
    :returns: the anonymized dataset'''
    
    corr, queries_proc = aux_functions.check_corr( queries )
    
    query_df, rest_df = aux_functions.get_query_dataframes(data, queries_proc, quasi_idents)
    
    arg_corr = None
    
    if len(corr) != 0:
        
        arg_corr = aux_functions.process_corr(corr, quasi_idents)
        
            
    return pd.concat([anonymity.entropy_l_diversity(query_df, quasi_idents, sens_atts, l, idents, arg_corr, taxonomies= taxonomies.copy() if taxonomies != None else taxonomies), 
                     anonymity.entropy_l_diversity(rest_df, quasi_idents, sens_atts, l, idents, arg_corr, taxonomies= taxonomies.copy() if taxonomies != None else taxonomies)]).reset_index(drop=True)

    
def workload_aware_recursive_c_l_diversity(data, quasi_idents, sens_atts, c, l, queries, idents = [], taxonomies= None):  
    '''Anonymizes based on the given workload. The goal is to preserve utility on the anonymization when having previous knowledge of the
    workload that will be done with the anonymizaed dataset
    
    :param data: dataset to anonymize
    :param quasi_idents: quasi identifiers of the dataset
    :param sens_atts: sensitive attributes of the dataset
    :param c: value of c to be used in recursive (c,l)-diversity
    :param l: value of l to be used in recursive (c,l)-diversity
    :param queries: workload to be applied on the dataset
    :param idents: identifiers of the dataset
    :param taxonomies: hierarchy to be used for quasi-identifer generalization
    
    :returns: the anonymized dataset'''
    
    corr, queries_proc = aux_functions.check_corr( queries )
    
    query_df, rest_df = aux_functions.get_query_dataframes(data, queries_proc, quasi_idents)
    
    arg_corr = None
    
    if len(corr) != 0:
        
        arg_corr = aux_functions.process_corr(corr, quasi_idents)
        
            
    return pd.concat([anonymity.recursive_cl_diversity(query_df, quasi_idents, sens_atts, c, l, idents, arg_corr, taxonomies= taxonomies.copy() if taxonomies != None else taxonomies), 
                     anonymity.recursive_cl_diversity(rest_df, quasi_idents, sens_atts, c, l, idents, arg_corr, taxonomies= taxonomies.copy() if taxonomies != None else taxonomies)]).reset_index(drop=True)
    

def workload_aware_t_closeness(data, quasi_idents, sens_atts, t, queries, idents = [], taxonomies= None):
    '''Anonymizes based on the given workload. The goal is to preserve utility on the anonymization when having previous knowledge of the
    workload that will be done with the anonymizaed dataset
    
    :param data: dataset to anonymize
    :param quasi_idents: quasi identifiers of the dataset
    :param sens_atts: sensitive attributes of the dataset
    :param t: t to be used in t-closeness
    :param queries: workload to be applied on the dataset
    :param idents: identifiers of the dataset
    :param taxonomies: hierarchy to be used for quasi-identifer generalization
    
    :returns: the anonymized dataset'''
    
    corr, queries_proc = aux_functions.check_corr( queries )
    
    query_df, rest_df = aux_functions.get_query_dataframes(data, queries_proc, quasi_idents)
    
    arg_corr = None
    
    if len(corr) != 0:
        
        arg_corr = aux_functions.process_corr(corr, quasi_idents)


    return pd.concat([anonymity.t_closeness(query_df, quasi_idents, sens_atts, t, idents, arg_corr, taxonomies= taxonomies.copy() if taxonomies != None else taxonomies), 
                     anonymity.t_closeness(rest_df, quasi_idents, sens_atts, t, idents, arg_corr, taxonomies= taxonomies.copy() if taxonomies != None else taxonomies)]).reset_index(drop=True)

