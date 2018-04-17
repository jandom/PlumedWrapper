import pandas as pd

def get_crossings(df, barrier, column='x'):
    df = get_velocities(df, barrier, column)

    # Select only the crossing times
    df = df[df['crossing'] == True]
    return df

def get_velocities(df, barrier, column='x'):
    """
    Get a dataframe with a TPS trajectory (backward or forward), and a barrier (float) along a column (default: drms), and get crossing times
    """

    df = df[['time', column]]
    df = df[df.time != 0.0]

    # Generate a column for the CV value at the next step (detect barrier crossings)
    next_column = 'next_{}'.format(column)
    df[next_column] = df[column].shift(-1)

    # Generate a next time
    df['next_time'] = df['time'].shift(-1)

    # Last row will contain NaNs
    df = df[:-1]

    # Pick out crossing times
    df['crossing'] = (
        ((df[column] >= barrier) & (df[next_column] < barrier)) |
        ((df[next_column] > barrier) & (df[column] <= barrier))
    )

    # Compute the velocities
    df['velocity'] = (df[next_column] - df[column]) / (df['next_time'] - df['time']) # ps, 1000 x timestep

    return df
