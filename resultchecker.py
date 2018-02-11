from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
from xvfbwrapper import Xvfb


def result_checker(register_number):
    display = Xvfb()
    display.start()


    chromedriver = '/home/hanlak/Music/chromedriver'


    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')

    driver= webdriver.Chrome(chromedriver,chrome_options=options)
    driver.get('https://aucoe.info/RDA/resultsnew/')

    #data_ntry = driver.find_element_by_class_name('dataTables_info')


    search_bar = driver.find_element_by_xpath('//*[@id="res_filter"]/label/input')
    search_bar.send_keys(' result to be searched ') # as per ur required result
    onclick = driver.find_element_by_xpath('//*[@id="res"]/tbody/tr/td[4]/form/button')

    onclick.send_keys(Keys.RETURN)

    reg_bar = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[2]/form/div/input[7]')
    reg_bar.send_keys(register_number)
    reg_bar.send_keys(Keys.RETURN)
    detail = []
    for r in driver.find_elements_by_xpath('/html/body/center[3]/table[3]'):
        for data in r.find_elements_by_tag_name('td'):
            detail.append(data.text)
    result = []
    for row in driver.find_elements_by_xpath("/html/body/table"):
        for data in  row.find_elements_by_tag_name("td"):
            result.append(data.text)

    driver.quit()
    display.stop

    return result,detail



def write_to_csv(res):
    with open('resulty.csv', 'wb') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(res)


def _list_maker():
        _result = []
        with open('resulty.csv','rb') as f:
            reader = csv.reader(f)
            for row in reader:
                for data in row:
                    _result.append(data)
        return _result

def _grade_ob_index(listy):
            count =0
            for data in listy:
                if data == "GRADE OBTAINED" or   data == "MARKS OBTAINED":
                    return count 
                else:
                    count = count +1


def _grade_for_namR(listy):
        counter = 0
        for _check in listy:
            if _check == " ":
                return counter
            else:
                counter = counter+1



def handle_csv(register_number,studentname,registernumber,check_detail):
    _result = _list_maker()
    list_max_count = len(_result)

    start = _grade_ob_index(_result)+1

    scores = []
    scores.append('STUDENTNAME')
    scores.append('REGISTERNUMBER')

    names = []
    names.append(studentname)
    names.append(registernumber)

    for allocate in range(start,list_max_count):
        if allocate % 2 == 0:
            alocname =_result[allocate]
            if check_detail: 
                scores.append(alocname)
            else:
                names.append(alocname)
        else:
            alocgrade = _result[allocate]
            if check_detail:
                names.append(alocgrade)
            else:
                scores.append(alocgrade) 
    return names,scores


def _handle_name_reg(counternr):
    _pie = []
    nameR = _list_maker()
    namsta = counternr+1
    regend = counternr+3
    for _checkNR in range(namsta,regend):
        piece = nameR[_checkNR].split(':')
        _pie.append(piece)
    return _pie[0][1].strip(),_pie[1][1].strip()


def append_to_the_final(_data):
    with open('TheFinal.csv', 'ab') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(_data)

def clear_the_csv():
    with open('TheFinal.csv','w') as myfile:
        myfile.truncate()

def handle_details_an(det):
    detai = []
    for _dat in det:
        detai.append(_dat.split(':'))
    return detai[0][1].strip(),detai[1][1].strip()


if __name__ == "__main__":
    
    print "Before Entering the details please press '1' or u can press any key  if you wish to continue"
    switch = input()
    if switch == 1:
        clear_the_csv()

    register_number_from= input('enter register_number from')
    register_number_to = input('enter register_number to')
    name_not_entered = True
    for register_number in range(register_number_from,register_number_to):
        res,det = result_checker(register_number)
        check_detail = False
        if det:
            check_detail = True

        if res:
            write_to_csv(res)
            if check_detail:
                studentname,registernumber = handle_details_an(det)
            else:
                counternr = _grade_for_namR(res)
                studentname,registernumber = _handle_name_reg(counternr)
            score,sub_name = handle_csv(register_number,studentname,registernumber,check_detail)
            if name_not_entered:
                append_to_the_final(sub_name)
                append_to_the_final(score)
                name_not_entered = False
            else:
                append_to_the_final(score)
        else:
            print 'result not found'
