from datetime import datetime
from typing import Dict

from design_processor import (
    extract_dimensions,
    generate_client_sheet,
    generate_workshop_sheet,
    verify_against_spec,
)


def get_current_time():
    now = datetime.now()
    return {"time": now.strftime("%H:%M:%S")}


def greet_user(name):
    return f"Привет, {name}! Рад тебя видеть."


def create_tech_sheets(file_path: str, spec: Dict[str, Dict[str, float]]):
    objects = extract_dimensions(file_path)
    verify_against_spec(objects, spec)
    client_sheet = generate_client_sheet(objects)
    workshop_sheet = generate_workshop_sheet(objects)
    return {
        "client_sheet": client_sheet,
        "workshop_sheet": workshop_sheet,
    }
