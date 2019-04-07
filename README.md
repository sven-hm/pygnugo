# pygnugo

Library to communicate with gnugo via gtp.

## Requirements

* gnugo
* python3

## Install

```sh
pip install pygnugo
```

## Usage

```python
In [1]: import pygnugo

In [2]: gnugo = pygnugo.GnuGo()

In [3]: gnugo.play(pygnugo.Color.BLACK, pygnugo.Vertex('D4'))

In [4]: gnugo.play(pygnugo.Color.WHITE, pygnugo.Vertex('Q16'))

In [5]: for i in range(10):
   ...:     gnugo.genmove(pygnugo.Color.WHITE)
   ...:     gnugo.genmove(pygnugo.Color.BLACK)
   ...:

In [6]: print(gnugo.showboard())
A B C D E F G H J K L M N O P Q R S T
19 . . . . . . . . . . . . . . . . . . . 19
18 . . . . . . . . . . . . . . . . . . . 18
17 . . . . . . . . . . . . . . . . O X . 17
16 . . . O . . . . . + . . . O . O . X . 16
15 . . . . . . . . . . . . . . . . . . . 15
14 . . X . . . . . . . . . . . X . X . . 14
13 . . . . . . . . . . . . . . . . . . . 13
12 . . . . . . . . . . . . . . . . . . . 12
11 . . . . . . . . . . . . . . . . . . . 11     WHITE (O) has captured 0 stones
10 . . . + . . . . . + . . . . . O . . . 10     BLACK (X) has captured 0 stones
 9 . . . . . . . . . . . . . . . . . . . 9
 8 . . X . . . . . . . . . . . . . . . . 8
 7 . . . . . . . . . . . . . . . . O . . 7
 6 . . O . O . O . . . . . . . . . . . . 6
 5 . . . . . . . . . . . . . . . . . . . 5
 4 . . . X . X . X . + . . . . . + X . . 4
 3 . . . . . . . . . . O . . O . X . . . 3
 2 . . . . . . . . . . . . . . . . . . . 2
 1 . . . . . . . . . . . . . . . . . . . 1
   A B C D E F G H J K L M N O P Q R S T

In [7]: gnugo.captures(pygnugo.Color.BLACK)
Out[7]: 0

In [8]: gnugo.captures(pygnugo.Color.WHITE)
Out[8]: 0

In [9]: gnugo.quit()
```

## Todo

* Map remaining gnugo gtp commands [here](pygnugo/gnugo.py).
