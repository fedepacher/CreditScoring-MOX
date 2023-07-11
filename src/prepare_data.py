"""Prepara data to train the model"""
from utils import CustomLogging, notebook_wrapper


if __name__ == '__main__':
    logging = CustomLogging()
    logger = logging.get_logger()

    logger.info('Fetching data...')

    FILE_NAME = 'etl_process_plus_target'
    # Run script
    exec(notebook_wrapper(file_name=FILE_NAME, logger=logger))
    logger.info('Data Fetched and prepared...')
