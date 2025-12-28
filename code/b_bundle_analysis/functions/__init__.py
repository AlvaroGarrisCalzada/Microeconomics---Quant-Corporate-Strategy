"""
Utility modules that support the bundle analysis notebook.

Each module focuses on a single task (data prep, metrics, visualization)
to keep the notebook focused on storytelling rather than plumbing.
"""

from .data_prep import build_and_save_basket_dataset, load_basket_dataset
from .basket_metrics import (
    summarize_basket_sizes,
    compute_category_support,
    prepare_basket_matrix,
    generate_rules,
    describe_rule_clusters,
    top_rules_by_consequent,
)
from .plotting import (
    plot_basket_size_distribution,
    plot_category_support,
    plot_rule_network,
)

__all__ = [
    "build_and_save_basket_dataset",
    "load_basket_dataset",
    "summarize_basket_sizes",
    "compute_category_support",
    "prepare_basket_matrix",
    "generate_rules",
    "describe_rule_clusters",
    "top_rules_by_consequent",
    "plot_basket_size_distribution",
    "plot_category_support",
    "plot_rule_network",
]
