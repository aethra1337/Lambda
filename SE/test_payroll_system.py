import unittest

# --- BOX 1: CALCULATION LOGIC ---
class PayrollCalculator:
    @staticmethod
    def calculate_overtime(hours: float) -> float:
        return max(0.0, hours - 40.0)

    @staticmethod
    def calculate_gross(hours: float, rate: float, bonus: float) -> float:
        return (hours * rate) + bonus

    @staticmethod
    def calculate_net(gross: float, tax_rate: float) -> float:
        # tax_rate is expected as a percentage (e.g., 0.20 for 20%)
        return gross - (gross * tax_rate)


# --- BOX 2: REPORTING LOGIC ---
class PayrollReport:
    @staticmethod
    def print_payslip(name, hours, overtime, rate, bonus, tax, total):
        print(f"\n{'='*40}")
        print(f"{'PAYROLL SLIP':^40}")
        print(f"{'='*40}")
        print(f" Employee Name   : {name}")
        print(f" Working Hours   : {hours} (OT: {overtime})")
        print(f" Hourly Rate     : ${rate:.2f}")
        print(f" Bonus           : ${bonus:.2f}")
        print(f" Tax Rate        : %{tax*100}")
        print(f"{'-'*40}")
        print(f" TOTAL NET PAY   : ${total:.2f}")
        print(f"{'='*40}\n")


# --- BOX 3: MAIN ENTITY (THE EMPLOYEE) ---
class Employee:
    def __init__(self, name: str, hours: float, pay_rate: float, bonus: float, tax_rate: float):
        self.name = name
        self.hours = hours
        self.pay_rate = pay_rate
        self.bonus = bonus
        self.tax_rate = tax_rate # e.g., 0.15 for 15%

    def get_total_earnings(self) -> float:
        gross = PayrollCalculator.calculate_gross(self.hours, self.pay_rate, self.bonus)
        return PayrollCalculator.calculate_net(gross, self.tax_rate)

    def show_payroll_details(self):
        overtime = PayrollCalculator.calculate_overtime(self.hours)
        total = self.get_total_earnings()
        PayrollReport.print_payslip(
            self.name, self.hours, overtime, self.pay_rate, 
            self.bonus, self.tax_rate, total
        )


# --- UNIT TESTING ---
class TestPayrollSystem(unittest.TestCase):
    
    def setUp(self):
        # Create a sample employee for testing
        # 50 hours, $100/hr, $1000 bonus, 20% tax
        self.emp = Employee("John Doe", 50, 100, 1000, 0.20)

    def test_overtime_calculation(self):
        ot = PayrollCalculator.calculate_overtime(self.emp.hours)
        self.assertEqual(ot, 10.0)

    def test_total_net_pay(self):
        # Calculation: (50*100) + 1000 = 6000 Gross
        # 6000 - (6000 * 0.20) = 4800 Net
        self.assertEqual(self.emp.get_total_earnings(), 4800.0)

    def test_calculator_gross(self):
        gross = PayrollCalculator.calculate_gross(40, 100, 500)
        self.assertEqual(gross, 4500.0)


# --- EXECUTION ---
if __name__ == "__main__":
    # Run Unit Tests
    print("Running Unit Tests...")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPayrollSystem)
    unittest.TextTestRunner(verbosity=2).run(suite)

    # Show a practical example
    print("\nDisplaying Sample Payroll Report:")
    emp1 = Employee("Alice Smith", 45, 120, 800, 0.15)
    emp1.show_payroll_details()