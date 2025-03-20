'''
Author: Alafi Dumo
Date: 20th March 2025
I'll simulate how much money a financially literate person v a non-financially literate will have after 40 years 
of small decisions in this program.
'''

import matplotlib.pyplot as plt

class Person:
    def __init__(self, savings, checking, debt, loan):
        '''
        Initialize the Person class with the following attributes:
        Args:
        - savings: Initial savings amount
        - checking: Initial checking account balance
        - debt: Initial debt amount
        - loan: Initial loan amount
        Return:
        - None
        '''
        self.savings = savings
        self.checking = checking
        self.debt = debt
        self.loan = loan

    def savings_bal(self, is_fl):
        '''
        Update the savings balance for the person after a year depending on whether they invest in a mutual fund or a savings account.
        Args:
        - is_fl: Boolean indicating whether the person is financially literate
        Return:
        - None
        '''
        mutual_fund_int = 0.07
        savings_int = 0.01
        inflation = 0.02
        if is_fl:
            self.savings *= 1 + mutual_fund_int
        else:
            self.savings *= (1 + savings_int) - inflation

    def debt_bal(self, is_fl):
        '''
        Update the debt balance for the person after a year depending on whether they make additional payments.
        Args:
        - is_fl: Boolean indicating whether the person is financially literate
        Return:
        - total_paid: Total amount paid towards the debt
        '''
        if not hasattr(self, 'total_debt_paid'):
            self.total_debt_paid = 0
        if not hasattr(self, 'years_in_debt'):
            self.years_in_debt = 0

        rem_debt = self.debt
        total_paid = 0

        for month in range(12):
            if rem_debt <= 0:
                break
            
            min_percent = 0.03
            min_pay = rem_debt * min_percent

            if is_fl:
                add_pay = 15
            else:
                add_pay = 1

            total_pay = min_pay + add_pay
            total_paid += total_pay 
            rem_debt -= total_pay

        int_rate = 0.2
        rem_debt *= 1 + int_rate
        self.debt = rem_debt
        self.total_debt_paid += total_paid

        if self.debt > 0:
            self.years_in_debt += 1

        return total_paid

    def sub_rent_checking(self):
        '''
        Update the checking account balance for the person after a year of rent payments.
        Args:
        - None
        Return:
        - None
        '''
        rent = 850
        if not hasattr(self, 'years_rented'):
            self.years_rented = 0

        for month in range(12):
            self.checking -= rent
        self.years_rented += 1  

    def sub_mortgage_checking(self, is_fl):
        '''
        Update the checking account balance for the person after a year of mortgage payments.
        Args:
        - is_fl: Boolean indicating whether the person is financially literate
        Return:
        - None
        ''' 
        N = 360
        house_price = 175000
        if is_fl:
            i = 0.045 / 12 
        else:
            i = 0.05 / 12  # (including PMI)

        D = ((i + 1) ** N - 1) / (i * (1 + i) ** N)
        P = (house_price - (self.checking if is_fl else house_price * 0.05)) / D 

        for month in range(12):
            self.checking -= P
            self.loan -= P

    def buy_house(self, is_fl):
        '''
        Buy a house if the person has enough money in their checking account.
        Args:
        - is_fl: Boolean indicating whether the person is financially literate
        Return:
        - None
        '''
        house_price = 175000

        if not hasattr(self, 'house'):
            self.house = False

        if not self.house:
            if is_fl:
                down_pay = house_price * 0.20
            else:
                down_pay = house_price * 0.05

            if self.checking >= down_pay:
                self.checking -= down_pay
                self.loan = house_price - down_pay
                self.house = True

    def yearly_income(self):
        '''
        Update the person's income after a year.
        Args:
        - None
        Return:
        - None
        '''
        income = 59000
        self.savings += income * 0.20
        self.checking += income * 0.30

    def calc_wealth(self):
        '''
        Calculate the person's total wealth.
        Args:
        - None
        Return:
        - wealth: Total wealth of the person
        '''
        # Calculate total wealth 
        return round(self.savings + self.checking - self.debt - self.loan)


class Sim:
    def __init__(self, person, is_fl):
        '''
        Initialize the simulation class with the following attributes:
        Args:
        - person: Person object
        - is_fl: Boolean indicating whether the person is financially literate
        Return:
        - None
        '''
        self.person = person
        self.is_fl = is_fl
        self.wealth_lst = []

    def run_sim(self):
        '''
        Run the simulation for 40 years.
        Args:
        - None
        Return:
        - wealth_lst: List of the person's wealth over 40 years
        '''
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



def plot_results(fl_wealth, nfl_wealth):
    '''
    Visualize the results of the simulation.
    Args:
    - fl_wealth: List of the financially literate person's wealth over 40 years
    - nfl_wealth: List of the non-financially literate person's wealth over 40 years
    Return:
    - graph: Plot of the wealth over 40 years
    '''
    years = list(range(41))  

    plt.figure(figsize=(8, 6))
    plt.plot(years, fl_wealth, label="Financially Literate (fl)", color="blue")
    plt.plot(years, nfl_wealth, label="Not Financially Literate (nfl)", color="red")
    plt.title("Wealth Over 40 Years")
    plt.xlabel("Years")
    plt.ylabel("Wealth ($)")
    plt.legend()
    plt.grid(True)
    plt.show()


def run_tests():
    '''
    Run tests for the Person and Simulation classes.
    Args:
    - None
    Return:
    - None
    '''

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
    assert fl_debt_paid > nfl_debt_paid, "fl should pay more debt than nfl after a year"

    # Test Sim class
    fl_sim = Sim(fl, is_fl=True)
    nfl_sim = Sim(nfl, is_fl=False)
    fl_wealth = fl_sim.run_sim()
    nfl_wealth = nfl_sim.run_sim()
    assert len(fl_wealth) == 41
    assert len(nfl_wealth) == 41


def main():
    '''
    Run the simulation for a financially literate and non-financially literate person.
    Args:
    - None
    Return:
    - None
    '''
    fl = Person(5000, 0, 30100, 0)
    nfl = Person(5000, 0, 30100, 0)

    fl_sim = Sim(fl, is_fl=True)
    nfl_sim = Sim(nfl, is_fl=False)

    fl_wealth = fl_sim.run_sim()
    nfl_wealth = nfl_sim.run_sim()


    print("Financially Literate (fl) Wealth Over 40 Years:")
    print(fl_wealth)
    print("\nNot Financially Literate (nfl) Wealth Over 40 Years:")
    print(nfl_wealth)

    # Visualize the results
    plot_results(fl_wealth, nfl_wealth)



if __name__ == "__main__":
    run_tests()
    main()