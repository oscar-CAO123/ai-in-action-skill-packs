#!/usr/bin/env python3
"""The house bottom-band type engine, shared by every rig that sets a band of copy.

One block of Anton in the bottom 1.5/4 of the frame, one size per frame, white with a
single blue accent, set flush on both margins and filling the band. Line breaking is a
fit decision made here, not an authoring one.

    from band import render_card
    render_card(["THE [[$30,000 TYPO]]", "HIDING IN ONE AUSSIE BUILDER"], Path("out/x.png"))

See skills/content-formats/formats/static-ads/SKILL.md section 0 for the law and the traps already paid for.
"""
import os
import html
import json
import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent
ASSETS = ROOT.parent / "assets"
CHROME = os.environ.get("CHROME_BIN",
                        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

W, H = 1080, 1350
BLUE = "#1269FF"
PAD = 64
WELL = H * 3 // 8             # every mark lives in the bottom 1.5/4 of the frame
LH = 0.95                     # tight, but clear of the ink Anton hangs below the baseline
GAP_MAX = 0.22                # a line gap never grows past this share of the type size
WORD_GAP_MAX = 0.55           # a justified word gap never grows past this share either
DIV_GAP = 44                  # the divider rule's clearance above the first line of type

PLATE = H - WELL           # the image plate area, above the band
BLEEDFADE = WELL + 470     # the full-bleed fade: the well, plus a long run-up above it

# Two typographic themes share this engine. `anton` is the original law: condensed caps,
# one blue accent. `noir` is the thin-your display typeface treatment for the B&W noir-painterly carousels,
# set to the locked design system's display weight (your display typeface 200, see
# context/design-system/SCHEMA.md: "Display type is weight 200"). Everything else about the
# band is unchanged from `anton`: all caps, justified flush both margins, one blue accent.
THEMES = {
    "anton": {
        "face": "@font-face {{ font-family:'Anton'; src:url('{a}/Anton-Regular.ttf'); }}",
        "family": "Anton",
        "transform": "uppercase",
        "tracking": "0.005em",
        "leading": 0.95,
        "pad_top": 0.16,      # Anton throws ink above its line box at this leading
        "accent": f"color:{BLUE};",
        "weight": 400,
        "anno_weight": 500,
    },
    "noir": {
        "face": ("@font-face {{ font-family:'your display typeface'; font-weight:200; "
                 "src:url('{a}/jost-200.ttf'); }}"
                 "@font-face {{ font-family:'your display typeface'; font-weight:300; "
                 "src:url('{a}/jost-300.ttf'); }}"),
        "family": "your display typeface",
        "transform": "uppercase",
        # Thin caps want air between the letters or the line reads as a smear at this size.
        "tracking": "0.02em",
        "leading": 1.06,      # your display typeface sits inside its box, so it wants air between lines
        "pad_top": 0.0,
        # The accent stays blue. Weight cannot carry it here: the whole band is one thin
        # weight, so a heavier accent word would break the even colour the thin face buys.
        "accent": f"color:{BLUE};",
        "weight": 200,
        # Plate annotations sit at 25px over paint. 300 is the lightest that still holds
        # at that size; 200 disappears into the plate.
        "anno_weight": 300,
    },
    # Same as `noir` in every respect except case. you, for the ripped news
    # collage: the band geometry and the thin your display typeface stay, the caps do not.
    "noir-lower": {
        "face": ("@font-face {{ font-family:'your display typeface'; font-weight:200; "
                 "src:url('{a}/jost-200.ttf'); }}"
                 "@font-face {{ font-family:'your display typeface'; font-weight:300; "
                 "src:url('{a}/jost-300.ttf'); }}"),
        "family": "your display typeface",
        "transform": "none",
        "tracking": "0.01em",
        "leading": 1.06,
        "pad_top": 0.0,
        "accent": f"color:{BLUE};",
        "weight": 200,
        "anno_weight": 300,
    },
}


# The band assumes a black card and white type everywhere. The candidate side needs one card
# whose plate is painted noir on PAPER, where white type is invisible and a fade to black would
# put a dark slab across a light picture. `ground="light"` flips exactly four things: the card
# background, the copy colour, the annotation fill and the direction both fades run.
# Default stays "dark", so every existing card renders byte-identical. you, .
GROUNDS = {
    "dark":  dict(bg="#000", ink="#fff", fade="0,0,0", anno="#fff"),
    "light": dict(bg="#f3ece1", ink="#0a0a0a", fade="243,236,225", anno="#0a0a0a"),
}


def css_for(theme="anton", assets=None, ground="dark"):
    t = THEMES[theme]
    a = ASSETS if assets is None else assets
    g = GROUNDS[ground]
    anno_w = t.get("anno_weight", 500)
    return f"""
{t["face"].format(a=a)}
/* your display typeface is always available to the overlay layer, whatever theme the band is on, because
   plate annotations are set in it regardless of what the band uses. */
@font-face {{ font-family:'your display typeface'; font-weight:300; src:url('{a}/jost-300.ttf'); }}
@font-face {{ font-family:'your display typeface'; font-weight:500; src:url('{a}/jost-500.ttf'); }}
.anno {{ font-family:'your display typeface'; font-weight:{anno_w}; font-size:25px; letter-spacing:0.09em;
        fill:{g["anno"]}; fill-opacity:0.88; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:{W}px; height:{H}px; overflow:hidden; background:{g["bg"]}; }}
.card {{ position:relative; width:{W}px; height:{H}px; background:{g["bg"]}; overflow:hidden; }}
/* Optional image plate. It fills the dead space ABOVE the band and never enters it, so
   the bottom-band law is untouched: the band still carries one block of type and nothing
   else. Falls off to black at its lower edge so the join is invisible. */
.plate {{ position:absolute; left:0; top:0; width:{W}px; height:{PLATE}px;
        object-fit:cover; object-position:center; }}
.overlay {{ position:absolute; left:0; top:0; pointer-events:none; }}
.plate-fade {{ position:absolute; left:0; width:{W}px; height:180px;
        top:calc({H}px - {WELL}px - 180px);
        background:linear-gradient(to bottom, rgba({g["fade"]},0), {g["bg"]}); }}
/* The full-bleed variant. `.plate-fade` assumes the plate STOPS above the band and dies into
   black; a bleeding plate has picture all the way down, so the fade has to climb the well from
   the bottom edge instead of landing on top of it. Never full black at the foot, or the bleed
   is pointless: it darkens the picture enough to carry white type and no further. */
.plate-bleed-fade {{ position:absolute; left:0; bottom:0; width:{W}px; height:{BLEEDFADE}px;
        background:linear-gradient(to top, rgba({g["fade"]},0.94) 0%, rgba({g["fade"]},0.88) 26%,
                                   rgba({g["fade"]},0.70) 48%, rgba({g["fade"]},0.38) 72%,
                                   rgba({g["fade"]},0) 100%); }}
/* The well IS the bottom band. Nothing renders above it.
   `--lift` raises the whole block off the bottom edge. It is 0 everywhere by default, so the
   law is unchanged; the lead-magnet split screen sets it because that card's copy sits over a
   photograph on both sides rather than over black. */
.well {{ position:absolute; left:0; right:0; bottom:var(--lift, 0px); height:{WELL}px;
        padding:0 {PAD}px {PAD}px; display:flex; flex-direction:column;
        justify-content:flex-end; overflow:hidden; }}
.copy {{ font-family:'{t["family"]}'; font-weight:{t.get("weight", 400)}; color:{g["ink"]};
        text-transform:{t["transform"]};
        letter-spacing:{t["tracking"]}; line-height:{t["leading"]}; }}
.copy .line {{ white-space:nowrap; }}
/* the span is what carries the text width; the div is always the full column */
.copy .ln {{ display:inline-block; white-space:nowrap; }}
.accent {{ {t["accent"]} }}
/* The divider rule (you, canonical on the inverted ends of a Theme B carousel).
   It runs the TYPE'S measure, not the card's: from the well's left padding to its right, which
   is exactly where the copy lands because the band justifies flush on both margins. A
   full-bleed version was tried first and rejected on .
   It sits on the card rather than inside `.well` so its `top` can be set independently, and
   the fit pass sets that once the copy block's height is known, because the height is not
   knowable until the type has been broken and sized. Hidden until then, so a card that somehow
   skips the fit pass shows no rule rather than one across the middle of the picture. */
.divider {{ position:absolute; left:{PAD}px; width:{W - 2 * PAD}px; height:2px;
        background:{g["ink"]}; display:none; }}
#rule {{ position:absolute; visibility:hidden; white-space:nowrap;
        font-family:'{t["family"]}'; font-weight:{t.get("weight", 400)}; font-size:100px;
        letter-spacing:{t["tracking"]}; text-transform:{t["transform"]}; }}
"""


CSS = css_for               # the default theme, kept for callers that read CSS directly

# Line breaking is a fit problem, not an authoring one. One size for the whole card; the
# breaks are chosen so the lines come out near-equal in length, and each line is then
# tracked out to sit flush on both margins. More lines means smaller type, so walk the
# counts and keep the largest stack that still clears the band.
FIT_JS = """
var WORDS = __WORDS__;
// fonts.ready alone is a trap here: the card starts empty, so nothing has requested the
// face and the promise resolves instantly against fallback metrics. Ask for it by name.
document.fonts.load('__WEIGHT__ 100px "__FAMILY__"', 'AZ09').then(function{
  return document.fonts.ready;
}).then(function{
  var well=document.querySelector('.well'), copy=document.querySelector('.copy');
  var ruler=document.getElementById('rule');
  var cs=getComputedStyle(well);
  var avail=well.clientHeight-parseFloat(cs.paddingTop)-parseFloat(cs.paddingBottom);
  var base=well.clientWidth-parseFloat(cs.paddingLeft)-parseFloat(cs.paddingRight);
  var REF=100, memo={};
  function natural(i,j){                     // width of words[i..j) at REF px
    var k=i+':'+j;
    if(memo[k]==null){
      ruler.textContent=WORDS.slice(i,j).map(function(w){return w.t;}).join(' ');
      memo[k]=ruler.offsetWidth;
    }
    return memo[k];
  }
  // Balanced break into n lines: minimise the spread of the natural line widths, which is
  // what keeps the tracking needed to justify each line small and even.
  function breakInto(n){
    var W=WORDS.length;
    if(n>W) return null;
    var best={}, from={};
    function key(i,l){ return i+'|'+l; }
    function solve(i,l){
      var k=key(i,l);
      if(best[k]!==undefined) return best[k];
      if(l===1){ best[k]=(i<W)?{cost:0, widths:[natural(i,W)]}:null; return best[k]; }
      var out=null;
      for(var j=i+1;j<=W-(l-1);j++){
        var rest=solve(j,l-1);
        if(!rest) continue;
        var widths=[natural(i,j)].concat(rest.widths);
        var mean=0; for(var q=0;q<widths.length;q++) mean+=widths[q];
        mean/=widths.length;
        var v=0; for(var q=0;q<widths.length;q++) v+=Math.pow(widths[q]-mean,2);
        if(out===null||v<out.cost) out={cost:v, widths:widths, cut:j};
      }
      best[k]=out; from[k]=out?out.cut:null;
      return out;
    }
    var r=solve(0,n);
    if(!r) return null;
    var cuts=[0], i=0;
    for(var l=n;l>1;l--){ i=from[key(i,l)]; cuts.push(i); }
    cuts.push(W);
    return {cuts:cuts, widths:r.widths};
  }
  // One size, set by the longest line: that line sits flush with no tracking and every
  // other line is opened up to reach the same right margin. The size is settled against
  // the painted spans, not the ruler, so accent markup and tracking cannot skew it.
  function paint(plan){
    copy.innerHTML='';
    var spans=[];
    for(var i=0;i<plan.widths.length;i++){
      var d=document.createElement('div'), s=document.createElement('span');
      d.className='line';
      s.className='ln';
      s.innerHTML=WORDS.slice(plan.cuts[i],plan.cuts[i+1])
.map(function(w){return w.h;}).join(' ');
      d.appendChild(s);
      copy.appendChild(d);
      spans.push(s);
    }
    function widest{
      var m=0;
      for(var i=0;i<spans.length;i++) m=Math.max(m, spans[i].getBoundingClientRect.width);
      return m;
    }
    var size=REF*base/Math.max.apply(null, plan.widths);
    for(var pass=0;pass<4;pass++){
      copy.style.fontSize=size+'px';
      for(var i=0;i<spans.length;i++) spans[i].style.letterSpacing='0px';
      size=size*base/widest;
    }
    copy.style.fontSize=size+'px';
    // Justify on the word gaps. Letters only take what the gaps cannot hold, and only up
    // to a hairline, because opening the letters inside a word is what reads as broken.
    // A theme can switch this off entirely and set ragged right instead.
    if(JUSTIFY) for(var i=0;i<spans.length;i++){
      var txt=spans[i].textContent;
      var gaps=txt.split(' ').length-1, chars=txt.length;
      spans[i].style.letterSpacing='0px';
      spans[i].style.wordSpacing='0px';
      var slack=base-spans[i].getBoundingClientRect.width;
      var byWord=Math.min(slack, gaps*WGMAX*size);
      if(gaps>0) spans[i].style.wordSpacing=(byWord/gaps)+'px';
      var left=slack-byWord;
      if(left>0&&chars>1) spans[i].style.letterSpacing=(left/(chars-1))+'px';
    }
    // Anton throws ink above its line box at this leading; the box cannot see it. your display typeface
    // sits inside its box, so its theme sets this to zero.
    copy.style.paddingTop=(PADTOP*size)+'px';
    return {h:copy.getBoundingClientRect.height, size:size};
  }
  // Among the line counts that clear the band, take the one whose worst line needs the
  // least stretching. Cramming in the most lines is not the goal; even colour is.
  var chosen=null, chosenScore=-1e9;
  for(var n=2;n<=Math.min(14,WORDS.length);n++){
    var plan=breakInto(n);
    if(!plan) continue;
    var r=paint(plan);
    if(r.h>avail) break;
    var spread=1-Math.min.apply(null,plan.widths)/Math.max.apply(null,plan.widths);
    var score=r.h/avail-spread;
    if(score>chosenScore){ chosen=plan; chosenScore=score; }
  }
  if(!chosen) chosen=breakInto(2);
  var r=paint(chosen);
  var n=chosen.widths.length;
  if(n>1){
    var gap=Math.min((avail-r.h)/(n-1), GAPMAX*r.size);
    if(gap>0){
      var els=copy.querySelectorAll('.line');
      for(var i=0;i<els.length-1;i++) els[i].style.marginBottom=gap+'px';
    }
  }
  // The divider sits DIVGAP above the first line of type, which is only knowable now.
  var dv=document.querySelector('.divider');
  if(dv){
    dv.style.top=Math.round(copy.getBoundingClientRect.top-DIVGAP)+'px';
    dv.style.display='block';
  }
  document.documentElement.dataset.fitted=
    n+' lines @ '+Math.round(r.size)+'px, fill '+
    Math.round(copy.getBoundingClientRect.height/avail*100)+'%';
});
""".replace("GAPMAX", str(GAP_MAX)).replace("WGMAX", str(WORD_GAP_MAX)) \
.replace("DIVGAP", str(DIV_GAP))


def fit_js_for(theme="anton"):
    t = THEMES[theme]
    return (FIT_JS.replace("__FAMILY__", t["family"])
.replace("__WEIGHT__", str(t.get("weight", 400)))
.replace("PADTOP", str(t["pad_top"]))
.replace("JUSTIFY", "true" if t.get("justify", True) else "false"))


def words(lines):
    """Flatten the authored copy to words, each carrying its own accent markup."""
    text = " ".join(lines)
    out, buf_h, buf_t, inside = [], [], [], False
    def flush:
        if buf_t:
            out.append({"h": "".join(buf_h), "t": "".join(buf_t)})
            buf_h.clear
            buf_t.clear
    i = 0
    while i < len(text):
        if text.startswith("[[", i):
            inside = True
            i += 2
        elif text.startswith("]]", i):
            inside = False
            i += 2
        elif text[i] == " ":
            flush
            i += 1
        else:
            ch = html.escape(text[i])
            buf_h.append(f'<span class="accent">{ch}</span>' if inside else ch)
            buf_t.append(text[i])
            i += 1
    flush
    return out




def render_card(lines, png, assets=None, chrome=None, plate=None, overlay=None,
                theme="anton", plate_full=False, plate_fade=False, lift=0, ground="dark",
                rule=False):
    """Render one card of copy to `png`. Returns the fit report string.

    `plate` is an optional path to an image that fills the frame ABOVE the band. The band
    itself stays pure black and keeps its single block of type, so the layout law is
    unchanged; the plate only occupies space that was previously empty.
    """
    css = css_for(theme, assets, ground)
    js = fit_js_for(theme).replace("__WORDS__", json.dumps(words(lines)))
    art = ""
    if plate:
        src = Path(plate).resolve.as_uri
        if plate_full:
            # The plate bleeds the whole frame. Added for the ripped news collage.
            # `plate_fade` climbs the well from the bottom edge; without it the type sits
            # straight on the picture, which is how this started and why it was hard to read.
            art = f'<img class="plate" src="{src}" style="height:{H}px">'
            if plate_fade:
                art += '<div class="plate-bleed-fade"></div>'
        else:
            art = f'<img class="plate" src="{src}"><div class="plate-fade"></div>'
    over = ""
    if overlay:
        over = (f'<svg class="overlay" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
                f'{overlay}</svg>')
    div = '<div class="divider"></div>' if rule else ''
    doc = (f'<meta charset="utf-8"><style>{css}</style>'
           f'<div class="card" style="--lift:{lift}px">'
           f'{art}<div class="well"><div class="copy"></div></div>'
           f'{over}{div}</div>'
           f'<div id="rule"></div><script>{js}</script>')
    with tempfile.NamedTemporaryFile("w", suffix=".html", dir=ROOT, delete=False) as f:
        f.write(doc)
        tmp = f.name
    exe = chrome or CHROME
    png = Path(png)
    png.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([exe, "--headless", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", f"--window-size={W},{H}",
                    f"--screenshot={png}", f"file://{tmp}"],
                   stderr=subprocess.DEVNULL, check=True)
    dom = subprocess.run([exe, "--headless", "--disable-gpu", "--virtual-time-budget=4000",
                          "--dump-dom", f"file://{tmp}"], capture_output=True, text=True).stdout
    Path(tmp).unlink
    m = re.search(r'data-fitted="([^"]+)"', dom)
    return m.group(1) if m else "?"
