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

        self.driver.find_element(By.XPATH,'/html/body/section/main/section/section/form/section/table/tbody/tr/td[4]/a[3]/button').send_keys(Keys.ENTER)
        time.sleep(4)
             
        self.driver.find_element(By.XPATH,'/html/body/section/main/section/section/section[2]/section/form/section/button').send_keys(Keys.ENTER)

        time.sleep(10)
        
        #self.driver.find_element(By.ID,"modalidad").send_keys(Keys.ENTER)


    # destructor (it runs after EVERY test)
    def tearDown(self) -> None:
        self.driver.close()

if __name__ == "__main__":
    unittest.main()