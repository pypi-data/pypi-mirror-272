"""Protocols for data access."""
from __future__ import annotations
import sqlite3
from collections.abc import Collection
from dataclasses import (
    astuple,
    dataclass,
)
from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from typing import (
    Literal as L,
)

import pandas as pd
import requests
from termcolor import cprint
from tqdm import tqdm

from wbg.sharepoint import paths as sharepoint

_DB = sharepoint.Paths.PROJS.value.joinpath('DB', 'organization.db')


class Dataset(Enum):
    """WBG Datasets."""

    STAFF_LOCATOR = auto()
    AA = auto()
    STAFF = auto()
    FUND_CENTER = auto()
    HIERARCHY = auto()

    @property
    def url(self) -> str:
        """Return URL of dataset."""
        return _URLS[self]


_DATA_EXPLORER_ROOT = 'https://dvresource.worldbank.org'


def _data_excel_url(file: str, root: str = _DATA_EXPLORER_ROOT) -> str:
    return f'{root}/docs/excel/{file}'


_URLS = {
    Dataset.STAFF_LOCATOR: "https://dvresource.worldbank.org/docs/excel/STAFF_LOCATOR_V2.xlsx",
    Dataset.AA: "https://dvresource.worldbank.org/docs/excel/STAFF_LOCATOR_V2.xlsx",
    Dataset.STAFF: "https://dvresource.worldbank.org/docs/excel/WB_STAFF_V2.xlsx",
    Dataset.FUND_CENTER: 'https://dvresource.worldbank.org/docs/excel/FUND_CENTER_HIERARCHY.xlsx',
    Dataset.HIERARCHY: _data_excel_url('CURRENT_ORGANIZATION_CHART_V2.xlsx'),
}


@dataclass(frozen=True, kw_only=True)
class StaffLocatorHeaders:
    """Name mapping for dataset headers.


    Dataset Reference: https://edc.worldbank.org/home/service-details.html?serviceId=c4c665ee-9e57-4d5e-92a1-44652baa0c72
    Data Model: https://dvresource.worldbank.org/docs/datamodel/Staff_Locator.pdf
    """

    # Staff
    appt_date: str
    first_name: str
    full_name: str
    last_name: str
    middle_name: str
    short_name: str
    nick_name: str
    upi: str
    unit_manager: str
    title: str

    # Contact
    mail_stop: str
    alternate_mobile: str
    email: str
    alternate_email_addr: str
    active_mailbox_flag: str
    voip: str
    work_extn: str
    work_mobile: str
    work_phone: str

    # Unit
    work_alpha: str
    admin_alpha: str
    admin_unit_vpu_alpha: str
    vpu: str
    admin_oui: str
    division: str
    work_oui: str
    work_moc: str
    org_name: str

    # Location
    room_num: str
    city_code: str
    city_name: str
    location: str
    province: str
    country_code: str
    country_name: str

    # Role
    job_code: str
    job_code_descr: str
    role_desc: str
    appt_type: str
    staff_type: str
    subtype: str
    can_app_id_extn_flag: str

    def tolist(self) -> list[str]:
        return list(astuple(self))


