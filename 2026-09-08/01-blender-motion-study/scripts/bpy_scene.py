"""Spec-driven Blender scene renderer. Runs INSIDE Blender, never in your project's Python.

Invoked headless by render.py:
    blender -b --python bpy_scene.py -- <resolved-scene.json> <out_dir>

render.py has already resolved the ratio to pixel dims, absolute file paths and the font path, so this
file reads one JSON and builds the scene it describes. Everything it can build is flat, lit, matte and
deterministic: primitives, extruded text, unlit image plates, imported GLB/OBJ/FBX/SVG, a keyed
camera and keyed objects, one to three lights, an optional Freestyle line pass. There is no emission
field on a material and no bloom, by design (see the visual banlist in SKILL.md).

Scene contract (every key optional except objects and output; render.py fills the defaults):
{
  "output": {"kind": "still"|"sequence", "w": 1080, "h": 1920, "fps": 24, "seconds": 4, "frame": 1,
             "samples": 32, "transparent": false, "view_transform": "Standard"},
  "world": {"bg": [r,g,b], "strength": 1.0},
  "materials": {"matte": {"color": [r,g,b], "roughness": 0.9, "metallic": 0.0}},
  "lights": [{"type": "SUN"|"AREA"|"POINT"|"SPOT", "loc": [x,y,z], "target": [x,y,z], "energy": 4,
              "color": [r,g,b], "size": 4}],
  "camera": {"lens": 35, "loc": [x,y,z], "target": [x,y,z], "ortho": false, "ortho_scale": 10,
             "dof": {"fstop": 2.8}, "shake": 0.0, "ease": "bezier"|"linear",
             "keys": [{"frame": 1, "loc": [..], "target": [..]}, ...]},
  "objects": [
     {"type": "plane|cube|sphere|cylinder|cone|torus", "name": "", "loc": [..], "rot": [deg,deg,deg],
      "scale": [..], "size": 2, "material": "matte", "bevel": 0.0, "smooth": false, "shadow": true,
      "keys": [{"frame": 1, "loc": [..], "rot": [..], "scale": [..]}]},
     {"type": "text", "body": "...", "font": "/abs/SomeFont-Regular.ttf", "size": 1, "extrude": 0.02,
      "align": "CENTER", "material": "ink", ...transform keys as above},
     {"type": "image", "file": "/abs/plate.png", "width": 2, ...transform keys as above},
     {"type": "import", "file": "/abs/model.glb", "material": null, ...transform keys as above}
  ],
  "freestyle": {"enabled": false, "thickness": 1.5, "color": [1,1,1]}
}
"""
import json
import math
import sys
from pathlib import Path

import bpy

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
spec = json.loads(Path(argv[0]).read_text(encoding="utf-8"))
out_dir = Path(argv[1])
out_dir.mkdir(parents=True, exist_ok=True)

out = spec.get("output", {}) or {}
W, H = int(out.get("w", 1080)), int(out.get("h", 1920))
fps = int(out.get("fps", 24))
seconds = float(out.get("seconds", 4))
kind = out.get("kind", "still")
frame_end = max(1, int(round(fps * seconds))) if kind == "sequence" else 1

_fonts = {}


def _rad(v):
    return [math.radians(float(a)) for a in (v or [0, 0, 0])]


def _font(path):
    if not path:
        return None
    if path not in _fonts:
        _fonts[path] = bpy.data.fonts.load(path)
    return _fonts[path]


# --- clean slate -------------------------------------------------------------
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
for coll in (bpy.data.materials, bpy.data.meshes, bpy.data.lights, bpy.data.cameras):
    for d in list(coll):
        coll.remove(d)

scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = frame_end
scene.render.fps = fps

ease = (spec.get("camera", {}) or {}).get("ease", "bezier")
bpy.context.preferences.edit.keyframe_new_interpolation_type = "LINEAR" if ease == "linear" else "BEZIER"

# --- materials (matte only, no emission by design) --------------------------
materials = {}


