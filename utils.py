import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import itertools
from graspologic.embed import AdjacencySpectralEmbed
from plotnine import ggplot, geom_density, geom_line, geom_bar, geom_histogram, geom_boxplot
from plotnine import aes, element_blank, labs, scale_fill_manual, scale_x_continuous, theme_minimal, facet_wrap, theme, element_text, element_rect

from omnibus_latent_pos import create_ase_omnibus_matrix


# Functions to display nodes and edges of a graph______________________________________
def show_graph_with_labels(adjacency_matrix, labels, community_labels=None, 
                            title="Graph", node_size=300, edge_width=1.0, 
                            show_labels=True, legend_loc="best", ax=None):
    rows, cols = np.where(adjacency_matrix == 1)
    edges = list(zip(rows.tolist(), cols.tolist()))

    gr = nx.Graph()
    gr.add_edges_from(edges)
    gr.add_nodes_from(labels.keys())
    pos = nx.kamada_kawai_layout(gr)

    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 6))

    if community_labels is not None:
        unique_communities = sorted(set(community_labels.values()))
        color_map = {comm: i for i, comm in enumerate(unique_communities)}
        node_colors = [color_map[community_labels[node]] for node in gr.nodes()]
        cmap = plt.cm.rainbow

        nodes = nx.draw_networkx_nodes(gr, pos, node_size=node_size, node_color=node_colors, cmap=cmap, ax=ax)

        handles = [ax.scatter([], [], color=cmap(color_map[comm] / len(unique_communities)), label=f"Species {comm+1}") for comm in unique_communities]
        ax.legend(handles=handles, title="Species", loc=legend_loc, fontsize=8)

    else:
        nodes = nx.draw_networkx_nodes(gr, pos, node_size=node_size, node_color="lightblue", ax=ax)

    nx.draw_networkx_edges(gr, pos, width=edge_width, edge_color="black", ax=ax)

    if show_labels:
        nx.draw_networkx_labels(gr, pos, labels=labels, font_size=8, font_color="black", ax=ax)

    ax.set_title(title)
    ax.axis("off")

def generate_labels_dict(n):
    return {i: i for i in range(n)}


# Functions used for data kernel explorations______________________________________
def get_dict_edges(data_kernel):
    """
    Creates two dictionaries that resumes nodes degrees properties.

    Parameters
    ----------
    data_kernel: ndarray of shape (n_samples, n_samples)
        A binary matrix where entry (i, j) is 1 if sample j is among the k-nearest 
        neighbors of sample i or if sample i is among the k nearest neighbors
        of sample j, and 0 otherwise.

    Returns
    -------
    dict_edge_nb: dict
        The number of nodes per degrees (ex: {2: 4, 3: 1})
    dict_edge: dict
        The degrees and nodes associated (ex: {2: [0, 1, 3, 4], 3: [2]})
    """
    graph = nx.from_numpy_array(data_kernel)
    dict_edge = dict()
    for i in range(data_kernel.shape[0]):
        if len(graph.edges(i)) not in dict_edge.keys():
            dict_edge[len(graph.edges(i))] = list()
        dict_edge[len(graph.edges(i))].append(i)
    dict_edge_nb = dict()
    for key, value in dict_edge.items():
        dict_edge_nb[key] = len(value)
    return dict_edge_nb, dict_edge

