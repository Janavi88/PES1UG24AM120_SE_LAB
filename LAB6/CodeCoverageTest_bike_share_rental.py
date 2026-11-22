import pytest
from bike_share_rental import ride_cost, dock_status, can_unlock

# ---- Starter tests ----
def test_standard_ride():
    assert ride_cost("standard", 45, False, False) == 40

def test_dock_available():
    assert dock_status(5, 10) == "available"

# ---- ride_cost: error lines ----
def test_ride_unknown_bike_type():
    with pytest.raises(ValueError, match="unknown bike type"):
        ride_cost("scooter", 30, False, False)

def test_ride_invalid_duration():
    with pytest.raises(ValueError, match="invalid duration"):
        ride_cost("standard", 0, False, False)

# ---- ride_cost: subscriber, peak, long-ride lines ----
def test_subscriber_short_ride_is_free():
    assert ride_cost("standard", 20, True, False) == 0

def test_electric_peak_long_ride():
    # 200 min -> 7 blocks * 35 = 245, +15 peak, +100 long ride
    assert ride_cost("electric", 200, False, True) == 360

# ---- dock_status: every return / raise line ----
def test_dock_invalid_capacity():
    with pytest.raises(ValueError, match="invalid capacity"):
        dock_status(0, 0)

def test_dock_invalid_count():
    with pytest.raises(ValueError, match="invalid bike count"):
        dock_status(-1, 10)

def test_dock_empty():
    assert dock_status(0, 10) == "empty"

def test_dock_full():
    assert dock_status(10, 10) == "full"

def test_dock_few_bikes():
    assert dock_status(2, 10) == "few bikes"

def test_dock_few_slots():
    assert dock_status(8, 10) == "few slots"

# ---- can_unlock: every return line ----
def test_unlock_active_ride():
    assert can_unlock(500, True, 30) is False

def test_unlock_too_young():
    assert can_unlock(500, False, 15) is False

def test_unlock_teen_with_balance():
    assert can_unlock(100, False, 17) is True

def test_unlock_adult_with_balance():
    assert can_unlock(50, False, 30) is True