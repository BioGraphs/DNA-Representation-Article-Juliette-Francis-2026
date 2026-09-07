import pandas as pd
import numpy as np
import json
import os
from glob import glob
import re
import argparse

def extract_results(filename, hyperparameter, sequences_group):
    filename = filename.replace(f'{sequences_group}_', '').replace(f'{hyperparameter}_', '').replace('_embedding_comparison.json', '')
    m1, m2 = filename.split('_vs_')
    return m1, m2

def create_datasets_from_comp_pvalues(comp_results_dir, hyperparameter, sequences_group, output_dir):
    all_json_files = glob(os.path.join(comp_results_dir, "*.json"))
    json_files = [f for f in all_json_files if (f'{hyperparameter}_' in os.path.basename(f)) and (f'{sequences_group}_' in os.path.basename(f))]
    comp_results = dict()
    for filepath in json_files:
        filename = os.path.basename(filepath)
        m1, m2 = extract_results(filename, hyperparameter, sequences_group)
        with open(filepath) as json_file:
            comp_results[(m1, m2)] = json.load(json_file)

    min_pvalues_dict = dict()
    for key in comp_results.keys():
        if f'{key[0]}_{key[1]}_p' not in min_pvalues_dict.keys() and f'{key[1]}_{key[0]}_p' not in min_pvalues_dict.keys():
            first_pvals = comp_results[key]['p-values']
            second_pvals = comp_results[(key[1], key[0])]['p-values']
            min_pvalues_dict[f'{key[0]}_{key[1]}_p'] = [np.min([first_pvals[i], second_pvals[i]]) for i in range(len(first_pvals))]
    df = pd.DataFrame(min_pvalues_dict)
    pd.DataFrame(min_pvalues_dict).to_csv(output_dir + f'/{sequences_group}_p_values_{hyperparameter}.csv', sep=",", index=False, header=True)
    return df

def get_comparison_pvalues(comp_results_dir, hyperparameter, sequences_group):
    all_json_files = glob(os.path.join(comp_results_dir, "*.json"))
    json_files = [f for f in all_json_files if f'{hyperparameter}_' in os.path.basename(f)]
    comp_results = dict()
    for filepath in json_files:
        filename = os.path.basename(filepath)
        m1, m2 = extract_results(filename, hyperparameter, sequences_group)
        with open(filepath) as json_file:
            comp_results[(m1, m2)] = json.load(json_file)
    return comp_results

def format_pvalue_data(results_dict):
    data = []
    for (model1, model2), metrics in results_dict.items():
        pvals = metrics.get("p-values", [])
        d = metrics.get("d", [])
        if not pvals:
            continue
        pair = f"{min(model1, model2)} & {max(model1, model2)}"
        direction = f"{model1} → {model2}"
        mean_pval = np.mean(pvals)
        std_pval = np.std(pvals)
        ymin = max(mean_pval - std_pval, 0)
        ymax = min(mean_pval + std_pval, 1)
        mean_dist_pval = np.mean([1 - p for p in pvals])
        seq_id = 1
        for p in pvals:
            data.append({
                "Seq ID": seq_id,
                "Models compared": pair,
                "Direction": direction,
                "p-value": p,
                "Mean p-value": mean_pval,
                "Std p-value": std_pval,
                "ymin": ymin,
                "ymax": ymax,
                "Distance p-values": 1 - p,
                "Mean distance p-values": mean_dist_pval,
                'd': d,
                'significant': p < 0.05
            })
            seq_id += 1

    df = pd.DataFrame(data)
    signif_rate = (
        df.groupby("Models compared")["p-value"]
        .apply(lambda x: 100 * (x < 0.05).mean())
        .rename("p-values < 0.05 %")
    )
    df = df.merge(signif_rate, on="Models compared")

    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                            prog='Prepare results files for plots and analysis',
                            description=(""))
    parser.add_argument('comp_results_dir',
                            type=str,
                            help="The path to the comparison results directory")
    parser.add_argument('hyperparameter',
                            type=str,
                            help="String containing the hyperparemeters of the comparison")
    parser.add_argument('data',
                            type=str,
                            help="The dataset name") 
    parser.add_argument('output_dir',
                            type=str,
                            help="The path to the output directory") 
    args = parser.parse_args()

    pvalues = create_datasets_from_comp_pvalues(args.comp_results_dir, args.hyperparameter, args.data, args.output_dir)

    columns_rename_dict = {'dna2vec_dnaberts_p': 'dna2vec_dnaberts_e', 
                        'dnabert2_dna2vec_p': 'dnabert2_dna2vec_e', 
                        'hyenadna_dna2vec_p': 'hyenadna_dna2vec_e',
                        'hyenadna_tnf_p': 'hyenadna_tnf_e', 
                        'dnaberts_tnf_p': 'dnaberts_tnf_e', 
                        'dnabert2_hyenadna_p': 'dnabert2_hyenadna_e',
                        'dnaberts_hyenadna_p': 'dnaberts_hyenadna_e',
                        'tnf_dna2vec_p': 'tnf_dna2vec_e', 
                        'dnabert2_dnaberts_p': 'dnabert2_dnaberts_e',
                        'tnf_dnabert2_p': 'tnf_dnabert2_e',
                        'dna2vec_dnabert2_p': 'dna2vec_dnabert2_e',
                        'dna2vec_tnf_p': 'dna2vec_tnf_e',
                        'dnaberts_dnabert2_p': 'dnaberts_dnabert2_e',
                        'hyenadna_dnaberts_p': 'hyenadna_dnaberts_e',
                        'dnabert2_tnf_p': 'dnabert2_tnf_e',
                        'tnf_hyenadna_p': 'tnf_hyenadna_e',
                        'tnf_dnaberts_p': 'tnf_dnaberts_e',
                        'dna2vec_hyenadna_p': 'dna2vec_hyenadna_e',
                        'dnaberts_dna2vec_p': 'dnaberts_dna2vec_e',
                        'hyenadna_dnabert2_p': 'hyenadna_dnabert2_e'}


    evidence_pvalues = -np.log10(pvalues)
    evidence_pvalues = evidence_pvalues.rename(columns=columns_rename_dict)
    evidence_pvalues.to_csv(f'{args.output_dir}/{args.data}_evidence_pvalues_{args.hyperparameter}.tsv', sep="\t", index=False, header=True)
    comp_results = get_comparison_pvalues(args.comp_results_dir, args.hyperparameter, args.data)
    df = format_pvalue_data(comp_results)
    df.to_csv(f'{args.output_dir}/{args.data}_data_for_k_exploration_{args.hyperparameter}.tsv', sep="\t", index=False, header=True)