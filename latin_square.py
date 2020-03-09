import os
from itertools import cycle

import pandas as pd


def read_multi_ext(file, extension=None):
    """Read csv, xlsx, and txt files and returns a pandas DataFrame.

    Arguments:
        file {str} -- File to read in

    Keyword Arguments:
        extension {str} -- Extension of the file; inferred if None (default: {None})

    Returns:
        df -- pandas DataFrame
    """
    if extension == None:
        _, extension = os.path.splitext(file)
    if extension == ".csv":
        df = pd.read_csv(file, sep=";")
    elif extension == ".xlsx":
        df = pd.read_excel(file)
    elif extension == ".txt":
        df = pd.read_table(file)
    return df


def save_multi_ext(df, file, extension=None):
    """Save a pandas DataFrame, depending on extension used in outname or given explicitly.

    Arguments:
        df {df} -- pandas DataFrame to save
        file {str} -- Name of the saved file

    Keyword Arguments:
        extension {str} -- Extension of the file; inferred if None (default: {None})
    """
    if extension == None:
        _, extension = os.path.splitext(file)
    if extension == ".csv":
        df.to_csv(file, sep=';', index=False)
    elif extension == ".xlsx":
        df.to_excel(file, sheet_name='Sheet1', index=False)
    elif extension == ".txt":
        df.to_table(file, index=False)


def reorder_columns(df, item_col, sub_exp_col, item_number_col, cond_col):
    """Reorder the columns of a data frame such that the most important ones are at the beginning; unnamed columns are appended at the right edge. Return reordered df.

    Arguments:
        df {[type]} -- pandas Dataframe
        item_col {str} -- Column with the item text
        sub_exp_col {str} -- Column containing the subexperiment identifier
        item_number_col {str} -- Column with the item number
        cond_col {str} -- Column containing the condition identifiers

    Returns:
        [type] -- [description]
    """
    # reorder the most important columns
    col_order = [item_col, sub_exp_col,
                 item_number_col, cond_col]
    # and just add the remaining columns (if any)
    new_cols = col_order + (df.columns.drop(col_order).tolist())
    return df[new_cols]


def check_permutations(df, item_number_col, cond_col, conditions):
    """Check if all combinations of items and conditions are present in the data. Raise exception if not.

    Arguments:
        df {[type]} -- pandas Dataframe with all conditions for each item
        item_number_col {str} -- Column with the item number (default: {"item_number"})
        cond_col {str} -- Column containing the condition identifiers (default: {"cond"})
        conditions {list} -- List of conditions
    Raises:
        Exception: Not all permutations present; lists which ones
    """
    # do a cartesian product of item numbers and conditions
    products = [(item, cond) for item in set(df[item_number_col])
                for cond in conditions]
    # check if all such products exist in the dataframe
    check_list = [((df[item_number_col] == item)
                   & (df[cond_col] == cond)).any() for item, cond in products]
    # if they are not all there, raise an error and show which combos are missing
    if not all(check_list):
        # get missing combinations
        missing_combos = ', '.join([''.join(map(str, product)) for product, boolean in zip(
            products, check_list) if not boolean])
        raise Exception(
            f"Not all permutations of items and conditions are present in the dataframe. Missing combinations: {missing_combos}")


def to_latin_square(df, outname, sub_exp_col="sub_exp", cond_col="cond", item_col="item", item_number_col="item_number"):
    """Take a dataframe with all conditions and restructure it with Latin Square. Saves the files.

    Arguments:
        df {df} -- pandas Dataframe with all conditions for each item
        outname {str} -- Name for the saved files (uniqueness handled automatically); include extension

    Keyword Arguments:
        sub_exp_col {str} -- Column containing the subexperiment identifier (default: {"sub_exp"})
        cond_col {str} -- Column containing the condition identifiers (default: {"cond"})
        item_col {str} -- Column with the item text (default: {"item"})
        item_number_col {str} -- Column with the item number (default: {"item_number"})
    """
    dfs_critical = []
    dfs_filler = []
    name, extension = os.path.splitext(outname)
    # split the dataframe by the sub experiment value
    dfs = [pd.DataFrame(x) for _, x in df.groupby(
        sub_exp_col, as_index=False)]
    for frame in dfs:
        # get the unique condition values and sort them
        conditions = sorted(list(set(frame[cond_col])))

        # check whether all combos of items and conditions are present
        check_permutations(frame, item_number_col, cond_col, conditions)

        # for filler dfs, just reorder the columns
        if len(conditions) == 1:
            frame = reorder_columns(
                frame, item_col, sub_exp_col, item_number_col, cond_col)
            # and add them to the correct list
            dfs_filler.append(frame)
        # for critical sub experiments generate the appropriate amount of lists
        else:
            for k in range(len(conditions)):
                # order the conditions to match the list being created
                lat_conditions = conditions[k:] + conditions[:k]
                # generate (and on subsequent runs reset) the new df with all the columns in the argument df
                out_df = pd.DataFrame(columns=frame.columns)
                # look for the appriate rows in the argument df (using the conditions multiple times with 'cycle')
                out_l = []
                for item, cond in zip(set(sorted(frame[item_number_col])), cycle(lat_conditions)):
                    out_l.append(frame[frame.item_number.eq(
                        item) & frame.cond.eq(cond)])
                out_df = pd.concat(out_l)
                # reorder the most important columns
                out_df = reorder_columns(
                    out_df, item_col, sub_exp_col, item_number_col, cond_col)
                dfs_critical.append(out_df)

    # add the fillers to the critical lists
    for i, df in enumerate(dfs_critical):
        dfs_critical[i] = pd.concat([df, *dfs_filler])
        save_multi_ext(df, f"{name}{i+1}{extension}")


if __name__ == "__main__":
    infile = os.path.join("data", "multi.txt")

    # this one should fail because of the permutation check
    # infile = os.path.join("data", "multi_exception.txt")

    df = read_multi_ext(infile)

    outfile = os.path.join("latin_squared", "final.csv")
    to_latin_square(df, outfile)
