from collections import namedtuple

import pandas as pd
from dynaconf.utils.boxing import DynaBox
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine


def connect(urls: dict | DynaBox) -> namedtuple:
    return namedtuple('Database', urls.keys())(
        *[create_engine(url) for url in urls.values()]
    )


def query(
    engine: Engine,
    stmt: str,
    params: dict | list[dict] = None,
    fetch: bool = True,
    as_dict: bool = False,
    index_col: str | list[str] | None = None,
) -> None | list[dict] | pd.DataFrame:
    if fetch:
        result = pd.read_sql(
            text(stmt),
            engine,
            params=params,
            index_col=index_col,
            coerce_float=True
        )
        if as_dict:
            result = result.to_dict(orient='records')
            if len(result) == 1:
                result = result[0]
            elif len(result) == 0:
                return {}
        return result
    else:
        with engine.connect() as conn:
            conn.execute(text(stmt), params)
            conn.commit()
