import pandas as pd
import numpy as np
import json
import os

points_per_event = 10
bonus_points_per_event = 2

# Read the input Excel file
input_df = pd.read_excel("C:\\Hayden\\Projects\\Apps\\Tipsters\\tipsdesktop_002\\src\\components\\Tipsters-2023.xlsx")

# Extract the events column from input_df
events_column = input_df.iloc[:, 0]

# Extract "Event", "Result", and "Bonus" columns into a separate DataFrame
events_df = input_df[["Event", "Result", "Bonus"]]
# Create a dictionary to map each unique event to its corresponding ID
event_id_mapping = {event: f"Event_{i+1}" for i, event in enumerate(events_df['Event'].unique())}
# Add the event ID to the events DataFrame
events_df['Event_ID'] = events_df['Event'].map(event_id_mapping)
# Rearrange columns to move 'Event_ID' to the second position
cols = events_df.columns.tolist()
cols = cols[:1] + [cols.pop(cols.index('Event_ID'))] + cols[1:]
events_df = events_df[cols]

# Add 'Correct_Tips' and 'Point_Share' columns to events_df and initialize them with zeros
events_df = events_df.assign(Correct_Tips=0, Point_Share=0)

# List of columns to remove
columns_to_remove = ['Event', 'Result', 'Bonus']

# Extract player names from the DataFrame columns
players_list = set(col.split(';')[0] for col in input_df.columns if col not in columns_to_remove)

# Initialize an empty dictionary to store player names
players_dict = {}

# Iterate over the players_list using enumerate to generate keys
for i, player_name in enumerate(sorted(players_list), start=1):
    # Split the player name by the '-' character
    parts = player_name.split('-')
    if len(parts) == 2:  # Ensure the split resulted in two parts
        # Assign first name (after '-') and last name (before '-')
        first_name = parts[1].strip()  # Remove any leading/trailing whitespace
        last_name = parts[0].strip()    # Remove any leading/trailing whitespace
        # Generate key in 'PlayerX' format
        player_key = f'Player{i}'
        # Add the player to the dictionary with first and last names
        players_dict[player_key] = {
            'first_name': first_name, 
            'last_name': last_name, 
            'correct_tips': 0, 
            'bonus_points': 0, 
            'points_tally': 0,}

# Create a new DataFrame for player selections with the desired structure
selections_df = input_df[[col for col in input_df.columns if col not in columns_to_remove]]

# Assign the events column to selections_df
selections_df.insert(0, 'Event', events_column)
# Add the event_id_mapping as the second column in the selections_df
selections_df.insert(1, 'Event_ID', selections_df['Event'].map(event_id_mapping))



# Iterate over the columns of selections_df and replace player names with their keys
for col in selections_df.columns:
    if 'Selection' in col or 'Bonus' in col:  # Check if the column contains 'Selection' or 'Bonus'
        player_name = col.split(';')[0]  # Extract player name from column name
        # Find the corresponding player key in the players_dict
        player_key = [key for key, value in players_dict.items() 
                      if value['last_name'] + ' - ' + value['first_name'] == player_name]
        if player_key:  # Check if the player key exists
            player_key = player_key[0]  # Get the player key
            new_col_name = f"{player_key};{'Selection' if 'Selection' in col else 'Bonus'}"
            # Rename the column
            selections_df.rename(columns={col: new_col_name}, inplace=True)
#print(selections_df.columns)
            
###Add players selections and bonus selections to dict
# Iterate over each row in selections_df
for index, row in selections_df.iterrows():
    event = row['Event']  # Get the event for this row
    event_id = event_id_mapping[event]  # Get the corresponding Event_ID

    for col in selections_df.columns[1:]:  # Exclude the 'Event' column
        if 'Selection' in col or 'Bonus' in col:  # Check if the column contains 'Selection' or 'Bonus'
            player_key = col.split(';')[0]  # Extract player key from column name
            selection_value = row[col]  # Get the selection value for this event

            # Update players_dict with the selection value referencing Event_ID
            players_dict[player_key].setdefault(event_id, {})
            if 'Selection' in col:
                players_dict[player_key][event_id]['Selection'] = selection_value
            elif 'Bonus' in col:
                players_dict[player_key][event_id]['Bonus'] = selection_value

#print(selections_df.columns)
#print(players_dict)

