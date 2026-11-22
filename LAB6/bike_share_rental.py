RATE_PER_30_MIN = {"standard": 20, "electric": 35, "cargo": 50}
def ride_cost(bike_type, minutes, is_subscriber, is_peak):
    if bike_type not in RATE_PER_30_MIN:
        raise ValueError("unknown bike type")
    if minutes <= 0:
        raise ValueError("invalid duration")
    blocks = (minutes + 29) // 30
    if is_subscriber:
        blocks -= 1
        if blocks <= 0:
            return 0
    cost = blocks * RATE_PER_30_MIN[bike_type]
    if is_peak and bike_type != "cargo":
        cost += 15
    if minutes > 180:
        cost += 100
    return cost


def dock_status(bikes_docked, capacity):
    if capacity <= 0:
        raise ValueError("invalid capacity")
    if bikes_docked < 0 or bikes_docked > capacity:
        raise ValueError("invalid bike count")
    free_slots = capacity - bikes_docked
    if bikes_docked == 0:
        return "empty"
    if free_slots == 0:
        return "full"
    if bikes_docked <= 2:
        return "few bikes"
    elif free_slots <= 2:
        return "few slots"
    return "available"


def can_unlock(account_balance, has_active_ride, age):
    if has_active_ride:
        return False
    if age < 16:
        return False
    elif age < 18:
        return account_balance >= 100
    return account_balance >= 50
