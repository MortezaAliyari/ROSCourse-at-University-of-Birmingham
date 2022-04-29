t1=t
  vl1=vl
  vr1=vr
  act1 = [vl1, vr1, t1]
  theta3 = 1 / math.asin(y1 / r)

  #print("yawpath",yawpath)
  #print("dos",dis)
  rot = theta1-yawpath
  #print("rot",rot)
  act=[]
# first action
  if yawpath==theta0:
    vl1=0
    vr1=0
    w1=0
    t1=0
    act1=[]
  else:
    if (theta0-yawpath)>0:
      vl1=wheel_radius*max_speed
      vr1=-wheel_radius*max_speed
    else:
      vl1 = -wheel_radius*max_speed
      vr1 = wheel_radius*max_speed

    w = (vr1 - vl1) / l
    t1=abs((theta0-yawpath)/w)


#second action
  if dis==0:
    vl2=0
    vr2=0
    w=0
    t2=0
    act2=[]
  else:
    vl2=wheel_radius*max_speed
    vr2=wheel_radius*max_speed
    w = (vr2 - vl2) / l
    t2 = (dis)/((vl2+vr2)/2)
    act2 = [vl2, vr2, t2]
#third action
  if rot==0:
    vl3=0
    vr3=0
    w=0
    t3=0
    act3=[]
  else:
    if rot>0:
      vl3=-wheel_radius*max_speed
      vr3=wheel_radius*max_speed
    else:
      vl3 = wheel_radius*max_speed
      vr3 = -wheel_radius*max_speed
    w= (vr3 - vl3) / l
    #print("w3: ",w)
    t3 =abs((rot)/w)
    act3 = [vl3, vr3, t3]
  act=act1+act2+act3
  #print(act)