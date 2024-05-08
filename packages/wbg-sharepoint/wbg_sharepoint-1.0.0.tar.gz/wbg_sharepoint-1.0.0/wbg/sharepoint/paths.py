import enum
import os
import urllib
from pathlib import Path
import typing


URL = typing.NewType('URL', str)

_USER_ROOT = Path(os.environ['USERPROFILE'])


def _aa_team(root: Path) -> Path:
    first_path = 'AskAccounting - WB - Documents'
    second_path = 'AskAccounting - Documents'
    first = root.joinpath('WBG', first_path)
    if not first.exists():
        first = root.joinpath('WBG', second_path)
    assert first.exists()
    return first


_WFA_CORPEX = _USER_ROOT.joinpath('WBG/WFA CorpExp Files - AskAccounting')
_AA_TEAM = _aa_team(_USER_ROOT)
_BASE_AA_TEAM_URL = 'https://worldbankgroup.sharepoint.com/teams/askaccounting-wbgroup/Shared%20Documents/Forms/AllItems.aspx'
_AA_TEAM_URL = (
    _BASE_AA_TEAM_URL + '?id=%2Fteams%2Faskaccounting%2Dwbgroup%2FShared%20Documents'
)


class Paths(enum.Enum):
    WFA_CORPEX = _WFA_CORPEX
    PROJS = _AA_TEAM.joinpath('projs')
    SHIV = _WFA_CORPEX.joinpath('Shiv')
    QUEUING = _WFA_CORPEX.joinpath('Queuing')


def construct_url(url: str, path_: str) -> URL:
    """Return URL encoded path."""
    return url + urllib.parse.quote_plus('/' + path_)


class WebURL(enum.StrEnum):
    """URL for sharepoint files/folders."""

    AA_TEAM_DOCS = _AA_TEAM_URL
    PROJS = construct_url(_AA_TEAM_URL, 'projs')
    CL_MAINTENANCE = construct_url(_AA_TEAM_URL, 'projs/credit-limit-maintenance')
