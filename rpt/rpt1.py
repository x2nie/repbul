import openpyxl

tpl = openpyxl.load_workbook('Inventory Report with  Sub-Category.xlsx')
# wb2 = openpyxl.load_workbook('file2.xlsx')

ws1 = tpl.active
# ws2 = wb2.active

for row in ws1.iter_rows():
    for cell in row:
        print( dir(cell.column) )
        break
    break