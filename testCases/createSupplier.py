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

        # Click on Suppliers 
        suppliers = self.driver.find_element(By.ID, "suppliers")
        suppliers.send_keys(Keys.ENTER)
        time.sleep(15)

        # Create a new Supplier
        newSupplier = self.driver.find_element(By.ID, "create_supplier")
        newSupplier.send_keys(Keys.ENTER)
        time.sleep(5)

        # Supplier Form 
        #info = ["ciudad", "pais", "nombre", "id", "correo", "dir", "sitio", "servicio", "telef"]
        #info = ["Seattle-Washingthon", "Estados Unidos", "AWS", "TIN- 1388870295", "customeraws@gmail.com", "4080 Stevens Creek Blvd. San Jose, CA 95129", "https://www.banesco.com.pa/", "Servicios de IT, Marketing", "1-800-925-6278"]
        #info = ["Ciudad de Panamá", "Panamá", "Banesco", "NIT-12456789", "banesco.panama@banesco.com", "Plaza Nuevo Tocumen, locales #33, #34 y #35", "https://www.banesco.com.pa/", "1- Apertura de cuentas bancarias,2- Tarjetas de débito y crédito 3- Creditos", "5078001300"]
        info = ["Caracas", "Venezuela", "Digitel", "RIF-J-12345678", "atencion.digitel@gmail.com", "Av Francisco de Miranda Torre Digitel. La Castellana Locales 1 al 14, PB", "http://www.digitel.com", "Telecomunicaciones", "58-212-123-45-67"]
        campo = self.driver.find_elements(By.ID, "input_info")

        # Fill form 
        for x in range(9):            
            campo[x].send_keys(info[x])
            #time.sleep(2)

        # Representante
        #infoRep = ["nombre", "cargo", "correo", "correo_personal", "telef", "telef_local", "pais"]
        #infoRep = ["Jose Sanchez", "CTO", "jose.sanchez@openlearn1.com", "nirvana01@gmail.com", "+1-317-938-5657", "No tiene", "Estados Unidos"]
        #infoRep = ["Jose Sanchez", "CTO", "Notiene@gmail.com", "nirvana01@gmail.com", "+50769305188", "No tiene", "Panama"]
        infoRep = ["Jose Sanchez", "CTO", "jose.sanchez@diigitel.com", "Notiene@gmail.com", "58-412-123-45-67", "No tiene", "Venezuela"]
        campoRep = self.driver.find_elements(By.ID, "representante")

        # Fill form 
        for x in range(7):            
            campoRep[x].send_keys(infoRep[x])
            #time.sleep(2)

        time.sleep(5)

        saveData = self.driver.find_element(By.ID, "save_supplier")
        saveData.send_keys(Keys.ENTER)

        time.sleep(20)

    # destructor (it runs after EVERY test)
    def tearDown(self) -> None:
        self.driver.close()

if __name__ == "__main__":
    unittest.main()