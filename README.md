# Midpoint

Enter two numbers; it returns half their difference added to the smaller one — the midpoint.

`((909 − 867) / 2) + 867 = 888`

That is the same as the plain average of the two numbers. The three steps are shown on screen so
the arithmetic stays checkable instead of disappearing into one division.

## Install on an iPhone

1. Open the site in **Safari** (https, or localhost).
2. Share → **Add to Home Screen**.
3. It launches full screen, with no browser chrome, and works with no network.

## Behaviour

- Order does not matter — the smaller number is found automatically and its field is marked blue.
- Decimals, negatives and equal numbers all work; equal numbers return that number.
- Large figures are grouped Indian-style for reading (`1,17,50,000`); **Copy** gives the plain number.
- Results are rounded at six decimal places to clear floating-point dust.

## Development

```bash
python3 -m http.server 4180 --directory ~/midpoint
```

One `index.html` with its CSS and JS inline, plus a manifest, a service worker and the icons.
No framework, no build step, no dependencies.

`tools/make-icons.py` regenerates the PNG icons using only the Python standard library.

**After changing any asset, bump `CACHE` in `sw.js`** — otherwise the service worker keeps serving
the previous version and the new one only appears on the second launch.
