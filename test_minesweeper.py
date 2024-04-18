import unittest  # Python's built-in testing library
import minesweeper  # Assuming your Minesweeper code is in 'minesweeper.py'

class TestMinesweeperAI(unittest.TestCase):

    def test_add_knowledge_corner_case(self):
        """MinesweeperAI.add_knowledge adds sentence in corner of board"""
        ms = minesweeper
        ms_ai = ms.MinesweeperAI(height=4, width=5)
        ms_ai.add_knowledge((3, 4), 1)
        s = ms.Sentence({(2, 3), (2, 4), (3, 3)}, 1)
        self.assertTrue(s in ms_ai.knowledge, f"Did not find sentence {s}")

        # Additional assertions (same as in the improved example)
        self.assertTrue((3, 4) in ms_ai.moves_made, "Cell (3, 4) should be marked as a move made")

        # Example: Assuming you can access neighbor cells directly 
        neighbor_cells = ms_ai.get_neighbor_cells((3, 4))  
        self.assertEqual(neighbor_cells, {(2, 3), (2, 4), (3, 3)}, "Incorrect neighbor cells found")

if __name__ == '__main__':
    unittest.main()
