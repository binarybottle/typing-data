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
    
    # Process each bigram
    for _, row in df.iterrows():
        first_char = row['first_char'].lower()
        second_char = row['second_char'].lower()
        comfort_score = row['comfort_score']
        
        # Skip if either character is not in our key mapping
        if first_char not in key_map or second_char not in key_map:
            continue
            
        # Get the key IDs
        origin_id = key_map[first_char]
        dest_id = key_map[second_char]
        
        # Add to output data
        output_data.append({
            'origin': origin_id,
            'dest': dest_id,
            'count': comfort_score
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
    print(f"Output saved to {output_file}")