import threading
import time

import pandas as pd

from backend.db import ENGINE
from backend.logs import create_logger

LOGGER = create_logger(__name__)


def _return_money(df: pd.DataFrame):
    for _, refund in df.iterrows():
        LOGGER.warning(f"Refund for {refund.to_dict()}")


def worker():
    while True:
        df = pd.read_sql(
            sql=f"""
        SELECT * FROM users.users_with_events
        """,
            con=ENGINE(),
        )
        last_expired_mask = df["last_date"] < pd.Timestamp.now()
        was_not_build = df["has_built"] == False

        bad_buildings = df[last_expired_mask & was_not_build]
        if not bad_buildings.empty:
            _return_money(bad_buildings)

        time.sleep(10)


def serve():
    thread = threading.Thread(target=worker, name="Serve auto-refund")
    thread.start()
    return thread


if __name__ == "__main__":
    serve()
