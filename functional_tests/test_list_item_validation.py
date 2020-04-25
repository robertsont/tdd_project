from functional_tests.base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class ItemValidationTest(FunctionalTest):
    
    def test_cannot_add_empty_list(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item"
        ))

        # She tries again with some text for the item, which now works
        self.browser.find_element_by_id('id_new_item').send_keys("Retry")
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        #self.assertNotIn("You can't have an empty list item", self.browser.page_source)
        self.wait_for_row_in_list_table("1. Retry")

        # Perversely, she now decides to submit a second blank list item
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # She receives a similar warning on the list page
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item"
        ))

        # And she can corrext it by filling some text in
        self.browser.find_element_by_id('id_new_item').send_keys("Retry twice")
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1. Retry")
        self.wait_for_row_in_list_table("2. Retry twice")
        #self.assertNotIn("You can't have an empty list item", self.browser.page_source)

