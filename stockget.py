import csv
import time
from bs4 import BeautifulSoup
from selenium import webdriver


driver = webdriver.Chrome(executable_path='D:/cenvet_scrapper/chromedriver')
driver.get('https://cenvet.orders.cenversa.com.au/account/login')

time.sleep(18)
username = driver.find_element_by_name("userNameOrEmailAddress")
username.clear()
username.send_keys("shanon@perthvetcare.com.au")

password = driver.find_element_by_name("password")
password.clear()
password.send_keys("xtest123")

driver.find_element_by_class_name('btn-primary').click()

time.sleep(10)

driver.get('https://cenvet.orders.cenversa.com.au/app/main/products/browse')

time.sleep(10)

def getResult(sku):
    searchTxt = driver.find_element_by_name("filterText")
    searchTxt.clear()
    searchTxt.send_keys(sku)

    driver.find_element_by_class_name('btn-primary').click()

    time.sleep(4)
    
    soup = BeautifulSoup(driver.page_source,"html.parser")
    try:
        stock = soup.find('pricedmarketproductstockmessage').text
    except:
        stock=''
    try:
        price = soup.find('span',attrs={'class':'text-danger'}).text
    except:
        price=''
    result = []
    result.append(stock)
    result.append(price)
    return result
# getResult = getResult('B0201')
# print(getResult[0])
# print(getResult[1])

# ID = []
# Type = []
# REF = []
def listToString(s): 
    
    # initialize an empty string
    str1 = "" 
    
    # traverse in the string  
    for ele in s: 
        str1 += ele  
    
    # return string  
    return str1 

with open('products_modify.csv', mode='w', newline='') as modify_file:
    modify_writer = csv.writer(modify_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    modify_writer.writerow(['ID','Type','REF','Name','Parent','SKU','Stock','Price'])
    with open('products.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                id = row[0]
                type = row[1]
                ref = row[2]
                name = row[3]
                parent = row[4]
                sku_value = row[5]
                str_sku = listToString(sku_value)
                getValue = getResult(str_sku)
                stock = getValue[0]
                price = getValue[1]

                modify_writer.writerow([id, type, ref, name, parent, sku_value, stock, price])
                # print(sku)
            line_count += 1

  