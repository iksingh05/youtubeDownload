import logging

def configure_logging():
    # Set up logging configuration
    logging.basicConfig(level=logging.INFO, filename='./app.log', format='%(asctime)s - %(levelname)s - %(message)s')
