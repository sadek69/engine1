##sdes budut hranitsja vse klassi i malo izmenjaemie funkcii!


import math
import os
import sys
import random
import Image                # PIL
from OpenGL.GL import *
from OpenGL.GLU import *
try:
    from OpenGL.WGL.EXT.swap_control import *
    swap_control=1
except:
    swap_control=0
from OpenGL.GL.ARB.multitexture import *
import pygame, pygame.image
from pygame.locals import *

global texture
SCREEN_SIZE=(1280.000,600.000)

#moi klass kameri
#peredelal iz ishodnikov na c++ vzjatih ot http://wingman.org.ru/opengl/
class CCamera:
    def __init__(self):
        self.vZero=Vec3f(0.0,0.0,0.0)#inicializiruem vektor pozicii
        self.vView=Vec3f(10,0.0,0.5)#inicializiruem vektor vzgljada
        self.vUp=Vec3f(0.0,0.0,1.0)#vertialnii vektor
        self.m_vStrafe=Vec3f(0.0,0.0,0.0)
        self.vCross=Vec3f(0.0,0.0,0.0)#peremennaja dlja rezultata cross
        
        self.m_vPosition=self.vZero#pozicija kameri
        self.m_vView=self.vView#napravlenie kameri
        self.m_vUpVector=self.vUp#vertikalnii vektor
        self.vVector=Vec3f(0.0,0.0,0.0)#vektor napravlenija vzglada
        #to sto sdes dlja dostupa iz vne k privatnim dannim
        self.Position=self.m_vPosition
        self.View=self.m_vView
        self.UpVector=self.m_vUpVector
        self.Strafe=self.m_vStrafe
        

    def PositionCamera(self,positionX,positionY,positionZ,
                       viewX,viewY,viewZ,
                       upVectorX,upVectorY,upVectorZ):
        #stob udobnee bilo zadavat polozenie kameri
        self.vPosition=Vec3f(positionX, positionY, positionZ)
        self.vView=Vec3f(viewX, viewY, viewZ)
        self.vUpVector=Vec3f(upVectorX, upVectorY, upVectorZ)

        self.m_vPosition=self.vPosition
        self.m_vView =self.vView
        self.m_vUpVector =self.vUpVector

    def MoveCamera(self,speed):
        #sdes mi polu4aem piziciju kuda smotrim 
        self.vVector=self.m_vView.sub(self.m_vPosition)
        self.vVector.z=0
        self.vVector.norm()
        #sdes dvigaem kameru vpered ili nazad
        self.m_vPosition.x=self.m_vPosition.x+(self.vVector.x*speed)
        self.m_vPosition.y=self.m_vPosition.y+(self.vVector.y*speed)
        self.m_vPosition.z=self.m_vPosition.z+(self.vVector.z*speed)
        self.m_vView.x=self.m_vView.x+(self.vVector.x*speed)
        self.m_vView.y=self.m_vView.y+(self.vVector.y*speed)
        self.m_vView.z=self.m_vView.z+(self.vVector.z*speed)#sdes pravil 

    def StrafeCamera(self,speed):
        #dobavim vektor streifa k pozicii
        self.m_vPosition.x=self.m_vPosition.x+(self.m_vStrafe.x*speed)
        self.m_vPosition.y=self.m_vPosition.y+(self.m_vStrafe.y*speed)
        #dobavim teper k vzgladu
        self.m_vView.x=self.m_vView.x+(self.m_vStrafe.x*speed)
        self.m_vView.y=self.m_vView.y+(self.m_vStrafe.y*speed)
      
    def RotateView(self,angle,x,y,z):
        self.vNewView=Vec3f(0,0,0)
        self.vView=Vec3f(self.m_vView.x-self.m_vPosition.x,#napravlenie po x
                         self.m_vView.y-self.m_vPosition.y,#napravlenie po y
                         self.m_vView.z-self.m_vPosition.z)#napravlenie po z
        self.cosTheta=math.cos(angle)#zaranee opredelim ugol
        self.sinTheta=math.sin(angle)
        #naidem poziciju dlja  x vrawaemoi to4ki
        self.vNewView.x=(self.cosTheta+(1-self.cosTheta)*x*x)*self.vView.x
        self.vNewView.x=self.vNewView.x+(((1-self.cosTheta)*x*y-z*self.sinTheta)*self.vView.y)
        self.vNewView.x=self.vNewView.x+(((1-self.cosTheta)*x*y+z*self.sinTheta)*self.vView.z)
        #naidem poziciju dlja y
        self.vNewView.y=((1-self.cosTheta)*x*y+z*self.sinTheta)*self.vView.x
        self.vNewView.y=self.vNewView.y+((self.cosTheta+(1-self.cosTheta)*y*y)*self.vView.y)
        self.vNewView.y=self.vNewView.y+(((1-self.cosTheta)*y*z-x*self.sinTheta)*self.vView.z)
        #i poziciju z
        self.vNewView.z=((1-self.cosTheta)*x*z-y*self.sinTheta)*self.vView.x
        self.vNewView.z=self.vNewView.z+(((1-self.cosTheta)*y*z+x*self.sinTheta)*self.vView.y)
        self.vNewView.z=self.vNewView.z+((self.cosTheta+(1-self.cosTheta)*z*z)*self.vView.z)
        #dobavim novii vektor vrawenija k nawei pozicii stob ustanovit novii vzglad kameri
        self.m_vView=self.m_vPosition.add(self.vNewView)

    def SetViewByMouse(self):
        self.mousePosx,self.mousePosy=pygame.mouse.get_pos()#pozicija mouse
        self.middleX=SCREEN_SIZE[0]/2#polovina wirini
        self.middleY=SCREEN_SIZE[1]/2#polovina visoti
        #self.angleY=0.0#napravlenie vzgljada verh/vniz
        #self.angleZ=0.0#zna4enie dlja vrawenija pravo vlevo po osi Y
        self.currentRotX=0.000
        #print self.mousePosx
        #print self.middleX
        #print self.mousePosy
        #print self.middleY
        if self.mousePosx == self.middleX and self.mousePosy == self.middleY :
           # print "ss"
            return()
                    
        pygame.mouse.set_pos(self.middleX,self.middleY)#vozvrawaem kursor v seredinu
        #print "self.mouseposx,posy,",self.mousePosx,self.mousePosy
        #opredeljaem vektor kuda sdvinulsja kursok delenie dlja umenwenija
        #skorosti dvizenija kameri.
        self.angleY=(self.middleX-self.mousePosx)/500
        self.angleZ=(self.middleY-self.mousePosy)/8000
        self.lastRotX=self.currentRotX#sohranjaem poslednii ugol vrawenija
        #esli ugol vrawenie bolwe 1 gradusa to obrezen stob zamedlit
        #print "currrotate:",self.currentRotX
        #print "lastrote:",self.lastRotX
        #print "angleY:",self.angleY
        #print "angleZ:",self.angleZ
        if self.currentRotX > 1.0 :
            self.currentRotX=1.0
            #vrawaem na ostavwiisja ugol
            if self.lastRotX != 1.0 :
                #stob naiti os vrawenija nada naiti vektor perpendikuljarnii
                #vzgljadu  iz kameri i vertikalnomu vektoru
                #eto i budet nawa os no ee nada normalizovat
                self.vAxis=self.m_vView.sub(self.m_vPosition)
                self.vAxis=self.vAxis.cross(self.m_vUpVector)
                self.vAxis.norm()
                ##vrawjaem kameru vokrog osi na zadanii ugol
                self.RotateView(1.0-self.lastRotX,self.vAxis.x,self.vAxis.y,self.vAxis.z)
        #esli ugol menwe -1.0 ubedimsja sto vrawenija ne budet
        if self.currentRotX < -1.0 :
            self.currentRotX = -1.0
            if self.lastRotX != -1.0 :
                #opjat vi4isljaem os
                self.vAxis=self.m_vView.sub(self.m_vPosition)
                self.vAxis=self.vAxis.cross(self.m_vUpVector)
                self.vAxis.norm()
                #vrawaem
                self.RotateView(-1.0-self.lastRotX,self.vAxis.x,self.vAxis.y,self.vAxis.z)
        else :
            #esli ukladivaemsja v predeli ot 1 do -1 to prosto vrawaem
            self.vAxis=self.m_vView.sub(self.m_vPosition)
            self.vAxis=self.vAxis.cross(self.m_vUpVector)
            self.vAxis.norm()
            #sdes obespe4ivaetsja povorot v vertikalnoi ploskosti
            self.RotateView(self.angleZ,self.vAxis.x,self.vAxis.y,self.vAxis.z)
        #vsegda vrawaem kameru vokrug osi Y
        self.RotateView(self.angleY,0,0,1)

    def Update(self):
        self.vCross=self.m_vView.sub(self.m_vPosition)
        self.vCross=self.vCross.cross(self.m_vUpVector)
        self.m_vStrafe=self.vCross.norm()
        self.SetViewByMouse()
                
                    

