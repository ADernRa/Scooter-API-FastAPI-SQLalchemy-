from datetime import datetime
base_cost = 10
def calculate_cost(start_ride: datetime, end_ride: datetime, cost: float) -> float:
    delta_time = end_ride - start_ride
    total_seconds = delta_time.total_seconds()
    total_minutes = total_seconds / 60

    total_cost = total_minutes*cost+base_cost
    return round(total_cost, 2)