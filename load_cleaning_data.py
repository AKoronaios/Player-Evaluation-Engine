import pandas as pd
import numpy as np

def clean_and_split_positions(position):
    # Split by commas and strip any leading/trailing whitespace
    positions = [pos.strip() for pos in position.split(',')]
    return positions


def add_parenthesis_number(value):
        # Split the string to get the main number
        main_number = int(value.split(' ')[0])  # Get the number before the space
        
        # Check if there's a parenthesis and extract the number if it exists
        if '(' in value and ')' in value:
            parenthesis_number = int(value.split('(')[1].split(')')[0])  # Extract the number inside parentheses
            return main_number + parenthesis_number
        else:
            return main_number  # Return just the main number if no parenthesis

def convert_positions_to_set(position_list):
    """
    Converts a list of position strings like ['AM (RL)', 'ST (C)']
    into a set of expanded roles like {'AMR', 'AML', 'STC'}.
    """
    role_set = set()

    if not isinstance(position_list, list):
        return role_set

    for pos in position_list:
        if not isinstance(pos, str):
            continue

        try:
            # Split into role and sides: "AM (RL)" → "AM", "RL"
            role, sides = pos.split(" (")
            sides = sides.strip(")").strip()  # remove trailing ")"

            for s in sides:
                role_set.add(f"{role.strip()}{s}")
        except ValueError:
            # If there's no side info like just "GK"
            role_set.add(pos.strip())

    return role_set

def compute_mean(value):
    """Process transfer values, handling 
    numerical text, ranges, and special cases."""
    
    if isinstance(value, (int, float)):
        return float(value)  # Directly convert numbers to float
    elif isinstance(value, str) and value.isdigit():
        return float(value)  # Convert pure numeric text to float
    elif isinstance(value, str) and '-' in value:
        try:
            lower, upper = map(int, value.split(' - '))  # Extract lower and upper values
            return (lower + upper) / 2  # Compute the mean
        except ValueError:
            return np.nan  # Handle unexpected formats
    else:
        return np.nan  # Replace other unknowns with NaN


