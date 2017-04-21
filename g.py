# g.py - globals
import pygame,utils,random

app='Sudoku'; ver='1.0'
ver='2.0'
# Journal load & save
ver='2.1'
# don't save finished puzzle
# thinking smiley
# no pointer while thinking
# improved visibility of black squares
# help counter added - only score if < 6
ver='2.2'
# g.py - sx & sy functions now have round off
# turn glow off when help clicked
ver='3.0'
# x-cursor
# redraw every 10 pixels
ver='3.1'
# sugar cursor
# no FPS
ver='3.2'
# g.mx,g.my not used anymore
# reset button if piece already in place after load - g.started
# right click puts a piece back
# thinking smiley
ver='3.3'
# save zero g.helped if finished
# flush event queue after help
# no pointer during help
# move smiley

def init(): # called by run()
    random.seed()
    global redraw
    global screen,w,h,pointer,font1,font2,clock
    global factor,offset,imgf,message,version_display
    redraw=True
    version_display=False
    screen = pygame.display.get_surface()
    grey=100; screen.fill((grey,grey,grey))
    pygame.display.flip()
    w,h=screen.get_size()
    if float(w)/float(h)>1.5: #widescreen
        offset=(w-4*h/3)/2 # we assume 4:3 - centre on widescreen
    else:
        h=int(.75*w) # allow for toolbar - works to 4:3
        offset=0
    #pygame.mouse.set_visible(False)
    pygame.display.set_caption(app)
    clock=pygame.time.Clock()
    factor=float(h)/24 # measurement scaling factor (32x24 = design units)
    imgf=float(h)/900 # image scaling factor - all images built for 1200x900
    if pygame.font:
        t=int(50*imgf); font1=pygame.font.Font(None,t)
        t=int(80*imgf); font2=pygame.font.Font(None,t)
    #pointer=utils.load_image('pointer.png',True)
    message=''
    
    # this activity only
    global pics,cream,cyan,d,count,yc,space,grid,grid1,cross,x0,y0,xc,smiley
    global glow,glow_sq,glow_d,shadow,smiley_y,finished,help1,help1_xy,started
    global thinking,thinking_xy,helped
    pics=[None]
    for i in range(1,10):
        img=utils.load_image(str(i)+'.png',True); pics.append(img)
    cream=utils.load_image('cream.png',False)
    cyan=utils.load_image('cyan.png',False)
    d=cyan.get_width(); space=sy(.08)
    yc=sy(23)
    grid=utils.load_image("grid.png",False)
    grid1=utils.load_image("grid1.png",True)
    cross=utils.load_image("cross.png",True)
    x0=sx(8.4); y0=sy(.6); xc=sx(30.7); yc=0; smiley_y=y0+4.5*(d+space)
    smiley=utils.load_image("smiley.png",True)
    glow=utils.load_image("glow.png",True)
    glow_d=(glow.get_width()-d)/2
    glow_sq=None
    shadow=utils.load_image("shadow.png",True)
    helped=0
    help1=utils.load_image("help1.png",True)
    help1_xy=(sx(29.55),sy(18.8))
    count=0
    finished=False
    started=0 # set by load_save retrieve if piece(s) already in place
    thinking=utils.load_image("thinking.png",True)
    thinking_xy=(sx(4.4),sy(11))
    
def sx(f): # scale x function
    return int(f*factor+offset+.5)

def sy(f): # scale y function
    return int(f*factor+.5)
