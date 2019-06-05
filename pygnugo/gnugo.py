from subprocess import Popen, PIPE, STDOUT
from queue import Queue
from threading import Thread, Event
import time

from enum import Enum


class Color(Enum):
    """
    Color Enum for go stones.
    """

    BLACK = 0
    WHITE = 1

    def __str__(self):
        return self.name.lower()

    def other(self):
        return Color((self.value + 1) % 2)


class Boardsize(Enum):
    """
    Boardsize Enum for standard board sizes.
    """

    LARGE  = 19
    MEDIUM = 13
    SMALL  =  9

    def __str__(self):
        return str(self.value)

"""
Allow construction of Boardsize enum from string of boardsize.
FIXME: This breaks copy-construction :/
"""
Boardsize.__new__ = lambda cls, value: super(Boardsize, cls).__new__(cls, int(value))


class Vertex(str):
    pass


class NoGameRunningError(Exception):
    pass


class GnuGoException(Exception):
    pass


class GnuGoNotImplemented(Exception):
    pass


class GnuGo(object):

    def __init__(self, boardsize=Boardsize.LARGE):

        self._boardsize = boardsize

        self._outputQ = Queue()
        cmd = ['gnugo',
                '--mode', 'gtp',
                '--boardsize', '{0}'.format(self._boardsize.value)]
        self._gnugo = Popen(cmd,
                stdin=PIPE, stdout=PIPE, stderr=STDOUT)

        self._stop_event = Event()
        self._readoutputthread = Thread(
                target=self._fillQ,
                args=[self._gnugo.stdout, self._outputQ, self._stop_event])
        self._readoutputthread.daemon = True
        self._readoutputthread.start()


    def quit(self):
        self._send('quit')
        self._stop_event.set()
        self._gnugo.terminate()
        self._gnugo.wait()
        self._gnugo = None
        self._readoutputthread.join()
        self._readoutputthread = None


    def _fillQ(self, output, Q, stop_event):
        """
        Callback function used by thread.
        """

        for line in iter(output.readline, ''):
            if stop_event.is_set():
                break
            Q.put(line)
        output.close()


    def _send(self, cmd):
        if self._gnugo is None:
            return

        self._gnugo.stdin.write('{0}\n'.format(cmd).encode('utf-8'))
        self._gnugo.stdin.flush()


    def get_output(self):
        if self._gnugo is None:
            raise NoGameRunningError("No game running.")

        if not self._readoutputthread.isAlive():
            raise Exception

        output = ''
        while not self._outputQ.empty():
            output += self._outputQ.get().decode()

        return output


    def GenerateGnuGoCmd(name, argtypes=[], returntype=None, delay=0.1):

        def method(self, *args):

            if len(args) != len(argtypes):
                raise Exception

            for ii, arg in enumerate(args):
                if not isinstance(arg, argtypes[ii]):
                    raise Exception

            # forward to gungo
            _cmd = name
            for arg in args:
                _cmd += ' ' + str(arg)

            self._send(_cmd)

            # wait for response
            while True:
                time.sleep(delay)
                _output = self.get_output()
                if _output.find('=') != -1:
                    break
                elif _output.find('?') != -1:
                    raise GnuGoException(_output.split('?')[1].strip())

            if returntype is None:
                return None
            else:
                ret_val = _output.split('=')[1]
                if returntype == str:
                    ret_val = '\n'.join(list(filter(str.strip, ret_val.splitlines())))
                else:
                    ret_val = ret_val.strip()
                return returntype(ret_val)

        method.__name__ = name
        return method

    def no_impl(self):
        raise GnuGoNotImplemented('Function not mapped yet.')

    """
    Register gnugo gtp commands.

    Compare https://www.gnu.org/software/gnugo/gnugo_19.html
    TODO: complete registration
    """
    curate_approxlib            = no_impl
    accuratelib                 = no_impl
    advance_random_seed         = no_impl
    all_legal                   = no_impl
    all_move_values             = no_impl
    analyze_eyegraph            = no_impl
    analyze_semeai              = no_impl
    analyze_semeai_after_move   = no_impl
    attack                      = no_impl
    attack_either               = no_impl
    black                       = GenerateGnuGoCmd('black', argtypes=[Vertex])
    block_off                   = no_impl
    boardsize                   = GenerateGnuGoCmd('boardsize', argtypes=[Boardsize])
    break_in                    = no_impl
    captures                    = GenerateGnuGoCmd('captures', argtypes=[Color], returntype=int)
    clear_board                 = GenerateGnuGoCmd('clear_board')
    clear_cache                 = no_impl
    color                       = no_impl
    combination_attack          = no_impl
    combination_defend          = no_impl
    connect                     = no_impl
    countlib                    = no_impl
    cputime                     = no_impl
    decrease_depths             = no_impl
    defend                      = no_impl
    defend_both                 = no_impl
    disconnect                  = no_impl
    does_attack                 = no_impl
    does_defend                 = no_impl
    does_surround               = no_impl
    dragon_data                 = no_impl
    dragon_status               = no_impl
    dragon_stones               = no_impl
    draw_search_area            = no_impl
    dump_stack                  = no_impl
    echo                        = no_impl
    echo_err                    = no_impl
    estimate_score              = no_impl
    eval_eye                    = no_impl
    experimental_score          = no_impl
    eye_data                    = no_impl
    final_score                 = no_impl
    final_status                = no_impl
    final_status_list           = no_impl
    findlib                     = no_impl
    finish_sgftrace             = no_impl
    fixed_handicap              = no_impl
    followup_influence          = no_impl
    genmove                     = GenerateGnuGoCmd('genmove', argtypes=[Color], returntype=str)
    genmove_black               = GenerateGnuGoCmd('genmove_black', returntype=str)
    genmove_white               = GenerateGnuGoCmd('genmove_white', returntype=str)
    get_connection_node_counter = no_impl
    get_handicap                = no_impl
    get_komi                    = GenerateGnuGoCmd('get_komi', returntype=float)
    get_life_node_counter       = no_impl
    get_owl_node_counter        = no_impl
    get_random_seed             = no_impl
    get_reading_node_counter    = no_impl
    get_trymove_counter         = no_impl
    gg_undo                     = no_impl
    gg_genmove                  = no_impl
    half_eye_data               = no_impl
    help                        = no_impl
    increase_depths             = no_impl
    initial_influence           = no_impl
    invariant_hash_for_moves    = no_impl
    invariant_hash              = no_impl
    is_legal                    = no_impl
    is_surrounded               = no_impl
    kgs_genmove_cleanup         = no_impl
    known_command               = no_impl
    komi                        = GenerateGnuGoCmd('komi', argtypes=[float])
    ladder_attack               = no_impl
    last_move                   = no_impl
    level                       = no_impl
    limit_search                = no_impl
    list_commands               = no_impl
    list_stones                 = no_impl
    loadsgf                     = GenerateGnuGoCmd('loadsgf', argtypes=[str], returntype=str)
    move_influence              = no_impl
    move_probabilities          = no_impl
    move_reasons                = no_impl
    move_uncertainty            = no_impl
    move_history                = GenerateGnuGoCmd('move_history', returntype=str, delay=0.1)
    name                        = no_impl
    new_score                   = no_impl
    orientation                 = no_impl
    owl_attack                  = no_impl
    owl_connection_defends      = no_impl
    owl_defend                  = no_impl
    owl_does_attack             = no_impl
    owl_does_defend             = no_impl
    owl_substantial             = no_impl
    owl_threaten_attack         = no_impl
    owl_threaten_defense        = no_impl
    place_free_handicap         = no_impl
    play                        = GenerateGnuGoCmd('play', argtypes=[Color, Vertex])
    popgo                       = no_impl
    printsgf                    = no_impl
    protocol_version            = GenerateGnuGoCmd('protocol_version', returntype=int)
    query_boardsize             = GenerateGnuGoCmd('query_boardsize', returntype=Boardsize)
    query_orientation           = no_impl
    reg_genmove                 = no_impl
    report_uncertainty          = no_impl
    reset_connection_node_counter = no_impl
    reset_life_node_counter     = no_impl
    reset_owl_node_counter      = no_impl
    reset_reading_node_counter  = no_impl
    reset_search_mask           = no_impl
    reset_trymove_counter       = no_impl
    restricted_genmove          = no_impl
    same_dragon                 = no_impl
    set_free_handicap           = no_impl
    set_random_seed             = no_impl
    set_search_diamond          = no_impl
    set_search_limit            = no_impl
    # showboard needs a longer delay to get the whole board.
    showboard                   = GenerateGnuGoCmd('showboard', returntype=str, delay=0.1)
    start_sgftrace              = no_impl
    surround_map                = no_impl
    tactical_analyze_semeai     = no_impl
    test_eyeshape               = no_impl
    time_left                   = no_impl
    time_settings               = no_impl
    top_moves                   = no_impl
    top_moves_black             = no_impl
    top_moves_white             = no_impl
    tryko                       = no_impl
    trymove                     = no_impl
    tune_move_ordering          = no_impl
    unconditional_status        = no_impl
    undo                        = GenerateGnuGoCmd('undo')
    version                     = no_impl
    white                       = no_impl
    worm_cutstone               = no_impl
    worm_data                   = no_impl
    worm_stones                 = no_impl