def load_cleaning_data(data_path,free_agent_day='30/6/2026'):
    """
    Loads and cleans player data from an HTML source.
    
    This function reads tabular player data from an HTML file, extracts key attributes, 
    cleans inconsistencies in values, standardizes formats, and merges relevant data frames.

    Parameters:
        data_path (str): Path or URL to the HTML file containing player data.
        free_agent_day (str): Default contract expiration date for missing values (format 'DD/MM/YYYY').

    Returns:
        pd.DataFrame: A cleaned and structured DataFrame containing player attributes and statistics.
    """

    df = pd.read_html(data_path, encoding='utf-8',flavor='html5lib')
    df = df[0]
    df =df.drop(columns=['Inf','Rec'])
    df_names = df[['Name','Style','Nat','Personality', 'Club','Division']]
    df_stats = df[['Name','Position','Age','Height','Weight','Preferred Foot','Expires','Salary','Transfer Value','Apps','Mins','Mins/Gm','Av Rat','PoM','Distance',
'Dist/90','Poss Won/90','Poss Lost/90','Gwin','Pts/Gm','Tgls/90','Tcon/90','Gls','Gls/90','Conv %','Mins/Gl','Last Gl','xG','xG/90','xG-OP','NP-xG',
'NP-xG/90','Shots','Shot/90','xG/shot','ShT','ShT/90','Shot %','Shots Outside Box/90','Goals Outside Box','Pens','Pens S','Pen/R','Ast','Asts/90','xA',
'xA/90','Pas A','Ps A/90','Ps C','Ps C/90','Pas %','Pr Passes','Pr passes/90','K Pas','K Ps/90','OP-KP','OP-KP/90','CCC','Ch C/90','Cr A','Crs A/90',
'Cr C','Cr C/90','Cr C/A','OP-Crs A','OP-Crs A/90','OP-Crs C','OP-Crs C/90','OP-Cr %','Drb','Drb/90','FA','Off','Sprints/90','Tck A','Tck/90','Tck C',
'Tck R','K Tck','K Tck/90','Itc','Int/90','Blk','Blk/90','Shts Blckd','Shts Blckd/90','Clear','Clr/90','Fls','Yel','Red','Gl Mst','Hdrs A','Aer A/90',
'Hdrs','Hdrs W/90','Hdrs L/90','Hdr %','K Hdrs/90','Pres A','Pres A/90','Pres C','Pres C/90','Shutouts','Cln/90','Conc','All/90','Last C','xGP','xGP/90',
'Svh','Svp','Svt','Saves/90','Sv %','xSv %','Pens Faced','Pens Saved','Pens Saved Ratio']]
    df_names['Division'] = df_names['Division'].apply(str).str.replace('cinch','Scottish')
    
    # Setting the 'Style', 'Nat', 'Personality', 'Club', 'Division' as categorical type
    for column in ['Style', 'Nat', 'Personality', 'Club', 'Division']:
        df_names[column] = df_names[column].astype('category')
    
    # Remove leading/trailing whitespace from string-type columns
    df_stats = df_stats.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    
    # Replace missing values represented by '-' with '0'
    for column in df_stats.columns:
        if column not in ['Name','Position', 'Age', 'Height', 'Weight', 'Preferred Foot', 'Expires','Salary', 'Transfer Value']:
            df_stats[column] = df_stats[column].apply(str).str.replace('-','0')
    
    # Clean and convert 'Salary' column
    df_stats['Salary'] = df_stats['Salary'].apply(str).str.replace(r'\b[pP]/[aAmMwW]\b', '', regex=True)
    df_stats['Salary'] = df_stats['Salary'].apply(str).str.replace('nan','-')
    df_stats['Salary'] = df_stats['Salary'].apply(str).str.replace(',','')
    df_stats['Salary'] = df_stats['Salary'].apply(str).str.replace(r'[€$£]','',regex=True)
    df_stats['Salary'] = df_stats['Salary'].replace('-', 0).astype(int)
    
    # Clean and convert 'Transfer Value' column
    df_stats['Transfer Value'] = df_stats['Transfer Value'].apply(str).str.replace(r'[€$£]','',regex=True)
    df_stats['Transfer Value'] = df_stats['Transfer Value'].apply(str).str.replace('M','000000')
    df_stats['Transfer Value'] = df_stats['Transfer Value'].apply(str).str.replace('K','000')
    df_stats['Transfer Value'] = df_stats['Transfer Value'].replace('Unknown','np.nan')
    df_stats['Transfer Value'] = df_stats['Transfer Value'].replace('Not for Sale', 1_000_000_000)
    # Apply the function to compute means
    df_stats['Transfer Value'] = df_stats['Transfer Value'].apply(compute_mean)

    # Replace NaN values with the mean of known values
    avg_value = df_stats['Transfer Value'].mean()
    df_stats['Transfer Value'].fillna(avg_value, inplace=True)
    df_stats['Transfer Value'] = df_stats['Transfer Value'].fillna(0).astype(int)


    df_stats['Preferred Foot'] = df_stats['Preferred Foot'].astype('category')
    df_stats['Position'] = df_stats['Position'].apply(clean_and_split_positions)
    
    # Suming all the appears 
    df_stats['Apps'] = df_stats['Apps'].apply(add_parenthesis_number).astype(int)

    # Further cleaning for numerical columns
    for column in df_stats.columns:
        if column not in ['Name','Position', 'Age', 'Height', 'Weight', 'Preferred Foot', 'Expires','Salary', 'Transfer Value', 'Apps']:
            df_stats[column] = df_stats[column].apply(str).str.replace('-','0')
            df_stats[column] = df_stats[column].apply(str).str.replace('%','')
            df_stats[column] = df_stats[column].apply(str).str.replace('cm','')
            df_stats[column] = df_stats[column].apply(str).str.replace('km','')
            df_stats[column] = df_stats[column].astype(float)
            df_stats[column].fillna(0,inplace=True)
    
    # Convert 'Height' and 'Weight' columns to float        
    df_stats['Height'] = df_stats['Height'].apply(str).str.replace('m','').astype(float)
    df_stats['Weight'] = df_stats['Weight'].apply(str).str.replace('kg','').astype(float)
    
    # Standardize Expires contract day
    df_stats['Expires'] = df_stats['Expires'].apply(str).str.replace('-',free_agent_day)
    df_stats['Expires'] = pd.to_datetime(df_stats['Expires'], format='%d/%m/%Y')

    full_df = pd.merge(df_names, df_stats, on='Name', how='left')

    # Convert positions to set for better filtering
    full_df['Position'] = full_df['Position'].apply(convert_positions_to_set)
    
    return full_df    