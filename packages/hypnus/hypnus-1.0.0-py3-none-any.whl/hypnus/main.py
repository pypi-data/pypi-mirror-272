#!/usr/bin/python
import logging
import sys

from hypnus import power, tempo

_logger = logging.getLogger(__name__)


def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    day_color = tempo.get_todays_tempo_color()

    _logger.info("Today is a %s day", day_color.name)

    if day_color is tempo.TempoDayColor.RED:
        _logger.info("Shutting down computer")
        power.shutdown()


if __name__ == "__main__":
    main()