def plot_degree_distribution(data_kernel_euc, data_kernel_cos, model_name):
    """
    Visualize and compare how node degrees vary between two graphs 
    constructed from Euclidean and cosine similarity matrices

    Parameters
    ----------
    data_kernel_euc: ndarray of shape (n_samples, n_samples)
        A data kernel calculated with the euclidean distance
    data_kernel_cos: ndarray of shape (n_samples, n_samples)
        A data kernel calculated with the cosine distance
    model_name: str
        The name of the model used to make the embedding

    Returns
    -------
    plot: plotnine.ggplot.ggplot
        Two histograms of node degrees for the two distances
    """
    data_kernel_euc_edges = get_dict_edges(data_kernel_euc)[1]
    data_kernel_cos_edges = get_dict_edges(data_kernel_cos)[1]
    
    all_degrees_euc = []
    all_degrees_cos = []
    for degree, nodes in data_kernel_euc_edges.items():
        all_degrees_euc.extend([degree] * len(nodes))
    for degree, nodes in data_kernel_cos_edges.items():
        all_degrees_cos.extend([degree] * len(nodes))
    df_euc = pd.DataFrame({'Degree': all_degrees_euc, 'Data_kernel': 'Euclidean'})
    df_cos = pd.DataFrame({'Degree': all_degrees_cos, 'Data_kernel': 'Cosine'})
    df = pd.concat([df_euc, df_cos], ignore_index=True)
    plot_title = f"Degree distribution of the {model_name} data kernel nodes"
    plot = (
        ggplot(df, aes(x='Degree', fill='Data_kernel'))
        + geom_histogram(binwidth=10, color="black", alpha=0.7, position="dodge")
        + labs(
            title=plot_title,
            x="Degree",
            y="Number of Nodes"
        )
        + scale_fill_manual(values=["#FFC300", "#9590FF"])
        + facet_wrap('~Data_kernel', scales='free_y')
        + theme_minimal()
    )
    return plot

def compute_embedding_norms_by_degree_threshold(data_kernel, embedding):
    """
    Compare embedding vector norms between strongly 
    and weakly connected nodes

    Parameters
    ----------
    data_kernel: ndarray of shape (n_samples, n_samples)
        A binary matrix where entry (i, j) is 1 if sample j is among the k-nearest 
        neighbors of sample i or if sample i is among the k nearest neighbors
        of sample j, and 0 otherwise.
    embedding: (n_samples, p_dimensions)
        The embedding used for the data kernel

    Returns
    -------
    norms_highly_connected: list
        The list of norms of highly connected nodes
    norms_not_highly_connected: list
        The list of norms of lightly connected nodes
    """
    nb_edges_dk, edges_dk = get_dict_edges(data_kernel)
    highly_connected = [embedding[node] for edge, node in edges_dk.items() if edge >= 250]
    highly_connected = list(itertools.chain(*highly_connected))
    norms_highly_connected = [np.linalg.norm(vector) for vector in highly_connected]

    not_highly_connected = [embedding[node] for edge, node in edges_dk.items() if edge < 250]
    not_highly_connected = list(itertools.chain(*not_highly_connected))
    norms_not_highly_connected = [np.linalg.norm(vector) for vector in not_highly_connected]

    return norms_highly_connected, norms_not_highly_connected
        
