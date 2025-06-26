import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

#Load the data from CSV file
df = pd.read_csv("youtube_comments_with_threads.csv")

valid_threads = df[df['thread_id'] != 'unknown']['thread_id'].unique()

# Print available thread IDs to choose from
print("Available thread IDs (sample):")
print(valid_threads[:10])  # Print first 10 

# Pick one thread to visualize (hardcoded)
thread_id_to_plot = valid_threads[0]  # Change index for a diffferent thread

# Filter the thread
thread_df = df[df['thread_id'] == thread_id_to_plot]

# Build a graph
G = nx.DiGraph()

# Add nodes with labels
for _, row in thread_df.iterrows():
    label = f"{row['author'][:10]}: {row['text'][:30]}..."  # Shortened label
    G.add_node(row['comment_id'], label=label, comment_type=row['comment_type'])

# Add edges (replies)
for _, row in thread_df.iterrows():
    if pd.notna(row['parent_id']) and row['parent_id'] in G.nodes:
        G.add_edge(row['parent_id'], row['comment_id'])

# define the layout of the hierarchy
def hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    pos = {}
    def _hierarchy_pos(G, node, left, right, vert_loc, pos, parent=None):
        center = (left + right) / 2 #calculate the center
        pos[node] = (center, vert_loc) # Place the current node here 
        children = list(G.successors(node)) # get the children of the current node

        # divide the horizontal space between the children
        if children:
            dx = (right - left) / len(children)
            nextx = left
            for child in children:
                pos = _hierarchy_pos(G, child, nextx, nextx + dx, vert_loc - vert_gap, pos, node)
                nextx += dx
        return pos
    # use recursion for each child
    return _hierarchy_pos(G, root, 0, width, vert_loc, pos)

# Find root node (top-level comment of this thread) 
root_id = thread_df[thread_df['comment_type'] == 'comment']['comment_id'].iloc[0]
pos = hierarchy_pos(G, root=root_id)

# Draw the graph
node_colors = ['skyblue' if G.nodes[n]['comment_type'] == 'comment' else 'lightgreen' for n in G.nodes()]
nx.draw(G, pos, with_labels=False, node_color=node_colors, node_size=1200, arrows=True)

# Draw labels
labels = nx.get_node_attributes(G, 'label')
nx.draw_networkx_labels(G, pos, labels, font_size=7)

plt.title(f"Visualization of Thread ID: {thread_id_to_plot}")
plt.tight_layout()
plt.show()