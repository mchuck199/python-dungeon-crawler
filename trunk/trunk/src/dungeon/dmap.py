# Class to produce random map layouts
# by Steve Wallace
# have a look at roguebasin.roguelikedevelopment.org/index.php?title=Dungeon_builder_written_in_Python
# roguebasin.roguelikedevelopment.org is just great
from numpy import *
from random import *
from math import *
class dMap:
   def __init__(self):
       self.roomList=[]
       self.cList=[]
   def makeMap(self,xsize,ysize,fail,b1,mrooms):
       """Generate random layout of rooms, corridors and other features"""
       #makeMap can be modified to accept arguments for values of failed, and percentile of features.
       #Create first room
       self.mapArr=ones((ysize,xsize))
       w,l,t=self.makeRoom()
       while len(self.roomList)==0:
           y=int(random()*(ysize-1-l))+1
           x=int(random()*(xsize-1-w))+1
           p=self.placeRoom(l,w,x,y,xsize,ysize,6,0)
       failed=0
       while failed<fail: #The lower the value that failed< , the smaller the dungeon
           chooseRoom=int(random()*len(self.roomList))
           ex,ey,ex2,ey2,et=self.makeExit(chooseRoom)
           feature=int(random()*100)
           if feature<b1: #Begin feature choosing (more features to be added here)
               w,l,t=self.makeCorridor()
           else:
               w,l,t=self.makeRoom()
           roomDone=self.placeRoom(l,w,ex2,ey2,xsize,ysize,t,et)
           if roomDone==0: #If placement failed increase possibility map is full
               failed=failed+1
           elif roomDone==2: #Possiblilty of linking rooms
               if self.mapArr[ey2][ex2]==0:
                   if int(random()*100)<7:
                       self.makePortal(ex,ey)
                       failed=failed+1
                   else:
                       failed=failed+1
           else: #Otherwise, link up the 2 rooms
               self.makePortal(ex,ey)
               failed=0
               if t<5:
                   tc=[len(self.roomList)-1,ex2,ey2,t]
                   self.cList.append(tc)
                   self.joinCorridor(len(self.roomList)-1,ex2,ey2,t,50)
           if len(self.roomList)==mrooms:
               failed=fail
       self.finalJoins()

   def makeRoom(self):
       """Randomly produce room size"""
       rtype=5
       rwide=int(random()*8)+3
       rlong=int(random()*8)+3
       return rwide,rlong,rtype
   def makeCorridor(self):
       """Randomly produce corridor length and heading"""
       clength=int(random()*18)+3
       heading=int(random()*4)
       if heading==0: #North
           wd=1
           lg=-clength
       if heading==1: #East
           wd=clength
           lg=1
       if heading==2: #South
           wd=1
           lg=clength
       if heading==3: #West
           wd=-clength
           lg=1
       return wd,lg,heading
   def placeRoom(self,ll,ww,xposs,yposs,xsize,ysize,rty,ext):
       """Place feature if enough space and return canPlace as true or false"""
       #Arrange for heading
       xpos=xposs
       ypos=yposs
       if ll<0:
           ypos=ypos+(ll+1)
           ll=int(sqrt(ll*ll))
       if ww<0:
           xpos=xpos+(ww+1)
           ww=int(sqrt(ww*ww))
       #Make offset if type is room
       if rty==5:
           if ext==0 or ext==2:
               offset=int(random()*ww)
               xpos=xpos-offset
           else:
               offset=int(random()*ll)
               ypos=ypos-offset
       #Then check if there is space
       canPlace=1
       if ww+xpos+1>xsize-1 or ll+ypos+1>ysize:
           canPlace=0
           return canPlace
       elif xpos<1 or ypos<1:
           canPlace=0
           return canPlace
       else:
           for j in range(ll):
               for k in range(ww):
                   if self.mapArr[(ypos)+j][(xpos)+k]!=1:
                       canPlace=2
       #If there is space, add to list of rooms
       if canPlace==1:
           temp=[ll,ww,xpos,ypos]
           self.roomList.append(temp)
           for j in range(ll+2): #Then build walls
               for k in range(ww+2):
                   self.mapArr[(ypos-1)+j][(xpos-1)+k]=2
           for j in range(ll): #Then build floor
               for k in range(ww):
                   self.mapArr[ypos+j][xpos+k]=0
       return canPlace #Return whether placed is true/false
   def makeExit(self,rn):
       """Pick random wall and random point along that wall"""
       room=self.roomList[rn]
       exitMade=0
       while exitMade==0:
           rw=int(random()*4)
           if rw==0: #North wall
               rx=int(random()*room[1])+room[2]
               ry=room[3]-1
               rx2=rx
               ry2=ry-1
           if rw==1: #East wall
               ry=int(random()*room[0])+room[3]
               rx=room[2]+room[1]
               rx2=rx+1
               ry2=ry
           if rw==2: #South wall
               rx=int(random()*room[1])+room[2]
               ry=room[3]+room[0]
               rx2=rx
               ry2=ry+1
           if rw==3: #West wall
               ry=int(random()*room[0])+room[3]
               rx=room[2]-1
               rx2=rx-1
               ry2=ry
           if self.mapArr[ry][rx]==2: #If space is a wall set exit flag
               exitMade=1
       return rx,ry,rx2,ry2,rw
   def makePortal(self,px,py):
       """Create doors in walls"""
       ptype=int(random()*100)
       if ptype>90: #Secret door
           self.mapArr[py][px]=5
           return
       if ptype>75: #Closed door
           self.mapArr[py][px]=4
           return
       if ptype>40: #Open door
           self.mapArr[py][px]=3
           return
       else: #Hole in the wall
           self.mapArr[py][px]=0
   def joinCorridor(self,cno,xp,yp,ed,psb):
       """Check corridor endpoint and make an exit if it links to another room"""
       cArea=self.roomList[cno]
       if xp!=cArea[2] or yp!=cArea[3]: #Find the corridor endpoint
           endx=xp-(cArea[1]-1)
           endy=yp-(cArea[0]-1)
       else:
           endx=xp+(cArea[1]-1)
           endy=yp+(cArea[0]-1)
       checkExit=[]
       if ed==0: #North corridor
           if endx>1:
               coords=[endx-2,endy,endx-1,endy]
               checkExit.append(coords)
           if endy>1:
               coords=[endx,endy-2,endx,endy-1]
               checkExit.append(coords)
           if endx<78:
               coords=[endx+2,endy,endx+1,endy]
               checkExit.append(coords)
       if ed==1: #East corridor
           if endy>1:
               coords=[endx,endy-2,endx,endy-1]
               checkExit.append(coords)
           if endx<78:
               coords=[endx+2,endy,endx+1,endy]
               checkExit.append(coords)
           if endy<38:
               coords=[endx,endy+2,endx,endy+1]
               checkExit.append(coords)
       if ed==2: #South corridor
           if endx<78:
               coords=[endx+2,endy,endx+1,endy]
               checkExit.append(coords)
           if endy<38:
               coords=[endx,endy+2,endx,endy+1]
               checkExit.append(coords)
           if endx>1:
               coords=[endx-2,endy,endx-1,endy]
               checkExit.append(coords)
       if ed==3: #West corridor
           if endx>1:
               coords=[endx-2,endy,endx-1,endy]
               checkExit.append(coords)
           if endy>1:
               coords=[endx,endy-2,endx,endy-1]
               checkExit.append(coords)
           if endy<38:
               coords=[endx,endy+2,endx,endy+1]
               checkExit.append(coords)
       for i in range(len(checkExit)): #Loop through possible exits
           xxx=checkExit[i][0]
           yyy=checkExit[i][1]
           xxx1=checkExit[i][2]
           yyy1=checkExit[i][3]
           if self.mapArr[yyy][xxx]==0: #If joins to a room
               if int(random()*100)<psb: #Possibility of linking rooms
                   self.makePortal(xxx1,yyy1)
   def finalJoins(self):
       """Final stage, loops through all the corridors to see if any can be joined to other rooms"""
       for i in range(len(self.cList)):
           self.joinCorridor(self.cList[i][0],self.cList[i][1],self.cList[i][2],self.cList[i][3],10)