def plot_embedding_norms_distribution(data_kernel_euc, data_kernel_cos, embedding, embedding_model):
    """
    Creates a data frame and 3 plots resuming embedding norms distributions 
    and comparing strongly and weakly connected nodes.

    Parameters
    ----------
    data_kernel_euc: ndarray of shape (n_samples, n_samples)
        A data kernel calculated with the euclidean distance
    data_kernel_cos: ndarray of shape (n_samples, n_samples)
        A data kernel calculated with the cosine distance
    embedding: (n_samples, p_dimensions)
        The embedding used for the data kernel
    embedding_model: str
        The name of the model used to make the embedding
    
    Dislays
    --------
    Plot of the euclidean norm distribution of sequence embedding
    with a density curve, a histogram, a boxplot, and colored by 
    number of edges per node (wether < 250 edges or >= 250 edges)

    Returns
    -------
    df: pandas.core.frame.DataFrame
        A data fame containing the following variables:
            Euclidean norm of embedding vectors
            Edges per node: < 250 edges or >= 250 edges
            Data_kernel_distance: 'Euclidean' or 'Cosine'
            Euclidean norm bins
            Bin midpoint
    """
    dist_full_euc, dist_not_full_euc = compute_embedding_norms_by_degree_threshold(data_kernel_euc, embedding)
    dist_full_cos, dist_not_full_cos = compute_embedding_norms_by_degree_threshold(data_kernel_cos, embedding)

    df_euc = pd.DataFrame({
        "Euclidean norm": np.concatenate([dist_full_euc, dist_not_full_euc]),
        "Edges per node": [">= 250 edges"] * len(dist_full_euc) + ["< 250 edges"] * len(dist_not_full_euc),
        "Data_kernel_distance": ["Euclidean"] * (len(dist_full_euc) + len(dist_not_full_euc))  # Corrected column name
    })

    df_cos = pd.DataFrame({
        "Euclidean norm": np.concatenate([dist_full_cos, dist_not_full_cos]),
        "Edges per node": [">= 250 edges"] * len(dist_full_cos) + ["< 250 edges"] * len(dist_not_full_cos),
        "Data_kernel_distance": ["Cosine"] * (len(dist_full_cos) + len(dist_not_full_cos))  # Corrected column name
    })

    df = pd.concat([df_euc, df_cos], ignore_index=True)

    # Dynamically calculate bin width based on the range of data
    min_value = df['Euclidean norm'].min()
    max_value = df['Euclidean norm'].max()
    range_value = max_value - min_value

    # Choose a bin width that is appropriate for the range
    bin_width = 0.1 if range_value >= 0.1 else range_value / 10  # If range < 0.1, divide it into smaller bins

    # Manually create bins
    bins = np.arange(min_value, max_value + bin_width, bin_width)  # Ensure the last bin is included
    df['Euclidean norm bins'] = pd.cut(df['Euclidean norm'], bins=bins, right=False)

    # Convert Interval objects to the midpoint for plotting
    df['Bin midpoint'] = df['Euclidean norm bins'].apply(lambda x: x.mid)
    
    # Titles and subtitles
    density_title = f'Euclidean norm distribution of {embedding_model} sequence embedding'
    hist_title = f'Histogram of the Euclidean norm of {embedding_model} sequence embedding'
    boxplot_title = f'Boxplot of the Euclidean norm of {embedding_model} sequence embedding'
    subtitle = "The data is split into two parts: sequences with fewer than 249 neighbors in\nthe data kernel and sequences with at least 250 neighbors in the data kernel"

    # Density plot
    plot_density = (
        ggplot(df, aes(x="Euclidean norm", fill="Edges per node"))
        + geom_density(alpha=0.5)
        + facet_wrap("~Data_kernel_distance")
        + labs(
            title=density_title,
            subtitle=subtitle,
            x="Euclidean norm",
            y="Density"
        )
        + scale_fill_manual(values=["#00BFC4", "#F8766D"])
        + scale_x_continuous(breaks=range(int(min(df['Euclidean norm'])), int(max(df['Euclidean norm'])) + 1))  # Adjusting the X-axis breaks
        + theme_minimal()
        + theme(
            plot_subtitle=element_text(size=7),  # Reduce subtitle size
            panel_border=element_rect(color="black", size=0.3)  # Thin border between facets
        )
    )

    # Histogram plot
    plot_hist = (
        ggplot(df, aes(x="Bin midpoint", fill="Edges per node"))
        + geom_bar(stat="count", position="dodge", alpha=0.5, color="black")
        + facet_wrap("~Data_kernel_distance")
        + labs(
            title=hist_title,
            subtitle=subtitle,
            x="Euclidean norm",
            y="Frequency"
        )
        + scale_fill_manual(values=["#00BFC4", "#F8766D"])
        + theme_minimal()
        + theme(
            plot_subtitle=element_text(size=7),
            panel_border=element_rect(color="black", size=0.3),
            axis_text_x=element_blank()
        )
    )

    # Boxplot
    plot_box = (
        ggplot(df, aes(x="Edges per node", y="Euclidean norm", fill="Edges per node"))
        + geom_boxplot(alpha=0.5)
        + facet_wrap("~Data_kernel_distance")
        + labs(
            title=boxplot_title,
            subtitle=subtitle,
            x="Edges per node",
            y="Euclidean norm"
        )
        + scale_fill_manual(values=["#00BFC4", "#F8766D"])
        + theme_minimal()
        + theme(
            plot_subtitle=element_text(size=7),  # Reduce subtitle size
            panel_border=element_rect(color="black", size=0.3)  # Thin border between facets
        )
    )

    # Display all plots
    display(plot_density)
    display(plot_hist)
    display(plot_box)
    return df


