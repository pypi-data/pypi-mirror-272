from __future__ import annotations
import functools as ft
from collections.abc import (
    Mapping,
    Sequence,
)
from dataclasses import (
    asdict,
    dataclass,
)
from pathlib import Path
from typing import (
    Final,
    overload,
)
import pandas as pd

import yaml

from . import (
    edc,
    query,
)
from .query import BaseStaff

OUI: Final = 10020
_DATASET = edc.Dataset.AA


@dataclass(frozen=True, kw_only=True)
class Staff(BaseStaff):
    """AA Staff data."""

    code: str | None
    nickname: str | None

    @classmethod
    def from_staff(cls, staff: BaseStaff, details: Details) -> Staff:
        return Staff(**asdict(staff), **asdict(details))

    @classmethod
    @overload
    def from_code(cls, code: str) -> Staff:
        """Return staff from staff code."""

    @classmethod
    @overload
    def from_code(cls, code: Sequence[str]) -> Sequence[Staff]:
        """Return staff Sequence from staff codes."""

    @classmethod
    def from_code(cls, code: str | Sequence[str]) -> Staff | Sequence[Staff]:
        is_scalar = isinstance(code, str)
        codes = (code,) if is_scalar else code

        details = staff_details()
        upi = tuple(upi_from_code(_code, details) for _code in map(str.upper, codes))
        staff = tuple(query.by_upi(upi, _DATASET))

        staff_list = tuple(
            cls.from_staff(_staff, details.get(_staff.upi, Details(code=None)))
            for _staff in staff
        )

        if is_scalar:
            return staff_list[0]
        return staff_list

    @classmethod
    @overload
    def from_upi(cls, upi: int) -> Staff:
        """Return staff from upi."""

    @classmethod
    @overload
    def from_upi(cls, upi: Sequence[int]) -> Sequence[Staff]:
        """Return staff Sequence from upis."""

    @classmethod
    def from_upi(cls, upi: int | Sequence[int]) -> Staff | Sequence[Staff]:
        is_scalar = isinstance(upi, int)
        upis = (upi,) if is_scalar else upi

        staff = tuple(query.by_upi(upis, _DATASET))
        if len(staff) != len(upis):
            raise ValueError("Invalid upi passed!")

        staff_list = tuple(
            cls.from_staff(_staff, staff_details().get(_staff.upi, Details(code=None)))
            for _staff in staff
        )

        if is_scalar:
            return staff_list[0]
        return staff_list

    @classmethod
    def from_first_name(cls, name: str) -> Staff:
        aa_staff = get_staff()
        cmp_name = name.lower().strip()

        # Dirty, but need to avoid ambiguity with Junaid
        if cmp_name == "mohammad":
            return aa_staff[553290]

        for staff in aa_staff.values():
            # Handle first name with two words (`Nicola Maria`)
            first_name = _real_first_name(staff.first_name)
            if first_name.lower() == cmp_name:
                break
            if staff.name.lower() == cmp_name:
                break
        else:
            raise ValueError(f"Invalid name: `{name}` passed")

        return staff

    @classmethod
    def from_name(cls, name: str) -> Staff:
        aa_staff = get_staff()
        cmp_name = name.lower().strip()
        for staff in aa_staff.values():
            if staff.full_name.lower() == cmp_name:
                return staff
        raise ValueError(f"Invalid name: `{name}` passed")

    @property
    def name(self) -> str:
        return self.nickname if self.nickname is not None else self.first_name


def _real_first_name(first_name: str) -> str:
    """Return first word in name if multiple words in name."""
    if " " in first_name:
        return first_name.split()[0]
    return first_name


@ft.total_ordering
@dataclass(frozen=True, kw_only=True)
class Details:
    code: str | None = None
    nickname: str | None = None

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Details):
            raise NotImplementedError("Can only compare with Details objects.")

        return self.code < other.code if self.code and other.code else False


@overload
def get_staff(*, upi: int) -> Staff:
    """Return staff from upi."""


@overload
def get_staff(*, upi: Sequence[int]) -> Sequence[Staff]:
    """Return staff Sequence from upi."""


@overload
def get_staff(*, code: str) -> Staff:
    """Return staff from staff code."""


