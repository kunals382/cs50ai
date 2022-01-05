import sys
import copy

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        d_copy = copy.deepcopy(self.domains)
        for var in d_copy: # for each variable
            for word in d_copy[var]: # for each word in the variable
                if len(word) != var.length: # if length is not equal
                    self.domains[var].remove(word) # make change in self not in d. copy


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        to_remove = []
        overlap = self.crossword.overlaps[x, y]

        if overlap:
            x_o, y_o = overlap # positions of overlap in x and y
            for var1 in self.domains[x]:
                matched = False
                for var2 in self.domains[y]:
                    if var1 != var2 and var1[x_o] == var2[y_o]: # same letter in overlapping position
                        matched = True
                        break
                if matched:
                    continue
                else:
                    to_remove.append(var1)
        else: 
            return False

        for word in to_remove:
            self.domains[x].remove(word)

        return len(to_remove) > 0


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            arcs = []
            for var1 in self.domains: # populating the queue when queue is embty
                for var2 in self.crossword.neighbors(var1):
                    arcs.append((var1, var2))            
        
        for x,y in arcs:
            if self.revise(x, y): # if change made
                for neighbour in self.crossword.neighbors(x):
                    arcs.append((x, neighbour))
        
        return len(self.domains[x]) > 0


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for variable in self.crossword.variables:
            if variable not in assignment.keys():
                return False
            if assignment[variable] not in self.crossword.words:
                return False
                
        return True


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # that is to say, all values are distinct,
        words = [*assignment.values()] 
        if len(words) != len(set(words)):
            return False 

        # every value is the correct length, 
        for var in assignment:
            if var.length != len(assignment[var]):
                return False

        # and there are no conflicts between neighboring variables.
        for var in assignment:
            for neighbour in self.crossword.neighbors(var):
                if neighbour in assignment:
                    x, y = self.crossword.overlaps[var, neighbour]
                    if assignment[var][x] != assignment[neighbour][y]:
                        return False
        # else 
        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        
        neighbours = self.crossword.neighbors(var)
        
        result = []

        for value in self.domains[var]:
            eliminated = 0
            for var2 in neighbours:
                if var2 in assignment: # if neighbour already has assigned value
                    continue
                else:
                    for value2 in self.domains[var2]:
                        x_o, y_o = self.crossword.overlaps[var, var2]
                        if x_o: # if overlap
                            if value[x_o] != value2[y_o]: 
                                eliminated += 1
                                
            result.append([value, eliminated])

        result.sort(key=lambda a: a[1])

        return [a[0] for a in result]


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        dictionary = {}
        
        for var in self.crossword.variables:
            if var not in assignment.keys():
                dictionary[var] = self.domains[var]
                
        sorted_list = [var for var, val in sorted(dictionary.items(), key=lambda item:len(item[1]))]
        
        return sorted_list[0]

        
    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        
        var = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            new_assignment[var] = value
            
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result:
                    return result
                    
        return None
        
        
def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
