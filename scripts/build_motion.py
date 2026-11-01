"""Precompute bidirectional optical-flow inbetweens. No model needed at runtime."""
from pathlib import Path
import cv2
import numpy as np
from PIL import Image
import json

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'app'/'motion'
OUT.mkdir(exist_ok=True)
atlas=Image.open(ROOT/'app'/'spritesheet.png').convert('RGBA')
counts=dict(zip(['idle','right','left','wave','jump','failed','waiting','working','review'],[6,8,8,4,5,8,6,6,6]))
yy,xx=np.mgrid[:208,:192].astype(np.float32)
steps=6
meta={'subframes':steps,'counts':counts,'method':'bidirectional optical flow'}
for row,(name,count) in enumerate(counts.items()):
    frames=[np.array(atlas.crop((i*192,row*208,(i+1)*192,(row+1)*208))) for i in range(count)]
    strip=Image.new('RGBA',(192*steps,count*208))
    def gray(a):
        alpha=a[:,:,3:4].astype(np.float32)/255
        rgb=a[:,:,:3]*alpha+160*(1-alpha)
        return cv2.cvtColor(rgb.astype(np.uint8),cv2.COLOR_RGB2GRAY)
    def normalize(frame):
        mask=Image.fromarray(frame[:,:,3]).point(lambda a:255 if a>=128 else 0)
        box=mask.getbbox()
        canvas=Image.new('RGBA',(192,208))
        canvas.paste(Image.fromarray(frame).crop(box).resize((160,176),Image.Resampling.LANCZOS),(16,16))
        return np.array(canvas),box
    def flow(a,b):
        engine=cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
        engine.setFinestScale(0)
        return engine.calc(gray(a),gray(b),None)
    for index,a in enumerate(frames):
        original=a
        a,box_a=normalize(a)
        b,box_b=normalize(frames[(index+1)%count])
        ab,ba=flow(a,b),flow(b,a)
        # Warp premultiplied color and alpha together to avoid dark/purple fringes.
        def premul(f):
            v=f.astype(np.float32)/255
            v[:,:,:3]*=v[:,:,3:4]
            return v
        pa,pb=premul(a),premul(b)
        for k in range(steps):
            t=k/steps
            wa=cv2.remap(pa,xx-ab[:,:,0]*t,yy-ab[:,:,1]*t,cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT)
            wb=cv2.remap(pb,xx-ba[:,:,0]*(1-t),yy-ba[:,:,1]*(1-t),cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT)
            c=wa*(1-t)+wb*t
            c[:,:,:3]/=np.maximum(c[:,:,3:4],1/255)
            # Morph the silhouettes, instead of fading two separated outlines.
            # This avoids translucent duplicate paws at larger pose changes.
            def distance(alpha):
                mask=(alpha>=.5).astype(np.uint8)
                return cv2.distanceTransform(mask,cv2.DIST_L2,5)-cv2.distanceTransform(1-mask,cv2.DIST_L2,5)
            edge=distance(wa[:,:,3])*(1-t)+distance(wb[:,:,3])*t
            c[:,:,3]=np.clip(.5+edge/2,0,1)
            normalized=Image.fromarray(np.clip(c*255,0,255).astype(np.uint8))
            box=[round(x*(1-t)+y*t) for x,y in zip(box_a,box_b)]
            out=Image.new('RGBA',(192,208))
            out.paste(normalized.crop((16,16,176,192)).resize((box[2]-box[0],box[3]-box[1]),Image.Resampling.LANCZOS),(box[0],box[1]))
            if k==0:out=Image.fromarray(original)
            strip.paste(out,(k*192,index*208))
    strip.save(OUT/f'{name}.png',optimize=True)
    print(name,count*steps,flush=True)
(OUT/'manifest.json').write_text(json.dumps(meta,indent=2))
frame=atlas.crop((0,0,192,208))
frame.save(ROOT/'site'/'assets'/'akkity.png')
frame.save(ROOT/'app'/'akkity.ico',sizes=[(32,32),(48,48),(64,64),(128,128),(192,192)])
