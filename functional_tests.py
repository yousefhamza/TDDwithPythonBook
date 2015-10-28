from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest (unittest.TestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	def test_can_start_a_list_and_retrieve_it_later(self):
		#User to website homepage
		self.browser.get('http://localhost:8000')

		#User notice title is 'to-do'
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		#User invited to add a to-do item
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)

		#User types "Buy peacock feather" into a textbox
		inputbox.send_keys('Buy peacock feather')

		#When user press enter	the page updates showing
		# "1:Buy peacock feather" as item in to-do list
		inputbox.send_keys(Keys.ENTER)

		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertTrue(
			any(row.text == '1: Buy peacock feather' for row in rows),
			"New to-do item did not appear in table"
		)

		#There's stil a box to enter another item
		self.fail('Finish the test!')
		#User enter "Use peacock feather to make a fly"

		#The page updates again showing both items

		#User sees a unique URL for his list

		#User check that URL to find his to-do list

		#User quits
		browser.quit()

if __name__ == '__main__':
	unittest.main()