#!/usr/bin/python
# Sudoku.py
"""
    Copyright (C) 2010  Peter Hewitt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""
import g,sud,pygame,utils,gtk,sys,buttons,load_save

class Sudoku:

    def __init__(self):
        self.journal=True # set to False if we come in via main()
        self.canvas=None # set to the pygame canvas if we come in via activity.py

    def display(self):
        grey=100; g.screen.fill((grey,grey,grey))
        buttons.draw()
        g.screen.blit(g.help1,g.help1_xy)
        utils.display_number(g.count,(g.xc,g.yc),g.font2,utils.CREAM)
        colour=utils.YELLOW
        if g.helped>5: colour=utils.RED
        utils.display_number(g.helped,(g.xc,g.yc+g.sy(6)),g.font1,colour)
        if g.finished:
            utils.centre_blit(g.screen,g.smiley,(g.sx(4),g.smiley_y))
        self.board.draw()

    def do_button(self,bu):
        if bu=='reset': self.board.reset(); buttons.off('reset')
        if bu=='new': self.board.setup(); buttons.off('reset')

    def help_check(self):
        if utils.mouse_on_img(g.help1,g.help1_xy):
            pygame.mouse.set_visible(False)
            g.glow_sq=None # turn off any glow
            self.display()
            utils.centre_blit(g.screen,g.thinking,g.thinking_xy)
            pygame.display.flip()
            self.board.find_move()
            # flush event queue
            while gtk.events_pending(): gtk.main_iteration()
            for event in pygame.event.get(): pass
            pygame.mouse.set_visible(True)
            return True
        return False

    def buttons_setup(self):
        d=g.d+g.space; x=g.xc; y=g.y0+d; dy=d
        buttons.Button('reset',(x,y),True); y+=dy
        buttons.Button('new',(x,y),True); y+=dy
        g.yc=y+d+d # for count
        if g.count==0: buttons.off('new')
        if g.started==0:
            buttons.off('reset') # turned on when tile placed by sud.click()

    def run(self):
        g.init()
        if not self.journal: utils.load()
        self.board=sud.Board()
        self.board.setup()
        load_save.retrieve()
        self.board.check()
        self.buttons_setup()
        if self.journal: # Sugar only
            a,b,c,d=pygame.cursors.load_xbm('my_cursor.xbm','my_cursor_mask.xbm')
            pygame.mouse.set_cursor(a,b,c,d)
        going=True
        while going:
            # Pump GTK messages.
            while gtk.events_pending(): gtk.main_iteration()

            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type==pygame.QUIT: # only in standalone version
                    if not self.journal: utils.save()
                    going=False
                elif event.type == pygame.MOUSEMOTION:
                    g.redraw=True
                    if self.canvas<>None: self.canvas.grab_focus()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    g.redraw=True
                    if event.button==2: # centre button
                        if not self.journal:
                            g.version_display=not g.version_display
                    if event.button==1:
                        bu=buttons.check()
                        if bu!='':
                            self.do_button(bu)
                        elif not g.finished:
                            if not self.help_check():
                                self.board.click()
                                if g.finished:
                                    buttons.on('new'); buttons.off('reset')
                    if event.button==3:
                        if not g.finished:
                            self.board.right_click()
            if not going: break
            if g.redraw:
                self.display()
                if g.version_display: utils.version_display()
                #g.screen.blit(g.pointer,(g.mx,g.my))
                pygame.display.flip()
                g.redraw=False
            self.count=g.count
            tf=False
            if pygame.mouse.get_focused(): tf=True
            pygame.mouse.set_visible(tf)
            g.clock.tick(40)

if __name__=="__main__":
    pygame.init()
    pygame.display.set_mode((800,600))
    game=Sudoku()
    game.journal=False
    game.run()
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)
