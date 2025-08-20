from pathlib import Path

from design_processor import (
    extract_dimensions,
    verify_against_spec,
    generate_client_sheet,
    generate_workshop_sheet,
)


DATA = Path(__file__).parent / "data" / "sample.svg"


def test_extract_dimensions():
    objs = extract_dimensions(str(DATA))
    ids = {o.id for o in objs}
    assert {"rect1", "rect2"} <= ids
    rect1 = next(o for o in objs if o.id == "rect1")
    assert rect1.width == 100
    assert rect1.height == 50


def test_verify_against_spec():
    objs = extract_dimensions(str(DATA))
    spec = {
        "rect1": {"width": 100, "height": 50},
        "rect2": {"width": 40, "height": 40},
    }
    mismatches = verify_against_spec(objs, spec)
    assert mismatches == []
    spec_bad = {"rect1": {"width": 110}}
    mismatches = verify_against_spec(objs, spec_bad)
    assert mismatches and mismatches[0]["expected"] == 110


def test_generate_sheets():
    objs = extract_dimensions(str(DATA))
    client = generate_client_sheet(objs)
    workshop = generate_workshop_sheet(objs)
    assert "rect1" in client
    assert "rect2" in workshop
from main import create_tech_sheets


def test_create_tech_sheets():
    spec = {"rect1": {"width": 100, "height": 50}}
    result = create_tech_sheets(str(DATA), spec)
    assert "client_sheet" in result and "workshop_sheet" in result
    assert "rect1" in result["client_sheet"]