# Functions used for latent positions explorations_________________________________

# 1. Function to study the evolution of distance between two Z over d
def cumulative_euclidean_distance_by_dimension(Z1, Z2, node_1, node_2):
    """
    Computes the cumulative Euclidean distance between two latent 
    positions vectors from Z1 and Z2, progressively increasing 
    the number of dimensions considered.
    For each dimension d from 1 to D-1 (where D is the total 
    number of dimensions), this function calculates the Euclidean 
    distance between the first d components of the two specified node
    latent positions.

    Parameters:
    ----------
    Z1: np.ndarray
        First latent positions matrix of shape (n_nodes, n_components).
    Z2: np.ndarray
        Second latent positions matrix of shape (n_nodes, n_components).
    node_1: int
        Index of the node in Z1 to compare.
    node_2: int
        Index of the node in Z2 to compare.

    Returns:
    -------
    distance_Z: list
        A list of cumulative Euclidean distance for each dimension d,
        showing how the difference between the two latent position
        evolves as dimensions increase.
    """
    distance_Z = list()
    Z1_node = Z1[node_1]
    Z2_node = Z2[node_2]
    for d in range(Z1.shape[1]-1):
        distance_Z.append((np.linalg.norm(Z1_node[0:d+1] - Z2_node[0:d+1]))**2)
    return distance_Z

