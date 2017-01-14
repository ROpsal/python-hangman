##
#    Author: Richard Opsal
#
#   Purpose: CS2321 - Laboratory exercise.
#            Console version of the the Hangman word guessing game.
#
#      Name: hangman.py
#
#   Started: 2010/03/08
#   Revised: 2010/03/11
##

## from __future__ import print_function
from random import randrange

def wordList(fname = 'dictionaryWords.txt'):
    """Generate list of possible words from the passed file."""
    wordlist = []
    with open(fname, 'r') as fin:
        for word in fin:
            word = word.rstrip() ;
            wordlist.append(word)
    return wordlist


def randWord(wordlist):
    """Return a random word for the passed list.  Remove word from list.
       Returned word is converted to upper case."""
    cwords = 0 if (None == wordlist) else len(wordlist)
    word = None
    if (0 < cwords):
        index  = randrange(cwords)
        word = wordlist.pop(index).upper()
    return word


def wordSplit(word):
    """Split the word into individual letters.  Place these in a list."""
    return list(word)


def letterMatch(letter, alphalist, letterlist, hanglist):
    """Hangman letter test with logic for no retries of prior submitted letters.
       Return True if match, False if no match, or None if invalid letter."""

    ch = letter[0] if (str == type(letter)) and (0 < len(letter)) else None

    fmatch = None
    if (None != ch) and (ch in alphalist):
        fmatch = False
        alphalist.remove(ch)
        for k in range(0, len(letterlist)):
            if ch == letterlist[k]:
                fmatch = True
                hanglist[k] = ch

    return fmatch


def letterMatch_gr(letter, letterlist, hanglist):
    """Hangman letter test with logic for no retries of prior submitted letters.
       Return True if match, False if no match, or None if invalid letter.
       This routine specific for the graphical version of Hangman."""

    ch = letter[0] if (0 < len(letter)) else None
    fvalid = (None != ch) and (ord('A') <= ord(ch) <= ord('Z'))

    fmatch = False
    if fvalid:
        for k in range(0, len(letterlist)):
            if ch == letterlist[k]:
                fmatch = True
                hanglist[k] = ch

    return None if not fvalid else fmatch


def alphaList() :
    """List of upper case letters for comparison."""
    return list(map(chr, range(ord('A'), ord('Z')+1)))


def joinLetterList(hanglist):
    """Form an easy to read string for the passed hanglist."""
    str = ''
    for ch in hanglist:
        str += ch
        str += ' '
    return str.strip()


def game() :
    """Driver routine for Hangman word game."""
    print('Welcome to the Hangman word guessing game.\n')

    # List of words to guess from.
    wordlist = wordList()

    # Formatting strings.
    strsta = '{0},  Wins : {1:>2d} Losses : {2:>2d}'

    fexit = False
    wins  = 0
    losses = 0
    while not fexit:
        print("Type 'Exit' to leave the game, 'New' for a new game.")
        print('Good luck!\n')

        letterlist = wordSplit(randWord(wordlist))
        hanglist   = wordSplit('_' * len(letterlist))
        alphalist  = alphaList()

##      print(letterlist)
##      print(hanglist)
##      print(alphalist)

        fnew = False
        ctries = 6
        while not fnew and not fexit:
            print(joinLetterList(hanglist), '  [Guesses left :', ctries, ']', end='')
            ## guess = raw_input('  Letter : ')
            guess = input('  Letter : ')
            guess = guess.upper()
            fexit = 'EXIT' == guess or 'QUIT' == guess
            fnew  = 'NEW'  == guess
            if fnew:
                losses += 1

            if not fexit and not fnew:
                if (False == letterMatch(guess, alphalist, letterlist, hanglist)):
                    ctries -= 1
                    if (0 == ctries):
                        fnew = True
                        losses += 1
                        print(joinLetterList(letterlist))
                        print(strsta.format('Better luck on the next word!', wins, losses))
                        print()

                elif (letterlist == hanglist):
                    fnew = True
                    wins += 1
                    print(joinLetterList(letterlist))
                    print(strsta.format('Congratulations on your win!', wins, losses))
                    print()


# Written this way so we can use as standalone program or as module.
if __name__=='__main__':
    game()