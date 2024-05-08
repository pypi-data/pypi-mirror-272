from dataclasses import asdict
from pathlib import Path
import numpy as np

import pandas as pd
import pytest

from wbg.organization import query, edc

from wbg.organization.aa import (
    Staff,
    Details,
    get_staff,
    upi_from_code,
    code_from_upi,
    code_from_name,
    from_staff_locator,
    stc,
)

# pylint: disable=redefined-outer-name
# pylint: disable=missing-class-docstring, missing-function-docstring

_TEST_DATA = Path(__file__).parent.joinpath("data")
_RAW = _TEST_DATA.joinpath("raw.csv")


@pytest.fixture
def raw_staff_locator() -> pd.DataFrame:
    return pd.read_csv(_RAW)


def shiv() -> Staff:
    return Staff(
        upi=570819,
        email="ssrinivasan13@worldbank.org",
        first_name="Shivnaren",
        middle_name=None,
        last_name="Srinivasan",
        code="SH",
        nickname="Shiv",
    )


def islam() -> Staff:
    return Staff(
        upi=553290,
        email="mislam30@worldbank.org",
        first_name="Mohammad",
        middle_name=None,
        last_name="Islam",
        code="MI",
        nickname="Islam",
    )


def nicola() -> Staff:
    return Staff(
        upi=548653,
        email="ngunnion@worldbank.org",
        first_name="Nicola Maria",
        middle_name=None,
        last_name="Gunnion",
        code="NM",
        nickname="Nico",
    )


class TestStaff:
    def test_constructor(self):
        Staff(
            upi=570819,
            email="ssrinivasan13@worldbank.org",
            first_name="Shivnaren",
            middle_name=None,
            last_name="Srinivasan",
            code=None,
            nickname="Shiv",
        )

    @pytest.mark.parametrize("staff", (shiv(), islam()))
    def test_from_staff(self, staff: Staff):
        base_staff = query.BaseStaff(
            **{
                key: value
                for key, value in asdict(staff).items()
                if key not in {"code", "nickname"}
            }
        )
        details = Details(code=staff.code, nickname=staff.nickname)

        actual_staff = Staff.from_staff(base_staff, details)
        assert actual_staff == staff

    @pytest.mark.parametrize(["code", "staff"], [("SH", shiv()), ("MI", islam())])
    def test_from_code_scalar(self, code: str, staff: Staff):
        actual_staff = Staff.from_code(code)
        assert actual_staff == staff

    def test_from_code_collection(self):
        actual_staff = Staff.from_code(("SH", "MI"))
        expected_staff = (shiv(), islam())
        assert set(actual_staff) == set(expected_staff)

    @pytest.mark.parametrize(["upi", "staff"], [(570819, shiv()), (553290, islam())])
    def test_from_upi_scalar(self, upi: int, staff: Staff):
        actual_staff = Staff.from_upi(upi)
        assert actual_staff == staff

    def test_from_upi_invalid_upi(self):
        upi = -1
        with pytest.raises(ValueError, match="Invalid upi passed!"):
            Staff.from_upi(upi)

    def test_from_upi_collection(self):
        actual_staff = Staff.from_upi((570819, 553290))
        expected_staff = (shiv(), islam())
        assert set(actual_staff) == set(expected_staff)

    def test_from_upi_invalid_upis(self):
        upi = (-1, -2)
        with pytest.raises(ValueError, match="Invalid upi passed!"):
            Staff.from_upi(upi)

    @pytest.mark.parametrize(
        ["name", "staff"],
        [
            ("Shivnaren", shiv()),
            ("Mohammad", islam()),
            ("islam", islam()),
            ("Nicola", nicola()),
        ],
    )
    def test_from_first_name(self, name: str, staff: Staff):
        # Test for nickname (`islam`), as well as multiple words in first name (`Nicola Maria`)
        actual_staff = Staff.from_first_name(name)
        assert actual_staff == staff

    def test_from_first_name_mohammad(self, islam: Staff = islam()):
        name = "Mohammad"
        actual_staff = Staff.from_first_name(name)
        assert actual_staff == islam

    def test_from_first_name_raises_value_error(self):
        name = "invalid"
        with pytest.raises(ValueError, match=f"Invalid name: `{name}` passed"):
            Staff.from_first_name(name)

    @pytest.mark.parametrize(
        ["name", "staff"],
        [("Shivnaren Srinivasan", shiv()), ("Mohammad Islam", islam())],
    )
    def test_from_name(self, name: str, staff: Staff):
        actual_staff = Staff.from_name(name)
        assert actual_staff == staff

    def test_from_name_raises_value_error(self):
        name = "invalid"
        with pytest.raises(ValueError, match=f"Invalid name: `{name}` passed"):
            Staff.from_name(name)

    @pytest.mark.parametrize(["name", "staff"], [("Shiv", shiv()), ("Islam", islam())])
    def test_name(self, name: str, staff: Staff):
        assert staff.name == name


