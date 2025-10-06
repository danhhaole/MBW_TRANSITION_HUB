# Copyright (c) 2025, mbwcloud.com and Contributors
# See license.txt

# import frappe
from frappe.tests import IntegrationTestCase, UnitTestCase


# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]


class UnitTestMira_Merge_Field_List(UnitTestCase):
	"""
	Unit tests for Mira_Merge_Field_List.
	Use this class for testing individual functions and methods.
	"""

	pass


class IntegrationTestMira_Merge_Field_List(IntegrationTestCase):
	"""
	Integration tests for Mira_Merge_Field_List.
	Use this class for testing interactions between multiple components.
	"""

	pass
