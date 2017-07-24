CINEMA_CODE={'QUEEN ST':502
} #I'm too lazy to update this, just go to main page, they have the codes there


VARS={'USERNAME':'',
       'PASSWORD':'',
       'CINEMA':502,
       'CARD_NUM':,
       'EX_DATE':''
}

def visualisegrid(grid):
    for row in grid:
        for slot in row:
            if slot[0]==True:
                print('.',end='')
            elif slot[0]==False :
                print('x',end='')
            else:
                print('O',end='')
        print()
def check(l):
    for i in l:
        if i[0]==False:
            return i[0]
    return True
def calculate(grid):
    numrow=len(grid)
    numcol=len(grid[0])
    idealCol=numcol//2+1
    idealRow=numrow//2+1
    basePointCol=numcol//2   
    basePointRow=numrow//2+1
    rowpoints=[]
    colpoints=[]
    for i in range(basePointCol+1):
        colpoints.append(i)
    for i in range(basePointCol-1,-1,-1):
        colpoints.append(i)
        if len(colpoints)>=numcol:break
    for i in range(0,basePointRow-1):
        rowpoints.append(i-0.5)
    if numrow%2==0: basePointRow-1
    for i in range(basePointRow-1,-1,-1):
        rowpoints.append(i)
        if len(rowpoints)>=numrow:break
    pointgrid=[]
    for i in range(numrow):
        temprow=[]
        for j in range(numcol):
            point=rowpoints[i]+colpoints[j]
            temprow.append(point)
        pointgrid.append(temprow)

    return pointgrid

         
    
    
