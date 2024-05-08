from multiprocessing import Pool, Manager
from threading import Lock
import numpy as np

class SimilarityGraph:
    def __init__(self, max_neighbors=10, similarity_threshold=0.5, num_processes=4):
        self.nodes = {}  # Dictionary to store nodes (data points) and their neighbors
        self.max_neighbors = max_neighbors
        self.similarity_threshold = similarity_threshold
        self.num_processes = num_processes

        # Efficient data structures
        self.node_ids = []  # List of node IDs for efficient iteration
        self.data_matrix = []  # Matrix of data points for efficient similarity calculation

        # Shared data structures for parallelization
        manager = Manager()
        self.shared_nodes = manager.dict(self.nodes)
        self.shared_node_ids = manager.list(self.node_ids)
        self.shared_data_matrix = manager.list(self.data_matrix)

        # Locks for thread safety
        self.node_lock = Lock()
        self.data_lock = Lock()

    def add_node(self, node_id, data):
        """
        Add a new node to the graph.
        """
        # Efficient similarity calculation
        similarities = self.calculate_similarities(data)

        # Filter and sort neighbors with additional pruning
        pruned_similarities = self.prune_similarities(similarities)
        neighbors = [id_ for id_, sim in sorted(pruned_similarities.items(), key=lambda x: x[1], reverse=True)[:self.max_neighbors] if sim >= self.similarity_threshold]

        # Add the new node and its neighbors
        with self.node_lock:
            self.nodes[node_id] = (data, neighbors)
            self.node_ids.append(node_id)
            self.data_matrix.append(data)
            self.shared_nodes[node_id] = (data, neighbors)
            self.shared_node_ids.append(node_id)
            self.shared_data_matrix.append(data)

        # Update neighbors of existing nodes
        self.update_neighbors(node_id, pruned_similarities)

    # Other methods (update_node, remove_node, get_neighbors, calculate_similarities, update_neighbors, calculate_similarity) are the same as before

    def prune_similarities(self, similarities):
        """
        Prune similarities using additional heuristics or strategies.
        """
        # Example heuristic: Discard similarities below a certain threshold
        pruned_similarities = {id_: sim for id_, sim in similarities.items() if sim >= self.similarity_threshold * 0.8}
        return pruned_similarities

    def calculate_similarities(self, data):
        """
        Calculate similarities between the given data and all existing nodes in parallel.
        """
        with self.data_lock:
            node_ids = list(self.shared_node_ids)
            data_matrix = list(self.shared_data_matrix)

        with Pool(processes=self.num_processes) as pool:
            similarities = pool.starmap(self.calculate_similarity, [(data, data_matrix[i]) for i in range(len(data_matrix))])

        return {node_ids[i]: sim for i, sim in enumerate(similarities)}

    def update_neighbors(self, node_id, similarities):
        """
        Update neighbors of existing nodes based on the new node and its similarities.
        """
        node_data, _ = self.nodes[node_id]
        for other_id, other_data, other_neighbors in [(id_, data, neighbors) for id_, (data, neighbors) in self.shared_nodes.items() if id_ != node_id]:
            if node_id in other_neighbors:
                continue  # Node is already a neighbor

            similarity = similarities.get(other_id, self.calculate_similarity(node_data, other_data))
            if similarity >= self.similarity_threshold:
                with self.node_lock:
                    other_neighbors.append(node_id)
                    other_neighbors = sorted(other_neighbors, key=lambda x: similarities[x], reverse=True)[:self.max_neighbors]
                    self.nodes[other_id] = (other_data, other_neighbors)
                    self.shared_nodes[other_id] = (other_data, other_neighbors)

# Usage example
graph = SimilarityGraph()

# Add nodes concurrently
import concurrent.futures

def add_node_worker(node_id, data):
    graph.add_node(node_id, data)

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    for i in range(100):
        data = np.random.rand(10)
        future = executor.submit(add_node_worker, i, data)
        futures.append(future)

    for future in concurrent.futures.as_completed(futures):
        try:
            future.result()
        except Exception as e:
            print(f"Error: {e}")

# Get neighbors of a node
neighbors = graph.get_neighbors(0, k=5)
print(neighbors)