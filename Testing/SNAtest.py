import networkx as nx
import matplotlib.pyplot as plt

# Create a social network graph
G = nx.Graph()

# Add nodes (people)
G.add_nodes_from(["Alice", "Bob", "Charlie", "David", "Eve", "Frank"])

# Add edges (friendships)
G.add_edges_from([
    ("Alice", "Bob"),
    ("Alice", "Charlie"),
    ("Bob", "David"),
    ("Charlie", "David"),
    ("David", "Eve"),
    ("Eve", "Frank")
])

# Visualize the network
plt.figure(figsize=(8, 6))
nx.draw(G, with_labels=True, node_color="skyblue", edge_color="gray", node_size=2000, font_size=15)
plt.title("Social Network Graph")
plt.show()

# Degree Centrality (who has the most connections?)
centrality = nx.degree_centrality(G)
print("Degree Centrality:")
for person, score in centrality.items():
    print(f"{person}: {score:.2f}")

# Detect communities using greedy modularity
from networkx.algorithms.community import greedy_modularity_communities
communities = list(greedy_modularity_communities(G))
print("\nDetected Communities:")
for i, community in enumerate(communities):
    print(f"Community {i + 1}: {sorted(community)}")
