# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2020-05-25

### Added
- UI for selecting different models and datasets
- New dataset (pre-trained): MSD (Million Song Dataset)
- New model: VGG trained on both MSD and MTAT
- Dropdown selector for tags and PCA components with search functionality

### Changed
- UI for audio toggle and log scale moved
- Made the plot section bigger

### Removed

- Support for dynamic PCA
- Selection of layers for t-SNE (now only [0, 1])

## [0.1.0] - 2020-04-16

### Added
- Graph area for visualization
- Input field for number fo tracks
- Embeddings and taggrams from MusiCNN model trained on MTAT
- 3 ways to visualize latent spaces: segments, averages, trajectories
- 2 spaces: taggrams and penultimate
- 3 projections: PCA, t-SNE and original with numerical input fields for X and Y
- Selection of the way audio is played: on-click, on-hover and disabled
- Optional log-scale for visualizations that are too clustered to axes
- Experimental UI for music exploration