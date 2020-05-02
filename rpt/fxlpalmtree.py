'''
Created on Nov 11, 2009

palm tree is parsing mechanism from flat-flag-rows into grouped-cluster of its children (palmhand of tree)
It's used and is part of fxl Report Builder.

@author: Fathony
'''

# from xlsdom import xlDoc,xlWorksheet,xlCell,xlRow
# from fxl import BANDS
from xml.dom.minidom import Element
import re

BANDS = {}
YCELL = 0
def strToPaths(pathf):
    if pathf.find('.') >=0:
        paths=pathf.split('.')
    else: 
        paths=[pathf]
    therow=list()
    for path in paths:
        if path:
            if path.find(':') >=0:
                (band,kind) = path.split(':')
            else:
                band = path
                kind = 'DAT'
            band = band.strip('~')
            kind = {'F':'FOT', 'H':'HDR', 'D':'DAT', 'A':'ALT'}.get(kind, kind)
            therow.append([band,kind])
        # elif path.strip():
            # therow.append([path,'DAT'])
        else:
            #therow.append([path]) # NO WAY! only perfect format is supported.
            therow.append(['',''])
    return therow

class Tpl(object):
    def __init__(self, cell):
        self.value = cell.value
        if self.value:
            self.style = cell.style
        self._field = cell.comment.text if cell.comment else None
            
    def apply(self, cell, data):
        if self._field:
            print('_f:', self._field)
            print(data)
            cell.value = data.get(self._field)
        else:
            cell.value = self.value
        
    def __repr__(self):
        return '' if self.value == None else str(self.value)
        
def parse_row(row):
    # return [Tpl(cell) for cell in row[1:]]
    cells = [Tpl(cell) for cell in row[1:]]
    while cells and not cells[-1].value:
        cells.pop()
    # z = len(cells) -1
    # for i,c in enumerate(reversed(cells)):
        # if c.value:
            # z -= i
            # break
    # cells = cells[:z]
    print(len(cells))
    return cells

### ========================================================================= ###
### ######   UPDATE =FORMULA() ()  ######################################### ###
### ========================================================================= ###

def _validateFoot(row,tplDatAltRowcount,datcount):
    "Handle the formula which is ranged within DAT..ALT into whole parsed of DAT..ALT"
    for icell in range(len(row.CellS)):
        cell = row.Cell(icell)
        f = cell.getFormula()
        #+([a-zA-Z_][a-zA-Z_0-9]*)
        #ss = '^(=[A-Z]+\(+)(\R\[+)([\-0-9]+)(\]+)(\C[\[\]\-0-9]*)(:*)(\R\[+)([\-0-9]*)(\]*)(\C[\[\]\-0-9]*)(\)*)$'
        #ss = '^(=[a-zA-Z_][a-zA-Z_0-9]+\(+)(\R\[+)([\-0-9]+)(\]+)(\C[\[\]\-0-9]*)(:*)(\R\[+)([\-0-9]*)(\]*)(\C[\[\]\-0-9]*)(\)*)$'
        #pat = r'^(=[a-zA-Z_][a-zA-Z_0-9]+\(+)(\R\[+)([\-0-9]+)(\]+)(\C[\[\]\-0-9]*)(:*)(\R\[+)([\-0-9]*)(\]*)(.*)$'
        pat = r'^(=[a-zA-Z_][a-zA-Z_0-9]+\(+)(\R\[+)([\-0-9]+)(\]+)(\C[\[\]\-0-9]*)(:*)(\R\[+)([\-0-9]*)(\]*)(.*)$'

        #=MAX(R[-2]C[-0]:R[-1]C[-0])
        #('=MAX(', 'R[', '-2', ']', 'C[-0]', ':', 'R[', '-1', ']', 'C[-0]', ')')
        #=MIN(R[-3]C:R[-2]C) 
        mm=re.search(pat, f)
        try:
            r=[]
            for m in mm.groups():
                r+=[m]
        except:
            continue
        # =MAX(R[-2]C[-0]:R[-1]C[-0])
        # =COUNTIF(R[-12]C[9]:R[-11]C[9],RC[-1])
        r7= int(r[7])
        r2= int(r[2])
        if abs(r2) - abs(r7) ==tplDatAltRowcount-1:
            r2 = r7  + (-1* (datcount-1))
            r[2]='%d' % r2
            f=''.join(r)
            #for m in range(len(r)):
            #    f+=r[m]
            #print f
            #print r
            cell.setFormula(f)
        
