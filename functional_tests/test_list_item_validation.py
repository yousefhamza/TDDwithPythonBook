from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys

class ItemValidationTest(FunctionalTest):
	#@skip
	def test_cannot_add_empty_list_items(self):
		#User go to homepage
		self.browser.get(self.server_url)

		#Submits an empty list item and hit enter
		inputbox = self.get_item_input_box()
		inputbox.send_keys(Keys.ENTER)

		#home page refreshes, and there is an error saying that the
		#list item cannot be blank
		error = self.browser.find_element_by_css_selector('.has-error')
		self.assertEqual(error.text, 'You can\'t have an empty list item')

		#User tries agaain with some text for the item, which now works
		inputbox = self.get_item_input_box()
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)
		self.check_for_row_in_list_table('1: Buy milk')

		#Now user try to submit another blank item
		inputbox = self.get_item_input_box()
		inputbox.send_keys(Keys.ENTER)

		#User recieve another error like the one before
		self.check_for_row_in_list_table('1: Buy milk')
		error = self.browser.find_element_by_css_selector('.has-error')
		self.assertEqual(error.text, 'You can\'t have an empty list item')

		#And can be fixed by submitting some text
		inputbox = self.get_item_input_box()
		inputbox.send_keys('Make tea')
		inputbox.send_keys(Keys.ENTER)

		self.check_for_row_in_list_table('1: Buy milk')
		self.check_for_row_in_list_table('2: Make tea')

	def test_cannot_add_duplicate_items(self):
		#User goes to homepage and starts a new list
		self.browser.get(self.server_url)
		inputbox = self.get_item_input_box()
		inputbox.send_keys('Buy wellies')
		inputbox.send_keys(Keys.ENTER)\

		#User accidently tries to enter a duplicate item
		inputbox = self.get_item_input_box()
		inputbox.send_keys('Buy wellies')
		inputbox.send_keys(Keys.ENTER)

		#User sees a helpful error message
		self.check_for_row_in_list_table('1: Buy wellies')
		error = self.browser.find_element_by_css_selector('.has-error')
		self.assertEqual(error.text, 'You\'ve already got this in yout list')