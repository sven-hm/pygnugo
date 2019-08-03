import unittest
import sys, os

test_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(test_path + '/..')

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

    def test_c_write_load_file(self):
        _tmp_filename = 'tests/tmp.sgf'
        gg = pygnugo.GnuGo()

        gg.play(pygnugo.Color.BLACK, pygnugo.Vertex('D4'))
        gg.genmove(pygnugo.Color.WHITE)
        gg.genmove(pygnugo.Color.BLACK)
        gg.genmove(pygnugo.Color.WHITE)
        gg.genmove(pygnugo.Color.BLACK)
        gg.genmove(pygnugo.Color.WHITE)
        gg.genmove(pygnugo.Color.BLACK)

        history = gg.move_history()

        gg.save_with_history(_tmp_filename)
        gg.quit()

        gg2 = pygnugo.GnuGo()
        gg2.loadsgf(_tmp_filename)

        self.assertEqual(history, gg2.move_history())

        gg2.quit()
        os.remove(_tmp_filename)

if __name__ == '__main__':
    unittest.main()
