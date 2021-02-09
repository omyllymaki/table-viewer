import pandas as pd


def load_data(file_paths, args):
    df_list = []
    for path in file_paths:
        df = pd.read_csv(path,
                         sep=args.separator,
                         header=args.header,
                         decimal=args.decimal,
                         parse_dates=args.datetime,
                         infer_datetime_format=True)
        df_list.append(df)
    data = pd.concat(df_list)
    return data
