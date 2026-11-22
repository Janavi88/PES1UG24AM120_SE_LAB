from hypothesis import given, strategies as st
from bike_share_rental_parser import (
    parse_ride_duration,
    format_station_code,
    parse_ride_log,
)

@given(st.text() | st.none())
def test_parse_ride_duration_no_crash(s):
    try:
        parse_ride_duration(s)
    except Exception as e:
        assert False, f"parse_ride_duration crashed with {s!r}: {e}"


@given(st.text() | st.none())
def test_format_station_code_no_crash(s):
    try:
        format_station_code(s)
    except Exception as e:
        assert False, f"format_station_code crashed with {s!r}: {e}"


@given(st.text() | st.none())
def test_parse_ride_log_no_crash(s):
    try:
        parse_ride_log(s)
    except Exception as e:
        assert False, f"parse_ride_log crashed with {s!r}: {e}"