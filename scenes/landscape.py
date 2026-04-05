"""
Landscape scene - country road with petals, walkers, carriage
draw_frame(image, now, mpd, scroll_x) を main.py から呼ぶ
"""
from PIL import Image, ImageDraw, ImageFont
from scenes.common import *
import random, math, datetime, subprocess

W2, H2 = 320, 240
VP_X = W2 * 0.50
VP_Y = H2 * 0.42
ROAD_W_NEAR = 130
ROAD_W_FAR  = 10

def road_x(t, side):
    half_w = (ROAD_W_FAR + (ROAD_W_NEAR - ROAD_W_FAR) * t) / 2
    cx = VP_X + (W2/2 - VP_X) * t
    return cx + side * half_w

def road_y(t):
    return VP_Y + (H2 - VP_Y) * t

def pscale(t):
    return 0.08 + 0.92 * t

def tw2(text, font):
    d = ImageDraw.Draw(Image.new("RGB",(1,1)))
    b = d.textbbox((0,0),text,font=font)
    return b[2]-b[0]

# ── 背景（時間帯対応） ────────────────────────────────────
def get_palette(hour):
    if 5 <= hour < 8:
        return dict(sky_top=(220,170,140),sky_bot=(240,210,170),gnd_top=(70,95,50),gnd_bot=(40,60,30),grass=(65,100,45))
    elif 8 <= hour < 17:
        return dict(sky_top=(155,200,115),sky_bot=(190,215,150),gnd_top=(75,110,55),gnd_bot=(35,70,28),grass=(70,110,48))
    elif 17 <= hour < 20:
        return dict(sky_top=(80,40,80),sky_bot=(230,100,40),gnd_top=(60,50,35),gnd_bot=(25,20,15),grass=(55,60,30))
    else:
        return dict(sky_top=(8,10,35),sky_bot=(25,30,65),gnd_top=(25,35,22),gnd_bot=(10,15,8),grass=(30,45,20))

_bg_cache  = None
_bg_hour   = -1

