import pandas as pd

# Load data from the CSV file into a DataFrame
df = pd.read_csv("youtube_comments_test.csv")

# add a thread_id for each top-level comment so that you can attach replies to the id
# create a new column called thread_id
df['thread_id'] = df.apply(
    # if the row is a top-level comment then the comment id = thread id
    lambda row: row['comment_id'] if row['comment_type'] == 'comment' else None,
    axis=1
)

# filter the dataFrame so that it only has top-level comments
comment_id_to_thread = df[df['comment_type'] == 'comment'].set_index('comment_id')['thread_id'].to_dict()

# Assign thread_id to replies based on their parent_id
def assign_thread_id(row):
    if row['comment_type'] == 'reply':
        return comment_id_to_thread.get(row['parent_id'])  # inherit from parent
    else:
        return row['thread_id']  # keep own ID

df['thread_id'] = df.apply(assign_thread_id, axis=1)

# Optional: Fill any missing thread_ids (e.g., reply to a missing/filtered comment)
df['thread_id'] = df['thread_id'].fillna('unknown')

# Save updated dataset into a CSV file 
df.to_csv("youtube_comments_with_threads.csv", index=False)
print("Saved updated file with thread_id to youtube_comments_with_threads.csv")
