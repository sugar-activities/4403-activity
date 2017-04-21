#load_save.py
import g,sud

loaded=[] # list of strings

def load(f):
    global loaded
    try:
        for line in f.readlines():
            loaded.append(line)
    except:
        pass

def save(f):
    f.write(str(g.count)+'\n')
    if g.finished: g.helped=0
    f.write(str(g.helped)+'\n')
    if not g.finished:
        for sq in sud.squares:
            piece=sq.piece
            if sq.given: piece+=10
            f.write(str(piece)+'\n')

def retrieve():
    global loaded
    if len(loaded)==0:
        pass
    elif len(loaded)==1:
        g.count=int(loaded[0])
    elif len(loaded)==2:
        g.count=int(loaded[0])
        g.helped=int(loaded[1])
    else:
        g.count=int(loaded[0])
        g.helped=int(loaded[1])
        for i in range(1,10): sud.piles[i]=9 # 1..9
        ind=2
        for sq in sud.squares:
            piece=int(loaded[ind]); given=False
            if piece>0 and piece<10: g.started=True
            if piece>9: piece-=10; given=True
            sq.piece=piece; sq.given=given; sud.piles[piece]-=1
            ind+=1


