from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys

class ItemValidationTest(FunctionalTest):
	#@skip
	def test_cannot_add_empty_list_items(self):
		#User go to homepage

		#Submits an empty list item and hit enter

		#home page refreshes, and there is an error saying that the
		#list item cannot be blank

		#User tries agaain with some text for the item, which now works

		#Now user try to submit another blank item

		#User recieve another error like the one before

		#And can be fixed by submitting some text

		self.fail('Write me!')
