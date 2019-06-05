import unittest
import sys, os

test_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(test_path + '/../pygnugo')

import pygnugo

class TestPyGnuGo(unittest.TestCase):

    def setUp(self):
        pass

    def test_a_basic(self):
        gg = pygnugo.GnuGo()

        print('protocol version: ' + str(gg.protocol_version()))

        self.assertEqual(gg.query_boardsize(), pygnugo.Boardsize.LARGE)
        gg.boardsize(pygnugo.Boardsize.SMALL)
        self.assertEqual(gg.query_boardsize(), pygnugo.Boardsize.SMALL)

        gg.quit()

    def test_b_game(self):
        gg = pygnugo.GnuGo()

        gg.play(pygnugo.Color.BLACK, pygnugo.Vertex('D4'))
        gg.genmove(pygnugo.Color.WHITE)
        gg.genmove(pygnugo.Color.BLACK)
        gg.genmove(pygnugo.Color.WHITE)
        gg.genmove(pygnugo.Color.BLACK)
        gg.genmove(pygnugo.Color.WHITE)
        gg.genmove(pygnugo.Color.BLACK)

        print(gg.showboard())

        print(gg.move_history())

        gg.quit()

    def test_c_load_from_file(self):
        gg = pygnugo.GnuGo()
        gg.loadsgf('tests/example2.sgf')
        print(gg.showboard())
        gg.genmove(pygnugo.Color.BLACK)
        gg.genmove(pygnugo.Color.WHITE)
        print(gg.showboard())
        print(gg.move_history())

if __name__ == '__main__':
    unittest.main()
