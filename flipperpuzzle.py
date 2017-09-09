#!/usr/bin/python
"""
A solver for a pancake flipping (or bit flipping) puzzle

Given an input file whose first line is the number of challenge lines to follow
and the subsequent challenge lines are composed of a series of + and - chars, followed by
a space, and then an integer.

The +- string denotes the starting position of the pancakes for that challenge.
The integer denotes the width of your multi-pancake flipper (number to flip at once).

Print out a solution for the minimum number of flips required to solve each challenge with
the given flipper width, or the word IMPOSSIBLE if no solution exists. The challenge is
considered solved when all pancakes are + characters.

Invocation:
./flipperpuzzle.py inputfile.txt

References:
https://code.google.com/codejam/contest/3264486/dashboard
"""

# IMPORTS
import doctest
import sys

# CLASSES
class Challenge():
    """
    Attributes
    ----------
    flipw - int - width in pancakes of the flipper
    npan  - int - number of pancakes on the griddle
    states - [[bool]] - list of states of pancakes
    cstate - [bool] - current pancake state as list of bools, T==+, F==-
    nflips - int - number of flips made so far
    solution - int - number of flips used to solve. None before solved, -1 if impossible

    """
    def __init__(self, flipw, start):
        """

        Parameters
        ----------
        flipw
        npan
        start

        Examples
        --------
        >>> from flipperpuzzle import *
        >>> chal = Challenge(2, '++')
        >>> chal.npan == 2
        True
        >>> all(chal.cstate)
        True

        """
        self.flipw  = flipw
        self.cstate = signs2bool(start)
        self.npan   = len(self.cstate)
        self.states = [self.cstate[:]]
        self.nflips = 0
        self.solution = None
        if self.flipw > self.npan:
            # flipper is too wide, check for already sovlved, else impossible
            if not self.is_solved():
                self.solution = -1

    def is_solved(self):
        """

        Returns
        -------
        is_solved - bool - T: all items in self.cstate are true (happy pancakes)

        Examples
        --------
        >>> from flipperpuzzle import *
        >>> chal = Challenge(2, '++')
        >>> chal.is_solved()
        True

        """
        if all(self.cstate):
            self.solution = self.nflips
            return True

    def flip_nth(self, nth):
        """
        Flip pancakes where nth pancake is the left most pancake flipped.
        Update self.cstate and self.states accordingly.

        Parameters
        ----------
        nth - int - index of left most pancake to flip

        Examples
        --------
        >>> from flipperpuzzle import *
        >>> chal = Challenge(2, '---')
        >>> chal.flip_nth(1)
        >>> chal.cstate == [False, True, True]
        True
        >>> chal.nflips == 1
        True

        """
        if self.npan - nth < self.flipw:
            # too close to the edge, cannot flip!
            pass
        else:
            for ix, pancake in enumerate(self.cstate[nth:nth+self.flipw]):
                self.cstate[nth+ix] = not pancake
            self.nflips += 1
        self.states.append(self.cstate[:])

    def dumbsolver(self):
        """
        Find the left most unhappy pancake and flip that.
        Repeat until solved or if cstate is a repeat of a previous state

        Examples
        --------
        >>> from flipperpuzzle import *
        >>> chal = Challenge(3, '---')
        >>> chal.dumbsolver()
        >>> chal.solution
        1
        >>> chal = Challenge(3, '--')
        >>> chal.dumbsolver()
        >>> chal.solution == -1
        True

        """
        while self.solution is None:
            if not self.is_solved():
                first = self.cstate.index(False)
                self.flip_nth(first)
                if not self.is_solved() and self.cstate in self.states[:-1]:
                    self.solution = -1

def signs2bool(signs):
    """

    Parameters
    ----------
    signs - str - string of + and - chars

    Returns
    -------
    bools - [bool] - list of bools based on input, +==True, -==False

    Examples
    --------
    >>> from flipperpuzzle import *
    >>> bools = signs2bool('+-+')
    >>> bools == [True, False, True]
    True

    """
    bools = []
    for sign in signs:
        if sign == '+':
            bools.append(True)
        elif sign == '-':
            bools.append(False)
        else:
            print('Ignoring invalid character found in string of signs: %s' % sign)
    return bools

def parse_line(line):
    """
    Parse a line of text describing a challenge, string of +- followed by integer flipper
    width

    Parameters
    ----------
    line - str - string of +- chars, space, integer flipper width

    Returns
    -------
    chal - Challenge Object - challenge object based on line contents

    Examples
    --------
    >>> from flipperpuzzle import *
    >>> chal = parse_line('+-+-+ 3')
    >>> chal.flipw == 3
    True
    >>> len(chal.cstate) == 5
    True
    >>> chal.cstate == [True, False, True, False, True]
    True

    """
    if not line:
        return None
    parts = line.strip().split()
    pancakes = parts[0]
    if not pancakes.count('+') + pancakes.count('-') == len(pancakes):
        print('Invalid character in pancake initial conditions: %s' % pancakes)
        return None
    flipw = parts[1]
    if not flipw.isdigit():
        print('Invalid spatula width "%s" given' % flipw)
    chal = Challenge(int(flipw), pancakes)
    return chal

if __name__ == "__main__":
    numargs = len(sys.argv)
    if numargs == 2:
        if sys.argv[1].lower()=='test':
            doctest.testmod()
        else:
            infile = sys.argv[1].strip()
            chals = []
            with open(infile, 'r') as fid:
                numpuzzles = fid.readline()
                for line in fid.readlines():
                    chal = parse_line(line)
                    chals.append(chal)
            # solve and print solutions
            ix = 0
            for chal in chals:
                ix += 1
                chal.dumbsolver()
                if chal.solution >= 0:
                    sol = chal.nflips
                else:
                    sol = 'IMPOSSIBLE'
                print('Case #%d: %s' % (ix, sol))
