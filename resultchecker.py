""""
Author: Prudhvi

"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
from xvfbwrapper import Xvfb


def result_checker(register_number):
    display = Xvfb()
    display.start()


    chromedriver = #add the chrome driver path Ex: '/home/hanlak/chromedriver' in linux(ubuntu)


    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')

    driver= webdriver.Chrome(chromedriver,chrome_options=options)
    driver.get('https://aucoe.info/RDA/resultsnew/')

    #data_ntry = driver.find_element_by_class_name('dataTables_info')


    search_bar = driver.find_element_by_xpath('//*[@id="res_filter"]/label/input')
    search_bar.send_keys('B.E./B.TECH FOURTH YEAR FIRST SEMESTER EXAMINATION HELD NOVEMBER 2017') #
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


def list_maker():
        result = []
        with open('resulty.csv','rb') as f:
            reader = csv.reader(f)
            for row in reader:
                for data in row:
                    result.append(data)
        return result

def grade_ob_index(listy):
            count =0
            for data in listy:
                if data == "GRADE OBTAINED" or   data == "MARKS OBTAINED":
                    return count 
                else:
                    count = count +1


def grade_for_namR(listy):
        counter = 0
        for check in listy:
            if check == " ":
                return counter
            else:
                counter = counter+1



def handle_csv(register_number,studentname,registernumber,check_detail):
    result = list_maker()
    list_max_count = len(result)

    start = grade_ob_index(result)+1

    scores = []
    scores.append('STUDENTNAME')
    scores.append('REGISTERNUMBER')

    names = []
    names.append(studentname)
    names.append(registernumber)

    for allocate in range(start,list_max_count):
        if allocate % 2 == 0:
            alocname =result[allocate]
            if check_detail: 
                scores.append(alocname)
            else:
                names.append(alocname)
        else:
            alocgrade = result[allocate]
            if check_detail:
                names.append(alocgrade)
            else:
                scores.append(alocgrade) 
    return names,scores


def handle_name_reg(counternr):
    pie = []
    nameR = list_maker()
    namsta = counternr+1
    regend = counternr+3
    for checkNR in range(namsta,regend):
        piece = nameR[checkNR].split(':')
        pie.append(piece)
    return pie[0][1].strip(),pie[1][1].strip()


def append_to_the_final(data,file_name):
    with open(file_name, 'ab') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(data)

def clear_the_csv(file_name):
    with open(file_name,'w') as myfile:
        myfile.truncate()

def handle_details_an(det):
    detai = []
    for dat in det:
        detai.append(dat.split(':'))
    return detai[0][1].strip(),detai[1][1].strip()


if __name__ == "__main__":
    print 'Enter the name of the csv file you want to store the result'
    file_name = str(raw_input())+'{}'.format('.csv')

    print "Before Entering the details please press '1' or u can press any key  if you wish to continue"
    switch = str(raw_input())
    if switch == '1':
        clear_the_csv(file_name)

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
                counternr = grade_for_namR(res)
                studentname,registernumber = handle_name_reg(counternr)
            score,sub_name = handle_csv(register_number,studentname,registernumber,check_detail)
            if name_not_entered:
                append_to_the_final(sub_name,file_name)
                append_to_the_final(score,file_name)
                name_not_entered = False
            else:
                append_to_the_final(score,file_name)
        else:
            print 'result not found'
