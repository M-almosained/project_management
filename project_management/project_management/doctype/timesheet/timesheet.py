# Copyright (c) 2025, f and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class TimeSheet(Document):
	def validate(self):
		self.validate_hours()
		self.update_task_hours()

	def validate_hours(self):
		"""Validate that hours are not negative"""
		if self.hours < 0:
			frappe.throw("Hours cannot be negative")

	def update_task_hours(self):
		"""Update task hours when timesheet is submitted"""
		if self.task and self.docstatus == 1:
			# Get the task document
			task = frappe.get_doc('Task', self.task)
			
			# Calculate total hours for this task
			total_hours = frappe.get_value('TimeSheet', 
				{'task': self.task, 'docstatus': 1}, 
				'sum(hours)'
			) or 0
			
			# Update task's hour_count
			task.hour_count = total_hours
			
			# Update assignment table if exists
			if task.assignment:
				for assignment in task.assignment:
					if assignment.employee == self.employee:
						# Calculate employee specific hours
						employee_hours = frappe.get_value('TimeSheet', 
							{
								'task': self.task,
								'employee': self.employee,
								'docstatus': 1
							},
							'sum(hours)'
						) or 0
						
						# Update employee's hour count
						assignment.hour_count = employee_hours
						break
			
			# Save the task
			task.save()
