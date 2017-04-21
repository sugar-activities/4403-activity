# sud.py
import g,random,utils,os,buttons,pygame

squares=[] # 9x9
piles=[0,0,0,0,0,0,0,0,0,0] # piles[1..9]= number of tiles left in pile 1..9
layout=[None,None,None,None,None,None]
layout[0]= [6,0,0,1,0,8,2,0,3,0,2,0,0,4,0,0,9,0,8,0,3,0,0,5,4,0,0,\
            5,0,4,6,0,7,0,0,9,0,3,0,0,0,0,0,5,0,7,0,0,8,0,3,1,0,2,\
            0,0,1,7,0,0,9,0,6,0,8,0,0,3,0,0,2,0,3,0,2,9,0,4,0,0,5]
layout[1]= [9,7,0,3,0,4,0,6,5,0,2,0,5,0,6,0,8,0,0,0,0,0,0,0,0,0,0,\
            0,0,5,8,0,2,9,0,0,0,0,2,0,4,0,3,0,0,0,0,8,7,0,5,1,0,0,\
            0,0,0,0,0,0,0,0,0,0,6,0,2,0,8,0,3,0,8,4,0,1,0,9,0,2,7]
layout[2]= [0,0,1,0,0,0,6,0,0,0,5,0,0,3,0,0,7,0,9,0,0,1,0,6,0,0,4,\
            0,0,2,0,7,0,8,0,0,0,7,0,4,0,3,0,9,0,0,0,4,0,1,0,2,0,0,\
            5,0,0,7,0,9,0,0,2,0,1,0,0,6,0,0,3,0,0,0,9,0,0,0,5,0,0]
layout[3]= [0,9,8,5,0,0,2,0,0,1,0,0,0,0,0,0,0,4,0,5,0,0,0,0,0,3,0,\
            0,0,2,6,4,3,1,0,0,0,0,0,9,0,8,0,0,0,0,0,7,1,5,2,6,0,0,\
            0,7,0,0,0,0,0,8,0,2,0,0,0,0,0,0,0,7,0,0,6,0,0,1,5,2,0]
layout[4]= [3,0,2,0,7,0,5,0,4,0,0,0,0,0,0,0,0,0,0,0,6,2,5,4,0,0,0,\
            0,9,0,0,0,0,6,0,0,0,0,8,9,6,5,1,0,0,0,0,5,0,0,0,0,2,0,\
            0,0,0,1,9,7,8,0,0,0,0,0,0,0,0,0,0,0,5,0,7,0,8,0,2,0,6]
layout[5]= [0,0,0,0,4,1,0,0,0,0,6,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,\
            3,2,0,6,0,0,0,0,0,0,0,0,0,5,0,0,4,1,7,0,0,0,0,0,0,0,0,\
            0,0,0,2,0,0,3,0,0,0,4,8,0,0,0,0,0,0,5,0,1,0,0,0,0,0,0]


class Square:
    def __init__(self,sqr,r,c,x,y): # sq,r,c all 0..8
        self.sqr=sqr; self.r=r; self.c=c; self.x=x; self.y=y
        self.given=False
        self.piece=0 # 0..9 (0=empty)

