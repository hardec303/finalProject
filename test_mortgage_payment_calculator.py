import unittest
import calculator


class MyTestCase(unittest.TestCase):
    mortgage_calculator = calculator.calc()
    mortgage_calculator.home_price.set(350000)
    mortgage_calculator.down_payment.set(70000)
    mortgage_calculator.amortization.set(25)
    mortgage_calculator.interest_rate.set(4.69)

    def test_mortgage_value(self):
        home_price = int(self.mortgage_calculator.home_price.get())
        down_payment = int(self.mortgage_calculator.down_payment.get())
        self.assertEqual(280000, home_price - down_payment)

    def test_monthly_payment(self):
        self.mortgage_calculator.payment_frequency.set('Monthly')
        monthly_payment = self.mortgage_calculator.PaymentCalculate()
        self.assertEqual(1587, monthly_payment)

    def test_semi_monthly_payment(self):
        self.mortgage_calculator.payment_frequency.set('Semi-Monthly')
        semi_monthly_payment = self.mortgage_calculator.PaymentCalculate()
        self.assertEqual(792, semi_monthly_payment)

    def test_weekly_payment(self):
        self.mortgage_calculator.payment_frequency.set('Weekly')
        weekly_payment = self.mortgage_calculator.PaymentCalculate()
        self.assertEqual(365, weekly_payment)


if __name__ == '__main__':
    unittest.main()
