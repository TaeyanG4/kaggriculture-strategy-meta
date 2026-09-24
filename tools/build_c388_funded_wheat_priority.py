"""Build the bounded purchase-order intervention separately from c386/c387."""
import argparse, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT_SHA = '05b8d6eedb266fcc131ec74b8b87659e15ed077707d91489a423ad4d1a567144'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--disabled', action='store_true')
    args = parser.parse_args()
    body = (ROOT/'agent/c384_predictive_tomato.py').read_bytes()
    assert hashlib.sha256(body).hexdigest() == PARENT_SHA
    layer = (ROOT/'agent/overlays/c388_funded_wheat_priority.py').read_text('utf8')
    if args.disabled:
        assert layer.count('_C388_ENABLED = True') == 1
        layer = layer.replace('_C388_ENABLED = True', '_C388_ENABLED = False')
    data = body.rstrip()+b'\n\n'+layer.encode('utf8')
    compile(data, str(args.out), 'exec')
    assert not args.out.exists()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_bytes(data)
    print(args.out, hashlib.sha256(data).hexdigest())


if __name__ == '__main__':
    main()