#nemoi tip dannih dlja hranenija treh mernih to4ek

class Vec3f:
    def __init__(self, x,y,z):
        """Vector constructor"""
        self.x=x
        self.y=y
        self.z=z

    def add(self, v):
        """Vector Addiction"""
        return Vec3f(self.x+v.x,
                     self.y+v.y,
                     self.z+v.z)

    def sub(self, v):
        """Vector Subtraction

        returns self-v"""
        return Vec3f(self.x-v.x,
                     self.y-v.y,
                     self.z-v.z)

    def mul(self, s):
        """Scalar Multiplication
        
        returns self*s (scalar multiplication)
        """

        return Vec3f(self.x*s,
                     self.y*s,
                     self.z*s)

    def dot(self, v):
        """Dot product."""
        return self.x*v.x+self.y*v.y+self.z*v.z

    def cross(self, v):
        """Cross product.

        self cross v
        """
        
        return Vec3f(self.y*v.z-self.z*v.y,
                     self.z*v.x-self.x*v.z,
                     self.x*v.y-self.y*v.x)

    def mag(self):
        """length
        
        return the magnitude(length) of the vector.
        """
        return math.sqrt(self.magSqr())
        pass

    def magSqr(self):
        """Square of the magnitude.
        
        this is faster than calling mag(), and is often just as useful.
        """
        return (self.x*self.x+
                self.y*self.y+
                self.z*self.z)

    def norm(self):
        """normalize
        
        returns a unit vector in the same direction as this vector.
        """
        m=self.mag()
        return Vec3f(self.x/m,
                     self.y/m,
                     self.z/m)

    def __str__(self):
        return "[%0.3f %0.3f %0.3f]"%(self.x, self.y, self.z)



