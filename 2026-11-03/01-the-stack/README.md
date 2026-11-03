# The stack

The tools for AI video editing and animation, open source first, with a link to each one.

Before you install any of them, check it first. Download it into a new, empty folder, scan it with
[NVIDIA SkillSpector](https://github.com/NVIDIA/skillspector) (the `2026-10-27/` folder shows how),
and note the version number you checked.

## The tools

| Tool | What it does | Link |
|---|---|---|
| HyperFrames | Writes video as HTML and renders it frame by frame. Everything else plugs into it | [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) |
| GSAP | Timelines and easing for type and shapes | [greensock/GSAP](https://github.com/greensock/GSAP) |
| Remotion | Video as React components | [remotion-dev/remotion](https://github.com/remotion-dev/remotion) |
| Lottie | Vector animation you can write as code | [airbnb/lottie-web](https://github.com/airbnb/lottie-web) |
| Three.js | 3D scenes and camera moves | [mrdoob/three.js](https://github.com/mrdoob/three.js) |
| p5.js | Drawing in code | [processing/p5.js](https://github.com/processing/p5.js) |
| p5.brush | Brush and paint strokes on top of p5.js | [acamposuribe/p5.brush](https://github.com/acamposuribe/p5.brush) |
| PixiJS | Fast 2D graphics and particles | [pixijs/pixijs](https://github.com/pixijs/pixijs) |
| flubber | Smooth morphs from one shape to another | [veltman/flubber](https://github.com/veltman/flubber) |
| Matter.js | 2D physics: things that fall, bounce and stack | [liabru/matter-js](https://github.com/liabru/matter-js) |
| Rough.js | A hand drawn, sketchy look | [pshihn/rough](https://github.com/pshihn/rough) |
| mo.js | Bursts and small motion effects | [mojs/mojs](https://github.com/mojs/mojs) |
| D3 | Charts and data driven shapes | [d3/d3](https://github.com/d3/d3) |
| NumberFlow | Numbers that count and roll | [barvian/number-flow](https://github.com/barvian/number-flow) |
| Satori | Turns HTML and CSS into images | [vercel/satori](https://github.com/vercel/satori) |
| Playwright | Drives a headless browser, so your agent can check every frame | [microsoft/playwright](https://github.com/microsoft/playwright) |
| FFmpeg | Cuts, joins and encodes the video and audio | [ffmpeg.org](https://ffmpeg.org) |
| whisper.cpp | Speech to text on your own machine, with a time for every word | [ggml-org/whisper.cpp](https://github.com/ggml-org/whisper.cpp) |
| earshot | Sound effects made in code | [Leonxlnx/earshot](https://github.com/Leonxlnx/earshot) |
| ElevenLabs | Voiceover and sound effects from text (paid service) | [elevenlabs.io](https://elevenlabs.io/docs) |
| Higgsfield | Generated images and video clips (paid service) | [higgsfield.ai](https://higgsfield.ai) |

## Put it together yourself

A content pipeline has four stages. You can start with one tool at each.

| Stage | What you need |
|---|---|
| Data | Your own call recordings and your post numbers. [Apify](https://apify.com) if you want to pull posts from accounts you study |
| Ideas | A coding agent such as [Claude Code](https://github.com/anthropics/claude-code), plus a SKILL.md that holds your own content rules |
| Production | HyperFrames and the libraries above. A paid image, video or voice service only where code cannot draw it |
| Posting | A scheduler with an API, such as [Buffer](https://buffer.com), and you approve the words before anything posts |

Two habits make it work. Have your agent render the film in sections, so a note on one shot redoes
only that section. And keep your rules in plain SKILL.md files, separate from the code, so you can
change how it writes without touching how it renders.

For the skills side, see `2026-08-11/content-formats/`, `2026-08-18/content-operating-system/` and
`2026-09-08/02-content-machine/` in this repo.
