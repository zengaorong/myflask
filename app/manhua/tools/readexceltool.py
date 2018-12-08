import xlrd

def readexcel_todict(addr_str,key_num,begin_num,sheetnum):
    excel_workbook = xlrd.open_workbook(addr_str)
    excel_sheet01 = excel_workbook.sheets()[sheetnum]
    terminal_num_nrows = excel_sheet01.nrows
    terminal_num_ncols = excel_sheet01.ncols
    excel_dict =  {}
    for r in range(begin_num,terminal_num_nrows):
        key_str = excel_sheet01.cell(r,key_num).value
        if type(key_str) is float:
            key_str = str(int(key_str))
        if check_is_nums(key_str):
            #print key_str + "123"
            key_str = int(key_str)
        hold = []
        #print int(key_str)
        for c in range(0,terminal_num_ncols):
            if type(excel_sheet01.cell(r,c).value) is float:

                hold.append(str(int(excel_sheet01.cell(r,c).value)))
            else:
                hold.append(excel_sheet01.cell(r,c).value)
        excel_dict[key_str] =  hold

    return excel_dict
def check_is_nums(str_check):
    isnum = True
    for key in str_check.decode('utf-8'):
        if u'\u0030'<=key<=u'\u0039':
            pass
        else:
            isnum = False
            return isnum

    if str_check == "":
        isnum = False
    return isnum