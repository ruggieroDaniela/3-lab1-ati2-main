import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

class testSupplier( unittest.TestCase ):
    
    # start driver as an attribute of the class (ir runs before EVERY test)
    def setUp(self):
        #self.driver =  webdriver.Chrome(executable_path=r"C:\driverChrome\chromedriver.exe")
        self.driver = webdriver.Firefox()

    # test create a new supplier
    def test_create_supplier(self):
        self.driver.get("http://localhost:8000")
        time.sleep(3)

        self.driver.find_element(By.ID,"Empleados").send_keys(Keys.ENTER)
        time.sleep(4)

        self.driver.find_element(By.XPATH,'/html/body/section/main/section/section/form/section/table/tbody/tr/td[4]/a[2]/button').send_keys(Keys.ENTER)
        time.sleep(15)

        info=["Daniela","Ruggiero","Administradora","ABC273645","daniela@empresa.com","daniela@personal.com","+58-0212-123-1235","+58-0212-123-1236","Roma","Italia","Facebook","1","Twitter","2"]

        self.driver.find_element(By.ID,"id_nombre").clear()
        self.driver.find_element(By.ID,"id_nombre").send_keys(info[0])
        self.driver.find_element(By.ID,"id_apellido").clear()
        self.driver.find_element(By.ID,"id_apellido").send_keys(info[1])
        
        self.driver.find_element(By.ID,"id_ci").clear()
        self.driver.find_element(By.ID,"id_ci").send_keys(info[3])
        
        select = self.driver.find_element(By.ID,"modalidad")
        for option in select.find_elements(By.TAG_NAME,'option'):
            if option.text == 'Honorario profesionales':
                option.click() # select() in earlier versions of webdriver
                break

        
        self.driver.find_element(By.ID,"id_email_emp").clear()
        self.driver.find_element(By.ID,"id_email_emp").send_keys(info[4])
        self.driver.find_element(By.ID,"id_email_p").clear()
        self.driver.find_element(By.ID,"id_email_p").send_keys(info[5])
        self.driver.find_element(By.ID,"id_tlf_local").clear()
        self.driver.find_element(By.ID,"id_tlf_local").send_keys(info[6])
        self.driver.find_element(By.ID,"id_tlf_celular").clear()
        self.driver.find_element(By.ID,"id_tlf_celular").send_keys(info[7])
        self.driver.find_element(By.ID,"id_ciudad").clear()
        self.driver.find_element(By.ID,"id_ciudad").send_keys(info[8])
        self.driver.find_element(By.ID,"id_pais").clear()
        self.driver.find_element(By.ID,"id_pais").send_keys(info[9])
        self.driver.find_element(By.ID,"id_form-0-nombre").clear()
        self.driver.find_element(By.ID,"id_form-0-nombre").send_keys(info[10])
        self.driver.find_element(By.ID,"id_form-0-valor").clear()
        self.driver.find_element(By.ID,"id_form-0-valor").send_keys(info[11])
        self.driver.find_element(By.ID,"id_form-1-nombre").send_keys(info[10])
        self.driver.find_element(By.ID,"id_form-1-valor").send_keys(info[11])

        self.driver.find_element(By.XPATH,"/html/body/section/main/section/section/form/section[9]/section/button").send_keys(Keys.ENTER)
            
            
                
        time.sleep(10)
        


        
            

        #self.driver.find_element(By.ID,"modalidad").send_keys(Keys.ENTER)


    # destructor (it runs after EVERY test)
    def tearDown(self) -> None:
        self.driver.close()

if __name__ == "__main__":
    unittest.main()