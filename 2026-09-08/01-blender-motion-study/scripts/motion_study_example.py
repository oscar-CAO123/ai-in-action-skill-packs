"""Five-second motion study: rapid recomposition and a weighted whole-object handoff. No external assets.

Run through monitor_render.py:
    python3 monitor_render.py motion_study_example.py <out_dir> proof
    python3 monitor_render.py motion_study_example.py <out_dir> animation

White constant-colour objects on pure black, 1080 x 1920, 60 fps, 300 frames, CPU Cycles at 8 samples.
The objects here (a compression, a pinball machine, a tree) are the study's own. Write your own
objects for your own script; inherit the timing, the holds and the two lanes, never the storyboard.
"""
import bpy, math, sys, json
from pathlib import Path
from mathutils import Vector

out=Path(sys.argv[sys.argv.index('--')+1]);mode=sys.argv[-1];out.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=8
s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=3
s.render.resolution_x=1080;s.render.resolution_y=1920;s.render.resolution_percentage=50 if mode=='proof' else 100
s.render.fps=60;s.frame_start=1;s.frame_end=300;s.render.image_settings.file_format='PNG'
s.world.color=(0,0,0);s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(0,0,0,1)
s.view_settings.view_transform='Standard';s.view_settings.look='None'
mat=bpy.data.materials.new('Constant white, no bloom');mat.use_nodes=True
n=mat.node_tree.nodes;n.clear();em=n.new('ShaderNodeEmission');em.inputs[0].default_value=(1,1,1,1)
mo=n.new('ShaderNodeOutputMaterial');mat.node_tree.links.new(em.outputs[0],mo.inputs['Surface'])
bpy.ops.object.camera_add(location=(0,-10,0));cam=bpy.context.object
cam.rotation_euler=(Vector((0,0,0))-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.type='ORTHO';cam.data.ortho_scale=6.3;s.camera=cam

def root(name):
 o=bpy.data.objects.new(name,None);s.collection.objects.link(o);return o
course=root('Pinball mechanism');tree=root('Branching action');intro=root('Compression')
def curve(name,pts,parent=course,width=.009,closed=False):
 if closed:pts=list(pts)+[pts[0]]
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=width;c.bevel_resolution=2
 sp=c.splines.new('POLY');sp.points.add(len(pts)-1)
 for p,(x,z) in zip(sp.points,pts):p.co=(x,0,z,1)
 sp.use_cyclic_u=False
 o=bpy.data.objects.new(name,c);s.collection.objects.link(o);o.parent=parent;c.materials.append(mat);return o
def disk(name,x,z,r,parent=course,count=32):
 m=bpy.data.meshes.new(name);m.from_pydata([(r*math.cos(i*math.tau/count),0,r*math.sin(i*math.tau/count)) for i in range(count)],[],[tuple(range(count))])
 o=bpy.data.objects.new(name,m);s.collection.objects.link(o);o.parent=parent;o.location=(x,-.018,z);m.materials.append(mat);return o
def ring(name,x,z,r,parent=course,width=.008):
 return curve(name,[(x+r*math.cos(i*math.tau/64),z+r*math.sin(i*math.tau/64)) for i in range(64)],parent,width,True)
def clamp(x):return max(0,min(1,x))
def ease(x):x=clamp(x);return x*x*x*(x*(x*6-15)+10)
def key(o,prop,f):o.keyframe_insert(prop,frame=f)
def scale(o,v,f):o.scale=(v,v,v);key(o,'scale',f)

triangles=[]
for sign in [1,-1]:
 m=bpy.data.meshes.new('Triangle');m.from_pydata([(-.60,0,0),(.60,0,0),(0,0,.60*sign)],[],[(0,1,2)])
 o=bpy.data.objects.new('Compression jaw',m);s.collection.objects.link(o);o.parent=intro;m.materials.append(mat);triangles.append(o)
bars=[curve('Compressed link', [(-.21,-.45+j*.10),(.21,-.45+j*.10)],intro,.007) for j in range(10)]
core=disk('Continuous diamond to round core',0,0,1,intro,64)

# The core becomes the central bumper, while the surrounding mechanism draws into place.
bumpers=[(0,.55,.18),(-.36,-.08,.145),(.36,-.08,.145)]
parts=[]
for i,(x,z,r) in enumerate(bumpers):
 parts.append((disk('Bumper face',x,z,r*.65),1.00+i*.035))
 parts.append((ring('Bumper rim',x,z,r),1.02+i*.035))
 for j in range(20):
  a=j*math.tau/20
  parts.append((curve('Bumper notch',[(x+r*.83*math.cos(a),z+r*.83*math.sin(a)),(x+r*math.cos(a),z+r*math.sin(a))],width=.005),1.03+i*.035))
outline=[]
for j in range(33):
 a=j*math.pi/32;outline.append((.79*math.cos(a),.72+.79*math.sin(a)))
for j in range(33):
 a=math.pi+j*math.pi/32;outline.append((.79*math.cos(a),-.72+.79*math.sin(a)))
parts.append((curve('Outer capsule',outline,width=.010,closed=True),1.12))
for x in [-.40,0,.40]:
 pts=[(x+.055*math.cos(a*math.tau/24),.94+.16*math.sin(a*math.tau/24)) for a in range(24)]
 parts.append((curve('Upper lane',pts,width=.006,closed=True),1.10))
for side in [-1,1]:
 for j in range(8):parts.append((disk('Guide pin',side*(.64-.016*j),.45-j*.15,.012),1.09+j*.010))
flippers=[]
for side in [-1,1]:
 r=root('Flipper pivot');r.parent=course;r.location=(side*.52,0,-.91)
 flippers.append(r)
 pts=[(0,0),(-side*.38,.13)]
 parts.append((curve('Flipper',pts,r,.031),1.04))
 parts.append((disk('Flipper axle',0,0,.043,r),1.04))
ball=disk('Moving ball',.30,1.1,.055)

# Deterministic planar gravity and restitution at capsule, circular bumpers and flippers.
dt=1/240;pos=Vector((.24,1.08));vel=Vector((-.35,-.40));trajectory=[];contacts=[]
def rebound(normal,penetration,stamp,label):
 global pos,vel
 pos+=normal*penetration
 vn=vel.dot(normal)
 if vn<0:vel-=1.84*vn*normal;contacts.append({'t':round(stamp,4),'target':label})
for step in range(1201):
 t=step*dt
 if t>=1.12:
  vel.y-=2.8*dt;pos+=vel*dt
  centre=Vector((0,max(-.72,min(.72,pos.y))));delta=pos-centre
  if delta.length>.735:rebound(-delta.normalized(),delta.length-.735,t,'wall')
  for x,z,r in bumpers:
   delta=pos-Vector((x,z));limit=r+.055
   if 0<delta.length<limit:rebound(delta.normalized(),limit-delta.length,t,'bumper')
  for side in [-1,1]:
   a=Vector((side*.52,-.91));b=a+Vector((-side*.38,.13));ab=b-a
   p=a+ab*clamp((pos-a).dot(ab)/ab.length_squared);delta=pos-p
   if 0<delta.length<.086:rebound(delta.normalized(),.086-delta.length,t,'flipper')
 trajectory.append(tuple(pos))

# A growing tree uses one connected branching construction, rather than random debris.
branches=[]
def branch(a,b,depth):
 branches.append((curve('Growing branch',[a,b],tree,.010 if depth>1 else .006),depth))
 if depth<=0:return
 v=Vector(b)-Vector(a);ang=math.atan2(v.y,v.x);length=v.length*.69
 for da in [-.52,.48]:
  end=(b[0]+length*math.cos(ang+da),b[1]+length*math.sin(ang+da));branch(b,end,depth-1)
branch((0,-.95),(0,-.12),4)
seed=disk('Root diamond',0,-.95,.15,tree,4)

for f in range(1,301):
 t=(f-1)/60
 close=ease((t-.28)/.38)
 for i,o in enumerate(triangles):
  o.location.z=[1,-1][i]*.52*(1-close);key(o,'location',f);scale(o,1 if t<.67 else 0,f)
 for o in bars:scale(o,1-close,f)
 u=ease((t-.67)/.24)
 for j,v in enumerate(core.data.vertices):
  a=j*math.tau/64;r=.60/(abs(math.cos(a))+abs(math.sin(a)))
  r=(r*(1-u)+.11*u)
  v.co=(r*math.cos(a),0,r*math.sin(a));v.keyframe_insert('co',frame=f)
 scale(core,1 if .67<=t<1.24 else 0,f)
 core.location.z=.55*ease((t-.91)/.17);key(core,'location',f)
 for o,start in parts:
  q=ease((t-start)/.24)
  if o.type=='CURVE':o.data.bevel_factor_end=q;o.data.keyframe_insert('bevel_factor_end',frame=f)
  else:scale(o,q,f)
 # Core face reaches its final size before the bridge disappears.
 scale(ball,ease((t-1.10)/.10),f);p=trajectory[min(1200,round(t/dt))];ball.location=(p[0],-.025,p[1]);key(ball,'location',f)
 # Whole mechanism accelerates out; the tree brakes into the same centre.
 course.location.x=-3.5*ease((t-3.24)/.36);key(course,'location',f)
 q=t-3.22
 if q<0:x=3.5;angle=0
 elif q<.38:
  u=q/.38;x=(2*u**3-3*u*u+1)*3.5+(u**3-2*u*u+u)*(-6)*.38+(u**3-u*u)*(-.25)*.38;angle=-.055*ease(u)
 else:
  v=q-.38;x=(-.25/17)*math.exp(-10*v)*math.sin(17*v);angle=-.055*math.exp(-9*v)*(math.cos(17*v)+9/17*math.sin(17*v))
 tree.location.x=x;tree.rotation_euler.y=angle;key(tree,'location',f);key(tree,'rotation_euler',f)
 for o,depth in branches:
  start=3.14+(4-depth)*.17;o.data.bevel_factor_end=ease((t-start)/.17);o.data.keyframe_insert('bevel_factor_end',frame=f)
 scale(seed,ease((t-3.12)/.18),f)

s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(out/'motion-study.blend'))
(out/'motion.json').write_text(json.dumps({'duration':5,'fps':60,'samples':8,'threads':3,'device':'CPU','physics':'2D gravity with restitution .84 against capsule, three circular bumpers and fixed flipper segments; handoff is authored kinematics','contacts':contacts,'lanes':['rapid core-mediated recomposition','weighted whole-object handoff'],'limitations':['Not frame-accurate source duplication','No 3D rigid body, cloth, fluid, glow or GPU rendering','Fixed flippers, collision response belongs to the ball']},indent=2))
folder=out/('proofs' if mode=='proof' else 'frames');folder.mkdir(exist_ok=True)
selected=([1,35,48,60,73,91,150,209,233,283] if mode=='proof' else range(65,77) if mode=='repair' else range(188,301) if mode=='handoff-repair' else range(188,243) if mode=='branch-repair' else range(1,301))
for f in selected:
 s.frame_set(f);s.render.filepath=str(folder/f'{f:04d}.png');bpy.ops.render.render(write_still=True)
