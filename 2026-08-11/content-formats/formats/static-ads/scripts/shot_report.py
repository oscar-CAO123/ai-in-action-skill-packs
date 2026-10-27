#!/usr/bin/env python3
"""Capture the filled scored report out of each lead-magnet prototype. FREE, no generation.

    python3 shot_report.py                # every industry that has a prototype
    python3 shot_report.py construction   # one
    python3 shot_report.py --secs 2       # cut lower down the report
    python3 shot_report.py --width 1200   # override the capture width

This is the deliverable in F-M2. your call : headless Chrome at 2x rather than a
driven browser, because it is deterministic, carries no window chrome and no cursor, is retina
sharp, and can be re-shot for free after any edit to the asset.

How it works, and why it does not touch the prototypes:

  The prototypes already ship a `jumpToReport()` used by their own "Skip to a filled report"
  button, which loads the DEMO answer set and renders the real scored report. This rig copies the
  prototype to a temp file **inside build/** (so `logo.svg` and every other relative path still
  resolves), appends a bootstrap script that calls that function and strips the page furniture,
  screenshots it, and deletes the temp file. Nothing in `build/` is modified.

Two passes, the same shape `band_basic.py` uses: measure the report off the DOM, then screenshot
at exactly that height. A fixed tall window leaves white space under short reports and crops
long ones.

**The cut is at the end of the first report section, not the end of the report.** The full
Systems Audit report measures 56,313px at 1200 wide. Dropped whole onto a 1080x1350 card that is
a 1:47 sliver with nothing legible in it. The top block, the score head, the meta line, the
topline figure and the first section, is the part a reader recognises as "the thing I get", and
it lands around 1:2. `--secs` moves the cut if a deeper section reads better on a given asset.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
from magnet_copy import INDUSTRIES, MAGNET_BUILD  # noqa: E402

OUT = ROOT / "out-magnet" / "_shots"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
WIDTH = 1200
# 0 cuts above section 01, which is the score head, the topline and the CTA bar and nothing
# else. Section 01 carries a min-height, so keeping it drags roughly 300px of dead black onto
# the bottom of the capture.
SECS = 0
MAX_H = 6000           # a capture past this is a sliver on the card, so it is a bug not a choice

# The page furniture that is not the deliverable. The report itself is <main id="report">.
BOOTSTRAP = """
<script>
(function(){
  jumpToReport();
  setTimeout(function(){
    ['.proto','.nav','.hero','.site-foot'].forEach(function(sel){
      document.querySelectorAll(sel).forEach(function(e){ e.remove(); });
    });
    document.body.style.margin = '0';
    var r = document.getElementById('report');
    r.style.margin = '0';
    window.scrollTo(0, 0);
    var top = r.getBoundingClientRect().top + window.scrollY;
    var secs = r.querySelectorAll('.sec');
    var cut = r.getBoundingClientRect().height;
    if(SECS === 0 && secs.length){
      // everything above section 01: the score head, the topline and the CTA bar
      cut = secs[0].getBoundingClientRect().top + window.scrollY - top;
    } else if(secs.length >= SECS){
      cut = secs[SECS - 1].getBoundingClientRect().bottom + window.scrollY - top;
    }
    document.documentElement.dataset.reportH = Math.ceil(cut);
  }, 400);
})();
</script>
"""


def temp_page(proto, secs=SECS):
    """Write the instrumented copy beside the original so relative assets still resolve."""
    html = proto.read_text()
    if "</body>" not in html:
        raise SystemExit(f"{proto.name}: no </body> to hook, the prototype shape changed")
    doc = html.replace("</body>", BOOTSTRAP.replace("SECS", str(secs)) + "</body>", 1)
    f = tempfile.NamedTemporaryFile("w", suffix=".html", dir=proto.parent, delete=False)
    f.write(doc)
    f.close()
    return Path(f.name)


def measure(page, width):
    dom = subprocess.run(
        [CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
         f"--window-size={width},2000", "--virtual-time-budget=6000",
         "--dump-dom", page.as_uri()],
        capture_output=True, text=True).stdout
    m = re.search(r'data-report-h="(\d+)"', dom)
    if not m:
        raise SystemExit("could not measure the report. Did jumpToReport() throw?")
    return int(m.group(1))


def capture(page, png, width, height):
    """Shoot TALL, then crop to the measured height.

    The report reveals its blocks on scroll, so anything below the fold of the capture viewport
    is still at opacity 0 when the shutter fires. Screenshotting at exactly the cut height
    returned a card with the score on it and nothing else. Shoot with the whole block on screen,
    then take the top `height` off the result.
    """
    from PIL import Image
    png.parent.mkdir(parents=True, exist_ok=True)
    tall = max(height, 1600)
    subprocess.run(
        [CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
         "--force-device-scale-factor=2", f"--window-size={width},{tall}",
         "--virtual-time-budget=6000", f"--screenshot={png}", page.as_uri()],
        stderr=subprocess.DEVNULL, check=True)
    im = Image.open(png)
    scale = im.width / width                      # device pixel ratio, 2
    im.crop((0, 0, im.width, round(height * scale))).save(png)


def shoot(industry, width=WIDTH, secs=SECS):
    proto = MAGNET_BUILD / industry["proto"]
    if not proto.exists():
        print(f"  {industry['key']:22} SKIPPED, no prototype at {proto.name}")
        return None
    page = temp_page(proto, secs)
    try:
        h = min(measure(page, width), MAX_H)
        png = OUT / f"{industry['key']}-report.png"
        capture(page, png, width, h)
    finally:
        page.unlink(missing_ok=True)
    print(f"  {industry['key']:22} {width}x{h} at 2x -> {png.name}")
    return png


def opt(argv, flag, default):
    if flag not in argv:
        return argv, default
    v = argv[argv.index(flag) + 1]
    return [a for a in argv if a not in (flag, v)], int(v)


if __name__ == "__main__":
    argv = sys.argv[1:]
    argv, width = opt(argv, "--width", WIDTH)
    argv, secs = opt(argv, "--secs", SECS)
    keys = [a for a in argv if not a.startswith("--")] or None
    for i in INDUSTRIES:
        if keys and i["key"] not in keys:
            continue
        shoot(i, width, secs)
    print(f"\n-> {OUT}")
