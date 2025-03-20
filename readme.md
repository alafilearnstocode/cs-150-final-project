
# CS-150 Final Project: Financial Literacy Simulation

## Overview

This repository contains the code for my final CS-150 project at Northwestern University during the winter quarter. The program simulates how much money a financially literate person (`fl`) versus a non-financially literate person (`nfl`) will have after 40 years of making small financial decisions. The simulation tracks savings, debt, rent, mortgage payments to demonstrate the long-term impact of financial literacy.


## Key Features

- **Simulation of Financial Decisions**:
  - Savings growth with different interest rates (7% for `fl` vs. 1% for `nfl`).
  - Debt repayment strategies (minimum payments + additional amounts).
  - Rent and mortgage payments.
  - Down payments for buying a house (20% for `fl` vs. 5% for `nfl`).

- **Wealth Calculation**:
  - Tracks total wealth over 40 years, including savings, checking, debt, and loans.

- **Visualization**:
  - Uses `matplotlib` to plot the wealth of `fl` and `nfl` over 40 years.


## How to Run the Program

### Prerequisites

1. **Python 3.x**: Ensure Python is installed on your system.
2. **Matplotlib**: Install the `matplotlib` library for visualization.



### Steps

1. **Clone the Repository**:

2. **Run the Program**:

3. **View the Results**:
   - The program will print the wealth of `fl` and `nfl` over 40 years.
   - A graph will pop up, showing the wealth trajectories of `fl` and `nfl`.


## Code Structure

- **`Person` Class**:
  - Represents a person with attributes like `savings`, `checking`, `debt`, and `loan`.
  - Methods include `savings_bal`, `debt_bal`, `sub_rent_checking`, `sub_mortgage_checking`, `buy_house`, `yearly_income`, and `calc_wealth`.

- **`Sim` Class**:
  - Simulates the financial decisions of a person over 40 years.
  - Tracks wealth and appends it to a list for visualization.

- **`visualize_results` Function**:
  - Uses `matplotlib` to plot the wealth of `fl` and `nfl` over 40 years.

- **`run_tests` Function**:
  - Tests the functionality of the `Person` and `Sim` classes.

- **`main` Function**:
  - Initializes `fl` and `nfl`, runs the simulation, and visualizes the results.


## Example Output

### Console Output

```
Financially Literate (fl) Wealth Over 40 Years:
[-25100, -20000, -15000, ..., 500000]

Not Financially Literate (nfl) Wealth Over 40 Years:
[-25100, -22000, -19000, ..., 200000]
```

### Graph Output

A graph will display two lines:
- **Blue Line**: Wealth of the financially literate person (`fl`).
- **Red Line**: Wealth of the non-financially literate person (`nfl`).


## Limitations

- **Initializations**:
  - The program initializes the financial state for `fl` and `nfl` as per the project instructions. Custom initializations are not supported.

- **Simplified Assumptions**:
  - The simulation assumes constant income, fixed interest rates, and no unexpected life events (e.g., medical emergencies, job loss).


## Future Improvements

- Add support for custom initializations (e.g., user-defined savings, debt, etc.).
- Incorporate more life events (e.g., promotions, emergencies, children's education).
- Allow user input for simulation parameters (e.g., income, interest rates).




