import re

import numpy as np
import pandas as pd
from pandas.core.dtypes.common import is_string_dtype


def filter_by_query(df: pd.DataFrame, query: str) -> pd.DataFrame:
    """
    Example queries:

    query = tampere
    Search "tampere" from all columns
    
    query = fin*
    Search "fin*" from all columns

    query = [Lives, Born] tampere
    Search "tampere" from columns Lives and Born

    query = [Lives, Born] tampere | [Nationality] finland
    Search "tampere" from columns Lives and Born or "finland" from column Nationality; return union.

    query = "[Lives, Born] tampere & [Nationality] finland"
    Search "tampere" from columns Lives and Born and "finland" from column Nationality; return interception.

    """

    if not query:
        return df

    all_cols = df.columns.tolist()

    operators_pattern = "&|\|"
    splitted = re.split(operators_pattern, query)
    operators = re.findall(operators_pattern, query)
    operators = [None] + operators

    boolean_vectors = []
    pattern = None
    for operation, term in zip(operators, splitted):
        sub_terms = term.split()
        col_candidates = []
        for t in sub_terms:
            if t.startswith("[") and t.endswith("]"):
                col_candidates += [s.strip() for s in t[1:-1].split(",")]
            else:
                pattern = t.strip()

        if len(col_candidates) == 0:
            cols = all_cols
        else:
            cols = []
            for cc in col_candidates:
                if cc in all_cols:
                    cols.append(cc)
                else:
                    raise Exception(f"{cc} is not a valid column")

        mask = np.column_stack([df[col].str.contains(pattern, na=False, flags=re.IGNORECASE)
                                for col in cols
                                if is_string_dtype(df[col])])

        boolean_vector = mask.any(axis=1)
        boolean_vectors.append(boolean_vector)

    is_match = None
    for b, operation in zip(boolean_vectors, operators):
        if operation is None:
            is_match = b
        else:
            if operation == "|":
                is_match = is_match | b
            elif operation == "&":
                is_match = is_match & b
            else:
                raise Exception(f"Unknown operation: {operation}")

    df_filtered = df[is_match]
    return df_filtered