@overload
def get_staff(*, code: Sequence[str]) -> Sequence[Staff]:
    """Return staff Sequence from staff codes."""


@overload
def get_staff(*, first_name: str) -> Staff:
    """Return staff from first name/nickname."""


@overload
def get_staff(*, name: str) -> Staff:
    """Return staff from full name."""


@overload
def get_staff() -> dict[int, Staff]:
    """Return upi-Staff mapping for AA."""


def get_staff(
    *,
    upi: int | Sequence[int] | None = None,
    code: str | Sequence[str] | None = None,
    first_name: str | None = None,
    name: str | None = None,
) -> dict[int, Staff] | Sequence[Staff] | Staff:
    """Returns AA staff instance(s).

    Parameters
    ----------
    upi : int | Sequence[int] | None, optional
        UPI of staff, by default None
    code : str | Sequence[str] | None, optional
        AA staff code, by default None
    first_name : str | None, optional
        first_name, by default None
    name : str | None, optional
        full name, by default None

    Returns
    -------
    dict[int, Staff] | Sequence[Staff] | Staff
        Sequence of staff instances
    """
    if upi is not None:
        return Staff.from_upi(upi)
    if code is not None:
        return Staff.from_code(code)
    if first_name is not None:
        return Staff.from_first_name(first_name)
    if name is not None:
        return Staff.from_name(name)

    details = staff_details()
    aa_staff = {
        staff.upi: Staff.from_staff(staff, details.get(staff.upi, Details(code=None)))
        for staff in query.by_oui([OUI], _DATASET)
    }

    return aa_staff


def active_staff() -> Mapping[int, Staff]:
    """Returns all active AA staff.

    Assumes the STAFF_LOCATOR table is updated."""
    _active = query.by_oui([10020], edc.Dataset.STAFF_LOCATOR)
    _active_upis = {staff.upi for staff in _active}

    all_staff = get_staff()
    return {upi: staff for upi, staff in all_staff.items() if upi in _active_upis}


_DETAILS_FP = Path(__file__).parent.joinpath("aa-staff.yaml")


def staff_details(
    filepath: Path = Path(__file__).parent.joinpath("aa-staff.yaml"),
) -> dict[int, Details]:
    """Return staff codes/nicknames."""
    with open(filepath) as fp:
        raw_details = yaml.safe_load(fp)
    return {upi: Details(**details) for upi, details in raw_details.items()}


def _add_staff_detail(upi: int, code: str, nickname: str | None = None) -> None:
    details = staff_details() | {upi: Details(code=code, nickname=nickname)}

    added = {
        upi: _detail_to_dict(detail)
        for upi, detail in sorted(details.items(), key=lambda item: item[1])
    }

    _write_details(added)


def _update_details(staff: dict[str, Staff]) -> None:
    details = staff_details()
    extra = details.keys() - staff.keys()

    active = {
        upi: _detail_to_dict(detail)
        for upi, detail in details.items()
        if upi not in extra
    }

    _write_details(active)


def _detail_to_dict(detail: Details) -> dict[str, str]:
    return {k: v for k, v in asdict(detail).items() if v is not None}


def _write_details(details: dict[int, dict[str, str]]) -> None:
    with open(_DETAILS_FP, "w") as fp:
        yaml.dump(details, fp, sort_keys=False)


def upi_from_code(
    staff_code: str, details: dict[int, Details] = staff_details()
) -> int:
    for upi, detail in details.items():
        if detail.code == staff_code.upper():
            return upi
    raise ValueError(f"Invalid staff code: `{staff_code}`")


def code_from_upi(
    upi: int, details: dict[int, Details] = staff_details()
) -> str | None:
    if upi not in get_staff():
        raise ValueError(f"Invalid aa UPI: `{upi}` passed")
    if upi not in details:
        return None
    return details[upi].code


def code_from_name(name: str) -> str | None:
    return get_staff(first_name=name).code


def from_staff_locator(df: pd.DataFrame) -> pd.DataFrame:
    """Subset AA staff from WBG staff."""
    return df.loc[df[edc.RAW_HEADERS.work_oui] == OUI]


def stc() -> frozenset[int]:
    """Return STC's in AA."""
    return frozenset(upi for upi in get_staff() if query.is_stc(upi))