def _build_bg(hour):
    img = Image.new("RGB",(W2,H2))
    d   = ImageDraw.Draw(img)
    pal = get_palette(hour)
    st,sb = pal['sky_top'],pal['sky_bot']
    for y in range(int(VP_Y)+1):
        t = y/max(1,VP_Y)
        d.line([(0,y),(W2,y)], fill=tuple(int(st[i]+(sb[i]-st[i])*t) for i in range(3)))

    # 星（夜）
    if hour>=20 or hour<5:
        rng=random.Random(99)
        for _ in range(55):
            sx=rng.randint(0,W2); sy=rng.randint(0,int(VP_Y)-2); br=rng.randint(160,255)
            d.point((sx,sy),fill=(br,br,min(255,br+20)))

    # 光
    for i in range(20,0,-1):
        ov=Image.new("RGBA",img.size,(0,0,0,0))
        od=ImageDraw.Draw(ov)
        od.ellipse([W2-i*7,-i*7,W2+i*7,i*7],fill=(255,240,180,i*7))
        img.paste(ov,mask=ov)

    # 地面
    gt,gb=pal['gnd_top'],pal['gnd_bot']
    for y in range(int(VP_Y),H2):
        t=(y-VP_Y)/(H2-VP_Y)
        d.line([(0,y),(W2,y)],fill=tuple(int(gt[i]+(gb[i]-gt[i])*t) for i in range(3)))

    # 草
    gc=pal['grass']; rng=random.Random(42)
    for _ in range(120):
        gx=rng.randint(0,W2); gy=rng.randint(int(VP_Y+5),H2-2)
        tg=(gy-VP_Y)/(H2-VP_Y)
        if road_x(tg,-1)<gx<road_x(tg,1): continue
        hg=rng.randint(2,int(4+tg*8))
        v=rng.randint(-15,15)
        d.line([(gx,gy),(gx+rng.randint(-2,2),gy-hg)],
               fill=(max(0,min(255,gc[0]+v)),max(0,min(255,gc[1]+v)),max(0,min(255,gc[2]+v//2))),width=1)

    # 道
    pts=[]
    for i in range(21):
        t=i/20; pts.append((road_x(t,-1),road_y(t)))
    for i in range(20,-1,-1):
        t=i/20; pts.append((road_x(t,1),road_y(t)))
    d.polygon(pts,fill=(175,155,105))
    for i in range(12):
        t0=i/12; t1=(i+0.4)/12
        x0=(road_x(t0,-1)+road_x(t0,1))/2; y0=road_y(t0)
        x1=(road_x(t1,-1)+road_x(t1,1))/2; y1=road_y(t1)
        d.line([(x0,y0),(x1,y1)],fill=(155,135,88),width=max(1,int(pscale(t0)*2)))

    # 木
    def draw_tree(bx,sc,t_val=None):
        by=int(road_y(t_val)) if t_val else int(VP_Y+(H2-VP_Y)*0.85)
        th=int(sc*160); tw3=int(sc*14)
        d.polygon([(bx-tw3,by),(bx-int(tw3*0.6),by-th),(bx+int(tw3*0.6),by-th),(bx+tw3,by)],fill=(52,62,38))
        lt=by-th
        clusters=[(bx,lt,int(sc*68),int(sc*52),(52,88,40)),(bx-int(sc*38),lt+int(sc*30),int(sc*52),int(sc*42),(62,98,48)),
                  (bx+int(sc*35),lt+int(sc*22),int(sc*55),int(sc*44),(58,92,44)),(bx,lt+int(sc*40),int(sc*60),int(sc*48),(65,102,50)),
                  (bx-int(sc*25),lt+int(sc*55),int(sc*42),int(sc*35),(70,108,54)),(bx+int(sc*28),lt+int(sc*50),int(sc*45),int(sc*36),(62,96,46))]
        for (cx2,cy2,rw,rh,col) in clusters:
            if rw<2 or rh<2: continue
            d.ellipse([cx2-rw,cy2-rh,cx2+rw,cy2+rh],fill=(col[0]-12,col[1]-12,col[2]-8))
            iw2,ih2=int(rw*0.55),int(rh*0.55)
            if iw2>1 and ih2>1:
                d.ellipse([cx2-iw2,cy2-ih2,cx2+iw2,cy2+ih2],fill=(min(255,col[0]+8),min(255,col[1]+8),col[2]))
        # 花
        rng_f=random.Random(int(sc*1000+by))
        for _ in range(int(sc*35)):
            fx=bx+rng_f.randint(-int(sc*65),int(sc*65))
            fy=lt+rng_f.randint(-int(sc*15),int(sc*55))
            pr=rng_f.randint(1,max(1,int(sc*3)))
            br=rng_f.randint(0,60)
            d.ellipse([fx-pr,fy-pr,fx+pr,fy+pr],fill=(230+br//3,155+br//4,170+br//3))
            if rng_f.random()>0.65 and pr>=1: d.point((fx,fy),fill=(255,240,245))

    left_trees=[(20,0.0,0.55),(-5,0.0,0.42),(35,0.0,0.38),(55,0.0,0.28)]
    right_trees=[(W2-20,0.0,0.50),(W2+5,0.0,0.38),(W2-40,0.0,0.30)]
    road_ts=[0.18,0.32,0.50,0.68]
    for t in road_ts:
        sc2=pscale(t)*0.65
        left_trees.append((road_x(t,-1)-pscale(t)*22,t,sc2))
        right_trees.append((road_x(t,1)+pscale(t)*22,t,sc2))

    # 建物（地平線）
    hy=int(VP_Y); base_y=hy+1
    col_bld=(40,50,33); col_roof=(52,40,28); col_ch=(45,45,36)
    def bld(bx2,bw2,bh2,bt):
        if bt==0:
            d.rectangle([bx2-bw2//2,base_y-bh2,bx2+bw2//2,base_y],fill=col_bld)
            d.polygon([(bx2-bw2//2-1,base_y-bh2),(bx2,base_y-bh2-bw2//2),(bx2+bw2//2+1,base_y-bh2)],fill=col_roof)
        elif bt==1:
            d.rectangle([bx2-bw2//2,int(base_y-bh2*0.55),bx2+bw2//2,base_y],fill=col_ch)
            d.polygon([(bx2-bw2//3,int(base_y-bh2*0.55)),(bx2,base_y-bh2),(bx2+bw2//3,int(base_y-bh2*0.55))],fill=col_ch)
            d.line([(bx2,base_y-bh2+1),(bx2,base_y-bh2+5)],fill=(200,190,165),width=1)
            d.line([(bx2-1,base_y-bh2+3),(bx2+1,base_y-bh2+3)],fill=(200,190,165),width=1)
        elif bt==2:
            d.rectangle([bx2-bw2//2,base_y-bh2,bx2+bw2//2,base_y],fill=(55,40,26))
            d.polygon([(bx2-bw2//2,base_y-bh2),(bx2,base_y-bh2-bh2//3),(bx2+bw2//2,base_y-bh2)],fill=(68,50,30))

    for (bx2,bw2,bh2,bt) in [(int(W2*0.82),10,14,0),(int(W2*0.88),8,18,1),(int(W2*0.93),12,11,2),(int(W2*0.77),8,10,0),
                               (int(W2*0.18),10,13,0),(int(W2*0.12),8,17,1),(int(W2*0.07),11,10,2),(int(W2*0.23),7,9,0)]:
        bld(bx2,bw2,bh2,bt)

    # 手前の建物
    ey=hy+5
    for (bx2,bw2,bh2,bt) in [(int(W2*0.82),14,18,0),(int(W2*0.90),12,22,1),(int(W2*0.93),16,14,2),
                               (int(W2*0.18),14,17,0),(int(W2*0.10),12,21,1),(int(W2*0.07),15,13,2)]:
        by2=ey+bh2
        if bt==0:
            d.rectangle([bx2-bw2//2,by2-bh2,bx2+bw2//2,by2],fill=col_bld)
            d.polygon([(bx2-bw2//2-1,by2-bh2),(bx2,by2-bh2-bw2//2),(bx2+bw2//2+1,by2-bh2)],fill=col_roof)
        elif bt==1:
            d.rectangle([bx2-bw2//2,int(by2-bh2*0.55),bx2+bw2//2,by2],fill=col_ch)
            d.polygon([(bx2-bw2//3,int(by2-bh2*0.55)),(bx2,by2-bh2),(bx2+bw2//3,int(by2-bh2*0.55))],fill=col_ch)
            d.line([(bx2,by2-bh2+1),(bx2,by2-bh2+6)],fill=(200,190,165),width=1)
        elif bt==2:
            d.rectangle([bx2-bw2//2,by2-bh2,bx2+bw2//2,by2],fill=(55,40,26))
            d.polygon([(bx2-bw2//2,by2-bh2),(bx2,by2-bh2-bh2//3),(bx2+bw2//2,by2-bh2)],fill=(68,50,30))

    # 木を建物の上に
    for (bx,t_val,sc) in sorted(left_trees+right_trees,key=lambda x:x[2],reverse=True):
        draw_tree(int(bx),sc,t_val if t_val>0 else None)

    # フェンス
    fc=(105,92,60)
    for side in [-1,1]:
        ppx,ppy=None,None
        for i in range(9):
            t=i/8; fx=road_x(t,side)+side*int(pscale(t)*6); fy=road_y(t)
            sc2=pscale(t); ph2=int(sc2*20); pw2=max(1,int(sc2*2))
            d.line([(int(fx),int(fy)),(int(fx),int(fy-ph2))],fill=fc,width=pw2)
            ts=max(1,int(sc2*3))
            d.polygon([(int(fx)-ts,int(fy-ph2)),(int(fx),int(fy-ph2-ts*1.2)),(int(fx)+ts,int(fy-ph2))],fill=fc)
            if ppx:
                d.line([(int(fx),int(fy-ph2*0.35)),(int(ppx),int(ppy-ph2*0.35))],fill=fc,width=max(1,int(sc2*1.5)))
                d.line([(int(fx),int(fy-ph2*0.68)),(int(ppx),int(ppy-ph2*0.68))],fill=fc,width=max(1,int(sc2*1.2)))
            ppx,ppy=fx,fy
    return img

# ── パーティクル ──────────────────────────────────────────
class Petal:
    def __init__(self,ry=False):
        self.reset(ry)
    def reset(self,ry=False):
        self.x=random.uniform(-8,W2+8); self.y=random.uniform(0,H2) if ry else random.uniform(-15,-3)
        self.r=random.uniform(2.5,5.0); self.vx=random.uniform(-0.3,0.4); self.vy=random.uniform(0.3,0.7)
        self.rot=random.uniform(0,math.pi*2); self.vrot=random.uniform(-0.05,0.05)
        self.swing=random.uniform(0,math.pi*2); self.sw_sp=random.uniform(0.012,0.028)
        self.color=random.choice([(240,195,175),(230,210,185),(245,205,178)])
    def update(self):
        self.swing+=self.sw_sp; self.x+=self.vx+math.sin(self.swing)*0.38; self.y+=self.vy; self.rot+=self.vrot
        if self.y>H2+10: self.reset()
    def draw(self,img):
        pw=max(2,int(self.r*2)); ph=max(2,int(self.r*1.1))
        p=Image.new("RGBA",(pw*2,ph*2),(0,0,0,0)); pd=ImageDraw.Draw(p)
        pd.ellipse([pw//2,ph//2,pw//2+pw,ph//2+ph],fill=(*self.color,175))
        rot=p.rotate(math.degrees(self.rot),expand=True)
        img.paste(rot,(int(self.x-rot.width//2),int(self.y-rot.height//2)),rot)

class Walker:
    def __init__(self):
        self.to_front=random.random()>0.45
        self.t=0.02 if self.to_front else 1.0; self.speed=random.uniform(0.004,0.007)
        self.offset_x=random.uniform(-0.25,0.25); self.step=0; self.opacity=0.0; self.active=True
    def update(self):
        self.step+=1
        self.t+=self.speed if self.to_front else -self.speed
        if self.to_front:
            if self.t<0.15: self.opacity=min(1.0,self.opacity+0.05)
            elif self.t>0.85: self.opacity=max(0.0,self.opacity-0.04)
            if self.t>1.05: self.active=False
        else:
            if self.t>0.85: self.opacity=min(1.0,self.opacity+0.05)
            elif self.t<0.15: self.opacity=max(0.0,self.opacity-0.04)
            if self.t<0.0: self.active=False
    def draw(self,img):
        t=max(0.01,min(1.0,self.t)); sc=pscale(t)
        cx=road_x(t,0)+self.offset_x*(road_x(t,1)-road_x(t,0))*0.5; cy=road_y(t)
        sz=sc*22; sw=math.sin(self.step*0.15)*3*sc; alpha=int(self.opacity*200)
        if alpha<5: return
        pw,ph=max(4,int(sz*2.5)),max(4,int(sz*3.5))
        person=Image.new("RGBA",(pw,ph),(0,0,0,0)); pd=ImageDraw.Draw(person)
        ccx=pw//2; col=(40,55,35,alpha); s=sz/20.0
        pd.ellipse([int(ccx-4*s+sw*0.4),int(ph*0.42),int(ccx-0.5*s+sw*0.4),int(ph*0.93)],fill=col)
        pd.ellipse([int(ccx+0.5*s-sw*0.4),int(ph*0.42),int(ccx+4*s-sw*0.4),int(ph*0.93)],fill=col)
        pd.ellipse([int(ccx-4.5*s),int(ph*0.12),int(ccx+4.5*s),int(ph*0.52)],fill=col)
        pd.ellipse([int(ccx-3.8*s),int(ph*0.0),int(ccx+3.8*s),int(ph*0.16)],fill=col)
        if not self.to_front: person=person.transpose(Image.FLIP_LEFT_RIGHT)
        img.paste(person,(int(cx-pw//2),int(cy-ph//2)),person)

class Carriage:
    def __init__(self):
        self.to_front=random.random()>0.45; self.t=0.02 if self.to_front else 1.0
        self.speed=random.uniform(0.006,0.010); self.offset_x=random.uniform(-0.15,0.15)
        self.wheel_rot=0.0; self.opacity=0.0; self.active=True
    def update(self):
        self.wheel_rot+=0.15
        self.t+=self.speed if self.to_front else -self.speed
        if self.to_front:
            if self.t<0.12: self.opacity=min(1.0,self.opacity+0.04)
            elif self.t>0.88: self.opacity=max(0.0,self.opacity-0.03)
            if self.t>1.05: self.active=False
        else:
            if self.t>0.88: self.opacity=min(1.0,self.opacity+0.04)
            elif self.t<0.12: self.opacity=max(0.0,self.opacity-0.03)
            if self.t<0.0: self.active=False
    def draw(self,img):
        t=max(0.01,min(1.0,self.t)); sc=pscale(t)
        cx=int(road_x(t,0)+self.offset_x*(road_x(t,1)-road_x(t,0))*0.4); cy=int(road_y(t))
        alpha=int(self.opacity*210)
        if alpha<5 or sc<0.08: return
        bw=max(4,int(sc*38)); bh=max(3,int(sc*26)); wr=max(2,int(sc*9))
        col_body=(70,45,25,alpha); col_roof=(52,32,16,alpha); col_wheel=(50,33,16,alpha)
        col_spoke=(82,58,28,alpha); col_horse=(48,35,20,alpha)
        cw2=bw*3; ch2=bh*5
        carriage=Image.new("RGBA",(cw2,ch2),(0,0,0,0)); cd=ImageDraw.Draw(carriage)
        ox,oy=cw2//2,ch2//2+bh
        cd.rectangle([ox-bw//2,oy-bh,ox+bw//2,oy],fill=col_body)
        cd.polygon([(ox-bw//2-2,oy-bh),(ox,oy-bh-int(bh*0.55)),(ox+bw//2+2,oy-bh)],fill=col_roof)
        if bw>10:
            ww=max(2,int(bw*0.38)); wh3=max(2,int(bh*0.38))
            cd.rectangle([ox-ww//2,oy-bh+int(bh*0.15),ox+ww//2,oy-bh+int(bh*0.15)+wh3],fill=(115,95,55,alpha))
        axle_y=oy+int(sc*3)
        cd.line([(ox-bw//2-wr,axle_y),(ox+bw//2+wr,axle_y)],fill=col_wheel,width=max(1,int(sc*2)))
        for wx_off in [-(bw//2+wr),(bw//2+wr)]:
            wx2=ox+wx_off; wy2=axle_y
            cd.ellipse([wx2-wr,wy2-wr,wx2+wr,wy2+wr],outline=col_wheel,width=max(1,int(sc*2)))
            for angle in [self.wheel_rot+i*math.pi/2 for i in range(4)]:
                sx2=wx2+int(wr*0.82*math.cos(angle)); sy2=wy2+int(wr*0.82*math.sin(angle))
                cd.line([(wx2,wy2),(sx2,sy2)],fill=col_spoke,width=max(1,int(sc*1.2)))
            cd.ellipse([wx2-max(1,int(wr*0.2)),wy2-max(1,int(wr*0.2)),wx2+max(1,int(wr*0.2)),wy2+max(1,int(wr*0.2))],fill=col_wheel)
        hy2=oy-bh-int(sc*20); hs=max(2,int(sc*11))
        cd.ellipse([ox-hs,hy2-hs//2,ox+hs,hy2+hs],fill=col_horse)
        cd.ellipse([ox-int(hs*0.55),hy2-hs-int(sc*6),ox+int(hs*0.55),hy2-hs+int(sc*2)],fill=col_horse)
        for fx_off in [-int(hs*0.5),int(hs*0.5)]:
            lg=math.sin(self.wheel_rot+(0 if fx_off<0 else math.pi))*int(sc*3)
            cd.line([(ox+fx_off,hy2+hs//2),(ox+fx_off+int(lg),hy2+hs+int(sc*12))],fill=col_horse,width=max(1,int(sc*2)))
        cd.line([(ox-int(hs*0.8),hy2+hs//2),(ox-bw//2,oy-bh+int(bh*0.4))],fill=(78,55,28,alpha),width=max(1,int(sc)))
        cd.line([(ox+int(hs*0.8),hy2+hs//2),(ox+bw//2,oy-bh+int(bh*0.4))],fill=(78,55,28,alpha),width=max(1,int(sc)))
        img.paste(carriage,(cx-cw2//2,cy-ch2//2-bh),carriage)

# ── グローバル状態 ────────────────────────────────────────
_petals        = [Petal(ry=True) for _ in range(16)]
_walkers       = []
_carriages     = []
_walker_timer  = 0
_next_walker   = random.randint(180,400)
_car_timer     = 0
_next_car      = random.randint(450,900)
_scroll_x      = 0
_scroll_pause  = 0
_last_song     = ""

def draw_frame(image, now, mpd, scroll_x):
    global _bg_cache, _bg_hour
    global _walkers, _carriages, _walker_timer, _next_walker, _car_timer, _next_car
    global _scroll_x, _scroll_pause, _last_song, _petals

    hour = now.hour
    if hour != _bg_hour:
        _bg_cache = _build_bg(hour)
        _bg_hour  = hour

    img = _bg_cache.copy().convert("RGBA")

    # 花びら（奥）
    for p in _petals:
        p.update()
        if p.y < VP_Y: p.draw(img)

    # エンティティ
    ents = [(w.t,w) for w in _walkers] + [(c.t,c) for c in _carriages]
    ents.sort(key=lambda e:e[0])
    for _,ent in ents:
        ent.update(); ent.draw(img)
        if not ent.active:
            if ent in _walkers:   _walkers.remove(ent)
            if ent in _carriages: _carriages.remove(ent)

    # 花びら（手前）
    for p in _petals:
        if p.y >= VP_Y: p.draw(img)

    # 新キャラ生成
    _walker_timer += 1
    if _walker_timer >= _next_walker:
        _walker_timer=0; _next_walker=random.randint(200,450); _walkers.append(Walker())
    _car_timer += 1
    if _car_timer >= _next_car:
        _car_timer=0; _next_car=random.randint(450,900); _carriages.append(Carriage())

    # UIオーバーレイ
    img_rgb = img.convert("RGB")
    d = ImageDraw.Draw(img_rgb)

    # スクロール
    if mpd["song"] != _last_song:
        _last_song=mpd["song"]; _scroll_x=0; _scroll_pause=0
    if tw2(mpd["song"],FONT_SMALL) > W2-36:
        if _scroll_pause<50: _scroll_pause+=1
        else: _scroll_x+=1.2

    # 上部バー
    bar=Image.new("RGBA",(W2,52),(18,28,18,155))
    img_rgb.paste(Image.fromarray(__import__('numpy').array(bar)[:,:,:3]),(0,0),bar)
    ts=now.strftime("%H:%M")
    tx=(W2-tw2(ts,FONT_LARGE))//2
    d.text((tx+1,5),ts,font=FONT_LARGE,fill=(20,30,20))
    d.text((tx,4),ts,font=FONT_LARGE,fill=CREAM)
    d.text((W2-tw2(now.strftime("%m/%d"),FONT_TINY)-6,6),now.strftime("%m/%d"),font=FONT_TINY,fill=CREAM2)

    # 下部バー（曲名）
    bar2=Image.new("RGBA",(W2,26),(18,28,18,148))
    img_rgb.paste(Image.fromarray(__import__('numpy').array(bar2)[:,:,:3]),(0,H2-26),bar2)
    icon="▶" if mpd["playing"] else "⏸"
    d.text((7,H2-20),icon,font=FONT_TINY,fill=SAGE if mpd["playing"] else MUTED)
    sw=tw2(mpd["song"],FONT_SMALL)
    area_x=26; area_w=W2-area_x-6
    if sw<=area_w:
        d.text((area_x,H2-20),mpd["song"],font=FONT_SMALL,fill=CREAM2)
    else:
        gap=38; loop_w=sw+gap
        off=Image.new("RGB",(loop_w*2,18),(18,28,18))
        od=ImageDraw.Draw(off)
        od.text((0,1),mpd["song"],font=FONT_SMALL,fill=CREAM2)
        od.text((loop_w,1),mpd["song"],font=FONT_SMALL,fill=CREAM2)
        crop_x=int(_scroll_x)%loop_w
        img_rgb.paste(off.crop((crop_x,0,crop_x+area_w,18)),(area_x,H2-20))

    image.paste(img_rgb,(0,0))