def plot_median_cumulative_euclidean_distance_by_dimension(A1, A2, d_max, model_comparison):
    """
    Plots the average cumulative Euclidean distance between latent
    positions of all nodes from two different graphs A1 and A2 
    as the number of dimensions increases.

    Uses Adjacency Spectral Embedding (ASE) applied to the omnibus matrix
    constructed from A1 and A2. For each node, it computes the Euclidean
    distance between its latent position in the two graphs, from dimension 1 
    to D, then averages these distances across all nodes.

    Parameters
    ----------
    A1: np.ndarray of shape (n_samples, n_samples)
        Adjacency matrix of the first graph.
    A2: np.ndarray of shape (n_samples, n_samples)
        Adjacency matrix of the second graph.
    model_comparison: str
        The names of the models for the plot title
    d_max: int
        The number of component of the ASE

    Returns
    -------
    plot: plotnine.ggplot.ggplot
        A ggplot object showing the mean evolution of Euclidean distance
        between latent positions as a function of the number of 
        dimensions used.
    """
    omnibus_Z1, omnibus_Z2 = create_ase_omnibus_matrix(A1, A2, n_components=d_max, save_memory=False)

    n_nodes = omnibus_Z1.shape[0]
    
    all_cumulative_dists = [
        cumulative_euclidean_distance_by_dimension(omnibus_Z1, omnibus_Z2, i, i)
        for i in range(n_nodes)
    ]
    mean_distances = np.median(all_cumulative_dists, axis=0)

    df = pd.DataFrame({
        'd': list(range(1, omnibus_Z1.shape[1])), 
        'Mean squared distance': mean_distances
    })

    plot = (
        ggplot(df, aes(x="d", y="Mean squared distance")) +
        geom_line(color="#1f77b4") +
        labs(
            title=r"Mean evolution of $||Z^1_i - Z^2_i||^2$ over $d$ for all nodes $i$",
            subtitle=f'$Z^1$ and $Z^2$ from {model_comparison[0]} and {model_comparison[1]} omnibus matrix',
            x=r"Number of dimensions $d$",
            y=r"Mean Euclidean distance"
        ) +
        scale_x_continuous(breaks=range(0, omnibus_Z1.shape[1] + 1, omnibus_Z1.shape[1] // 10)) +
        theme_minimal()
    )
    return plot

def plot_cumulative_euclidean_distance_by_cluster_and_model(A1, A2, node, same_cluster_node, diff_cluster_node, model_comparison):
    """
    Plots the evolution of Euclidean distances between latent positions 
    of a target node and other nodes, under different relationship 
    conditions (same cluster / different cluster, same model / 
    different model).

    Parameters
    ----------
    A1: np.ndarray
        Adjacency matrix of the first graph (model).
    A2: np.ndarray
        Adjacency matrix of the second graph (different model).
    node: int
        Index of the reference node in the graphs.
    same_cluster_node: int
        Index of a node in the same cluster as `node`.
    diff_cluster_node: int
        Index of a node in a different cluster from `node`.
    model_comparison: str
        The names of the models for the plot title

    Returns
    -------
    plot: plotnine.ggplot.ggplot
        A ggplot object comparing the cumulative Euclidean 
        distance evolution across node pair types.
    """
    Z1, Z2 = create_ase_omnibus_matrix(A1, A2, n_components=A1.shape[0], save_memory=False)

    df = pd.DataFrame({
        "d": list(range(1, Z1.shape[1])),
        f"$Z^1_{{{node+1}}}$ vs $Z^1_{{{same_cluster_node+1}}}$ Intra-cluster (same model)": cumulative_euclidean_distance_by_dimension(Z1, Z1, node, same_cluster_node),
        f"$Z^1_{{{node+1}}}$ vs $Z^1_{{{diff_cluster_node+1}}}$ Inter-cluster (same model)": cumulative_euclidean_distance_by_dimension(Z1, Z1, node, diff_cluster_node),
        f"$Z^1_{{{node+1}}}$ vs $Z^2_{{{node+1}}}$ Intra-cluster (cross model)": cumulative_euclidean_distance_by_dimension(Z1, Z2, node, node),
    })

    df_long = df.melt(id_vars="d", var_name="Comparison type", value_name="Distance")

    plot = (
        ggplot(df_long, aes(x="d", y="Distance", color="Comparison type")) +
        geom_line() +
        labs(
            title=f"Evolution of $||Z^1_{{{node+1}}} - Z^m_j||^2$ over $d$",
            subtitle=f'$Z^1$ and $Z^2$ from {model_comparison[0]} and {model_comparison[1]} omnibus matrix',
            x=r"Number of dimensions $d$",
            y=f"$||Z^1_{{{node+1}}} - Z^m_j||^2$",
            color="Comparison type"
        ) +
        theme_minimal()
    )

    return plot

# 2. Function to study the distribution of Z before and after d
def distribution_z_before_after_d(A, node):
    """
    Plots the distribution of Z for a given node before and after 
    the optimal dimension `d`.

    The function computes:
    - A full-rank embedding `Z_full` with `n_components = A.shape[0]`
    - A truncated embedding `Z` where the optimal latent positions 
      dimension `d` is automatically selected
    It then compares the values in `Z_full` corresponding to the first 
    `d` dimensions (interpreted as "signal") with the remaining dimensions 
    (interpreted as "noise") for the specified node.

    Parameters
    ----------
    A: np.ndarray
        Adjacency matrix of the graph.
    node: int
        Index of the node whose distribution is to be analyzed.

    Returns
    -------
    plot: plotnine.ggplot.ggplot
        A density plot showing the distribution of the node's latent
        positions distribution in the signal dimensions ([:d]) vs. 
        the remaining dimensions ([d:]).
    """
    Z_full = AdjacencySpectralEmbed(n_components=A.shape[0], algorithm='full', check_lcc=False, diag_aug=False).fit_transform(A)
    Z = AdjacencySpectralEmbed(algorithm='full', check_lcc=False, diag_aug=False).fit_transform(A)
    Z_before = Z_full[node, 0:Z.shape[1]]
    Z_after = Z_full[node, Z.shape[1]:]
    df = pd.DataFrame({
        'value': list(Z_before) + list(Z_after),
        f'Part of $Z_{{{node+1}}}$': [f'$Z_{{{node+1}}}$[:{Z.shape[1]}]'] * len(Z_before) + [f'$Z_{{{node+1}}}$[{Z.shape[1]}:]'] * len(Z_after)})
    plot = (
        ggplot(df, aes(x='value', fill=f'Part of $Z_{{{node+1}}}$', color=f'Part of $Z_{{{node+1}}}$')) +
        geom_density(alpha=0.3) +
        labs(
            title=f'Distribution of Z for node {node+1} before and after $d = {Z.shape[1]}$',
            x='Z',
            y='Density'
        ) +
        theme_minimal()
    )
    return plot

# 3. Function to study edge probability between every node
def get_cluster_of_node(node, cluster_dict):
    """
    Returns the cluster ID that a given node belongs to.

    Parameters
    ----------
    node: int
        The node index to search for.
    cluster_dict: dict
        A dictionary mapping cluster IDs to lists of node indices.
        Example: {1: [0, 1, 2], 2: [3, 4]}.

    Returns
    -------
    cluster: int
        The cluster ID containing the node.
    """
    for cluster, indices in cluster_dict.items():
        if node in indices:
            return cluster

def get_nodes_id_of_clusters(clusters):
    """
    Generates a dictionary mapping cluster IDs to node indices,
    based on a list of cluster sizes.

    Parameters
    ----------
    clusters: list of int
        A list where each entry represents the number of nodes in a cluster.
        Example: [3, 2, 4] creates three clusters of sizes 3, 2, and 4.

    Returns
    -------
    cluster_dict: dict
        A dictionary where keys are cluster IDs (starting at 1),
        and values are lists of node indices belonging to each cluster.
        Example: {1: [0, 1, 2], 2: [3, 4], 3: [5, 6, 7, 8]}.
    """
    range_clusters = [0] * (len(clusters) + 1)
    for k in range(len(clusters)):
        range_clusters = range_clusters[0:k+1] + list(map(lambda x:x+clusters[k], range_clusters[k+1:]))
    cluster_dict = dict()
    for i in range(len(clusters)):    
        cluster_dict[i+1] = list(range(range_clusters[i], range_clusters[i+1]))
    return cluster_dict

def node_edges_probability(node, Z, clusters):
    """
    Computes the average dot product (i.e., estimated edge probability) 
    between a given node and other nodes in the same cluster vs. nodes 
    in different clusters.

    Parameters
    ----------
    node: int
        Index of the reference node.
    Z: np.ndarray
        Latent positions matrix.
    clusters: list of int
        List of cluster sizes. Example: [3, 2, 4] means 3 nodes in cluster 1, 
        2 in cluster 2, etc.

    Returns
    -------
    tuple of float
        (1) Average dot product between `node` and nodes in the same cluster 
            (excluding itself),  
        (2) Average dot product between `node` and nodes in other clusters.
    """
    clusters_dict = get_nodes_id_of_clusters(clusters)
    ZZT = Z @ Z.T
    node_cluster = get_cluster_of_node(node, clusters_dict)
    same_clust_indices = clusters_dict[node_cluster]
    same_clust_indices.remove(node)
    del clusters_dict[node_cluster]
    other_clust_indices = sum(clusters_dict.values(), [])
    return np.mean(ZZT[node][same_clust_indices]), np.mean(ZZT[node][other_clust_indices])

def mean_nodes_edges_probabilities(clusters, A=None, Z=None, use_Z=False):
    """
    Computes and visualizes the distribution of average edge 
    probabilities for each node with respect to nodes in the 
    same cluster and nodes in different clusters.

    Depending on the `use_Z` flag, the edge probabilities are 
    estimated using either:
    - the latent positions from an Adjacency Spectral Embedding 
      (ASE) of the adjacency matrix `A`, or
    - the provided latent position matrix `Z`.

    Parameters
    ----------
    clusters: list of int
        A list where each entry represents the number of nodes 
        in a cluster. Example: [3, 2, 4] means there are three 
        clusters with 3, 2, and 4 nodes respectively.
    A: np.ndarray, optional
        Adjacency matrix of the graph. Required if `use_Z` is False.
    Z: np.ndarray, optional
        Latent position matrix, required if `use_Z` is True.
    use_Z: bool, default=False
        If True, uses the provided `Z` instead of computing one 
        from `A` using ASE.

    Returns
    -------
    plot: plotnine.ggplot.ggplot
        A boxplot comparing the mean estimated edge probabilities 
        (dot products) between:
        - nodes and others in the same cluster
        - nodes and others in different clusters
    """
    if not use_Z:
        Z = AdjacencySpectralEmbed(algorithm='full', check_lcc=False, diag_aug=False).fit_transform(A)
    ZZT_same_cluster = list()
    ZZT_other_clusters = list()
    for i in range(Z.shape[0]):
        ZZT_mean = node_edges_probability(i, Z, clusters)
        ZZT_same_cluster.append(ZZT_mean[0])
        ZZT_other_clusters.append(ZZT_mean[1])
    ZZT_df = pd.DataFrame({'ZZT same cluster': ZZT_same_cluster, 'ZZT other clusters': ZZT_other_clusters, 'Node id': list(range(Z.shape[0]))})
    ZZT_df = ZZT_df.melt(var_name="Which cluster", value_name="Mean ZZT", id_vars='Node id')
    plot = (
    ggplot(ZZT_df, aes(x='Which cluster', y='Mean ZZT', fill="Which cluster", color="Which cluster")) + 
    geom_boxplot(alpha=0.5) +
    labs(title='Mean edges probabilities for each node',
           x="Mean ZZT",
           y="Density") +
    theme_minimal()
    )
    return plot



# 4. Function to compare variance of distributions before and after d optimal with cumulative euclidean distance before and after d optimal
# It doesn't to be an equality here but i am not sure that my function is correct
# def compare_variance_and_cumulative_euclidean_distance_by_dimension(A1, A2, node, d_max, model_comparison):
#     Z1_full = AdjacencySpectralEmbed(n_components=A1.shape[0], algorithm='full', check_lcc=False, diag_aug=False).fit_transform(A1)
#     Z1 = AdjacencySpectralEmbed(algorithm='full', check_lcc=False, diag_aug=False).fit_transform(A1)
#     Z1_before = Z1_full[node, 0:Z1.shape[1]]
#     Z1_after = Z1_full[node, Z1.shape[1]:]
#     variance_Z1_before = np.var(Z1_before)
#     variance_Z1_after = np.var(Z1_after)


#     Z2_full = AdjacencySpectralEmbed(n_components=A2.shape[0], algorithm='full', check_lcc=False, diag_aug=False).fit_transform(A2)
#     Z2 = AdjacencySpectralEmbed(algorithm='full', check_lcc=False, diag_aug=False).fit_transform(A2)
#     Z2_before = Z2_full[node, 0:Z2.shape[1]]
#     Z2_after = Z2_full[node, Z2.shape[1]:]
#     variance_Z2_before = np.var(Z2_before)
#     variance_Z2_after = np.var(Z2_after)

    
#     omnibus_Z1, omnibus_Z2 = create_ase_omnibus_matrix(A1, A2, n_components=d_max, save_memory=False)

#     # Z1_before = omnibus_Z1[node, 0:Z1.shape[1]]
#     # Z1_after = omnibus_Z1[node, Z1.shape[1]:]
#     # variance_Z1_before = np.var(Z1_before)
#     # variance_Z1_after = np.var(Z1_after)

#     # Z2_before = omnibus_Z2[node, 0:Z2.shape[1]]
#     # Z2_after = omnibus_Z2[node, Z2.shape[1]:]
#     # variance_Z2_before = np.var(Z2_before)
#     # variance_Z2_after = np.var(Z2_after)
    
#     cumulative_distances = cumulative_euclidean_distance_by_dimension(omnibus_Z1, omnibus_Z2, node, node)
#     slope1_before = (cumulative_distances[Z1.shape[1] - 1] - cumulative_distances[0]) / (Z1.shape[1] - 1)
#     slope2_before = (cumulative_distances[Z2.shape[1] - 1] - cumulative_distances[0]) / (Z2.shape[1] - 1)

#     print('variance_Z1_before :', variance_Z1_before, 'slope1_before :', slope1_before)
#     print('variance_Z2_before :', variance_Z2_before, 'slope2_before :', slope2_before)
#     # return variance_Z1_before, variance_Z1_after, variance_Z2_before, variance_Z2_after
