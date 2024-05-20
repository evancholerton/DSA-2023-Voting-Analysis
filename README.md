# DSA 2023 Voting Analysis
Mann Whitney test on publicly available info for DSA chapters related to the 2023 DSA National Convention

- Are bigger chapters really more "moderate"? (Yes)
- Are bigger chapters *relative to their area's overall population* more "moderate"? (No, and neither vice versa)

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

*(IMPORTANT: The delegate-level voter data for the 2023 DSA National Convention may or may not be sensitive information. For the sake of caution, it won't be publicly available here (at least for now). If you want to clone this data and run it yourself, please contact me at evancholerton@gmail.com, or DM me on Twitter/Instagram at @evancholerton, and send verification that you're a DSA member.)*

---

#### Results are as follows:

```
Mann-Whitney U Test Results (Absolute Chapter Size):
U-statistic: 50247.0, p-value: 4.390103695210757e-13

Mann-Whitney U Test Results (DSA % Population):
U-statistic: 68800.0, p-value: 0.25203863437592944
```
---

DSA 2023 Voting Analysis by Evan Cholerton is marked with CC0 1.0 Universal. To view a copy of this license, visit https://creativecommons.org/publicdomain/zero/1.0/
