import os
import pandas as pd


def clean(DirPath):
    ls = []
    if not os.path.exists(DirPath) or not os.path.isdir(DirPath): 
        print("Директорії не існує ")
    else:
        files = os.listdir(DirPath)
        for i, file in enumerate(files):
            if file.endswith(".csv"):
                FilePath = os.path.join(DirPath, file)
                df = pd.read_csv(FilePath, index_col=False, header=1)
                df["ID"] = i + 1
                ls.append(df)
        df = pd.concat(ls).drop_duplicates().reset_index(drop=True)
    df = df.rename(columns={" VHI<br>": "VHI"})
    df[" SMN"] = df[" SMN"].astype(str).str.strip()
    df["year"].replace({"<tt><pre>1982": "1982"}, inplace=True)
    df = df.drop(df.loc[df["VHI"] == -1].index)
    df = df.drop(df.index[-1])

    df["year"]= pd.to_numeric(df["year"], errors="coerce")
    print(df.columns)
    return df

def nwid(df):
    newid = {
        1: 22,
        2: 24,
        3: 23,
        4: 25,
        5: 3,
        6: 4,
        7: 8,
        8: 19,
        9: 20,
        10: 21,
        11: 9,
        13: 10,
        14: 11,
        15: 12,
        16: 13,
        17: 14,
        18: 15,
        19: 16,
        21: 17,
        22: 18,
        23: 6,
        24: 1,
        25: 2,
        26: 7,
        27: 5,
    } 
    df["ID"].replace(newid, inplace=True)
    return(df)
DirPath = "csv_data"
if __name__ == "__main__":       
    nwid(clean(DirPath))         
