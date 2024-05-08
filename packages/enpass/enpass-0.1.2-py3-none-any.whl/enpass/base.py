def calc_base(password):
    """
    Calculates the base of the entropy calculation based on the character types present in the password.
    
    Character Sets:
        26 lowercase letters
        26 uppercase letters
        10 digits
        36 special characters (assuming common ASCII set)

    Assuming a password is using at least 1 character of each set, the base would be: 98 (26 + 26 + 10 + 36)
    """
    
    base = 0    
    character_types = {
        'lower': False, 
        'upper': False, 
        'digit': False, 
        'special': False
        }

    for c in password:
        #If all characters have been encountered (ie: True) exit the loop early
        #This helps with efficiency for longer passwords
        if all(character_types.values()):
            break
        if c.islower() and not character_types['lower']:
            base += 26
            character_types['lower'] = True
        elif c.isupper() and not character_types['upper']:
            base += 26
            character_types['upper'] = True
        elif c.isdigit() and not character_types['digit']:
            base += 10
            character_types['digit'] = True
        elif not c.isalnum() and not character_types['special']:
            base += 36
            character_types['special'] = True

    return base