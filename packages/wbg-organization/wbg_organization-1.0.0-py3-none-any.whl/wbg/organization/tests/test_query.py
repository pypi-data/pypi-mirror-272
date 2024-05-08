from collections.abc import Iterable
from dataclasses import asdict
import pandas as pd
import pytest

from wbg.organization import (
    edc,
)

from wbg.organization.query import (
    BaseStaff,
    staff_to_frame,
    appt_type,
    is_stc,
)


def _staff() -> BaseStaff:
    return BaseStaff(
        upi=570819,
        email="ssrinivasan13@worldbank.org",
        first_name="Shivnaren",
        middle_name=None,
        last_name="Srinivasan",
    )


class TestStaffToFrame:
    def test_iterable_returns_frame(self, staff: BaseStaff = _staff()):
        assert isinstance(staff_to_frame([staff]), pd.DataFrame)

    def test_iterable_returns_valid_frame(self, staff: BaseStaff = _staff()):
        df = staff_to_frame([staff])
        assert df.loc[0].to_dict() == asdict(staff)


def _stc() -> tuple[int, ...]:
    # Stateful, and that's not ideal
    return (608681, 606133)


def _not_stc() -> Iterable[int]:
    return (570819,)


class TestApptType:
    @pytest.mark.parametrize("upi", _stc())
    def test_stc(self, upi: int):
        assert appt_type(upi) is edc.StaffType.STC

    @pytest.mark.parametrize("upi", _not_stc())
    def test_staff(self, upi: int):
        assert appt_type(upi) is edc.StaffType.STAFF

    def test_invalid_upi_raises(self):
        assert appt_type(-1) is None


class TestIsSTC:
    @pytest.mark.parametrize("upi", _stc())
    def test_true(self, upi: int):
        assert is_stc(upi)

    @pytest.mark.parametrize("upi", _not_stc())
    def test_false(self, upi: int):
        assert not is_stc(upi)
