import pandas as pd
import json
import random

# path='/home/genouest/cnrs_umr6074/jfrancis/Data/dnaberts_synthetic_data/reference/'

# with open(f"{path}eval_species_count_0.json") as f:
#     groups = json.load(f)
    
# bacteria_species = list()
# for group, species_dict in groups.items():
#     if group == "bacteria":
#         for species in species_dict:
#             bacteria_species.append(species)

# bacteria_36_species = random.sample(bacteria_species, 36)

# bacteria_1 = bacteria_36_species[0:10]
# bacteria_2 = bacteria_36_species[10:20]
# bacteria_3 = bacteria_36_species[20:30]
# bacteria_4 = bacteria_36_species[26:]

# sequences_path = '/home/genouest/cnrs_umr6074/jfrancis/Data/dnaberts_synthetic_data/reference/clustering_0_with_GC.csv'
# sequences = pd.read_csv(sequences_path, header=[0], skiprows=list(range(1,10001)), sep=',')


# def create_batceria_datasets(bacteria, sequences_df):
#     bacteria_df = pd.DataFrame({'sequence': list(),
#                     'bin_id': list(), 
#                     'per GC': list(), 
#                     'per AT': list(), 
#                     'per other': list(),
#                     'mean per GC for same species': list(), 
#                     'delta_GC_vs_species_mean': list()})

#     for species in bacteria:
#         species_sequences = sequences_df.loc[sequences_df['bin_id'] == species]
#         species_50_sequences = species_sequences.sample(50, axis='index')
#         bacteria_df = pd.concat([bacteria_df, species_50_sequences])

#     return bacteria_df

# bacteria_1_df = create_batceria_datasets(bacteria_1, sequences)
# bacteria_2_df = create_batceria_datasets(bacteria_2, sequences)
# bacteria_3_df = create_batceria_datasets(bacteria_3, sequences)
# bacteria_4_df = create_batceria_datasets(bacteria_4, sequences)

# print(bacteria_1_df.shape)
# print(bacteria_2_df.shape)
# print(bacteria_3_df.shape)
# print(bacteria_4_df.shape)

# bacteria_1_df.to_csv('/home/genouest/cnrs_umr6074/jfrancis/Data/dnaberts_synthetic_data/reference/bacteria_1.tsv', sep='\t', index=False)
# bacteria_2_df.to_csv('/home/genouest/cnrs_umr6074/jfrancis/Data/dnaberts_synthetic_data/reference/bacteria_2.tsv', sep='\t', index=False)
# bacteria_3_df.to_csv('/home/genouest/cnrs_umr6074/jfrancis/Data/dnaberts_synthetic_data/reference/bacteria_3.tsv', sep='\t', index=False)
# bacteria_4_df.to_csv('/home/genouest/cnrs_umr6074/jfrancis/Data/dnaberts_synthetic_data/reference/bacteria_4.tsv', sep='\t', index=False)

bacteria_df = pd.read_csv('/home/genouest/cnrs_umr6074/jfrancis/Data/dnaberts_synthetic_data/reference/article_sequences/bacteria.tsv', sep='\t')

bacteria_1_df = pd.read_csv('/home/genouest/cnrs_umr6074/jfrancis/Data/dnaberts_synthetic_data/reference/article_sequences/bacteria_1.tsv', sep='\t', header=0)
bacteria_2_df = pd.read_csv('/home/genouest/cnrs_umr6074/jfrancis/Data/dnaberts_synthetic_data/reference/article_sequences/bacteria_2.tsv', sep='\t', header=0)
bacteria_3_df = pd.read_csv('/home/genouest/cnrs_umr6074/jfrancis/Data/dnaberts_synthetic_data/reference/article_sequences/bacteria_3.tsv', sep='\t', header=0)
bacteria_4_df = pd.read_csv('/home/genouest/cnrs_umr6074/jfrancis/Data/dnaberts_synthetic_data/reference/article_sequences/bacteria_4.tsv', sep='\t', header=0)

result_path='/home/genouest/cnrs_umr6074/jfrancis//Results/dnaberts_synthetic_data_embeddings/reference/'

dnabert2_emb = pd.read_csv(f'{result_path}clustering_0_dnabert2_embedding.csv', sep=',')

dnabert2_emb[dnabert2_emb.iloc[:, 0].isin(bacteria_df['sequence'])].to_csv(f'{result_path}article_embeddings/bacteria_dnabert2_tmp_embedding.csv', sep=',')

dnabert2_emb[dnabert2_emb.iloc[:, 0].isin(bacteria_1_df['sequence'])].to_csv(f'{result_path}article_embeddings/bacteria_1_dnabert2_tmp_embedding.csv', index=False, sep=',', header=None)
dnabert2_emb[dnabert2_emb.iloc[:, 0].isin(bacteria_2_df['sequence'])].to_csv(f'{result_path}article_embeddings/bacteria_2_dnabert2_tmp_embedding.csv', index=False, sep=',', header=None)
dnabert2_emb[dnabert2_emb.iloc[:, 0].isin(bacteria_3_df['sequence'])].to_csv(f'{result_path}article_embeddings/bacteria_3_dnabert2_tmp_embedding.csv', index=False, sep=',', header=None)
dnabert2_emb[dnabert2_emb.iloc[:, 0].isin(bacteria_4_df['sequence'])].to_csv(f'{result_path}article_embeddings/bacteria_4_dnabert2_tmp_embedding.csv', index=False, sep=',', header=None)


dnaberts_emb = pd.read_csv(f'{result_path}clustering_0_dnaberts_embedding.csv', sep=',')

dnaberts_emb[dnaberts_emb.iloc[:, 0].isin(bacteria_df['sequence'])].to_csv(f'{result_path}article_embeddings/bacteria_dnaberts_tmp_embedding.csv', sep=',')

dnaberts_emb[dnaberts_emb.iloc[:, 0].isin(bacteria_1_df['sequence'])].to_csv(f'{result_path}article_embeddings/bacteria_1_dnaberts_tmp_embedding.csv', index=False, sep=',', header=None)
dnaberts_emb[dnaberts_emb.iloc[:, 0].isin(bacteria_2_df['sequence'])].to_csv(f'{result_path}article_embeddings/bacteria_2_dnaberts_tmp_embedding.csv', index=False, sep=',', header=None)
dnaberts_emb[dnaberts_emb.iloc[:, 0].isin(bacteria_3_df['sequence'])].to_csv(f'{result_path}article_embeddings/bacteria_3_dnaberts_tmp_embedding.csv', index=False, sep=',', header=None)
dnaberts_emb[dnaberts_emb.iloc[:, 0].isin(bacteria_4_df['sequence'])].to_csv(f'{result_path}article_embeddings/bacteria_4_dnaberts_tmp_embedding.csv', index=False, sep=',', header=None)