def _validateName(xl,tplDatAltRowcount,datcount):
    pat = r"^(=[^#]*)([=a-zA-Z_0-9\'\s!]\R+)([0-9]+)(\C)([0-9]+)(\:)(\R)([0-9]+)(\C)([0-9]+)$"
    #import re
    prog = re.compile(pat)
    #result = prog.match(str)
    for nr in xl.NamedRangeS:
        RefersTo = nr.getAttribute('ss:RefersTo')

        if RefersTo.find(':') >= 0:
            mm=prog.search(RefersTo)
            try:
                r=[]
                for m in mm.groups():
                    r+=[m]
            except:
                continue
            r7 = int(r[7])
            r2 = int(r[2])
            if r7-r2==tplDatAltRowcount-1:
                r7 = r2  + (datcount-1)
                r[7]='%d' % r7
                RefersTo=''.join(r)
                #for m in range(len(r)):
                #    f+=r[m]
                #print f
                #print r
                nr.setAttribute('ss:RefersTo',RefersTo)
            
        
### ========================================================================= ###
### ######   FILL A SINGLE ROW ()  ######################################### ###
### ========================================================================= ###

def _fillxlrow(worksheet,row,typvars,vars):
    global YCELL
    YCELL +=1 # ws.cell() always require one based (not zero based)
    for x,tcell in enumerate(row):
        col = x+1 # ws.cell() always require one based (not zero based)
        cell=worksheet.cell(row=YCELL, column=col)
        # txt = cell.getText()
        if True:
            tcell.apply(cell, vars)
        # elif txt.find(':') >=0:
            # cell.setText('')
        else:
            f = cell.getFormula()
            if f and f.rfind(')') < 0: #its lookup to the name
                f=f.lstrip('= ')
                varf=f
                if varf.find('.')>=0:
                    band,varf=f.split('.',2)
                #band='i not really need band here'
                
                cell.delFormula()
                try:typevar=typvars[varf]
                except:typevar=None
                try:
                    if vars.has_key(varf):
                        if vars[varf] != None:
                        #cell.setText(vars[varf],typevar)
                            cell.setText(vars[varf],True)                            
                        else:                        
                            #cell.setText('') bugfix 2009.12.14                            
                            cell.clearData()
                    #else: cell.setText('diubah(%s)' % varf)
                except:
                    pass
    # parsed.Table.appendChild(row.row)
    return 1 #single row

class fxl:
    ''' 
    XML-Excel-spreadsheet format Filler
    PLAIN MODEL. 
    All inheritence may implement in colaboration with CSV,Dictionary,DB, etc...
    All inheritence must Consist at least methods: hasData() and bandData() and bandHeader()  
    '''
    def __init__( self ):
        self.parent = ''
        if not hasattr( self, 'child' ):
            self.child = {}
        self.counter = 0
        self.xl = None
        #self.cur=None
        #self.params={}
        #self.defaults={}
        #self.SQL=''
        #register class instance:
        if not hasattr( self, '_name' ):
            self._name = self.__class__.__name__
        BANDS[self._name] = self
        #else: BANDS[self.__class__.__name__] = self

    #def onCreate(self):
    def init( self ): #its call before any worksheet parsed.
        pass
    
    def hasData( self ):
        "Needed for prevent endless loop"
        return self.counter < 3
    
    def reset( self ):
        self.counter = 0
        
    def bandTitle( self ):
        #canReturn= ['How Much','Where','When']
        return []
    
    def bandType( self ):
        #canReturn= ['Number','String','DateTime']
        return []
    
    def bandData( self ):
        if self.hasData():
            self.counter += 1
            ##t=time.time()
            t = datetime.fromtimestamp( time.time() )
            t = t.strftime( '%Y-%m-%dT%H:%M:%S' )
            return {'No.':self.counter, 'str':'Number' + str( self.counter ), 'today':t}
        else:
            return {}
            
