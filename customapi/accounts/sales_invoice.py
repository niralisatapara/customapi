import frappe
from customapi.controllers.base_controller import BaseController

class SalesInvoice(BaseController):
	def __init__(self, doctype,name=None):
		 super().__init__(doctype, name)
