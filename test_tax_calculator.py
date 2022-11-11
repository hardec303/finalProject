import unittest
import calculator


class MyTestCase(unittest.TestCase):
    tax_calculator = calculator.calc()
    tax_calculator.taxable_income.set(75000)
    taxable_income = round(int(tax_calculator.taxable_income.get()), 2)

    def test_tax_payable(self):
        tax_payable = self.tax_calculator.TaxCalculate()
        self.assertEqual(14520.05, tax_payable)
        return round(tax_payable, 2)

    def test_federal_tax(self):
        federal_tax = self.tax_calculator._calculate_federal_tax(self.taxable_income)
        self.assertEqual(10454.11, federal_tax)
        return federal_tax

    def test_provincial_tax(self):
        provincial_tax = self.tax_calculator._calculate_provincial_tax(self.taxable_income)
        self.assertEqual(4065.94, provincial_tax)
        return provincial_tax

    def test_tax_payable_as_sum(self):
        tax_payable = round(self.test_federal_tax() + self.test_provincial_tax(), 2)
        self.assertEqual(14520.05, tax_payable)

    def test_after_tax_income(self):
        after_tax_income = self.taxable_income - self.test_tax_payable()
        self.assertEqual(60479.95, after_tax_income)

    def test_average_tax_rate(self):
        average_tax_rate = round((self.test_tax_payable() / self.taxable_income) * 100, 2)
        self.assertEqual(19.36, average_tax_rate)

    def test_marginal_tax_rate(self):
        marginal_tax = self.tax_calculator._get_percentages(self.taxable_income)
        marginal_tax_rate = marginal_tax[0]
        self.assertEqual(28.20, marginal_tax_rate)

    def test_marginal_rate_eligible_dividends(self):
        marginal_tax = self.tax_calculator._get_percentages(self.taxable_income)
        marginal_rate_eligible_dividends = marginal_tax[1]
        self.assertEqual(7.56, marginal_rate_eligible_dividends)

    def test_marginal_rate_ineligible_dividends(self):
        marginal_tax = self.tax_calculator._get_percentages(self.taxable_income)
        marginal_rate_ineligible_dividends = marginal_tax[2]
        self.assertEqual(19.80, marginal_rate_ineligible_dividends)

    def test_marginal_rate_capital_gain(self):
        marginal_tax = self.tax_calculator._get_percentages(self.taxable_income)
        marginal_rate_capital_gain = marginal_tax[3]
        self.assertEqual(14.10, marginal_rate_capital_gain)


if __name__ == '__main__':
    unittest.main()
