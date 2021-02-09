import re

import numpy as np
import pandas as pd
from pandas.core.dtypes.common import is_string_dtype


def filter_by_query(df: pd.DataFrame, query: str) -> pd.DataFrame:
    """
    Query syntax:
    [col1, col2]: search from col1 and col2.
    &&: logical and, returns intersection.
    ||: logical or, returns union.

    [col1, col2] regxp1 && regxp2 || [col3] regexp3

    means that

    search regexp1 pattern from col1 and col2
    AND
    search regexp2 from every column
    OR
    search regexp3 pattern from col3
    """

    if not query:
        return df

    all_cols = df.columns.tolist()

    operators_pattern = "&&|\|\|"  # && or ||
    sub_queries = re.split(operators_pattern, query)
    logical_operators = [None] + re.findall(operators_pattern, query)

    boolean_vectors = []
    search_pattern = None
    for sub_query in sub_queries:
        sub_terms = sub_query.split()
        column_candidates = []
        for term in sub_terms:
            is_column_name = term.startswith("[") and term.endswith("]")
            if is_column_name:
                column_candidates += [s.strip() for s in term[1:-1].split(",")]
            else:
                search_pattern = term.strip()

        if len(column_candidates) == 0:
            cols = all_cols
        else:
            cols = []
            for cc in column_candidates:
                if cc in all_cols:
                    cols.append(cc)
                else:
                    raise Exception(f"{cc} is not a valid column. Please modify query.")

        mask = np.column_stack([df[col].str.contains(search_pattern, na=False, flags=re.IGNORECASE)
                                for col in cols
                                if is_string_dtype(df[col])])

        boolean_vector = mask.any(axis=1)
        boolean_vectors.append(boolean_vector)

    is_match = None
    for boolean_vector, operation in zip(boolean_vectors, logical_operators):
        if operation is None:
            is_match = boolean_vector
        else:
            if operation == "||":
                is_match = is_match | boolean_vector
            elif operation == "&&":
                is_match = is_match & boolean_vector
            else:
                raise Exception(f"Unknown logical operator: {operation}")

    df_filtered = df[is_match]
    return df_filtered
