from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase

class NewVisitorTest (LiveServerTestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])

	def test_can_start_a_list_and_retrieve_it_later(self):
		#User to website homepage
		self.browser.get(self.live_server_url)

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

		user_list_url = self.browser.current_url
		self.assertRegexpMatches(user_list_url, '/lists/.+')
		self.check_for_row_in_list_table('1: Buy peacock feather')

		#There's stil a box to enter another item
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)

		#User enter "Use peacock feather to make a fly"
		inputbox.send_keys('Use peacock feather to make a fly')
		inputbox.send_keys(Keys.ENTER)

		#The page updates again showing both items

		self.check_for_row_in_list_table('1: Buy peacock feather')
		self.check_for_row_in_list_table('2: Use peacock feather to make a fly')

		#Now a new user comes along to the site.
		#we use a new browser session to make sure that no information
		#of the first user is coming through cookies etc.
		self.browser.quit()
		self.browser = webdriver.Firefox()

		#New user visit the home page. There is no sign of first user list
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertNotIn('make a fly', page_text)

		#New user starts a new list
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)

		#New user gets a unique URL
		new_user_url = self.browser.current_url
		self.assertRegexpMatches(new_user_url, '/lists/.+')
		self.assertNotEqual(new_user_url, user_list_url)

		#User quits
		browser.quit()