import frappe
from customapi.controllers.base_controller import BaseController

class Item(BaseController):
	def __init__(self, doctype="Item",name=None):
		 super().__init__(doctype, name)

@frappe.whitelist()
def get_list():
	d = Item()
	d.get_list()