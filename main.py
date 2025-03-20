'''
Author: Alafi Dumo
Date: 20th March 2025
I'll simulate how much money a financially literate person v a non-financially literate will have after 40 years 
of small decisions in this program.
'''

import matplotlib.pyplot as plt

class Person:
    def __init__(self, savings, checking, debt, loan):
        self.savings = savings
        self.checking = checking
        self.debt = debt
        self.loan = loan

    def savings_bal(self, is_fl):
        # The financially literate person invests their money in a mutual fund with 7% interest per annum
        if is_fl:
            self.savings *= 1.07
        # For the non-financially literate, savings lose value due to the inflation of 2% although they earn a 1% interest
        else:
            self.savings *= 0.99

    def debt_bal(self, is_fl):
        # Initialize attributes if they don't exist
        if not hasattr(self, 'total_debt_paid'):
            self.total_debt_paid = 0
        if not hasattr(self, 'years_in_debt'):
            self.years_in_debt = 0

        rem_debt = self.debt
        total_paid = 0

        # Simulate 12 months of debt payments
        for month in range(12):
            if rem_debt <= 0:
                break

            # Minimum payment is 3% of the remaining debt
            min_pay = rem_debt * 0.03

            # Additional payments
            if is_fl:
                add_pay = 15
            else:
                add_pay = 1

            total_pay = min_pay + add_pay
            total_paid += total_pay 
            rem_debt -= total_pay

        # Apply annual compound interest
        rem_debt *= 1.2
        self.debt = rem_debt
        self.total_debt_paid += total_paid

        if self.debt > 0:
            self.years_in_debt += 1

        return total_paid

    def sub_rent_checking(self):
        # Initialize years rented if not already initialized
        if not hasattr(self, 'years_rented'):
            self.years_rented = 0

        # Simulate 12 months of rent payments
        for month in range(12):
            self.checking -= 850
        self.years_rented += 1  # Increment years rented after 12 months

    def sub_mortgage_checking(self, is_fl):
        # Assume they pay the mortgage in 30 years (360 months)
        N = 360
        if is_fl:
            i = 0.045 / 12  # 4.5% annual interest
        else:
            i = 0.05 / 12  # 5% annual interest (including PMI)

        # Discount factor
        D = ((i + 1) ** N - 1) / (i * (1 + i) ** N)
        P = (175000 - (self.checking if is_fl else 175000 * 0.05)) / D  # Fixed: Use 175000 instead of 17500

        # Simulate 12 months of mortgage payments
        for month in range(12):
            self.checking -= P
            self.loan -= P

    def buy_house(self, is_fl):
        # Initialize house attribute if not already initialized
        if not hasattr(self, 'house'):
            self.house = False

        if not self.house:
            if is_fl:
                down_pay = 175000 * 0.20
            else:
                down_pay = 175000 * 0.05

            if self.checking >= down_pay:
                self.checking -= down_pay
                self.loan = 175000 - down_pay
                self.house = True

    def yearly_income(self):
        # Update annual income: 20% to savings, 30% to checking
        self.savings += 59000 * 0.20
        self.checking += 59000 * 0.30

    def calc_wealth(self):
        # Calculate total wealth (savings + checking - debt - loan)
        return round(self.savings + self.checking - self.debt - self.loan)


class Sim:
    def __init__(self, person, is_fl):
        self.person = person
        self.is_fl = is_fl
        self.wealth_lst = []

    def run_sim(self):
        # Append initial wealth
        self.wealth_lst.append(self.person.calc_wealth())

        # Simulate 40 years
        for year in range(40):
            self.person.yearly_income()
            self.person.savings_bal(self.is_fl)
            self.person.debt_bal(self.is_fl)

            if not hasattr(self.person, 'house') or not self.person.house:
                self.person.sub_rent_checking()
                self.person.buy_house(self.is_fl)
            else:
                self.person.sub_mortgage_checking(self.is_fl)

            # Append wealth for the current year
            self.wealth_lst.append(self.person.calc_wealth())

        return self.wealth_lst


def visualize_results(fl_wealth, nfl_wealth):
    years = list(range(41))  

    plt.figure(figsize=(10, 6))
    plt.plot(years, fl_wealth, label="Financially Literate (fl)", color="blue")
    plt.plot(years, nfl_wealth, label="Not Financially Literate (nfl)", color="red")
    plt.title("Wealth Over 40 Years")
    plt.xlabel("Years")
    plt.ylabel("Wealth ($)")
    plt.legend()
    plt.grid(True)
    plt.show()


def run_tests():
    # Test Person class
    fl = Person(5000, 0, 30100, 0)
    nfl = Person(5000, 0, 30100, 0)

    # Test initial savings
    assert fl.savings == 5000
    assert nfl.savings == 5000

    # Test savings balance after a year
    fl.savings_bal(is_fl=True)
    nfl.savings_bal(is_fl=False)
    assert fl.savings == 5350
    assert nfl.savings == 4950

    # Test debt balance after a year
    fl_debt_paid = fl.debt_bal(is_fl=True)
    nfl_debt_paid = nfl.debt_bal(is_fl=False)
    assert fl_debt_paid > nfl_debt_paid, "fl should pay more debt than nfl"

    # Test Simulation class
    fl_sim = Sim(fl, is_fl=True)
    nfl_sim = Sim(nfl, is_fl=False)
    fl_wealth = fl_sim.run_sim()
    nfl_wealth = nfl_sim.run_sim()
    assert len(fl_wealth) == 41
    assert len(nfl_wealth) == 41

    print("All tests passed!")


def main():
    fl = Person(savings=5000, checking=0, debt=30100, loan=0)
    nfl = Person(savings=5000, checking=0, debt=30100, loan=0)

    fl_sim = Sim(fl, is_fl=True)
    nfl_sim = Sim(nfl, is_fl=False)

    fl_wealth = fl_sim.run_sim()
    nfl_wealth = nfl_sim.run_sim()

    print("Financially Literate (fl) Wealth Over 40 Years:")
    print(fl_wealth)
    print("\nNot Financially Literate (nfl) Wealth Over 40 Years:")
    print(nfl_wealth)

    # Visualize the results
    visualize_results(fl_wealth, nfl_wealth)


if __name__ == "__main__":
    run_tests()
    main()