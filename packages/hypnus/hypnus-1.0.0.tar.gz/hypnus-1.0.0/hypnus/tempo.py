import enum
import json
import urllib.request
from typing import TypedDict

_TEMPO_API_BASE_URL = "https://www.api-couleur-tempo.fr"


class _TempoDayInformation(TypedDict):
    dateJour: str
    codeJour: int
    periode: str


class TempoDayColor(enum.IntEnum):
    BLUE = 1
    WHITE = 2
    RED = 3


def get_todays_tempo_color() -> TempoDayColor:
    """Fetches and returns today's EDF Tempo day color.

    Returns:
        Today's EDF Tempo day color enum.
    """
    # NOTE: URL is built from hardcoded string
    with urllib.request.urlopen(  # noqa: S310
        f"{_TEMPO_API_BASE_URL}/api/jourTempo/today",
    ) as response:
        tempo_day_information: _TempoDayInformation = json.load(response)

        return TempoDayColor(tempo_day_information["codeJour"])
