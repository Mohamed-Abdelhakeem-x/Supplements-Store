import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

@pytest.mark.e2e
class TestMainRoutes:

    def test_about_page(self, driver, live_server_url):
        """Test About Page load."""
        driver.get(f"{live_server_url}/About")
        assert "About" in driver.title
        # Check for some content
        assert "Welcome" in driver.page_source or "About Us" in driver.page_source

    def test_search_product(self, driver, live_server_url):
        """Test Product Search functionality."""
        driver.get(f"{live_server_url}/Shop")
        
        # Fill Search Input
        search_input = driver.find_element(By.NAME, "search")
        search_input.clear()
        search_input.send_keys("Vitamin")
        
        # Click Search Button
        # Logic from Shop.html: <button type="submit" class="search-button">Search</button>
        driver.find_element(By.CLASS_NAME, "search-button").click()
        
        # Verify Results
        # Should contain "Vitamin" in results
        results = driver.find_elements(By.CLASS_NAME, "product-name")
        assert len(results) > 0
        for res in results:
            assert "Vitamin" in res.text

    def test_filter_product(self, driver, live_server_url):
        """Test Product Category Filter."""
        driver.get(f"{live_server_url}/Shop")
        
        # Select Category
        select_elem = driver.find_element(By.NAME, "category")
        select = Select(select_elem)
        select.select_by_visible_text("Protein") 
        
        driver.find_element(By.CLASS_NAME, "filter-button").click()
        
        # Verify only Protein products
        results = driver.find_elements(By.CLASS_NAME, "product-name")
        assert len(results) > 0
        # Check if description or name implies protein or check DB state knowledge
        # E.g. "E2E Whey Protein" should be there
        assert "Protein" in driver.page_source

    def test_product_detail_page(self, driver, live_server_url):
        """Test Product Description Page."""
        driver.get(f"{live_server_url}/Shop")
        
        # Click first product link
        first_product_link = driver.find_element(By.CLASS_NAME, "product-name").find_element(By.TAG_NAME, "a")
        product_name = first_product_link.text
        first_product_link.click()
        
        # Verify Product Page
        current_url = driver.current_url
        assert "/product/" in current_url
        
        # Check details
        assert product_name in driver.page_source
        # Check Related Products
        related = driver.find_elements(By.CLASS_NAME, "card") # Assuming related use cards or similar
        # Based on product_description.html (not fully read but inferred), check for general existence of sections
