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
from OpenGL.GL.ARB.vertex_buffer_object import *######


from pygame.locals import *
from pygame.display import *
from pygame.event import *
from pygame.key import *
from pygame.mouse import *
from pygame.font import *
from pygame.image import *
from pygame.time import *
from pygame import *

from vector02 import *



mapgrid=[1,2,0.5,0.75,2,
         1,0,0,0,1,
         1,0,0.25,0,1,
         1,0,0.25,0,1,
         1,0.25,1,0.25,1]

bigmap=range(1,2501)





LightAmb=(0.7, 0.7, 0.7)
LightDif=(1.0, 1.0, 1.0)
LightPos=(400.0, 400.0, 600.0, 1000.0)

fogMode=GL_EXP
fogColor=(0.5,0.5,0.5,1.0)

kSpeed=0.03 #skorost dvizenija kameri
g_Camera=CCamera()
g_Camera.PositionCamera(20,20,23,0,20,23,0,0,1)#moja pozicija,23 eto visota kameri tipa 230 santimetrov rost :)

gTime=0.0




SCREEN_SIZE=(1280,600)

##delaet iz odnomernogo massiva dvuhmernii!
def group(array, howmany):
    """Turns a 1D list into a 2D list"""
    i=0
    tmp=[]
    while i<len(array):
        tmp.extend([[array[i+j] for j in range(howmany)]])
        i+=howmany
    return tmp






#sozdaet v scene slu4ainie stolbiki i 0
def scenedoing(string):
    """Generiruet zapisi v vide 0 ili cifr """
    for n in range(len(string)):
        if random.randint(1,100) >=90 :
            string[n]=random.randint(1,7)# tipa 10% dolzno viiti
        else :
            string[n]=0
    return string

scenedoing(bigmap)
#sdes delaetsja iz odnomernogo massiva dvuhmernii s pomowju group
mapgrid=group(mapgrid,5)
bigmap=group(bigmap,50)

def scene2():
    drawfloor(-10000,10000,10000,-10000,0,0,texturefloor)
    for i in range(0,50,1):
        for b in range(0,50,1):
            if bigmap[i][b] != 0 :
                drawbox((i*20),(i*20)+20,(b*20),(b*20)+20,0,bigmap[i][b]*40,texturecube)            

          

def scene1():
    drawfloor(-10000,10000,10000,-10000,0,0,texturefloor)
    for i in range(0,5,1):
        for b in range(0,5,1):
            if mapgrid[i][b] != 0 :
                drawbox((i*20),(i*20)+20,(b*20),(b*20)+20,0,mapgrid[i][b]*40,texturecube)

    



def loadtexture ( fileName ):
    image  = Image.open ( fileName )
    width  = image.size [0]
    height = image.size [1]
    image  = image.tostring ( "raw", "RGBX", 0, -1 )
    texture = glGenTextures ( 1 )

    #glActiveTextureARB(GL_TEXTURE1_ARB)
    #glEnable(GL_TEXTURE_2D)
    
    
    glBindTexture     ( GL_TEXTURE_2D, texture )   # 2d texture (x and y size)
    glPixelStorei     ( GL_UNPACK_ALIGNMENT,1 )
    glTexParameterf   ( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT )
    glTexParameterf   ( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT )
    glTexParameteri   ( GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR )
    glTexParameteri   ( GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR_MIPMAP_LINEAR )
    gluBuild2DMipmaps ( GL_TEXTURE_2D, 3, width, height, GL_RGBA, GL_UNSIGNED_BYTE, image )
    return texture


def resize(width, height):
    if height==0:
        height=1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, 1.0*width/height, 1.0, 1000.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()




def init():
    glEnable(GL_TEXTURE_2D)
    glShadeModel(GL_SMOOTH)
    glClearColor(0.9, 0.9, 0.9, 1.0)
    glClearDepth(100.0)
    glEnable(GL_DEPTH_TEST)
    #glEnable(GL_CULL_FACE)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glShadeModel (GL_FLAT)
    glLineWidth(1.5)
    glPointSize(2.0)
    glInitMultitextureARB()
    #glEnable(GL_COLOR_MATERIAL)
    glLightfv(GL_LIGHT0, GL_AMBIENT, LightAmb)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, LightDif)
    glLightfv(GL_LIGHT0, GL_POSITION, LightPos)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    #glFogi(GL_FOG_MODE,fogMode)
    #glFogfv(GL_FOG_COLOR,fogColor)
    #glFogf(GL_FOG_DENSITY,0.002)
    #glEnable(GL_FOG)



    
 