def _material(name, m):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        c = m.get("color", [0.55, 0.55, 0.58])
        bsdf.inputs["Base Color"].default_value = (c[0], c[1], c[2], 1.0)
        bsdf.inputs["Roughness"].default_value = float(m.get("roughness", 0.9))
        bsdf.inputs["Metallic"].default_value = float(m.get("metallic", 0.0))
    return mat


for name, m in (spec.get("materials") or {}).items():
    materials[name] = _material(name, m)
if "matte" not in materials:
    materials["matte"] = _material("matte", {"color": [0.55, 0.55, 0.58]})


def _assign(ob, name):
    mat = materials.get(name) or materials["matte"]
    if hasattr(ob.data, "materials"):
        ob.data.materials.clear()
        ob.data.materials.append(mat)


def _image_material(path):
    """Unlit plate: the image's own colours, untouched by scene light. Flat, not glowing."""
    img = bpy.data.images.load(path)
    mat = bpy.data.materials.new("plate_" + Path(path).stem)
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    outn = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Strength"].default_value = 1.0
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    nt.links.new(tex.outputs["Color"], em.inputs["Color"])
    nt.links.new(em.outputs["Emission"], outn.inputs["Surface"])
    return mat, img


# --- objects ---------------------------------------------------------------
PRIMS = {
    "plane": lambda s, loc: bpy.ops.mesh.primitive_plane_add(size=s, location=loc),
    "cube": lambda s, loc: bpy.ops.mesh.primitive_cube_add(size=s, location=loc),
    "sphere": lambda s, loc: bpy.ops.mesh.primitive_uv_sphere_add(radius=s / 2, location=loc),
    "cylinder": lambda s, loc: bpy.ops.mesh.primitive_cylinder_add(radius=s / 2, depth=s, location=loc),
    "cone": lambda s, loc: bpy.ops.mesh.primitive_cone_add(radius1=s / 2, depth=s, location=loc),
    "torus": lambda s, loc: bpy.ops.mesh.primitive_torus_add(major_radius=s / 2, minor_radius=s / 8, location=loc),
}


def _transform(ob, o):
    ob.location = o.get("loc", ob.location)
    if "rot" in o:
        ob.rotation_euler = _rad(o["rot"])
    if "scale" in o:
        ob.scale = o["scale"]


def _keys(ob, keys):
    for k in keys or []:
        f = int(k.get("frame", 1))
        if "loc" in k:
            ob.location = k["loc"]
            ob.keyframe_insert("location", frame=f)
        if "rot" in k:
            ob.rotation_euler = _rad(k["rot"])
            ob.keyframe_insert("rotation_euler", frame=f)
        if "scale" in k:
            ob.scale = k["scale"]
            ob.keyframe_insert("scale", frame=f)


def _finish(ob, o):
    if o.get("name"):
        ob.name = o["name"]
    _transform(ob, o)
    if o.get("bevel", 0) and ob.type == "MESH":
        m = ob.modifiers.new("bevel", "BEVEL")
        m.width = float(o["bevel"])
        m.segments = 3
    if o.get("smooth") and ob.type == "MESH":
        for p in ob.data.polygons:
            p.use_smooth = True
    if o.get("shadow", True) is False:
        try:
            ob.visible_shadow = False
        except Exception:
            pass
    _keys(ob, o.get("keys"))


