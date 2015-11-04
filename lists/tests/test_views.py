from lists.models import Item, List
from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import TestCase
from django.http import HttpRequest
from django.utils.html import escape
from lists.views import home_page
from lists.forms import ItemForm, EMPTY_ITEM_ERROR

# Create your tests here.
class HomePageTest(TestCase):

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html',{'form': ItemForm()})
		self.assertMultiLineEqual(response.content.decode(), expected_html)

	def test_home_page_uses_item_form(self):
		response = self.client.get('/')
		self.assertIsInstance(response.context['form'], ItemForm)

	def test_for_invalid_input_renders_home_template(self):
		response = self.client.post('/lists/new', data={'text':''})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'home.html')

	def test_validation_errors_are_shown_on_home_page(self):
		response = self.client.post('/lists/new', data={'text':''})
		self.assertContains(response, escape(EMPTY_ITEM_ERROR))

	def test_for_validation_input_passes_form_to_template(self):
		response = self.client.post('/lists/new', data={'text':''})
		self.assertIsInstance(response.context['form'], ItemForm)

class ListViewTest(TestCase):
	def test_uses_list_template(self):
		list_ = List.objects.create()
		response = self.client.get('/lists/%d/' % (list_.id,))
		self.assertTemplateUsed(response, 'list.html')

	def test_displays_only_items_for_that_list(self):
		correct_list = List.objects.create()
		Item.objects.create(text='itemey 1', list=correct_list)
		Item.objects.create(text='itemey 2', list=correct_list)

		other_list = List.objects.create()
		Item.objects.create(text='other 1', list=other_list)
		Item.objects.create(text='other 2', list=other_list)

		response = self.client.get('/lists/%d/' % (correct_list.id,))

		self.assertContains(response, 'itemey 1')
		self.assertContains(response, 'itemey 2')
		self.assertNotContains(response, 'other 1')
		self.assertNotContains(response, 'other 2')

		self.assertTemplateUsed(response, 'list.html')

	def test_passes_correct_list_to_tempalate(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		response = self.client.get('/lists/%d/' % (correct_list.id,))
		self.assertEqual(response.context['list'], correct_list)

	def test_can_save_a_POST_request_to_an_existing_list(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		self.client.post(
			'/lists/%d/' % (correct_list.id,),
			data = {
				'text': 'A new item for an existing list'
			}
		)

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new item for an existing list')
		self.assertEqual(new_item.list, correct_list)

	def test_redirects_to_list_view(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		response = self.client.post(
			'/lists/%d/' % (correct_list.id,),
			data = {
				'text': 'A new item for an exisitng list'
			}
		)
		self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))
	def test_validation_errors_end_up_on_list_page(self):
		list_ = List.objects.create()
		response = self.client.post (
				'/lists/%d/' % (list_.id,),
				data =  {
					'text': '',
				}
			)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'list.html')
		expected_error = escape('You can\'t have an empty list item')
		self.assertContains(response, expected_error)

	def test_displays_item_form(self):
		list_ = List.objects.create()
		response = self.client.get('/lists/%d/' % (list_.id,))
		self.assertIsInstance(response.context['form'], ItemForm)
		self.assertContains(response, 'name="text"')


	def post_invlaid_input(self):
		list_ = List.objects.create()
		return self.client.post('/lists/%d/' % (list_.id,),
				data = {'text': ''}
			)
	def test_for_invalid_input_nothing_renders_list_tempalte(self):
		self.post_invlaid_input()
		self.assertEqual(Item.objects.count(), 0)

	def test_for_invalid_input_renders_list_template(self):
		response = self.post_invlaid_input()
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'list.html')

	def test_for_invalid_input_passes_form_to_template(self):
		response = self.post_invlaid_input()
		self.assertIsInstance(response.context['form'], ItemForm)

	def test_for_invalid_input_shows_error_on_page(self):
		response = self.post_invlaid_input()
		self.assertContains(response, escape(EMPTY_ITEM_ERROR))