###
### Calculate number of correct tips for each event
###
# Iterate over each row in selections_df
for index, row in selections_df.iterrows():
    event = row['Event']  # Get the event for this row
    for col in selections_df.columns[1:]:  # Exclude the 'Event' column
        if 'Selection' in col:
            player_name = col.split(';')[0]  # Extract player name from column name
            player_selection = row[col]  # Get the player's selection for this event

            # Find the row in events_df corresponding to the event
            event_row = events_df[events_df['Event'] == event]

            # Check if the player's selection matches the actual result for the event
            if not event_row.empty and event_row.iloc[0]['Result'] == player_selection:
                # Increment 'Correct_Tips' for the corresponding event
                events_df.loc[event_row.index, 'Correct_Tips'] += 1

###
### Calculate Point_Share with conditional handling for division by zero
###
events_df['Point_Share'] = np.where(events_df['Correct_Tips'] != 0,
                                    points_per_event / events_df['Correct_Tips'],
                                    0)

###Allocate point share to each player for each event
# Iterate over each row in selections_df
for index, row in selections_df.iterrows():
    event_id = row['Event_ID']  # Get the event ID for this row
    for player_key, player_data in players_dict.items():
        #print(player_key)
        player_selection = player_data[event_id]['Selection']  # Get the player's selection for this event
        #print(player_selection)


        # Find the corresponding event in events_df
        event_row = events_df[events_df['Event_ID'] == event_id]

        # Check if the player's selection matches the actual result for the event
        if not event_row.empty and event_row.iloc[0]['Result'] == player_selection:
            # Increment 'points_tally' for the corresponding player and event
            players_dict[player_key]['correct_tips'] += 1
            players_dict[player_key]['points_tally'] += event_row.iloc[0]['Point_Share']

###Allocate bonus points for each player
# Iterate over each row in selections_df
for index, row in selections_df.iterrows():
    event_id = row['Event_ID']  # Get the event ID for this row
    for player_key, player_data in players_dict.items():
        player_selection = player_data[event_id]['Selection']  # Get the player's selection for this event
        player_bonus = player_data[event_id]['Bonus']  # Get the player's bonus selection for this event

        # Find the corresponding event in events_df
        event_row = events_df[events_df['Event_ID'] == event_id]

        # Check if the player's selection matches the actual result for the event
        if not event_row.empty and event_row.iloc[0]['Result'] == player_selection:
            # Check if the player's bonus selection matches the bonus for the event
            if event_row.iloc[0]['Bonus'] == player_bonus:
                # Add the bonus points to the player's bonus_points
                players_dict[player_key]['bonus_points'] += bonus_points_per_event
                players_dict[player_key]['points_tally'] += bonus_points_per_event


print(selections_df)
print(events_df)
#print(players_dict)

# Print player info
num_players = len(players_dict)
print("Number of players:", num_players)
for player_key, player_info in players_dict.items():
    print(f"Player Key: {player_key}")
    print(f"First Name: {player_info['first_name']}")
    print(f"Last Name: {player_info['last_name']}")
    print(f"Correct Tips: {player_info['correct_tips']}")
    print(f"Bonus Points: {player_info['bonus_points']}")
    print(f"Points Tally: {player_info['points_tally']}")
    print("-" * 20)  # Separator for clarity

# Save events_df and players_dict to JSON files
# Convert NaN to None
players_dict_cleaned = {}
for player_id, player_data in players_dict.items():
    player_data_cleaned = {}
    for event_id, event_data in player_data.items():
        if isinstance(event_data, dict):
            event_data_cleaned = {
                key: value if value == value else None  # Replace NaN with None
                for key, value in event_data.items()
            }
        else:
            event_data_cleaned = event_data  # Keep the original value if it's not a dictionary
        player_data_cleaned[event_id] = event_data_cleaned
    players_dict_cleaned[player_id] = player_data_cleaned

# Convert dictionary to JSON
players_json = json.dumps(players_dict_cleaned, indent=2)
# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Write JSON data to players_data.json file in the same directory
players_data_out_fp = os.path.join(current_dir, 'players_data.json')
with open(players_data_out_fp, 'w') as json_file:
    json_file.write(players_json)

print(f"Players data has been written to: {players_data_out_fp}")

events_data_out_fp = os.path.join(current_dir, 'events_data.json')
events_df.to_json(events_data_out_fp, orient='records')

print(f"Events data has been written to: {events_data_out_fp}")