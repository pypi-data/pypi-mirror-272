from os import PathLike

import pandas as pd

from .data_models import Mdoc


def read(filename: PathLike) -> pd.DataFrame:
    """Read an mdoc file as a pandas dataframe.

    Parameters
    ----------
    filename : PathLike
        SerialEM mdoc file to read

    Returns
    -------
    df : pd.DataFrame
        dataframe containing info from mdoc file
    """
    mdoc = Mdoc.from_file(filename)
    global_data = mdoc.global_data.model_dump()
    section_data = {
        k: [section.model_dump()[k] for section in mdoc.section_data]
        for k
        in mdoc.section_data[0].model_dump().keys()
    }
    df = pd.DataFrame(data=section_data)

    # add duplicate copies of global data and mdoc file titles to each row of
    # the dataframe - tidy data is easier to analyse
    for k, v in global_data.items():
        df[k] = [v] * len(df)
    df['titles'] = [mdoc.titles] * len(df)
    df = df.dropna(axis='columns', how='all')
    return df
