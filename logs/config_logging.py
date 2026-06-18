import logging

def config():
    logging.basicConfig(
        filename="logs/app.log",
        format= '%(asctime)s  %(levelname)s %(message)s',
        level=20

    )

