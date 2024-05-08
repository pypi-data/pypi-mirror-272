from __future__ import annotations
import re
import nltk
import pandas as pd

_STOPWORDS = set(nltk.corpus.stopwords.words('english'))
_COMMON_TOKENS = {
    'Lead',
    'Assistant',
    'Chief',
    'Associate',
    'Principal',
    'Specialist',
    'Officer',
    'Analyst',
    'Sr',
    'Special',
    'Senior',
    'Development',
    'Team',
}


_SENIOR = frozenset(
    {
        'Sr',
        'Advisor',
        'Director',
        'President',
        'Senior',
        'Chief',
        'Special',
        'Lead',
        'Principal',
        'Officer',
    }
)


_STOPTOKENS = _COMMON_TOKENS | _STOPWORDS


def handcrafted_map(job_code: pd.Series[str]) -> pd.DataFrame:
    return job_code.loc[~job_code.duplicated()].pipe(_build_features)


def _build_features(job_code: pd.Series[str]) -> pd.DataFrame:
    norm = job_code.apply(_norm_title)
    return pd.DataFrame(
        {
            'JOB_CODE_DESCR': job_code,
            '_job_descr': norm.apply(remove_stop_tokens).replace('', '<Other>'),
            'is_senior': norm.apply(_is_senior),
        },
    ).set_index(job_code.name)


def _norm_title(title: str | None) -> str:
    if not isinstance(title, str):
        return ''
    clean = re.sub(r'\.|-|&|/|,\s{2,}', ' ', title)
    # primarily cleans up `Contractor: xxx` titles
    mat = re.search(r'([\w ]+):?', clean)
    assert mat, (title, mat)
    return mat.group(1).strip()


def remove_stop_tokens(title: str) -> str:
    return ' '.join(_s for _s in title.split() if _s not in _STOPTOKENS)


def _is_senior(s: str) -> bool:
    intersect = set(s.split()) & _SENIOR
    return len(intersect) > 0