for o in spec.get("objects", []):
    t = o.get("type", "cube")
    loc = o.get("loc", [0, 0, 0])
    if t in PRIMS:
        PRIMS[t](float(o.get("size", 2)), loc)
        ob = bpy.context.active_object
        _assign(ob, o.get("material", "matte"))
    elif t == "text":
        bpy.ops.object.text_add(location=loc)
        ob = bpy.context.active_object
        ob.data.body = o.get("body", "")
        fnt = _font(o.get("font"))
        if fnt:
            ob.data.font = fnt
        ob.data.size = float(o.get("size", 1))
        ob.data.extrude = float(o.get("extrude", 0.0))
        ob.data.align_x = o.get("align", "CENTER")
        ob.data.align_y = o.get("align_y", "CENTER")
        _assign(ob, o.get("material", "matte"))
    elif t == "image":
        mat, img = _image_material(o["file"])
        w = float(o.get("width", 2))
        h = w * img.size[1] / max(1, img.size[0])
        bpy.ops.mesh.primitive_plane_add(size=1, location=loc)
        ob = bpy.context.active_object
        ob.scale = [w, h, 1]
        ob.data.materials.append(mat)
        o = {**o, "scale": o.get("scale", [w, h, 1])}
    elif t == "import":
        f = o["file"]
        ext = Path(f).suffix.lower()
        bpy.ops.object.select_all(action="DESELECT")
        if ext in (".glb", ".gltf"):
            bpy.ops.import_scene.gltf(filepath=f)
        elif ext == ".obj":
            bpy.ops.wm.obj_import(filepath=f)
        elif ext == ".fbx":
            bpy.ops.import_scene.fbx(filepath=f)
        elif ext == ".svg":
            if hasattr(bpy.ops.wm, "svg_import"):
                bpy.ops.wm.svg_import(filepath=f)
            else:
                bpy.ops.import_curve.svg(filepath=f)
        else:
            raise SystemExit(f"unsupported import: {f}")
        imported = list(bpy.context.selected_objects)
        bpy.ops.object.empty_add(location=(0, 0, 0))
        ob = bpy.context.active_object
        for child in imported:
            if child.parent is None:
                child.parent = ob
            if o.get("material"):
                _assign(child, o["material"])
    else:
        raise SystemExit(f"unknown object type: {t}")
    _finish(ob, o)

# --- camera ------------------------------------------------------------------
cam_s = spec.get("camera", {}) or {}
keys = cam_s.get("keys") or []
first_loc = keys[0]["loc"] if keys and "loc" in keys[0] else cam_s.get("loc", [0, -12, 4])
first_tgt = keys[0].get("target") if keys else None
first_tgt = first_tgt or cam_s.get("target", [0, 0, 1])

bpy.ops.object.empty_add(location=first_tgt)
target = bpy.context.active_object
target.name = "cam_target"
bpy.ops.object.camera_add(location=first_loc)
cam = bpy.context.active_object
cam.name = "cam"
cam.data.lens = float(cam_s.get("lens", 35))
if cam_s.get("ortho"):
    cam.data.type = "ORTHO"
    cam.data.ortho_scale = float(cam_s.get("ortho_scale", 10))
trk = cam.constraints.new(type="TRACK_TO")
trk.target = target
trk.track_axis = "TRACK_NEGATIVE_Z"
trk.up_axis = "UP_Y"
scene.camera = cam
dof = cam_s.get("dof")
if dof:
    cam.data.dof.use_dof = True
    cam.data.dof.focus_object = target
    cam.data.dof.aperture_fstop = float(dof.get("fstop", 2.8))
for k in keys:
    f = int(k.get("frame", 1))
    if "loc" in k:
        cam.location = k["loc"]
        cam.keyframe_insert("location", frame=f)
    if "target" in k:
        target.location = k["target"]
        target.keyframe_insert("location", frame=f)
    if "lens" in k:
        cam.data.lens = float(k["lens"])
        cam.data.keyframe_insert("lens", frame=f)

shake = float(cam_s.get("shake", 0.0))
if shake > 0:
    try:
        ad = cam.animation_data
        act = ad.action if ad else None
        fcs = list(getattr(act, "fcurves", []) or []) if act else []
        if not fcs and act:
            for layer in getattr(act, "layers", []):
                for strip in getattr(layer, "strips", []):
                    cb = strip.channelbag(ad.action_slot) if hasattr(strip, "channelbag") and ad.action_slot else None
                    fcs += list(getattr(cb, "fcurves", []) if cb else [])
        for fc in fcs:
            if fc.data_path == "location":
                m = fc.modifiers.new(type="NOISE")
                m.strength = shake
                m.scale = max(1.0, fps / 3.0)
    except Exception as exc:  # noqa: BLE001
        print("SCENE shake skipped:", exc)

