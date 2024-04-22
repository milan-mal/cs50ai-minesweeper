import copy
import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if(len(self.cells) == self.count):
            return self.cells
        else:
            return set()
            

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if(self.count == 0):
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if(cell in self.cells):
            self.cells = self.cells - {cell}
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if(cell in self.cells):
            self.cells = self.cells - {cell}


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            if cell in sentence.cells:
                sentence.cells.remove(cell)
                sentence.count -= 1

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            if cell in sentence.cells:
                sentence.cells.remove(cell)
                if len(sentence.cells) < 1:
                    self.knowledge.remove(sentence)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        
        self.moves_made.add(cell)
        self.mark_safe(cell)

        neighbor_cells = set((x, y)
            for x in range(max(0, cell[0] - 1), min(self.height, cell[0] + 2))    # +1 for one line down, +1 as per range spec
            for y in range(max(0, cell[1] - 1), min(self.width, cell[1] + 2))
        ) - {cell}

        # remove known safes from the neighbor cells
        for i in self.safes:
            if i in neighbor_cells:
                neighbor_cells.remove(i)

        # remove knowns mines from the neighbor cells
        for i in self.mines:
            if i in neighbor_cells:
                neighbor_cells.remove(i)
                count -= 1

        if neighbor_cells:
            if count == 0:
                for i in neighbor_cells:
                    if i not in self.safes:
                        self.mark_safe(i)
            elif len(neighbor_cells) == count:
                for i in neighbor_cells:
                    if i not in self.mines:
                        self.mark_mine(i)
            else:
                new_sentence = Sentence(neighbor_cells, count)
                if new_sentence not in self.knowledge:
                    self.knowledge.append(new_sentence)

        # 4) mark any additional cells as safe or as mines
        #    if it can be concluded based on the AI's knowledge base:

        changes = 1
        while changes > 0:
            changes = 0
            knowledge_copy = copy.deepcopy(self.knowledge)
            for i in range(len(knowledge_copy)):
                if knowledge_copy[i].count < 1:
                    for cell in knowledge_copy[i].cells:
                        if cell not in self.safes:
                            self.mark_safe(cell)
                elif knowledge_copy[i].count == len(knowledge_copy[i].cells):
                    for cell in knowledge_copy[i].cells:
                        if cell not in self.mines:
                            self.mark_mine(cell)
                    changes += 1

            # 5) add any new sentences to the AI's knowledge base
            #    if they can be inferred from existing knowledge
        
            knowledge_max_i = len(self.knowledge) - 1
            for i in range(knowledge_max_i):
                for j in range(i + 1, knowledge_max_i + 1):
                    if self.knowledge[i].cells > self.knowledge[j].cells:
                        if self.knowledge[i].count >= self.knowledge[j].count:
                            new_sentence = Sentence(self.knowledge[i].cells - self.knowledge[j].cells, self.knowledge[i].count - self.knowledge[j].count)
                            if new_sentence not in self.knowledge:  # to avoid duplicates
                                self.knowledge.append(new_sentence)
                                self.knowledge.remove(self.knowledge[i])
                                changes += 1
            for i in range(knowledge_max_i):
                for j in range(i, knowledge_max_i):
                    if self.knowledge[i].cells < self.knowledge[j + 1].cells:
                        if self.knowledge[i].count <= self.knowledge[j + 1].count:
                            new_sentence = Sentence(self.knowledge[j + 1].cells - self.knowledge[i].cells, self.knowledge[j + 1].count - self.knowledge[i].count)
                            if new_sentence not in self.knowledge:  # to avoid duplicates
                                self.knowledge.append(new_sentence)
                                self.knowledge.remove(self.knowledge[j + 1])
                                changes += 1
        
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        safes_not_moves = self.safes - self.moves_made
        if safes_not_moves:
            return safes_not_moves.pop()
        else:
            return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        not_move_not_mine = set((x, y)
            for x in range(self.height)
            for y in range(self.width)
        ) - self.mines - self.moves_made

        if not_move_not_mine:
            return not_move_not_mine.pop()
        else:
            return None