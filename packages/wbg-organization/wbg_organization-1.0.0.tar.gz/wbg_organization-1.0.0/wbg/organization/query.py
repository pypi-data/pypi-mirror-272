"""Base WBG data querying facility."""
from __future__ import annotations
import sqlite3
from collections.abc import (
    Iterable,
    Sequence,
)
from dataclasses import (
    dataclass,
    fields,
    asdict,
)
from typing import TypedDict

import pandas as pd

from . import edc
from .edc import RAW_HEADERS as RAW


@dataclass(frozen=True, kw_only=True)
class BaseStaff:
    """Base WBG Staff details."""

    upi: int
    email: str
    first_name: str
    middle_name: str | None
    last_name: str

    @classmethod
    @property
    def keys(cls) -> Iterable[str]:
        """Return attributes of class."""
        return tuple(attr.name for attr in fields(cls))

    @property
    def full_name(self) -> str:
        """Return full name of staff."""
        if self.middle_name is None:
            return f"{self.first_name} {self.last_name}"
        return f"{self.first_name} {self.middle_name} {self.last_name}"


def by_upi(upi: Sequence[int], dataset: edc.Dataset) -> Iterable[BaseStaff]:
    """Return staff from upi."""
    query = f"""
    {_select_query(dataset)}
    WHERE {RAW.upi} IN ({_placeholders(upi)})"""
    cur = _get_cursor()
    cur.execute(query, upi)

    return _exec_query(query, upi)


def by_oui(oui: Sequence[int], dataset: edc.Dataset) -> Iterable[BaseStaff]:
    """Return staff by OUI (unit)."""
    query = f"""
    {_select_query(dataset)}
    WHERE {RAW.work_oui} IN ({_placeholders(oui)})
    """
    params = list(oui)

    return _exec_query(query, params)


def by_alpha(oui: Sequence[str], dataset: edc.Dataset) -> Iterable[BaseStaff]:
    """Return staff by unit name (alpha)."""
    query = f"""
    {_select_query(dataset)}
    WHERE {RAW.work_alpha} IN ({_placeholders(oui)})"""

    return _exec_query(query, tuple(map(str.upper, oui)))


def by_vpu(vpu: Sequence[str], dataset: edc.Dataset) -> Iterable[BaseStaff]:
    """Return staff in VPU."""
    query = f"""
    {_select_query(dataset)}
    WHERE {RAW.vpu} IN ({_placeholders(vpu)})"""

    return _exec_query(query, tuple(map(str.upper, vpu)))


def by_name(first: str, last: str, dataset: edc.Dataset) -> Iterable[BaseStaff]:
    """Return single staff by first and last name (fuzzy match)."""
    query = f"""
    {_select_query(dataset)}
    WHERE {RAW.first_name} LIKE '%{first}%'
    AND {RAW.last_name} LIKE '%{last}%'
    """
    cur = _get_cursor()
    cur.execute(query)
    return _create_staff(cur)


def _exec_query(
    query: str, placeholder: Sequence[str | int | float]
) -> Iterable[BaseStaff]:
    cur = _get_cursor()
    cur.execute(query, placeholder)
    return _create_staff(cur)


def _placeholders(x: Iterable[object]) -> str:
    return ", ".join("?" for _ in x)


def _create_staff(cur: sqlite3.Cursor) -> Iterable[BaseStaff]:
    return (
        BaseStaff(**_rename_keys(staff))
        for staff in cur.fetchall()
        if _has_valid_staff_attrs(staff)  # possible for email to be missing
    )


def _has_valid_staff_attrs(row: sqlite3.Row[_QueryResult]) -> bool:
    """Validate row for required attributes."""

    def _valid_keys() -> bool:
        return set(row.keys()) >= {RAW.email}

    def _valid_data() -> bool:
        return bool(row[edc.RAW_HEADERS.email])

    return all([_valid_keys(), _valid_data()])


def _get_cursor() -> sqlite3.Cursor:
    con = edc.connect()
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    return cur


def _select_query(dataset: edc.Dataset) -> str:
    staff_table = edc.table_name(dataset)
    query = f"""
    SELECT {RAW.upi}, {RAW.email}, {RAW.first_name}, {RAW.middle_name}, {RAW.last_name}
    FROM {staff_table}"""
    return query


_QueryResult = str | float | int | None


class _Staff(TypedDict):
    upi: int
    email: str
    first_name: str
    middle_name: str | None
    last_name: str


def _rename_keys(row: sqlite3.Row[_QueryResult]) -> _Staff:
    return {attr: value for attr, value in zip(BaseStaff.keys, row)}  # type: ignore


def staff_to_frame(staff: Iterable[BaseStaff]) -> pd.DataFrame:
    """Return dataframe from staff iterable."""
    return pd.DataFrame([asdict(_staff) for _staff in staff])


def appt_type(upi: int) -> edc.StaffType | None:
    """Return appointment type of active staff."""
    tbl = edc.Dataset.STAFF_LOCATOR
    con = edc.connect()
    query = f"""
    SELECT {RAW.upi}, {RAW.staff_type}
    FROM {edc.table_name(tbl)}
    WHERE {RAW.upi} = (?)"""

    cur = con.cursor()
    res = cur.execute(query, (upi,)).fetchone()

    return edc.StaffType.from_str(res[1]) if res else None


def is_stc(upi: int) -> bool:
    """Return true if staff is an STC."""
    return appt_type(upi) is edc.StaffType.STC
