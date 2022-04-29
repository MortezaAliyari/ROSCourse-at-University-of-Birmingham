#!/usr/bin/env python3
import math

def forward(p, a, rd):
  (x,y,theta) = p
  (vl,vr,t) = a
  (axle_length, wheel_radius, max_speed) = rd
  dt=t
  vl=wheel_radius*vl
  vr=wheel_radius*vr
  l=axle_length
  w=(vr-vl)/l
  if abs(vr)==abs(vl):
    thetanew=theta + w*dt
    xnew=x+((vr+vl)/2.0)*(math.cos(thetanew))*dt
    ynew=y+((vr+vl)/2.0)*(math.sin(thetanew))*dt
  else:
    R = (l / 2) * (vr + vl) / (vr - vl)
    Iccx = x - R*math.sin(theta)
    Iccy = y + R * math.cos(theta)
    xnew=(x-Iccx)*math.cos(w*dt)-(y-Iccy)*math.sin(w*dt)+Iccx
    ynew = (x - Iccx) * math.sin(w * dt) + (y - Iccy) * math.cos(w * dt) + Iccy
    thetanew=theta+w*dt
  return xnew, ynew, thetanew

def inverse(p0, p1, rd):
  (x0,y0,theta0) = p0
  (x1,y1,theta1) = p1
  (axle_length, wheel_radius, max_speed) = rd
  l=axle_length
  yawpath = math.atan2((y1 - y0), (x1 - x0))
  dis=math.sqrt((x0 - x1)*(x0 - x1)+(y0 - y1)*(y0 - y1))
  act1=act2=[]
  PI=math.pi
  #############################################Check action1##############################
  if dis!=0:
    # need to action 1
    if math.sin(yawpath)==math.sin(theta0):
      if yawpath>theta0:
        vl=-1
        vr=-1
      else:
        vl=1
        vr=1
      v=(vr+vl)/2
      t=dis/v
      theta3=yawpath
    else:
      Cx=x0
      m2=-1/((y1-y0)/(x1-x0))
      xn=(x0+x1)/2
      yn=(y0+y1)/2
      Cy=m2*Cx-m2*xn+yn
      r=math.sqrt((Cx-x1)*(Cx-x1)+(Cy-y1)*(Cy-y1))
      deltatheta=-math.atan2((y0-Cy),(x0-Cx))+math.atan2((y1-Cy),(x1-Cx))
      d=abs(r*deltatheta)

      if yawpath>0:
        if deltatheta>0: #just go forward CCW
          vr=1
          a=r/(l/2)
          vl=(a-vr)/(vr+a)
          w=(vr-vl)/l
        else:#just go backward-->CW
          vr=-1
          a=r/(l/2)
          vl=-(a+vr)/(-vr+a)
          w=(vr-vl)/l
      else:
        if deltatheta<0:#just go forward with same speed-->CW
          vl=1
          a=r/(l/2)
          vr=(a-1)/(1+a)
          w=(vr-vl)/l
        else:#just go backward with same speed -->CCW
          vl=-1
          a=r/(l/2)
          vr=-(a+vl)/(-vl+a)
          w=(vr-vl)/l
      t=abs(deltatheta/w)
      theta3 =w*t
    act1=[vl,vr,t]
  else:
    # no need to action 1
    act1=[]
    theta3=theta0
  #############################################Check action2##############################
  if round(theta3,3)==round(theta1,3): # i don't use math.sin() because sin(pi)=sin(0)
    # no need to action 2
    act2=[]
  else:
    # need to action 2
    if theta3-theta1>0:#CCW
      vl=1
      vr=-1
    else:#CW
      vl=-1
      vr=1
    w=(vr-vl)/l
    t=abs((theta3-theta1)/w)
    act2=[vl,vr,t]
  act=act1+act2
  return act