RAW_HEADERS = StaffLocatorHeaders(
    # Staff
    appt_date="APPT_EFFECTIVE_DATE",
    first_name="FIRST_NAME",
    full_name="FULL_NAME",
    last_name="LAST_NAME",
    middle_name="MIDDLE_NAME",
    short_name="SHORT_NAME",
    nick_name="NICK_NAME",
    upi="UPI",
    unit_manager="UNIT_MANAGER",
    title="TITLE",
    # Contact
    mail_stop="MAIL_STOP_NBR",
    alternate_mobile="ALTERNATE_MOBILE_NBR",
    email="INTERNET_ADDR",
    alternate_email_addr="ALTERNATE_EMAIL_ADDR",
    active_mailbox_flag="ACTIVE_MAILBOX_FLAG",
    voip="VOIP",
    work_extn="WORK_EXTN",
    work_mobile="WORK_MOBILE",
    work_phone="WORK_PHONE",
    # Unit
    work_alpha="WORK_ALPHA",
    admin_alpha="ADMIN_ALPHA",
    admin_unit_vpu_alpha="ADMIN_UNIT_VPU_ALPHA",
    vpu="WORK_PMU",
    admin_oui="ADMIN_OUI",
    division="DIVISION",
    work_oui="WORK_OUI",
    work_moc="WORK_MOC",
    org_name="ORG_NAME",
    # Location
    room_num="ROOM_NUM",
    city_code="CITY_CODE",
    city_name="CITY_NAME",
    location="LOCATION",
    province="PROVINCE",
    country_code="COUNTRY_CODE",
    country_name="COUNTRY_NAME",
    # Role
    job_code="JOB_CODE",
    job_code_descr="JOB_CODE_DESCR",
    role_desc="APPT_TYPE_DESC",
    appt_type="APPTTYPE",
    staff_type="ALT_STAFF_TYPE",
    subtype="SUBTYPE",
    can_app_id_extn_flag="CAN_APP_ID_EXTN_FLAG",
)


RENAMED_HEADERS = StaffLocatorHeaders(
    appt_date="Join Date",
    first_name="First Name",
    full_name="Full Name",
    last_name="Last Name",
    middle_name="Middle Name",
    short_name="Short Name",
    nick_name="Nick Name",
    upi="UPI",
    unit_manager="Unit Manager",
    title="Title",
    mail_stop="Mail Stop #",
    alternate_mobile="Alternate Mobile #",
    email="Email",
    alternate_email_addr="Alternate Email Addr",
    active_mailbox_flag="Active Mailbox Flag",
    voip="VOIP",
    work_extn="Work Extn.",
    work_mobile="Work Mobile #",
    work_phone="Work Phone",
    work_alpha="OUI",
    admin_alpha="OUI1",
    admin_unit_vpu_alpha="Admin Unit VPU Name",
    vpu="VPU",
    admin_oui="Admin OUI",
    division="Division",
    work_oui="Work OUI",
    work_moc="Work MOC",
    org_name="Org Name",
    room_num="Room Num",
    city_code="City Code",
    city_name="City Name",
    location="Location",
    province="Province",
    country_code="Country Code",
    country_name="Country Name",
    job_code="Job Code",
    job_code_descr="Job Description",
    role_desc="Role",
    appt_type="Appttype",
    staff_type="Staff Type",
    subtype="Subtype",
    can_app_id_extn_flag="Can App Id Extn Flag",
)


class StaffType(Enum):
    """Staff Designation."""

    STC = auto()
    STAFF = auto()
    CONTRACTOR = auto()
    ETC = auto()

    @classmethod
    def from_str(cls, staff_type: str) -> StaffType:
        if staff_type in cls.__members__:
            return cls.__members__[staff_type]
        raise ValueError(f"Invalid staff type: `{staff_type}` passed")


class VPNError(ConnectionError):
    """Issue connecting to WBG server requiring VPN."""


def load_data(
    dataset: Dataset,
    save_dir: Path = sharepoint.Paths.PROJS.value.joinpath('DB', 'staff'),
    filename: str = f"{datetime.today():%F}.xlsx",
) -> pd.DataFrame:
    """Download dataset from EDC.

    Parameters
    ----------
    dataset : Dataset
        Reference to EDC dataset to download
    save_dir : Path, optional
        Path to directory; defaults to `data` dir

    Returns
    -------
    pd.DataFrame
        Raw data

    Raises
    ------
    NotADirectoryError
        Raises if `save_dir` is invalid path
    """
    # TODO: Implement caching logic, if same day access
    if not save_dir.exists():
        raise NotADirectoryError(f"Could not find directory: {save_dir}")

    filepath = save_dir.joinpath(filename)
    if not filepath.exists():
        _download_data(dataset, filepath)
    data = pd.read_excel(filepath, header=4)

    return data


