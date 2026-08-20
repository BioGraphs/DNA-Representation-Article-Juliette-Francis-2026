import argparse
import pandas as pd
import os
import json
from pathlib import Path

if __name__ == "__main__":
	parser = argparse.ArgumentParser(
	                        prog='Prepare data for Embedding Comparator')
	parser.add_argument('embedding_files',
	                        type=str,
	                        help="A file containing path to the embedding files")
	args = parser.parse_args()
	with open(args.embedding_files) as fd:
		first_file = True
		sequence_id = []
		for line in fd:
			file_name = os.path.basename(line)
			name = os.path.splitext(file_name)[0]
			if "bacteria_1" in name:
				outdir = "./Results/Jaccard_distance/bacteria_1/embeddings_in_tsv_format"
				Path(outdir).mkdir(parents=True, exist_ok=True)

			elif "bacteria_2" in name:
				outdir = "./Results/Jaccard_distance/bacteria_2/embeddings_in_tsv_format"
				Path(outdir).mkdir(parents=True, exist_ok=True)

			elif "bacteria_3" in name:
				outdir = "./Results/Jaccard_distance/bacteria_3/embeddings_in_tsv_format"
				Path(outdir).mkdir(parents=True, exist_ok=True)

			elif "bacteria_4" in name:
				outdir = "./Results/Jaccard_distance/bacteria_4/embeddings_in_tsv_format"
				Path(outdir).mkdir(parents=True, exist_ok=True)

			else:
				raise ValueError("Output directory is not defined")
			embedding_df = pd.read_csv(line.strip(), header=None)
			if first_file:
				first_file = False
				specie = embedding_df.iloc[0,1]
				i_specie = 1
				specie_dict = dict()
				specie_dict[i_specie] = embedding_df.iloc[0,1]
				for i in range(embedding_df.shape[0]):
					if embedding_df.iloc[i,1] != specie:
						specie = embedding_df.iloc[i,1]
						i_specie += 1
						specie_dict[i_specie] = embedding_df.iloc[i,1]
					sequence_id.append(f"Seq-{i+1}-Spe-{i_specie}")
				pd.DataFrame(sequence_id).to_csv(f"{outdir}/sequence_id.tsv", sep="\t", index=False, header=False)
				with open(f"{outdir}/species_index.json", 'w') as fh:
					json.dump(specie_dict, fh)
			embedding_df = embedding_df.drop(embedding_df.columns[[0, 1]], axis=1)
			embedding_df.to_csv(f"{outdir}/{name}.tsv", sep="\t", index=False, header=False)
	
