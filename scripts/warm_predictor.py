"""Keep the deployed model server warm, or let it scale to zero again.

The predictor runs on Modal as a parameterized class, so the number of always-on containers is
set on the deployed instance rather than at deploy time. One warm container removes the cold
start (about 1.5 minutes of model loading) from the first audit after an idle period.

Usage (from the project root, Modal logged in):
  python scripts/warm_predictor.py --min-containers 1
  python scripts/warm_predictor.py --min-containers 0
"""
from __future__ import annotations

import argparse

import modal

APP_NAME = "sheettruth-predict"
CLASS_NAME = "Predictor"
DEFAULT_ADAPTER = "/models/glimmer-sheettruth-v2/adapter"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--min-containers", type=int, required=True, help="containers to keep running at all times")
    ap.add_argument("--adapter", default=DEFAULT_ADAPTER, help="adapter path the web app uses (its SHEETTRUTH_ADAPTER)")
    args = ap.parse_args()

    predictor = modal.Cls.from_name(APP_NAME, CLASS_NAME)
    instance = predictor(adapter_dir=args.adapter)
    instance.update_autoscaler(min_containers=args.min_containers)
    print(f"{APP_NAME}.{CLASS_NAME}(adapter_dir={args.adapter}): min_containers={args.min_containers}")


if __name__ == "__main__":
    main()