def drawbox(x1, x2, y1, y2, z1, z2,texture):
 
    glBindTexture ( GL_TEXTURE_2D, texture )
    glBegin       ( GL_POLYGON )                        # front face
    glNormal3f    ( 0.0, 0.0, 1.0 )
    glTexCoord2f   (0, 0 )
    glVertex3f    ( x1, y1, z2 )
    glTexCoord2f  ( 1, 0 )
    glVertex3f    ( x2, y1, z2 )
    glTexCoord2f  ( 1, 1 )
    glVertex3f    ( x2, y2, z2 )
    glTexCoord2f  ( 0, 1 )
    glVertex3f    ( x1, y2, z2 )
    glEnd         ()
    
    glBegin      ( GL_POLYGON )                         # back face
    glNormal3f   ( 0.0, 0.0, -1.0 )
    glTexCoord2f ( 1, 0 )
    glVertex3f   ( x2, y1, z1 )
    glTexCoord2f ( 0, 0 )
    glVertex3f   ( x1, y1, z1 )
    glTexCoord2f ( 0, 1 )
    glVertex3f   ( x1, y2, z1 )
    glTexCoord2f ( 1, 1 )
    glVertex3f   ( x2, y2, z1 )
    glEnd        ()
    
    glBegin      ( GL_POLYGON )                         # left face
    glNormal3f   ( -1.0, 0.0, 0.0 )
    glTexCoord2f ( 0, 0 )
    glVertex3f   ( x1, y1, z1 )
    glTexCoord2f ( 0, 1 )
    glVertex3f   ( x1, y1, z2 )
    glTexCoord2f ( 1, 1 )
    glVertex3f   ( x1, y2, z2 )
    glTexCoord2f ( 1, 0 )
    glVertex3f   ( x1, y2, z1 )
    glEnd        ()
    
    glBegin      ( GL_POLYGON )                         #  right face
    glNormal3f   ( 1.0, 0.0, 0.0 )
    glTexCoord2f ( 0, 1 )
    glVertex3f   ( x2, y1, z2 )
    glTexCoord2f ( 0, 0 )
    glVertex3f   ( x2, y1, z1 )
    glTexCoord2f ( 1, 0 )
    glVertex3f   ( x2, y2, z1 )
    glTexCoord2f ( 1, 1 )
    glVertex3f   ( x2, y2, z2 )
    glEnd        ()
    
    glBegin      ( GL_POLYGON )                 # top face
    glNormal3f   ( 0.0, 1.0, 0.0 )
    glTexCoord2f ( 0, 1 )
    glVertex3f   ( x1, y2, z2 )
    glTexCoord2f ( 1, 1 )
    glVertex3f   ( x2, y2, z2 )
    glTexCoord2f ( 1, 0 )
    glVertex3f   ( x2, y2, z1 )
    glTexCoord2f ( 0, 0 )
    glVertex3f   ( x1, y2, z1 )
    glEnd        ()
    
    glBegin      ( GL_QUADS )                 #  bottom face
    glNormal3f   ( 0.0, -1.0, 0.0 )
    glTexCoord2f ( 1, 1 )
    glVertex3f   ( x2, y1, z2 )
    glTexCoord2f ( 1, 0 )
    glVertex3f   ( x1, y1, z2 )
    glTexCoord2f ( 0, 0 )
    glVertex3f   ( x1, y1, z1 )
    glTexCoord2f ( 1, 0 )
    glVertex3f   ( x2, y1, z1 )
    glEnd        ()




def drawfloor(x1, x2, y1, y2, z1, z2,texture):

    glBindTexture ( GL_TEXTURE_2D, texture )
    glBegin      ( GL_POLYGON )                         # back face
    glNormal3f   ( 0.0, 0.0, -1.0 )
    glTexCoord2f ( 1, 0 )
    glVertex3f   ( x2, y1, z1 )
    glTexCoord2f ( 0, 0 )
    glVertex3f   ( x1, y1, z1 )
    glTexCoord2f ( 0, 1 )
    glVertex3f   ( x1, y2, z1 )
    glTexCoord2f ( 1, 1 )
    glVertex3f   ( x2, y2, z1 )
    glEnd        ()



