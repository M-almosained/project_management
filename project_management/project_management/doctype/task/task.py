# Copyright (c) 2025, f and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Task(Document):
	def validate(self):
		self.calculate_total_hours()

	def calculate_total_hours(self):
		"""Calculate total hours from TimeSheet entries and update hour_count"""
		# Get total hours from timesheet
		total_hours = frappe.get_value('TimeSheet', {'task': self.name, 'docstatus': 1}, 'sum(hours)') or 0
		
		# Update the hour_count field
		self.hour_count = total_hours

		# Update assignment table with total hours
		if self.assignment:
			for assignment in self.assignment:
				# Get employee specific hours from timesheet
				employee_hours = frappe.get_value('TimeSheet', 
					{
						'task': self.name, 
						'employee': assignment.employee, 
						'docstatus': 1
					}, 
					'sum(hours)'
				) or 0
				
				# Update employee's hour count in the assignment table
				assignment.hour_count = employee_hours
