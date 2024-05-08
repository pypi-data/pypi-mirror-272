![Enpass](https://raw.githubusercontent.com/Aresshu/enpass/main/data/logo.png "Enpass")

### Enpass is a simple password entropy strength validator
This project can be used to validate a password strength. Designed to be lightweight with the following benefits:
* No external API calls
* No large data sets
* Focused entirely on raw entropy values
* More flexible (doesn't require uppercase, numbers, special characters)


## Installation
```bash
pip install enpass
```
## Quick Start
`calc_entropy` calculates the entropy of a password in bits.
    
Entropy equation = log2(B^L) 
`B = Base; L = Length`
```python
    from enpass import *

    password = 'P@SSW0RD!'

    #Calculates the entropy of a password in bits.
    entropy = enpass.calc_entopy(password)
```
`validate` checks if the password's entropy meets the specified minimum requirement.

Passwords should ideally be > 60.
Great Passwords should be between 70-90.
```python
    min_entropy = 60.0
    # Checks if the password's entropy meets the specified minimum requirement.
    validate = enpass.validate(entropy, min_entropy)
```
`estimate_bruteforce_time` assumes that cracking time scales linearly with the number of possible combinations.

While this might hold for straightforward brute-force attacks, more sophisticated attacks,
such as dictionary attacks or those exploiting weaknesses in password hashing algorithms, may have different time complexities.
```python
    guesses_per_second = 100_000_000
    # Estimates the amount of time required to brute-force a password 
    time_brute_estimate = enpass.estimate_bruteforce_time(entropy, guesses_per_second)
```
## Roadmap
- [x] Entropy Calculator
- [x] Brute-Force Estimate
- [ ] Scoring
- [ ] Feedback
- [ ] Throttling/Hashing Brute-Force Estimate
- [ ] Character Sequences

## Contributing
Contributions are welcome!