class palmTree():
    "PalmTree is advanced mechanism of FXL Report Builder using class() for it iteration"
    def __init__(self,paths=None,rowobj=None, parent=None):
        if paths and paths[0] != '':
            self.Band=paths[0][0]
            #self.Kind={'HDR':list(),'DAT':list(),'ALT':list(),'FOT':list()}            
        else: 
            self.Band=''
            #self.tree=list()
        self.clear()
        self.parent = parent
        if rowobj:
            self.put(paths, rowobj)
    def __len__(self):
        return len(self.tree)
    
    def __iter__(self):
        return self
    
    def next(self):
        if not self.tree or self.curiter >= len(self.tree):
            raise StopIteration 
        else:
            result= self.tree[self.curiter]
            self.curiter+=1
            return result

    def clear(self):
        "make empty the children"
        self.Kind={'HDR':list(),'DAT':list(),'ALT':list(),'FOT':list()}            
        self.tree=list()
        self.curiter=0 #len(self.tree)
        
    def accept(self,paths,rowobj):
        "Is paths leading by self.band?" #call within class it self
        if len(paths) > 0 and paths[0][0] == self.Band:
            #cut leading:
            ownpath=paths.pop(0)
            if paths: #stil has tail?                                # yg bakal ditambah = anak.
                self.put(paths, rowobj,ownpath)
            else:                                                    # artinya ini baris kedua dari band yg sama, yg bakal ditambah = sibling.
                try:
                    band,kind=ownpath
                    #kind=ownpath[1]
                    if not self.Kind[kind]:
                        self.Kind[kind]=palmTree(parent=self)
                    self.Kind[kind].tree.append(rowobj)
                except:
                    pass
            return True
        else: return False
        
    def put(self,paths,rowobj,ownpath=list()):
        "Hire rowObj dictated by paths" #call by outer class, also by __init__
        if not paths or paths[0][0] == '': ## '' ~~> '9'=OBJ  ## it may the right most paths 
            self.tree.append(rowobj)
        elif not self.accept(paths, rowobj):
            if ownpath and ownpath[0]==self.Band: #exp.: kpi:FOT
                if not self.Kind[ownpath[1]]:
                    self.Kind[ownpath[1]]=palmTree(parent=self) # create New
                    #self.Kind[ownpath[1]].append(palmTree()) # create New
                found=False
                for twig in self.Kind[ownpath[1]].tree:
                    if isinstance(twig,palmTree) and twig.accept(paths,rowobj):
                        found=True
                        break
                if not found:
                    self.Kind[ownpath[1]].tree.append(palmTree(paths,rowobj, parent=self))                
            else:
                found=False
                for twig in self.tree:
                    if isinstance(twig,palmTree) and twig.accept(paths,rowobj):
                        found=True
                        break
                if not found:
                    #ownpath=paths.pop(0)
                    self.tree.append(palmTree(paths,rowobj,parent=self))
                    
    def harvestCluster(self,harvest,plainvars):
        "fill a single cluster. a cluster exists of HDR,DAT,ALT,FOT"        
        if not self.Band in BANDS: #exit()        
            #return False,False            
            return
        BANDS[self.Band].reset()
        
        
        L=len(self.Kind['DAT'])
        L+=len(self.Kind['ALT'])
        self.tplDatAltRows=L
        self.usealt=len(self.Kind['ALT']) > 0
        self.altused=False 
        self.dynvar=BANDS[self.Band].bandData()  #GET FIST DATA
        self.ssTypeS=BANDS[self.Band].bandType()
        self.datharvested=0
        rowsharvest=0
        myvars=plainvars.copy()
        for kind in ['HDR','DAT','FOT']: #--- kind
            if not self.Kind[kind]: continue #skip if empty
                        
                            
            while True: #has data?
                myvars.update(self.dynvar)        
                for cluster in self.Kind[kind]:
                    if isinstance(cluster,list): 
                        if kind=='FOT':
                            _validateFoot(cluster,self.tplDatAltRows,self.datharvested)
                        if self.dynvar or kind in ['HDR']:
                            #DONT PRINT IF NO DATA, BUT HDR IS ALWAYS PRINT
                            rowsharvest+=_fillxlrow(harvest,cluster,self.ssTypeS,myvars)         
                    elif isinstance(cluster,palmTree):
                        cluster.harvestCluster(harvest,plainvars)
                
                if kind in ['DAT','ALT']: #fetch next:
                    self.datharvested+=1
                    if not BANDS[self.Band].hasData():
                        # _validateName(xl,self.tplDatAltRows,self.datharvested)
                        break
                    self.dynvar=BANDS[self.Band].bandData()
                    if self.usealt: # and kind=='DAT': #--- selang-seling
                        self.altused=not self.altused
                        if self.altused:
                            kind='ALT'
                        else:
                            kind='DAT'
                else:
                    break
                if YCELL > 30: 
                    break #limit develoopment
                
                
        #=======================================================================
        # dat=GROUP['DAT']
        # tplDatAltRows+=len(dat['Rows'])
        # if GROUP.has_key('ALT'):
        #    alt=GROUP['ALT']
        #    tplDatAltRows+=len(alt['Rows'])
        # band=dat['Band']
        # data=BANDS[band].bandData()
        # type=BANDS[band].bandType()
        # usalt=False
        #=======================================================================
        
        #=======================================================================
        # #--------------------------------- HDR
        # if GROUP.has_key('HDR'):
        #    hdr=GROUP['HDR']
        #    myvars.update(data)
        
        #    
        # #--------------------------------- DAT
        # datcount=0
        # 
        # while BANDS[band].hasData():
        #    datcount+=1
        #    if usalt:
        #        rows = alt
        #    else: 
        #        rows = dat
        #    myvars.update(data)    
        #    data=BANDS[band].bandData()
        #    if alt: usalt = not usalt
        # 
        # #--------------------------------- FOOTER
        # if GROUP.has_key('FOT'):
        #    foot=GROUP['FOT']
        #    myvars.update(data)
        #    for row in foot['Rows'].values():
        #        _validateFoot(row,tplDatAltRows,datcount)
        #    
        # #--------------------------------- NAMES
        # _validateName(xl,tplDatAltRows,datcount)
        #=======================================================================
    
    def harvestFarm(self,worksheet,ourvars={}):
        "fill a worksheet with clustered-seed that prepared previously"
        
        # if not self.tree: 
            # return worksheet

        # harvest=worksheet.worksheet.ownerDocument.importNode(worksheet.worksheet,1)        
        
        # harvest=xlWorksheet(harvest)
        # harvest.clearRows()
        
        #WE WILL NOT CONTINUE WHILE NO BANDS DEFINED
        if not self.tree: #return worksheet.Table,worksheet.Table
            return worksheet
        
        #=======================================================================
        # for Band in BANDS:
        #    #BANDS[Band].cur = cur
        #    BANDS[Band].reset()
        #=======================================================================
        
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        # Okay, now we ready to PARSING cells.... #
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

        #---- Parsing
        rowsharvest=0
        #for iblock in range(len(BLOCKS)):
        for cluster in self.tree:
            #GROUP = BLOCKS[str(iblock)]
            #reset vars tobe harvest
            plainvars=ourvars.copy()
            #if not GROUP.has_key('DAT'):
            if isinstance(cluster,list):
                rowsharvest+=_fillxlrow(worksheet,cluster,None,plainvars)         
            elif isinstance(cluster,palmTree):
                cluster.harvestCluster(worksheet,plainvars)
        return worksheet

    def showMap(self):
        "export inner class into array/list-dict structure"
        if self.Band:
            result = self.Kind
            for i in self.Kind:
                if isinstance(self.Kind[i],palmTree):
                    result[i]=self.Kind[i].showMap()
                #else: result[i].append(i)
            result['Band']=self.Band
        else:
            result=list()
            for i in self.tree:
                if isinstance(i,palmTree):
                    result.append(i.showMap())
                else:
                    result.append(i)
        return result
    
    def arrangeSeed(self,workseed):
        "identify seed's cluster of a worksheet by path-flag, row-by-row"
        self.clear()
        #HARVEST EACH ROW
        for row in workseed.rows:
            # row = xlRow(row)
            # for cell in row:
                # print('cell:',cell, dir(cell))
            # break
            # cell = row[0] #first cellbit
            flag = row[0].value
            if not flag:
                self.put([['','']], parse_row(row))
                continue # force next row, there is no more cell for scanning
            paths = strToPaths(flag) # we rely on strToPaths() of parsing the format
            print( row[0].value, paths )
            self.put(paths, parse_row(row))
            