# --- lights ------------------------------------------------------------------
lights = spec.get("lights") or [{"type": "SUN", "loc": [6, -8, 20], "energy": 4.0, "rot": [35, 10, 25]}]
for i, L in enumerate(lights[:3]):
    bpy.ops.object.light_add(type=L.get("type", "SUN"), location=L.get("loc", [6, -8, 20]))
    lt = bpy.context.active_object
    lt.name = f"light_{i}"
    lt.data.energy = float(L.get("energy", 4.0))
    c = L.get("color", [1, 1, 1])
    lt.data.color = (c[0], c[1], c[2])
    if L.get("type") == "AREA":
        lt.data.size = float(L.get("size", 4))
        lt.data.shape = "SQUARE"
    if L.get("type") == "SPOT":
        lt.data.spot_size = math.radians(float(L.get("spot", 45)))
    if L.get("type", "SUN") == "SUN":
        lt.data.angle = math.radians(float(L.get("soft", 2)))
    if "target" in L:
        bpy.ops.object.empty_add(location=L["target"])
        te = bpy.context.active_object
        te.name = f"light_target_{i}"
        c2 = lt.constraints.new(type="TRACK_TO")
        c2.target = te
        c2.track_axis = "TRACK_NEGATIVE_Z"
        c2.up_axis = "UP_Y"
    elif "rot" in L:
        lt.rotation_euler = _rad(L["rot"])

# --- world -------------------------------------------------------------------
wd = spec.get("world", {}) or {}
world = bpy.data.worlds.new("W")
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
if bg:
    c = wd.get("bg", [0.13, 0.15, 0.18])
    bg.inputs[0].default_value = (c[0], c[1], c[2], 1.0)
    bg.inputs[1].default_value = float(wd.get("strength", 1.0))

# --- freestyle (optional line pass) -----------------------------------------
fs = spec.get("freestyle") or {}
scene.render.use_freestyle = bool(fs.get("enabled", False))
if scene.render.use_freestyle:
    scene.render.line_thickness = float(fs.get("thickness", 1.5))
    try:
        fss = bpy.context.view_layer.freestyle_settings
        ls = fss.linesets.new("lines") if not fss.linesets else fss.linesets[0]
        c = fs.get("color", [1, 1, 1])
        ls.linestyle.color = (c[0], c[1], c[2])
    except Exception as exc:  # noqa: BLE001
        print("SCENE freestyle lineset skipped:", exc)

# --- render ------------------------------------------------------------------
engines = {e.identifier for e in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items}
scene.render.engine = "BLENDER_EEVEE" if "BLENDER_EEVEE" in engines else sorted(engines)[0]
scene.render.resolution_x = W
scene.render.resolution_y = H
scene.render.resolution_percentage = 100
scene.render.film_transparent = bool(out.get("transparent", False))
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGBA" if scene.render.film_transparent else "RGB"
try:
    scene.eevee.taa_render_samples = int(out.get("samples", 32))
    if hasattr(scene.eevee, "use_shadows"):
        scene.eevee.use_shadows = True
except Exception as exc:  # noqa: BLE001
    print("SCENE eevee settings skipped:", exc)
try:
    scene.view_settings.view_transform = out.get("view_transform", "Standard")
    scene.view_settings.look = "None"
except Exception as exc:  # noqa: BLE001
    print("SCENE view transform skipped:", exc)

print(f"SCENE engine={scene.render.engine} dims={W}x{H} kind={kind} frames={scene.frame_start}-{scene.frame_end}")
if kind == "sequence":
    frames = out_dir / "frames"
    frames.mkdir(parents=True, exist_ok=True)
    scene.render.filepath = str(frames / "f_")
    bpy.ops.render.render(animation=True)
else:
    scene.frame_set(int(out.get("frame", 1)))
    scene.render.filepath = str(out_dir / "still.png")
    bpy.ops.render.render(write_still=True)
print("SCENE DONE")