def _download_data(dataset: Dataset, savepath: Path) -> None:
    """Display progress while downloading dataset.

    Make a local copy, as network time is over a minute.
    """
    print("Downloading raw EDC dataset...")
    session = requests.Session()

    try:
        resp = session.get(dataset.url, stream=True)
    except requests.ConnectionError as err:
        msg = "Could not download file--Check if VPN was connected?"
        raise VPNError(msg) from err

    tot_length = int(resp.headers.get("content-length", 0))
    if tot_length == 0:
        raise ValueError("Was unable to get download the dataset!")

    chunk_size = 1024 * 10
    progress_bar = tqdm(total=tot_length, unit="iB", unit_scale=True)

    with open(savepath, "wb") as f:
        for chunk in tqdm(resp.iter_content(chunk_size)):
            progress_bar.update(len(chunk))
            f.write(chunk)
    cprint("Downloaded file", "green")


def load_db(dataset: Dataset) -> pd.DataFrame:
    """Fast data load."""
    con = connect()
    query = f"""SELECT * FROM {table_name(dataset)}"""
    df = pd.read_sql(query, con)
    con.close()
    return df


def clean(
    df: pd.DataFrame,
    raw: StaffLocatorHeaders = RAW_HEADERS,
    renamed: StaffLocatorHeaders = RENAMED_HEADERS,
) -> pd.DataFrame:
    """Rename and subset columns of dataset."""
    _validate_raw_frame(df, raw)
    cleaned = rename(select_cols(df, raw), raw, renamed)
    return cleaned


def _validate_raw_frame(df: pd.DataFrame, cols: StaffLocatorHeaders) -> None:
    from pandas.api import types

    assert types.is_integer_dtype(
        df[cols.upi]
    ), f"Expected: integer dtype for `UPI`, got `{df[cols.upi].dtype}`"


def rename(
    df: pd.DataFrame,
    raw: StaffLocatorHeaders = RAW_HEADERS,
    renamed: StaffLocatorHeaders = RENAMED_HEADERS,
) -> pd.DataFrame:
    """Rename columns of dataset."""
    return df.rename(
        columns={raw: renamed for raw, renamed in zip(astuple(raw), astuple(renamed))}
    )


def select_cols(df: pd.DataFrame, headers: StaffLocatorHeaders) -> pd.DataFrame:
    """Subset columns in `RAW`."""
    return df.loc[:, list(astuple(headers))]


def connect(mode: L["ro", "rw"] = "ro") -> sqlite3.Connection:
    """Return read-only connection to database."""
    con = sqlite3.connect(f"file:{_DB}?mode={mode}", uri=True)
    return con


def update(dataset: Dataset, sourcefile: Path) -> None:
    """Update db with new file.

    Assumes file to be raw staff locator."""
    con = sqlite3.connect(_DB)
    df = pd.read_excel(sourcefile, header=4)
    update_from_frame(df, dataset, con, if_exists="replace")
    con.commit()
    con.close()


def update_from_frame(
    df: pd.DataFrame, dataset: Dataset, con: sqlite3.Connection, if_exists: str
) -> None:
    """Update dataset from dataframe."""
    # need to filter using valid columns, as new columns have been added
    table_columns = list(_table_columns(dataset, con))
    db_df = (
        df
        if RAW_HEADERS.upi in df or RAW_HEADERS.upi not in df.reset_index()
        else df.reset_index()
    ).filter(table_columns)

    db_df.to_sql(dataset.name, con, if_exists=if_exists, index=False)
    root = Path(__file__).parent
    sql_file = root.joinpath("create_index.sql")
    db_path = root.joinpath("data.db")
    cursor = con.cursor()
    cursor.executescript(sql_file.read_text())


def _table_columns(dataset: Dataset, con: sqlite3.Connection) -> Collection[str]:
    query = f'pragma table_info({table_name(dataset)})'

    schema = pd.read_sql(query, con)
    return schema['name']


def table_name(dataset: Dataset) -> str:
    """Return SQL table name of dataset."""
    return dataset.name
