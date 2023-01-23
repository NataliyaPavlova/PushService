from etl_logs.src.extractor import Extractor
from etl_logs.src.loader import Loader
from etl_logs.settings import get_settings
from etl_logs.logger import get_logger

settings = get_settings()
logger = get_logger(settings.log_filename)


async def make_etl() -> None:
    logger.info('ETL process started: from OneSignal to ClickHouse.')

    extractor = Extractor().get_data()
    loader = Loader()

    while True:
        try:
            data_to_load, batch_info, push_tokens = await anext(extractor)
            if data_to_load:
                await loader.load_data(data_to_load, batch_info, push_tokens)
                logger.info(f'Inserted next batch {batch_info.notification_id} to Clickhouse')
        except StopAsyncIteration:
            logger.info(f'No new batches in DB')
            break
        except Exception as e:
            logger.error(f'ETL exception: {e}')
    logger.info('ETL process closed.')
