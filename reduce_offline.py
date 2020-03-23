from pathlib import Path
import argparse

from visualize.commons import reduce
from tqdm import tqdm
import numpy as np


def reduce_offline(input_dir, output_dir, projection_type):
    input_dir = Path(input_dir)

    embedding_files = sorted(input_dir.rglob('*.npy'))
    if len(embedding_files) == 0:
        raise RuntimeError(f'The directory is empty: {input_dir}')

    print('Loading embeddings...')
    embeddings = [np.load(str(embedding_file)) for embedding_file in tqdm(embedding_files)]

    print(f'Applying {projection_type}...')
    if projection_type == 'pca':
        embeddings_reduced = reduce(embeddings, projection_type, verbose=True)
    elif projection_type == 'tsne':
        embeddings_reduced = reduce(embeddings, projection_type, n_dimensions_in=50, n_dimensions_out=2, verbose=True)
    else:
        raise ValueError(f'Invalid projection_type: {projection_type}')

    print('Saving reduced...')
    output_dir = Path(output_dir)
    for embedding_file, data in zip(tqdm(embedding_files), embeddings_reduced):
        relative_path = embedding_file.relative_to(input_dir)
        reduced_file = output_dir / relative_path
        if not reduced_file.exists():
            reduced_file.parent.mkdir(parents=True, exist_ok=True)
            np.save(reduced_file, data)

    print('Done!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_dir')
    parser.add_argument('output_dir')
    parser.add_argument('projection_type', choices=['pca', 'tsne'])
    args = parser.parse_args()

    reduce_offline(args.input_dir, args.output_dir, args.projection_type)