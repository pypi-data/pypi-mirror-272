"""Update staff details in DB."""

import pandas as pd
from wbg.organization import edc, aa


def main() -> None:
    """Update downloaded information."""
    staff = edc.load_data(edc.Dataset.STAFF_LOCATOR)
    _update(staff)


def _update(staff: pd.DataFrame) -> None:
    aa_staff = aa.from_staff_locator(staff)
    existing_aa_staff = edc.load_db(edc.Dataset.AA)
    new_aa_staff = aa_staff.loc[~aa_staff['UPI'].isin(existing_aa_staff['UPI'])]

    con = edc.connect('rw')
    edc.update_from_frame(staff, edc.Dataset.STAFF_LOCATOR, con, 'replace')
    edc.update_from_frame(new_aa_staff, edc.Dataset.AA, con, 'append')


if __name__ == '__main__':
    main()
