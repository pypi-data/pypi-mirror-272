import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score, adjusted_mutual_info_score, fowlkes_mallows_score, v_measure_score

from scores import purity_score
from scs import scs_metric


def create_table(columns, rows):
    # Calculate column widths
    column_widths = [max(len(str(row[i])) for row in rows) for i in range(len(columns))]

    # Print header
    header = "|".join(column.center(width) for column, width in zip(columns, column_widths))
    print(header)

    # Print separator
    separator = "+".join("-" * width for width in column_widths)
    print(separator)

    # Print rows
    for row in rows:
        row_str = "|".join(str(cell).ljust(width) for cell, width in zip(row, column_widths))
        print(row_str)



columns = ["Data", "ARI", "AMI", "Purity", "FMI", "VM", "SCS"]


rows = []
for sim_nr in [1,4,21,22,30]:
    X = np.load(f"./data/sim{sim_nr}_data.npy")
    y = np.load(f"./data/sim{sim_nr}_labels.npy")

    nr_clusters = len(np.unique(y))
    kmeans = KMeans(n_clusters=nr_clusters, random_state=0).fit(X)

    rows.append([f"Sim{sim_nr}",
                 f"{adjusted_rand_score(y, kmeans.labels_):.3f}",
                 f"{adjusted_mutual_info_score(y, kmeans.labels_):.3f}",
                 f"{purity_score(y, kmeans.labels_):.3f}",
                 f"{fowlkes_mallows_score(y, kmeans.labels_):.3f}",
                 f"{v_measure_score(y, kmeans.labels_):.3f}",
                 f"{scs_metric(y, kmeans.labels_):.3f}",
                 ])

create_table(columns, rows)