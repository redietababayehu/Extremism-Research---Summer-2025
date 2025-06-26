import pandas as pd

# Load your dataset
df = pd.read_csv('youtube_comments_with_emotions.csv')

# Find comment IDs that are parent of other comments
comments_with_replies = df[df['parent_id'].isin(df['comment_id'])]['parent_id'].unique()

# Filter dataframe to include only comments that are in comments_with_replies or are replies themselves
filtered_df = df[df['comment_id'].isin(comments_with_replies) | df['parent_id'].isin(comments_with_replies)]

# Save the filtered dataset to a new CSV
filtered_df.to_csv('youtube_comments_with_replies_filtered.csv', index=False)

# Print sizes
print(f"Original dataset size: {len(df)}")
print(f"Filtered dataset size: {len(filtered_df)}")
print("Filtered dataset saved as 'youtube_comments_with_replies_filtered.csv'")