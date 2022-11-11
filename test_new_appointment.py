import unittest
from new_appointment import Createnewappointment


class MyTestCase(unittest.TestCase):
    appt = Createnewappointment("John Doe, 999999999, 1960-01-01")

    def test_appt_name_is_null(self):
        # Test fails if the appointment name is null
        self.appt.entry_appointment_name.insert(0, "Test Name")
        appt_name = self.appt.entry_appointment_name.get()
        self.assertIsNotNone(appt_name)

    def test_appt_details_is_null(self):
        # Test fails if the appointment details field is null
        self.appt.entry_appointment_info.insert(0, "Test Details")
        appt_details = self.appt.entry_appointment_info.get()
        self.assertIsNotNone(appt_details)

if __name__ == '__main__':
    unittest.main()
