"""Build the exact-one urgent feed repair from the frozen c129/c148 sources."""
import ast
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "agent/c129_feed_liquidity.py"
SOURCE_OVERLAY = ROOT / "agent/overlays/c148_urgent_feed_coexist.py"
TARGET_OVERLAY = ROOT / "agent/overlays/c153_urgent_feed_exact1.py"
TARGET = ROOT / "agent/c153_urgent_feed_exact1.py"
PARENT_SHA = "e9973586cbe2c0bbb034243f3d3e4c9fdcac4fcac432c0de32b0ba0e61f7ca61"
OVERLAY_SHA = "2f1f37ad7668e4a90c4ea63368c4e938bc95016f917d00380cbd75c9e18da21d"


def frozen_write(path: Path, data: bytes):
    if path.exists() and path.read_bytes() != data:
        raise ValueError("Existing c153 artifact differs: " + str(path))
    path.write_bytes(data)


def main():
    parent = PARENT.read_bytes()
    original = SOURCE_OVERLAY.read_bytes()
    assert hashlib.sha256(parent).hexdigest() == PARENT_SHA, "c129 parent drift"
    assert hashlib.sha256(original).hexdigest() == OVERLAY_SHA, "c148 overlay drift"
    overlay = original.decode("utf-8").replace("\r\n", "\n").replace("c148", "c153").replace("C148", "C153")
    order_gate = '''    if len(orders) >= 10 or not any(order and order[0] != "SELL" for order in orders):
        return parent
'''
    exact_gate = '''    if len(orders) >= 10 or not any(order and order[0] != "SELL" for order in orders):
        return parent
    if any(len(order) >= 2 and order[:2] == ["SELL", "WHEAT"] for order in orders):
        state["wheat_sale_declines"] += 1
        return parent
'''
    assert overlay.count(order_gate) == 1
    overlay = overlay.replace(order_gate, exact_gate)
    quantity_gate = '''    if deficit <= 0:
        state["already_funded"] += 1
        return parent
    day_room = 4 - parent_day_units - state["day_units"]
'''
    exact_quantity = '''    if deficit <= 0:
        state["already_funded"] += 1
        return parent
    if deficit != 1:
        state["quantity_declines"] += 1
        return parent
    day_room = 4 - parent_day_units - state["day_units"]
'''
    assert overlay.count(quantity_gate) == 1
    overlay = overlay.replace(quantity_gate, exact_quantity)
    counter = '"prefix_declines": 0, "quantity_declines": 0,'
    assert overlay.count(counter) == 1
    overlay = overlay.replace(counter, '"prefix_declines": 0, "wheat_sale_declines": 0, "quantity_declines": 0,')
    overlay_bytes = overlay.encode("utf-8")
    candidate = parent + b"\n" + overlay_bytes
    compile(candidate, "c153", "exec"); ast.parse(candidate.decode("utf-8"))
    frozen_write(TARGET_OVERLAY, overlay_bytes)
    frozen_write(TARGET, candidate)
    print("c153 overlay SHA256:", hashlib.sha256(overlay_bytes).hexdigest())
    print("c153 candidate SHA256:", hashlib.sha256(candidate).hexdigest())


if __name__ == "__main__":
    main()
