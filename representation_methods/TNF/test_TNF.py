import os
import pytest
import pandas as pd
from TNF import main 

@pytest.fixture
def setup_files():
    input_file = "test_input.csv"
    output_file = "test_output.csv"
    dna_sequences = [["ATGCATGCATGC", "species1"],
                     ["TACGTACGTACG", "species2"]]
    with open(input_file, "w") as f:
        f.write("dna_seq,species\n")
        for seq, species in dna_sequences:
            f.write(f"{seq},{species}\n")
    yield input_file, output_file, dna_sequences
    if os.path.exists(input_file):
        os.remove(input_file)
    if os.path.exists(output_file):
        os.remove(output_file)

def test_embedding_dimension_3mers(setup_files):
    input_file, output_file, dna_sequences = setup_files
    main(input_file, output_file, 3)
    output_df = pd.read_csv(output_file, header=None)
    embedding_columns = output_df.columns[2:] 
    assert len(embedding_columns) == 64, f"Expected 64 embedding dimensions, but got {len(embedding_columns)}."

def test_embedding_dimension_4mers(setup_files):
    input_file, output_file, dna_sequences = setup_files
    main(input_file, output_file, 4)
    output_df = pd.read_csv(output_file, header=None)
    embedding_columns = output_df.columns[2:] 
    assert len(embedding_columns) == 256, f"Expected 256 embedding dimensions, but got {len(embedding_columns)}."

def test_output_file_shape_3mers(setup_files):
    input_file, output_file, dna_sequences = setup_files
    main(input_file, output_file, 3)
    output_df = pd.read_csv(output_file, header=None)
    num_sequences = len(dna_sequences)
    num_columns = 66
    assert output_df.shape == (num_sequences, num_columns), (
        f"Output file should have {num_sequences} rows and {num_columns} columns, but got {output_df.shape}.")

def test_output_file_shape_4mers(setup_files):
    input_file, output_file, dna_sequences = setup_files
    main(input_file, output_file, 4)
    output_df = pd.read_csv(output_file, header=None)
    num_sequences = len(dna_sequences)
    num_columns = 258
    assert output_df.shape == (num_sequences, num_columns), (
        f"Output file should have {num_sequences} rows and {num_columns} columns, but got {output_df.shape}.")