#vivodit stroku s zadanimi koordinatami vidna otovsjudu!,est variant s vivodom na fone kvadrata
def TextOut(text,x,y,z):
    textureSurface = pygame.Surface((512,512))
    x,y =0,0#pygame.mouse.get_rel()
    title_font = pygame.font.Font(None, 25)
 
    #Text = "Posizija 0,0 and FPS : %s "%(frames)
    Text = text
    #print mouseText
    text2 = title_font.render(Text, 1, (250,250,250))
    textureSurface.blit(text2, (200,70))
 
    #Raster Block 1
    #textureData = pygame.image.tostring(textureSurface, "RGBX", 1)
    #size = textureSurface.get_size()
   # glRasterPos3f(-.2,-.2,-1)
   # glDrawPixels(size[0], size[1], GL_RGBA, GL_UNSIGNED_BYTE, textureData)
 
    #Raster Block 2
    textureData = pygame.image.tostring(text2, "RGBX", 1)
    size = text2.get_size()
    glRasterPos3f(x,y,z)
    glDrawPixels(size[0], size[1], GL_RGBA, GL_UNSIGNED_BYTE, textureData)




def draw():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, 4.0/3.0, 1.0, 1000.0)
    glMatrixMode(GL_MODELVIEW)
    
    glLoadIdentity()
    #glRotate(-90,1,0,0)

    gluLookAt(g_Camera.m_vPosition.x,g_Camera.m_vPosition.y,g_Camera.m_vPosition.z,
              g_Camera.m_vView.x,g_Camera.m_vView.y,g_Camera.m_vView.z,
              g_Camera.m_vUpVector.x,g_Camera.m_vUpVector.y,g_Camera.m_vUpVector.z)


    scene2()
    
    ##vivodit FPS
    TextOut("Posizija 0,0,50 and FPS : %s "%((frames*1000)/(pygame.time.get_ticks()-ticks)),0,0,50)
    #vremja s na4ala zapusska igri
    minutes,seconds=divmod(gTime,60.0)
    TextOut("elapsedTime: %d:%02d"%(int(minutes), int(seconds)),0,0,60)
    
    
#sdes obnsovaljetsja kamera i obrabativajutsja nazatija na knopki!
def input(events):
    
    pygame.event.pump()
    if pygame.key.get_pressed()[27]==1:#esc
        os._exit(0)
    if pygame.key.get_pressed()[119]==1:#w
        g_Camera.MoveCamera(kSpeed)
    if pygame.key.get_pressed()[115]==1:#s
        g_Camera.MoveCamera(-kSpeed)
    if pygame.key.get_pressed()[97]==1:#a
        g_Camera.StrafeCamera(-kSpeed*20)
    if pygame.key.get_pressed()[100]==1:#d
        g_Camera.StrafeCamera(kSpeed*20)
    if pygame.key.get_pressed()[101]==1:#q
        g_Camera.RotateView(-kSpeed*2,0,0,1)
    if pygame.key.get_pressed()[113]==1:#e
        g_Camera.RotateView(kSpeed*2,0,0,1)

     
    
#sdes mozna vstavt kod vi4eslenija dvizenija objektov?    
def updateCamera(dt):
    
    g_Camera.Update()

    
    
      
    
   
    
   
def main():
    global mx,my,gTime,texturecube,texturefloor,SCREEN_SIZE,frames,ticks
    
    video_flags = OPENGL|DOUBLEBUF|NOFRAME|ASYNCBLIT|HWSURFACE|HWPALETTE
    #|FULLSCREEN
    

 
    
    
    pygame.init()
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    try:
        surface = pygame.display.set_mode(SCREEN_SIZE, video_flags)
    except pygame.error:
        print "I only know about the following modes:"
        print pygame.display.list_modes()
        print "and of those, only the following fit our flags:"
        print pygame.display.list_modes(0,video_flags)
        return

    if swap_control and wglInitSwapControlARB():
        print "setting swap control"
        if wglSwapIntervalEXT(0):
            print "swap control set to 0"
        else:
            print "swap control not set"
    else:
        print "cannot set vsync"
    resize(*SCREEN_SIZE)
    pygame.display.set_caption("pong I")
    init()
    print "texture units:",glGetIntegerv(GL_MAX_TEXTURE_UNITS_ARB)
    frames = 0
    ticks = pygame.time.get_ticks()
    myClock=pygame.time.Clock()
    texturecube= loadtexture ( "cet.bmp" )
    texturefloor= loadtexture ("cet.bmp")


    myClock.tick()
    gameOver=0
    while not gameOver:
        
        ms=myClock.tick(100)
        tm=pygame.time.get_ticks()
        
        gTime=tm/1000.0
        #update #sdes opredeljaetsja skorost obnovlenija funkcii updatecamera()
        deltaT=ms/1000.0
        updateCamera(deltaT)
        draw()#sna4ala risuem ,patom s4itaem fiziku i ai esli kogdto budet stoto!
         
        pygame.time.wait(2)
        pygame.display.flip()
        frames = frames+1
        input(pygame.event.get())
        
        
    
        
        
   
    
if __name__ == '__main__': main()
    
