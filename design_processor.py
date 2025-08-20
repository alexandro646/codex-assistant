"""Module for processing design files (SVG/CDR) and generating technical sheets."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional
import xml.etree.ElementTree as ET


@dataclass
class DesignObject:
    """Represents a graphical object with dimensions."""
    id: str
    type: str
    width: float
    height: float


def extract_dimensions(file_path: str) -> List[DesignObject]:
    """Extract objects and their dimensions from a design file.

    Currently supports basic SVG files. CDR support is not implemented
    and will raise :class:`NotImplementedError`.
    """
    if file_path.lower().endswith(".svg"):
        return _extract_svg(file_path)
    if file_path.lower().endswith(".cdr"):
        raise NotImplementedError("CDR parsing is not implemented")
    raise ValueError("Unsupported file type")


def _extract_svg(file_path: str) -> List[DesignObject]:
    tree = ET.parse(file_path)
    root = tree.getroot()
    ns = {"svg": "http://www.w3.org/2000/svg"}
    objects: List[DesignObject] = []
    # rectangles
    for rect in root.findall(".//svg:rect", ns):
        obj_id = rect.get("id", "rect")
        width = float(rect.get("width", 0))
        height = float(rect.get("height", 0))
        objects.append(DesignObject(obj_id, "rect", width, height))
    # circles – use diameter for width/height
    for circle in root.findall(".//svg:circle", ns):
        obj_id = circle.get("id", "circle")
        r = float(circle.get("r", 0))
        d = 2 * r
        objects.append(DesignObject(obj_id, "circle", d, d))
    return objects


def verify_against_spec(
    objects: List[DesignObject], spec: Dict[str, Dict[str, float]], *, tolerance: float = 1e-6
) -> List[Dict[str, float]]:
    """Check that extracted objects match the provided specification.

    Parameters
    ----------
    objects: List[DesignObject]
        Extracted objects.
    spec: Dict[str, Dict[str, float]]
        Mapping of object id to expected dimensions.
    tolerance: float
        Allowed absolute difference.

    Returns
    -------
    List of mismatches. Each mismatch contains ``id``, ``field``,
    ``expected`` and ``actual`` values.
    """
    mismatches: List[Dict[str, float]] = []
    for obj in objects:
        expected = spec.get(obj.id)
        if not expected:
            continue
        for field in ("width", "height"):
            exp_val = expected.get(field)
            if exp_val is None:
                continue
            act_val = getattr(obj, field)
            if abs(act_val - exp_val) > tolerance:
                mismatches.append(
                    {
                        "id": obj.id,
                        "field": field,
                        "expected": exp_val,
                        "actual": act_val,
                    }
                )
    return mismatches


def generate_client_sheet(objects: List[DesignObject]) -> str:
    """Generate a simple technical sheet for clients."""
    lines = ["Тех.лист для клиента:"]
    for obj in objects:
        lines.append(f"- {obj.id}: {obj.width}×{obj.height} ({obj.type})")
    return "\n".join(lines)


def generate_workshop_sheet(objects: List[DesignObject]) -> str:
    """Generate a technical sheet for workshop."""
    lines = ["Тех.лист для цеха:", "ID\tТип\tШирина\tВысота"]
    for obj in objects:
        lines.append(f"{obj.id}\t{obj.type}\t{obj.width}\t{obj.height}")
    return "\n".join(lines)
