#!/usr/bin/env python3
"""Capture a browser screenshot for a local HTML file or URL.

Requires Python Playwright to already be installed in the current environment.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def to_target(value: str) -> str:
    if value.startswith(("http://", "https://", "file://")):
        return value

    path = Path(value).expanduser().resolve()
    if not path.exists():
        raise SystemExit(f"Target does not exist: {path}")
    return path.as_uri()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Capture a Chromium screenshot for design-to-HTML validation."
    )
    parser.add_argument("target", help="Local HTML file path, file:// URL, or http(s) URL")
    parser.add_argument("output", help="Screenshot output path, usually .png")
    parser.add_argument("--width", type=int, default=1440, help="Viewport width")
    parser.add_argument("--height", type=int, default=900, help="Viewport height")
    parser.add_argument(
        "--full-page",
        action="store_true",
        help="Capture the full scrollable page instead of the viewport",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    target = to_target(args.target)
    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "Python Playwright is not installed. Use an available browser tool, "
            "or ask the user before installing Playwright for this helper.",
            file=sys.stderr,
        )
        return 2

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": args.width, "height": args.height})
        page.goto(target, wait_until="networkidle")
        page.screenshot(path=str(output), full_page=args.full_page)
        browser.close()

    print(f"Screenshot saved: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
