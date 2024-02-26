# Function to check if the formula is an expression that is completely enclosed by brackets
def uselessbraces(form):
    if isvariable_or_primitive(form):
        return False
    if form[0] == "(" and form[-1] == ")":
        numberofopening = 0
        numberofclosing = 0
        for i in range(len(form)):
            x = form[i]
            if x == "(":
                numberofopening += 1
            elif x == ")":
                numberofclosing += 1
            if numberofopening == numberofclosing and not i == len(form) - 1:
                return False
        else:
            return True


# Function to check if the formula is a variable
def isvariable(form):
    if isvariable_or_primitive(form):
        if form.upper() == "TRUE" or form.upper() == "FALSE":
            return False
        return True
    return False


# Function to check if the formula is a variable or a primitive (like False or True)
def isvariable_or_primitive(form):
    for x in form:
        if x in {"|", "&", "!", "(", ")", ">", "="}:
            return False
    return True


# Function to check if the formula is a primitive like True or False
def isprimitive(form):
    if isvariable_or_primitive(form):
        if form.upper() == "TRUE" or form.upper() == "FALSE":
            return True
        return False
    return False


# Function to check if the formula is a negation
def isnegation(form):
    if form[0] == "!" and (uselessbraces(form[1:]) or isvariable_or_primitive(form[1:])):
        return True
    return False


# Function to check if the formula has correct braces
def correctbraces(form):
    opening = 0
    closing = 0
    for x in form:
        if x == "(":
            opening += 1
        elif x == ")":
            closing += 1
        if closing > opening:
            return False
    if not closing == opening:
        return False
    return True


# Function to remove useless braces (but just them that are completely around the formula)
def elminateuselessbraces(form):
    if uselessbraces(form):
        return form[1:-1]
    return form


# Function to find all direct subformulas and the highest element in the syntax tree, also the position of the highest element (without useless braces)
def directsubformulas(form):
    if form == "":
        return [], "e", 0

    dirsubformulas = []

    # Delete all useless braces around the formula
    if uselessbraces(form):
        return directsubformulas(form[1:-1])

    # check if the formula is just a single variable
    if isvariable(form):
        return [], "v", 0

    # Check if the formula is just a single primitive
    if isprimitive(form):
        return [], "p", 0

    # Now we have to find the highest element in the syntax tree

    # check if the highest element is a negation
    if isnegation(form):
        dirsubformulas.append(elminateuselessbraces(form[1:]))
        return dirsubformulas, "!", 0

    # Check if the highest element is a logical equivalence. Equivalence is treated as LEFTASSOCIATIVE
    for i in range(len(form)):
        if form[-i] == "=" and correctbraces(form[-i + 1:]):
            dirsubformulas.append(elminateuselessbraces(form[:-i]))
            dirsubformulas.append(elminateuselessbraces(form[-i + 1:]))
            return dirsubformulas, "=", i

    # check if the highest element is a logical implication. Implication is treated as RIGHTASSOCIATIVE
    for i in range(len(form)):
        if form[i] == ">" and correctbraces(form[i + 1:]):
            dirsubformulas.append(elminateuselessbraces(form[:i]))
            dirsubformulas.append(elminateuselessbraces(form[i + 1:]))
            return dirsubformulas, ">", i

    # check if the highest element is a logical or. Or is treated as LEFTASSOCIATIVE
    for i in range(len(form)):
        if form[-i] == "|" and correctbraces(form[-i + 1:]):
            dirsubformulas.append(elminateuselessbraces(form[:-i]))
            dirsubformulas.append(elminateuselessbraces(form[-i + 1:]))
            return dirsubformulas, "|", i

    # check if the highest element is a logical and. And is treated as LEFTASSOCIATIVE
    for i in range(len(form)):
        if form[-i] == "&" and correctbraces(form[-i + 1:]):
            dirsubformulas.append(elminateuselessbraces(form[:-i]))
            dirsubformulas.append(elminateuselessbraces(form[-i + 1:]))
            return dirsubformulas, "&", i

    # If the formula is not syntactically correct, raise an error
    raise ValueError("Formel ist nicht syntaktisch korrekt")


# & ist the logic and, | is the logic or, > is the logic implication, = is the logic equivalence and ! is the logic not
# Variables are not allowed to contain any logic symbols or braces

if __name__ == "__main__":
    while True:
        formula = input("Gib jetzt die Formel ein: ")
        print(directsubformulas(formula))
