import unittest  # Python's built-in testing library
import minesweeper  # Assuming your Minesweeper code is in 'minesweeper.py'

class TestMinesweeperAI(unittest.TestCase):

    def test_add_knowledge_corner_case(self):
        """MinesweeperAI.add_knowledge adds sentence in corner of board"""
        ms_ai = minesweeper.MinesweeperAI(height=4, width=5)
        ms_ai.add_knowledge((3, 4), 1)
        s = minesweeper.Sentence({(2, 3), (2, 4), (3, 3)}, 1)
        self.assertTrue(s in ms_ai.knowledge, f"Did not find sentence {s}")

        self.assertTrue((3, 4) in ms_ai.moves_made, "Cell (3, 4) should be marked as a move made")

    def test_add_knowledge_check_mines(self):
        """MinesweeperAI.add_knowledge ignores known mines when adding new sentence"""
        ms_ai = minesweeper.MinesweeperAI(height=4, width=5)
        ms_ai.add_knowledge((0, 0), 3)
        ms_ai.mines.update({(0, 1), (1, 0), (1, 1)}) # just in case submission doesn't infer already
        ms_ai.add_knowledge((0, 2), 3)
        s = minesweeper.Sentence({(0, 3), (1, 2), (1, 3)}, 1)
        self.assertTrue(s in ms_ai.knowledge, f"Did not find sentence {s}")

    def test_add_knowledge_infer_mine(self):
        """MinesweeperAI.add_knowledge can infer mine when given new information"""
        ai = minesweeper.MinesweeperAI(height=4, width=5)
        ai.add_knowledge((2, 4), 1)
        ai.add_knowledge((2, 3), 1)
        ai.add_knowledge((1, 4), 0)
        ai.add_knowledge((3, 2), 0)
        expected = {(3, 4)}
        result = ai.mines
        if expected != result:
            self.assertEqual(str(expected), str(result), f'expected {expected}, not {result}')

    def test_add_knowledge_infer_mines_multiple(self):
        """MinesweeperAI.add_knowledge can infer multiple mines when given new information"""
        ai = minesweeper.MinesweeperAI(height=4, width=5)
        ai.add_knowledge((2, 0), 2)
        ai.add_knowledge((3, 1), 0)
        expected = {(1, 0), (1, 1)}
        result = ai.mines
        if expected != result:
            self.assertEqual(str(expected), str(result), f'expected {expected}, not {result}')

    def test_add_knowledge_infer_safes(self):
        """MinesweeperAI.add_knowledge can infer safe cells when given new information"""
        ai = minesweeper.MinesweeperAI(height=4, width=5)
        ai.add_knowledge((0, 1), 1)
        ai.add_knowledge((1, 0), 1)
        ai.add_knowledge((1, 2), 1)
        ai.add_knowledge((3, 1), 0)
        ai.add_knowledge((0, 4), 0)
        ai.add_knowledge((3, 4), 0)
        safes = [(0, 0), (0, 2)]
        for safe in safes:
            self.assertTrue(safe in ai.safes, f"Did not find safe {safe}")

if __name__ == '__main__':
    unittest.main()