class TestDetails:
    def test_lesser_than(self) -> None:
        lesser = Details(code='A')
        greater = Details(code='B')
        assert lesser < greater

    def test_equal(self) -> None:
        detail1 = Details(code='A')
        detail2 = Details(code='A')
        assert detail1 == detail2


class TestGetStaff:
    @pytest.mark.parametrize(["code", "staff"], [("SH", shiv()), ("MI", islam())])
    def test_from_code_scalar(self, code: str, staff: Staff):
        actual_staff = get_staff(code=code)
        assert actual_staff == staff

    def test_from_code_collection(self):
        actual_staff = get_staff(code=("SH", "MI"))
        expected_staff = (shiv(), islam())
        assert set(actual_staff) == set(expected_staff)

    @pytest.mark.parametrize(["upi", "staff"], [(570819, shiv()), (553290, islam())])
    def test_from_upi_scalar(self, upi: int, staff: Staff):
        actual_staff = get_staff(upi=upi)
        assert actual_staff == staff

    def test_from_upi_collection(self):
        actual_staff = get_staff(upi=(570819, 553290))
        expected_staff = (shiv(), islam())
        assert set(actual_staff) == set(expected_staff)

    @pytest.mark.parametrize(
        ["name", "staff"], [("Shivnaren", shiv()), ("Mohammad", islam())]
    )
    def test_from_first_name(self, name: str, staff: Staff):
        actual_staff = get_staff(first_name=name)
        assert actual_staff == staff

    @pytest.mark.parametrize(
        ["name", "staff"],
        [("Shivnaren Srinivasan", shiv()), ("Mohammad Islam", islam())],
    )
    def test_from_name(self, name: str, staff: Staff):
        actual_staff = get_staff(name=name)
        assert actual_staff == staff

    def test_default(self):
        all_staff = get_staff()

        keys_are_upi = all(isinstance(key, int) for key in all_staff)
        values_are_staff = all(isinstance(value, Staff) for value in all_staff.values())

        assert keys_are_upi
        assert values_are_staff


class TestCodeFromUPI:
    @pytest.mark.parametrize(["upi", "staff"], [(570819, shiv()), (553290, islam())])
    def test_valid_upi_returns_str_code(self, upi: int, staff: Staff):
        assert code_from_upi(upi) == staff.code

    @pytest.mark.parametrize(["upi"], [(224652,), (299155,), (440870,)])
    def test_no_code_returns_none(self, upi: int):
        assert code_from_upi(upi) is None

    @pytest.mark.parametrize(["upi"], [(-1,), (209062,)])
    def test_invalid_upi_raises(self, upi: int):
        with pytest.raises(ValueError, match=f"Invalid aa UPI: `{upi}` passed"):
            code_from_upi(upi)


class TestUPIFromCode:
    @pytest.mark.parametrize(["code", "staff"], [("SH", shiv()), ("MI", islam())])
    def test_upi_from_code(self, code: str, staff: Staff):
        assert Staff.from_code(code) == staff

    def test_raises_value_error(self):
        invalid_code = "zz"
        with pytest.raises(ValueError, match=f"Invalid staff code: `{invalid_code}`"):
            upi_from_code(invalid_code)


class TestCodeFromName:
    @pytest.mark.parametrize(
        ["name", "code"],
        [("Shiv", "SH"), ("Islam", "MI"), ("Rosclr", "RM"), ("Atul", None)],
    )
    def test_default(self, name: str, code: str | None):
        assert code_from_name(name) == code


class TestFromStaffLocator:
    @pytest.fixture
    def _expected(self) -> pd.DataFrame:
        return pd.read_csv(_TEST_DATA.joinpath("aa.csv"))

    def test_upis_equal(
        self, raw_staff_locator: pd.DataFrame, _expected: pd.DataFrame
    ) -> None:
        actual = from_staff_locator(raw_staff_locator)
        assert np.array_equal(
            actual[edc.RAW_HEADERS.upi], _expected[edc.RAW_HEADERS.upi]
        )
