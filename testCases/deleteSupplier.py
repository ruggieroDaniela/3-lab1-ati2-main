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

    # test delete supplier
    def test_create_supplier(self):
        self.driver.get("http://localhost:8000")
        time.sleep(3)

        # Click on Suppliers 
        suppliers = self.driver.find_element(By.ID, "suppliers")
        suppliers.send_keys(Keys.ENTER)
        time.sleep(15)

        # Delete second supplier
        deleteSupplier = self.driver.find_elements(By.ID, "delete_supplier")
        deleteSupplier[1].send_keys(Keys.ENTER)
        time.sleep(15)

    # destructor (it runs after EVERY test)
    def tearDown(self) -> None:
        self.driver.close()

if __name__ == "__main__":
    unittest.main()