import unittest
from update_appointment import updateappointment


class MyTestCase(unittest.TestCase):
    appt = updateappointment("John Doe, 999999999, 1960-01-01", "67", "Appt 1")

    def test_appt_name_is_null(self):
        # Test fails if the appointment name is null
        appt_name = self.appt.entry_appointment_name.get()
        self.assertIsNotNone(appt_name)

    def test_appt_details_is_null(self):
        # Test fails if the appointment details field is null
        self.appt.entry_appointment_info.insert(0, "Test Details")
        appt_details = self.appt.entry_appointment_info.get()
        self.assertIsNotNone(appt_details)


if __name__ == '__main__':
    unittest.main()
