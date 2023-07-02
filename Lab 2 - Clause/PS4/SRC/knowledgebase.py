from itertools import combinations

class Literal:
    # Init literal
    def __init__(self, symbol = "", negation = False) -> None:
        self.symbol = symbol
        self.negation = negation

    # Represent literal
    def __repr__(self):
        return '-{}'.format(self.symbol) if self.negation == True else self.symbol

    # Override == (object of class become unhashable)
    def __eq__(self, literal) -> bool:
        return self.symbol == literal.symbol and self.negation == literal.negation
    
    # Hash type literal (make object of class become hashable)
    def __hash__(self):
        result = '-' + self.symbol if self.negation else self.symbol
        return hash(result)

    # Override < (to sort literals)
    def __lt__(self, literal) -> bool:
        if self.symbol != literal.symbol:
            return self.symbol < literal.symbol
        return self.negation < literal.negation # negation = False (0) < negation = True (1) 
                                                # A < -A
                                                # A OR -A

    # Negate symbol
    def negate(self):
        self.negation = 1 - self.negation # if a = True (1) -> a = 1 - True = 0 => False
                                          # if a = False (0) -> a = 1 - False = 1 => True
        
    # Check if opposite literals
    def is_opposite(self, literal):
        return self.negation != literal.negation and self.symbol == literal.symbol
    
    # Parse literal
    def parse_literal(string_literal):
        string_literal = string_literal.strip() # remove spaces at the beginning and at the end of the character

        if string_literal[0] == '-':
            new_literal = Literal(symbol = string_literal[1], negation = True) # negative literal
        else:
            new_literal = Literal(symbol = string_literal[0], negation = False) # positive literal

        return new_literal   

class Clause:
    # Init clause
    def __init__(self) -> None:
        self.literals = [] # clause is a list of literals
    
    # Represent clause
    def __repr__(self):
        if len(self.literals) != 0:
            return ' OR '.join(str(literal) for literal in self.literals)
        else:
            return '{}'
    
    # Override == (object of class become unhashable)
    def __eq__(self, clause) -> bool:
        if len(self.literals) != len(clause.literals):
            return False
        return set(self.literals) == set(clause.literals)
    
    # Hash type clause (make object of class become hashable)
    def __hash__(self) -> int:
        result = tuple(self.literals) # conver to tuple to hash because unhashable type: 'list'
        return hash(result)
    
    # Override < (to sort clauses)
    def __lt__(self, clause) -> bool:
        if len(self.literals) != len(clause.literals):
            return len(self.literals) < len(clause.literals)
        
        for index in range(len(self.literals)):
            if self.literals[index] != clause.literals[index]:
                return self.literals[index] < clause.literals[index]        
        return False
    
    # Check if clause is empty
    def is_empty(self):
        return len(self.literals) == 0
    
    # Check if clause is meaningless (example: A OR -B OR B)
    def is_meaning_less(self):
        for index in range(len(self.literals) - 1):   
            if self.literals[index].is_opposite(self.literals[index + 1]):
                return True                                               
        return False

    # Add literal into clause
    def add_literal(self, literal):
        self.literals.append(literal)
    
    # Remove duplicate and sort literals
    def clean_clause(self):
        self.literals = sorted(set(self.literals))

    # Clone clause with exception
    def cloneClauseNot(self, _literal):
        new_clause = Clause() 

        for literal in self.literals:
            if literal != _literal:
                new_clause.add_literal(literal)
        
        return new_clause
    
    # Parse clause
    def parse_clause(string_clause):
        new_clause = Clause()
        string_clause = string_clause.strip() # remove spaces at the beginning and at the end of the string
        string_literals = string_clause.split('OR') # split string into list with seperator OR
        
        for string_literal in string_literals:
            literal = Literal.parse_literal(string_literal)
            new_clause.add_literal(literal)
        
        new_clause.clean_clause()
        return new_clause

    # Merge clauses
    def mergeClauses(clause1, clause2):
        new_clause = Clause() 
        new_clause.literals = clause1.literals + clause2.literals 
        new_clause.clean_clause()
        return new_clause

    # Negate clause
    def negate(self):
        for literal in self.literals:
            literal.negate()

    # Resolve clauses
    def PL_Resolve(clause1, clause2):
        is_empty = False
        resolvents = set()

        for literal1 in clause1.literals:
            for literal2 in clause2.literals:
                if literal1.is_opposite(literal2):
                    new_clause = Clause.mergeClauses(clause1.cloneClauseNot(literal1), 
                        clause2.cloneClauseNot(literal2))
                    if new_clause.is_meaning_less():
                        continue
                    if new_clause.is_empty():
                        is_empty = True
                    resolvents.add(new_clause)

        return resolvents, is_empty
    

class Knowledge_Base:
    # Init KB
    def __init__(self) -> None:
        self.clauses = [] # KB is a list of CNF clause

    # Add clause into KB
    def add_clause(self, clause):
        self.clauses.append(clause)

    # Remove duplicate and sort clauses
    def build_Knowledge_Base(self, string_alpha, string_clauses):
        string_alpha = string_alpha.strip()
        string_literals = string_alpha.split('OR')
        for string_literal in string_literals:
            clause = Clause.parse_clause(string_literal)
            clause.negate()
            self.add_clause(clause)
        for string_clause in string_clauses:
            clause = Clause.parse_clause(string_clause)
            clause.clean_clause()
            self.add_clause(clause)
    
    def PL_Resolution(self):
        input_clauses = set(self.clauses) # contain input clauses
        output_clauses = [] # contain output clauses
        is_unsatisfiable = False
        
        while True:
            new = set() # to remove duplicate after update          
            for (clause1, clause2) in combinations(input_clauses, 2): # create a combination with 2 clauses
                resolvents, is_empty = Clause.PL_Resolve(clause1, clause2)
                new.update(resolvents)
                is_unsatisfiable |= is_empty # if contain the empty clause -> True

            diffence_clauses = new.difference(input_clauses) # diffence_clauses =  new \ input_clauses
            output_clauses.append(diffence_clauses)
            input_clauses.update(new)

            if is_unsatisfiable == True:    # if entail
                return True, output_clauses
            if len(diffence_clauses) == 0:  # if new is a subset of input_clauses
                return False, output_clauses 
            
