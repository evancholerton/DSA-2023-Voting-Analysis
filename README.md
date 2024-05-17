# DSA 2023 Voting Analysis
Simple t-tests on publicly available data for DSA chapters

- Are bigger chapters really more "moderate"? (Yes)
- Are bigger chapters *relative to their area's overall population* more "moderate"? (No)

---

#### Info:

Chapter "leftness" is measured by its delegates' first-choice slate votes at the 2023 DSA National Convention.

- "Left" slates are defined as:
   - Alexander Morash
   - Brandy Pride
   - Julius Kapushinski
   - Luisa M.
   - Anti-Zionist
   - Bread & Roses
   - Emerge
   - Libertarian Socialist Caucus
   - Marxist Unity Group
   - Red Labor
   - Red Star
   - Reform & Revolution
- "Moderate" slates are defined as:
   - Groundwork
   - North Star
   - Socialist Majority Caucus

Delegates who ranked Aaron Berger first are treated as a special case and categorized by their second-choice vote. They are categorized as "left" if they voted for 
- Ahmed Husain
- C.S. Jackson
- Catherine Elias
- John Lewis
- Jorge Rocha
- Kristin Schall
- Megan Romer
- Rashad X
- Sam Heft-Luthy, or
- Tom Julstrom

for second-choice; and they are categorized as "moderate" if they voted for
- Cara Tobe
- Colleen Johnston
- Grace Mausser
- Renée Paradis, or
- Rose DuBois

for second-choice.

---

#### Results are as follows:

Descriptive Statistics (Absolute Chapter Size):
                count       mean        std  min  25%   50%   75%    max
slate_category                                                          
left            449.0  22.614699  27.277441  1.0  5.0  11.0  30.0  102.0
moderate        322.0  38.897516  34.268848  1.0  8.0  38.0  57.0  102.0

T-Test Results (Absolute Chapter Size):
t-statistic: -7.069996952443903, p-value: 4.384643960842792e-12

Descriptive Statistics (DSA % Population):
                count      mean       std       min       25%       50%       75%       max
slate_category                                                                             
left            449.0  0.000552  0.000394  0.000026  0.000253  0.000451  0.000775  0.001693
moderate        322.0  0.000565  0.000323  0.000026  0.000280  0.000580  0.000694  0.001465

T-Test Results (DSA % Population):
t-statistic: -0.4863492897187075, p-value: 0.6268606275814825

Logistic Regression Results (Absolute Chapter Size):
Coefficient: -0.016948487503096833
Intercept: 0.8380512677398374
Odds Ratio: 0.9831943301253464

Logistic Regression Results (DSA % Population):
Coefficient: 0.00014606752677880888
Intercept: 0.3324713221403164
Odds Ratio: 1.0001460781951594

---

DSA 2023 Voting Analysis by Evan Cholerton is marked with CC0 1.0 Universal. To view a copy of this license, visit https://creativecommons.org/publicdomain/zero/1.0/
