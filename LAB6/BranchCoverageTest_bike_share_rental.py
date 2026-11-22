import pytest
from bike_share_rental import ride_cost, dock_status, can_unlock

# ---- Starter tests ----
def test_standard_ride():
    assert ride_cost("standard", 45, False, False) == 40

def test_dock_available():
    assert dock_status(5, 10) == "available"

# =====================  ride_cost  =====================
# Branch: bike_type not in RATE (True / False)
def test_ride_unknown_bike_type():
    with pytest.raises(ValueError, match="unknown bike type"):
        ride_cost("scooter", 30, False, False)

# Branch: minutes <= 0 (True; False covered by valid rides)
def test_ride_zero_minutes():
    with pytest.raises(ValueError, match="invalid duration"):
        ride_cost("standard", 0, False, False)

def test_ride_negative_minutes():
    with pytest.raises(ValueError, match="invalid duration"):
        ride_cost("standard", -5, False, False)

# Branch: is_subscriber True -> blocks <= 0 True (free ride)
def test_subscriber_short_ride_free():
    assert ride_cost("standard", 20, True, False) == 0

def test_subscriber_exactly_one_block_free():
    assert ride_cost("electric", 30, True, False) == 0

# Branch: is_subscriber True -> blocks <= 0 False (pays remaining blocks)
def test_subscriber_pays_after_free_block():
    # 45 min -> 2 blocks, minus 1 free = 1 * 35
    assert ride_cost("electric", 45, True, False) == 35

# Branch: is_subscriber False (covered by starter test as well)
def test_non_subscriber_pays_all_blocks():
    assert ride_cost("cargo", 60, False, False) == 100

# Branch: is_peak and bike != cargo  -> True
def test_peak_non_cargo_surcharge():
    assert ride_cost("standard", 30, False, True) == 35

# Branch: is_peak True but bike == cargo -> False (second operand)
def test_peak_cargo_no_surcharge():
    assert ride_cost("cargo", 30, False, True) == 50

# Branch: is_peak False -> False (first operand)
def test_off_peak_no_surcharge():
    assert ride_cost("standard", 30, False, False) == 20

# Branch: minutes > 180 -> True
def test_long_ride_penalty():
    # 181 min -> 7 blocks * 20 = 140 + 100
    assert ride_cost("standard", 181, False, False) == 240

# Boundary: minutes == 180 -> False (no penalty)
def test_exactly_180_minutes_no_penalty():
    assert ride_cost("standard", 180, False, False) == 120

# All surcharges combined
def test_subscriber_peak_long_ride():
    # 200 min -> 7 blocks - 1 = 6 * 35 = 210, +15 peak, +100 long
    assert ride_cost("electric", 200, True, True) == 325

# =====================  dock_status  =====================
# Branch: capacity <= 0 (True)
def test_dock_zero_capacity():
    with pytest.raises(ValueError, match="invalid capacity"):
        dock_status(0, 0)

def test_dock_negative_capacity():
    with pytest.raises(ValueError, match="invalid capacity"):
        dock_status(0, -3)

# Branch: bikes < 0 (True)
def test_dock_negative_bikes():
    with pytest.raises(ValueError, match="invalid bike count"):
        dock_status(-1, 10)

# Branch: bikes < 0 False, bikes > capacity True
def test_dock_bikes_exceed_capacity():
    with pytest.raises(ValueError, match="invalid bike count"):
        dock_status(11, 10)

# Branch: bikes == 0 (True)
def test_dock_empty():
    assert dock_status(0, 10) == "empty"

# Branch: free_slots == 0 (True)
def test_dock_full():
    assert dock_status(10, 10) == "full"

# Branch: bikes <= 2 (True), both sides of the boundary
def test_dock_one_bike():
    assert dock_status(1, 10) == "few bikes"

def test_dock_two_bikes():
    assert dock_status(2, 10) == "few bikes"

# Branch: bikes <= 2 False, free_slots <= 2 True
def test_dock_two_free_slots():
    assert dock_status(8, 10) == "few slots"

def test_dock_one_free_slot():
    assert dock_status(9, 10) == "few slots"

# Branch: both False -> available (boundaries 3 bikes / 3 free slots)
def test_dock_three_bikes_available():
    assert dock_status(3, 10) == "available"

def test_dock_three_free_slots_available():
    assert dock_status(7, 10) == "available"

# =====================  can_unlock  =====================
# Branch: has_active_ride True
def test_unlock_blocked_by_active_ride():
    assert can_unlock(500, True, 30) is False

# Branch: age < 16 True
def test_unlock_under_16():
    assert can_unlock(500, False, 15) is False

# Branch: age < 16 False, age < 18 True (balance both outcomes)
def test_unlock_age_16_enough_balance():
    assert can_unlock(100, False, 16) is True

def test_unlock_age_17_insufficient_balance():
    assert can_unlock(99, False, 17) is False

# Branch: age < 18 False (adult, balance both outcomes)
def test_unlock_age_18_enough_balance():
    assert can_unlock(50, False, 18) is True

def test_unlock_adult_insufficient_balance():
    assert can_unlock(49, False, 40) is False