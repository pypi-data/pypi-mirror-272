from enum import Enum


class Methods(Enum):
    units_arrived = "units_arrived"
    recipe_activated = "recipe_activated"
    validate_units = "validate_units"
    work_started = "work_started"
    units_inspected = "units_inspected"
    work_completed = "work_completed"
    units_departed = "units_departed"
    state_change = "state_change"
