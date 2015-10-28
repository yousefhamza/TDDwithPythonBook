from selenium import webdriver
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
		self.fail('Finish the test!')

		#User invited to add a to-do item

		#User types "Buy peacock feather" into a textbox

		#When user press enter	the page updates showing
		# "1:Buy peacock feather" as item in to-do list

		#There's stil a box to enter another item

		#User enter "Use peacock feather to make a fly"

		#The page updates again showing both items

		#User sees a unique URL for his list

		#User check that URL to find his to-do list

		#User quits
		browser.quit()

if __name__ == '__main__':
	unittest.main()