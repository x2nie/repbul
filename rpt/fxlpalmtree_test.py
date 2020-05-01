'''
Created on Nov 11, 2009

@author: Administrator
'''


import fxlpalmtree
from pprint import pprint

rows=[  '',
        'kpi:HDR',
        'kpi:HDR',
        
        'kpi',        
        'kpi:DAT',
        'kpi:DAT.kpic:DAT',
        'kpi:DAT.kpic:ALT',
        
        'kpi:ALT',
        'kpi:ALT',
        'kpi:ALT.kpic:DAT',
        'kpi:ALT.kpic:ALT',
        
        'kpi:FOT',
        'kpi:FOT',
        '',
        '',
        'kernet:HDR',
        'kernet:DAT',
        'kernet:DAT.kernetc:HDR',
        'kernet:DAT.kernetc:DAT',
        'kernet:DAT.kernetc:ALT',
        'kernet:DAT.kernetc:FOT',
        
        'kernet:ALT',
        'kernet:ALT.kernetc:HDR',
        'kernet:ALT.kernetc:DAT',
        'kernet:ALT.kernetc:ALT',
        'kernet:ALT.kernetc:FOT',
        'kernet:FOT',        
        ]

def strToPaths(pathf):
    if pathf.find('.') >=0:
        paths=pathf.split('.')
    else: 
        paths=[pathf]
    therow=list()
    for path in paths:
        if path.find(':') >=0:
            therow.append(path.split(':'))
        elif path.strip():
            therow.append([path,'DAT'])
        else:
            therow.append([path])
    return therow
    
therows=list()
#===============================================================================
# for pathf in rows:
#    if pathf.find('.') >=0:
#        paths=pathf.split('.')
#    else: 
#        paths=[pathf]
#    therow=list()
#    for path in paths:
#        if path.find(':') >=0:
#            therow.append(path.split(':'))
#        else:
#            therow.append([path])
#    therows.append(therow)
#===============================================================================
for pathf in rows:
    therows.append(strToPaths(pathf))
                   
print ("therows")
pprint(therows)
B=fxlpalmtree.palmTree()
i=0
for row in therows:
    B.put(row, '<DOM Element: Row at 0x1e4558%d>' % i)
    i+=1
    print( 'it\'s',row,'@',i )
print( "==========================================" )

pprint( B.showMap() )



#    [[['']], 
#    [['kpi', 'HDR']], 
#    [['kpi', 'HDR']], 
#    [['kpi', 'DAT']], 
#    [['kpi', 'DAT']], 
#    [['kpi', 'DAT'], 
#        ['kpic', 'DAT']], 
#    [['kpi', 'DAT'], 
#        ['kpic', 'ALT']], 
#    [['kpi', 'ALT']], 
#    [['kpi', 'ALT']], 
#    [['kpi', 'ALT'], 
#        ['kpic', 'DAT']], 
#    [['kpi', 'ALT'], 
#        ['kpic', 'ALT']], 
#    [['kpi', 'FOT']], 
#    [['kpi', 'FOT']], 
#    [['']], [['']], 
#    [['kernet', 'HDR']], 
#    [['kernet', 'DAT']], 
#    [['kernet', 'DAT'], ['kernetc', 'HDR']], 
#    [['kernet', 'DAT'], ['kernetc', 'DAT']], 
#    [['kernet', 'DAT'], ['kernetc', 'ALT']], 
#    [['kernet', 'DAT'], ['kernetc', 'FOT']], 
#    [['kernet', 'ALT']], 
#    [['kernet', 'ALT'], ['kernetc', 'HDR']], 
#    [['kernet', 'ALT'], ['kernetc', 'DAT']], 
#    [['kernet', 'ALT'], ['kernetc', 'ALT']], [['kernet', 'ALT'], ['kernetc', 'FOT']], [['kernet', 'FOT']]]
#    ===================================
#    [
#            '<DOM Element: Row at 0x1e45580>', 
#            {'DAT': [
#                    '<DOM Element: Row at 0x1e45583>', 
#                    '<DOM Element: Row at 0x1e45584>', 
#                    {'DAT': [
#                             '<DOM Element: Row at 0x1e45585>'], 
#                     'FOT': [], 
#                     'ALT': ['<DOM Element: Row at 0x1e45586>'], 
#                     'HDR': [], 
#                     'Band': 'kpic'}], 
#             'FOT': [
#                     '<DOM Element: Row at 0x1e455811>', 
#                     '<DOM Element: Row at 0x1e455812>'], 
#             'ALT': [
#                             '<DOM Element: Row at 0x1e45587>', 
#                             '<DOM Element: Row at 0x1e45588>', 
#                             {'DAT': ['<DOM Element: Row at 0x1e45589>'], 
#                              'FOT': [], 
#                              'ALT': ['<DOM Element: Row at 0x1e455810>'], 
#                              'HDR': [], 
#                              'Band': 'kpic'
#                              }], 
#            'HDR': [
#                             '<DOM Element: Row at 0x1e45581>', 
#                             '<DOM Element: Row at 0x1e45582>'], 
#            'Band': 'kpi'
#            }, 
#         '<DOM Element: Row at 0x1e455813>', 
#         '<DOM Element: Row at 0x1e455814>', 
#         {'DAT': [
#                  '<DOM Element: Row at 0x1e455816>', 
#                  {'DAT': ['<DOM Element: Row at 0x1e455818>'], 
#                   'FOT': ['<DOM Element: Row at 0x1e455820>'], 
#                   'ALT': ['<DOM Element: Row at 0x1e455819>'], 
#                   'HDR': ['<DOM Element: Row at 0x1e455817>'], 
#                   'Band': 'kernetc'
#                   }], 
#          'FOT': ['<DOM Element: Row at 0x1e455826>'], 
#          'ALT': [
#                  '<DOM Element: Row at 0x1e455821>', 
#                  {'DAT': ['<DOM Element: Row at 0x1e455823>'], 
#                   'FOT': ['<DOM Element: Row at 0x1e455825>'], 
#                   'ALT': ['<DOM Element: Row at 0x1e455824>'], 
#                   'HDR': ['<DOM Element: Row at 0x1e455822>'], 
#                   'Band': 'kernetc'
#                   }], 
#          'HDR': ['<DOM Element: Row at 0x1e455815>'], 
#          'Band': 'kernet'
#         }
#    ]

