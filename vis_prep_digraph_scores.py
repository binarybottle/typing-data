import pandas as pd
import numpy as np

def load_key_locations():
    """Load the key locations mapping with their IDs"""
    key_locations = [
        # First row (top)
        (1, 'q'), (2, 'w'), (3, 'e'), (4, 'r'), (25, 't'),
        (28, 'y'), (13, 'u'), (14, 'i'), (15, 'o'), (16, 'p'), (31, '['),
        # Second row (middle)
        (5, 'a'), (6, 's'), (7, 'd'), (8, 'f'), (26, 'g'),
        (29, 'h'), (17, 'j'), (18, 'k'), (19, 'l'), (20, ';'), (32, "'"),
        # Third row (bottom)
        (9, 'z'), (10, 'x'), (11, 'c'), (12, 'v'), (27, 'b'),
        (30, 'n'), (21, 'm'), (22, ','), (23, '.'), (24, '/')
    ]
    return {char: id for id, char in key_locations}

def normalize_scores(scores, target_min=1, target_max=100):
    """
    Normalize scores to integer values within specified range
    
    Args:
        scores: Array of comfort scores
        target_min: Minimum value for normalized scores
        target_max: Maximum value for normalized scores
    """
    # Handle negative values by shifting everything to positive
    min_score = min(scores)
    if min_score < 0:
        scores = [s - min_score for s in scores]
    
    # Normalize to [0, 1] range
    min_score = min(scores)
    max_score = max(scores)
    normalized = [(s - min_score) / (max_score - min_score) for s in scores]
    
    # Scale to target range and convert to integers
    scaled = [int(round(n * (target_max - target_min) + target_min)) for n in normalized]
    
    return scaled

def process_bigram_scores(input_file, output_file):
    """
    Process bigram comfort scores and output in the keypairtimes format
    
    Args:
        input_file: Path to the bigram comfort scores CSV
        output_file: Path to output the processed scores
    """
    # Read the bigram comfort scores
    df = pd.read_csv(input_file)
    
    # Load key location mapping
    key_map = load_key_locations()
    
    # Initialize output data
    output_data = []
    
    # Extract comfort scores for normalization
    valid_scores = []
    valid_rows = []
    
    # First pass to collect valid scores
    for _, row in df.iterrows():
        first_char = row['first_char'].lower()
        second_char = row['second_char'].lower()
        
        # Only include scores where both characters are in our mapping
        if first_char in key_map and second_char in key_map:
            valid_scores.append(row['comfort_score'])
            valid_rows.append(row)
    
    # Normalize the scores
    normalized_scores = normalize_scores(valid_scores)
    
    # Second pass to create output with normalized scores
    for score, row in zip(normalized_scores, valid_rows):
        first_char = row['first_char'].lower()
        second_char = row['second_char'].lower()
        
        origin_id = key_map[first_char]
        dest_id = key_map[second_char]
        
        output_data.append({
            'origin': origin_id,
            'dest': dest_id,
            'count': score
        })
    
    # Convert to DataFrame and sort
    output_df = pd.DataFrame(output_data)
    output_df = output_df.sort_values(['origin', 'dest'])
    
    # Save to CSV
    output_df.to_csv(output_file, index=False)
    
    return output_df

if __name__ == "__main__":
    input_file = "input/digraph_comfort_scores.csv"
    output_file = "key-pair-scores.csv"
    
    result_df = process_bigram_scores(input_file, output_file)
    print(f"Processed {len(result_df)} bigram pairs")
    print(f"Score range: {result_df['count'].min()} to {result_df['count'].max()}")
    print(f"Output saved to {output_file}")
