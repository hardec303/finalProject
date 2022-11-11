import unittest
import calculator


class MyTestCase(unittest.TestCase):
    mortgage_calculator = calculator.calc()
    mortgage_calculator.annual_household_income.set(60000)
    mortgage_calculator.down_payment2.set(50000)
    mortgage_calculator.loans_other_debits.set(100)
    mortgage_calculator.credit_cards.set(50)
    mortgage_calculator.monthly_condo_fees.set(0)

    def test_total_debts(self):
        total_debts = float(self.mortgage_calculator.loans_other_debits.get()) + float(
            self.mortgage_calculator.credit_cards.get()) + float(self.mortgage_calculator.monthly_condo_fees.get())
        self.assertEqual(150, total_debts)
        return total_debts

    def test_monthly_gross_income(self):
        monthly_income = float(self.mortgage_calculator.annual_household_income.get()) / 12
        self.assertEqual(5000, monthly_income)
        return monthly_income

    def test_monthly_payment(self):
        monthly_payment = self.mortgage_calculator.AffordabilityCalculate()[0]
        self.assertEqual(1550, monthly_payment)

    def test_mortgage_affordability(self):
        mortgage_affordability = self.mortgage_calculator.AffordabilityCalculate()[1]
        self.assertEqual(281214, mortgage_affordability)
        return int(mortgage_affordability)

    def test_home_affordability(self):
        home_affordability = self.mortgage_calculator.AffordabilityCalculate()[2]
        self.assertEqual(331214, home_affordability)

    def test_home_affordability_as_sum(self):
        home_affordability = int(self.test_mortgage_affordability() + int(self.mortgage_calculator.down_payment2.get()))
        self.assertEqual(331214, home_affordability)


if __name__ == '__main__':
    unittest.main()
