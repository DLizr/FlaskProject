from src.Server import Server
from src.util.Logger import LogFormatter, logger


if __name__ == "__main__":
    LogFormatter.debugMode(True)
    Server.run(__file__)
