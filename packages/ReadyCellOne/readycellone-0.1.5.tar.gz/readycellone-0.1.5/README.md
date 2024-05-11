# ReadyCellOne
ReadyCellOne is a computational tool to enable task-centric cell engineering. It maps phenotypes associated with various metabolic functions to transcriptional states in single-cells.

## Installation

```
pip install ReadyCellOne
```

## Running ReadyCellOne

To predict functional phenotypes in engineered cells, we need to train a model on *in vivo* single-cell data. In order to do so, you need a few things:

- Single-cell transcriptomes
- A class label for each cell that serves as a proxy for its functional output (e.g. a spatial location, or a timepoint annotation)
- A Molecular Signatures gene set that corresponds to genes related to your query cellular function.


### Training

The following command is an example usage of the main function, `train_rco_model`:

```
clf, liver_matrix, liang_matrix, y_true, y_true_liang, cgenes = train_rco_model(liver_ad, liver_ad_obs_col, liang_D56, "GOBP_XENOBIOTIC_METABOLIC_PROCESS",
                                                                species='mouse', num_random_samples=100, train_order=train_order,
                                                                test_cell_state_obs_column=liang_D56_obs_col, test_order=test_order)

```

Note that you need to supply both the train and test anndata objects since RCO needs to process both datasets uniformly.

### Predicting cell states and cell state similarity scores

RCO provides two functions to predict most likely cell states and similarity scores for each train cell state:

Cell state similarity scores example call:

```
y_scores, predictions = predict_cell_state_similarity_scores(clf, liang_matrix, liang_D56.obs['is_hepatocyte'].values)
```

Predicting cell states example call:

```
y_preds = predict_cell_states(clf, spatial_liver_matrix)
```


### Visualization

We provide a few plotting functions such as heatmaps for visualizing cell state similarity scores for your query cells as well as precision-recall plotting functions for assessing model performance:

Heatmap of cell state similarity scores:

```
heatmap_rco_scores(y_scores, predictions, cls=['Adult', 'Fetal', 'random'], title='DesLO prediction, Xenobiotic Metabolism', xlabel='DesLO hepatocyte-like cells', ylabel='Cell State Similarity Score')
```

Precision-recall curves for classification performance:
```
plot_pr_curves(y_true_liang, y_scores, test_order)
```