class Board:
    def __init__(self):
        d=g.d+g.space
        y=g.y0; sqr0=0
        for r in range(9): # 0..8
            x=g.x0; sqr=sqr0
            for c in range(9): # 0..8
                sq=Square(sqr,r,c,x,y)
                squares.append(sq)
                x+=d
                if c in (2,5): sqr+=1
            y+=d
            if r in (2,5): sqr0+=3
        self.layout_n=0
        if g.count>0: self.layout_n=random.randint(1,3)

    def setup(self):
        for i in range(1,10): piles[i]=9 # 1..9
        ind=0
        for piece in layout[self.layout_n]:
            squares[ind].piece=0; squares[ind].given=False
            if piece>0:
                squares[ind].piece=piece; squares[ind].given=True
                piles[piece]-=1
            ind+=1
        self.clear()
        if g.count>0: self.shuffle(); self.layout_n+=1
        if self.layout_n==len(layout):
            self.layout_n=1 # don't do extra easy one again
        g.helped=0 # don't count if helped>5

    def reset(self):
        if self.carry>0: piles[self.carry]+=1 
        for sq in squares:
            if sq.piece>0 and not sq.given:
                piles[sq.piece]+=1; sq.piece=0
        self.clear()

    def clear(self):
        self.carry=0; self.clashes=[]; g.finished=False; g.glow_sq=None

    def draw(self):
        d=g.sy(.16)
        x=squares[0].x-d; y=squares[0].y-d
        g.screen.blit(g.grid,(x,y))
        for sq in squares:
            x=sq.x; y=sq.y
            if sq.piece>0:
                tile=g.cream
                if sq.given: tile=g.cyan
                g.screen.blit(tile,(sq.x,sq.y))
                g.screen.blit(g.pics[sq.piece],(sq.x,sq.y))
        x=squares[0].x-d; y=squares[0].y-d
        g.screen.blit(g.grid1,(x,y))
        y=squares[0].y; dx=g.sy(.8); dy=g.d+g.space
        for r in range(9): # 0..8
            piece=r+1; x=g.sx(.2)
            for i in range(piles[piece]):
                g.screen.blit(g.cream,(x,y))
                g.screen.blit(g.pics[piece],(x,y)); x+=dx
            y+=dy
        for sq in self.clashes: g.screen.blit(g.cross,(sq.x,sq.y))
        if g.glow_sq<>None:
            x=g.glow_sq.x-g.glow_d; y=g.glow_sq.y-g.glow_d
            g.screen.blit(g.glow,(x,y))
        if self.carry:
            mx,my=pygame.mouse.get_pos()
            utils.centre_blit(g.screen,g.shadow,(mx,my))
            utils.centre_blit(g.screen,g.cream,(mx,my))
            utils.centre_blit(g.screen,g.pics[self.carry],(mx,my))
            
    def click(self):
        g.glow_sq=None
        if self.carry==0:
            n=self.which_pile()
            if n>0:
                piles[n]-=1; self.carry=n
            else:
                sq=self.which_square()
                if sq<>None:
                    if not sq.given:
                        if sq<>None: self.carry=sq.piece; sq.piece=0
        else:
            sq=self.which_square()
            if sq==None:
                piles[self.carry]+=1; self.carry=0
            else:
                if not sq.given:
                    if sq.piece>0: # piece already there
                        piles[sq.piece]+=1 # put it back
                    sq.piece=self.carry; self.carry=0
                    buttons.on('reset')
        self.check()

    def right_click(self):
        g.glow_sq=None
        if self.carry>0:
            piles[self.carry]+=1; self.carry=0
        else:
            sq=self.which_square()
            if sq==None: return
            if sq.given: return
            if sq.piece==0: return
            piles[sq.piece]+=1 # put it back
            sq.piece=0
            self.check() # maybe clash removed

    def which_pile(self):
        y=squares[0].y; dx=g.sy(.8); dy=g.d+g.space
        for r in range(1,10): # 1..9
            x=g.sx(.2)
            for i in range(1,piles[r]+1):
                if i==piles[r]:
                    if utils.mouse_in(x,y,x+g.d,y+g.d): return r
                x+=dx
            y+=dy
        return 0
    
    def which_square(self):
        for sq in squares:
            if utils.mouse_in(sq.x,sq.y,sq.x+g.d,sq.y+g.d): return sq
        return None
        
    def check(self): # generates list of clashing squares
        clashes=[]
        # rows
        for r in range(9): # 0..8
            for piece in range(1,10): # 1..9
                sqs=[]
                for sq in squares:
                    if sq.r==r:
                        if sq.piece==piece: sqs.append(sq)
                if len(sqs)>1:
                    for sq in sqs:
                        if sq not in clashes: clashes.append(sq)
        #columns
        for c in range(9): # 0..8
            for piece in range(1,10): # 1..9
                sqs=[]
                for sq in squares:
                    if sq.c==c:
                        if sq.piece==piece: sqs.append(sq)
                if len(sqs)>1:
                    for sq in sqs:
                        if sq not in clashes: clashes.append(sq)
        #squares
        for sqr in range(9): # 0..8
            for piece in range(1,10): # 1..9
                sqs=[]
                for sq in squares:
                    if sq.sqr==sqr:
                        if sq.piece==piece: sqs.append(sq)
                if len(sqs)>1:
                    for sq in sqs:
                        if sq not in clashes: clashes.append(sq)
        self.clashes=clashes
        if len(clashes)==0: self.complete() # check if complete

    def complete(self):
        if g.finished:
            return True
        else:
            if self.carry>0: return False # make sure last piece put down !
            for i in range(1,10): # 1..9
                if piles[i]>0: return False
            g.finished=True
            if g.helped<6: g.count+=1
            return True
        
    def row_swap(self,r1,r2):
        ind1=r1*9; ind2=r2*9
        for i in range(9): # 0..8
            sq1=squares[ind1]; sq2=squares[ind2]
            sq1.given,sq2.given=sq2.given,sq1.given
            sq1.piece,sq2.piece=sq2.piece,sq1.piece
            ind1+=1; ind2+=1
        
    def col_swap(self,c1,c2):
        ind1=c1; ind2=c2
        for i in range(9): # 0..8
            sq1=squares[ind1]; sq2=squares[ind2]
            sq1.given,sq2.given=sq2.given,sq1.given
            sq1.piece,sq2.piece=sq2.piece,sq1.piece
            ind1+=9; ind2+=9
        
    def shuffle(self): # shuffle the current layout
        for i in range(5):
            # row swap
            r1=random.randint(0,2); r2=random.randint(0,2)
            d=random.randint(0,2)*3
            self.row_swap(r1+d,r2+d)
            # col swap
            c1=random.randint(0,2); c2=random.randint(0,2)
            d=random.randint(0,2)*3
            self.col_swap(c1+d,c2+d)
            # hor squares swap
            r1=random.randint(0,2)*3; r2=random.randint(0,2)*3
            for d in range(3): self.row_swap(r1+d,r2+d)
            # ver squares swap
            c1=random.randint(0,2)*3; c2=random.randint(0,2)*3
            for d in range(3): self.col_swap(c1+d,c2+d)

    def find_move(self):
        for sq in squares:
            if sq.piece==0:
                for r in range(1,10): # 1..9
                    if piles[r]>0:
                        sq.piece=r; self.check(); sq.piece=0
                        if len(self.clashes)==0:
                            if self.only(r,sq):
                                g.helped+=1
                                g.glow_sq=sq
                                piles[r]-=1; sq.piece=r; return
                        else:
                            self.clashes=[]

    def solve(self): # for debugging
        while not g.finished:
            self.find_move()
            self.complete()

    # trying piece0 in sq0
    # is this the only poss posn in any of this row or col or sq?
    def only(self,piece0,sq0):
        r=sq0.r; c=sq0.c; sqr=sq0.sqr
        #row
        result=True
        for sq in squares:
            if sq.r==r:
                if sq.c<>c:
                    if sq.piece==0:
                        sq.piece=piece0
                        self.check()
                        sq.piece=0
                        if len(self.clashes)==0: result=False; break
                        self.clashes=[]
        if result: return True
        result=True
        #col
        for sq in squares:
            if sq.c==c:
                if sq.r<>r:
                    if sq.piece==0:
                        sq.piece=piece0
                        self.check()
                        sq.piece=0
                        if len(self.clashes)==0: result=False; break
                        self.clashes=[]
        if result: return True
        result=True
        #square
        for sq in squares:
            if sq.sqr==sqr:
                if sq<>sq0:
                    if sq.piece==0:
                        sq.piece=piece0
                        self.check()
                        sq.piece=0
                        if len(self.clashes)==0: result=False; break
                        self.clashes=[]
        if result: return True
        return False
        

    
                    


