import pandas as pd

def evaluate_players_by_position(df, stat_weights, inverse_stats=None):
    """
    Filters and evaluates players by position using stat_weights and optional inverse stats.

    Returns:
        pd.DataFrame: Players in that position sorted by Rating.
    """
    if inverse_stats is None:
        inverse_stats = []

    # Validate weights
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

    # Apply inverse logic
    for stat in inverse_stats:
        if stat in df_eval.columns:
            df_eval[stat] = -df_eval[stat]

    # Normalize and scale
    weighted_cols = []
    for stat, weight in stat_weights.items():
        weighted_col = stat + "_weighted"
        df_eval[weighted_col] = df_eval[stat] * weight
        weighted_cols.append(weighted_col)
    
    # Compute the rating as a weighted average.
    # (Sum of weighted stats divided by the sum of weights) multiplied by 100.
    df_eval['Rating'] = df_eval[weighted_cols].sum(axis=1) / sum(stat_weights.values()) * 100

    return df_eval[['Name', 'Club', 'Age', 'Position', 'Rating'] + list(stat_weights.keys())]\
        .sort_values(by='Rating', ascending=False).reset_index(drop=True)
