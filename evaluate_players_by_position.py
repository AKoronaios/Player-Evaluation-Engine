import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Define the inverse stas list
inverse_stats = [
    'Dist/90', 'Poss Lost/90', 'Tcon/90', 'Mins/Gl', 'Last Gl', 'Off', 'FA', 
    'Fls', 'Yel', 'Red', 'Conc', 'All/90', 'Last C']

#Define scaler
scaler = MinMaxScaler(feature_range=(0,100))


def evaluate_players_by_position(df, stat_weights):
    """
    Filters and evaluates players by position using stat_weights and optional inverse stats.

    Inputs:
        df: the filtered pd.DataFrame
        stat_weights: a dict with the stats and their correnspoding weight 

    Returns:
        pd.DataFrame: Players in that position sorted by Rating.
    """
    

    # Validate weights <- Maybe this check is not useless, already checked
    for stat, weight in stat_weights.items():
        if weight <= 0:
            raise ValueError(f"Weight for stat '{stat}' must be > 0.")
        if stat not in df.columns:
            raise ValueError(f"Stat '{stat}' not in DataFrame.")
        if not pd.api.types.is_numeric_dtype(df[stat]):
            raise TypeError(f"Stat '{stat}' must be numeric.")

    # Filter by position in set
    df_eval = df.copy()

    if df_eval.empty:
        return pd.DataFrame()  # No players found

    # Create weifhted columns
    weighted_cols = []
    for stat, weight in stat_weights.items():
        weighted_col = stat + "_weighted"

        # Apply inverse logic if the stat is in the inverse_stats list
        if stat in inverse_stats:
            df_eval[weighted_col] = - df_eval[stat] * weight
        else:
            df_eval[weighted_col] = df_eval[stat] * weight

        weighted_cols.append(weighted_col)
    
    # Compute the rating as a weighted average.
    raw_rating = df_eval[weighted_cols].sum(axis=1) / sum(stat_weights.values()) * 100

    df_eval['Rating'] = scaler.fit_transform(raw_rating.values.reshape(-1,1))

    return df_eval[['Name', 'Club', 'Age', 'Position', 'Rating'] + list(stat_weights.keys())]\
        .sort_values(by='Rating', ascending=False).reset_index(drop=True)
