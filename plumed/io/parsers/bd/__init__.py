
import pandas as pd

def callback(df, basinA, basinB, column='x'):
    v = df[column].values[-1]
    if v <= basinA: return "A"
    if v >= basinB: return "B"
    return None

def read_commitorrs(trajectories, basinA, basinB):
    return { k: callback(df, basinA, basinB) for k, df in trajectories.items()}

def read_trajectories(files):
    # Read the trajectory data, each trajectory as a pd.DataFrame
    return {f: pd.read_fwf(f, names=["time", "x"]) for f in files}
