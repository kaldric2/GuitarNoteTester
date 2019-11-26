# Guitar Note Tester
#     a Pygame app designed to help a guitar player learn to find the position of staff notes on a fretboard
#     created by Kevin Aldrich on July 22, 2014
#

import pygame
from pygame.locals import *

import math
import numpy
import random
import time
import pdb

# by Timothy Downs, inputbox written for my map editor
# http://www.pygame.org/pcr/inputbox/

# This program needs a little cleaning up
# It ignores the shift key
# And, for reasons of my own, this program converts "-" to "_"

# A program to get user input, allowing backspace etc
# shown in a box in the middle of the screen
# Called by:
# import inputbox
# answer = inputbox.ask(screen, "Your name")
#
# Only near the center of the screen is blitted to

import pygame, pygame.font, pygame.event, pygame.draw, pygame.mixer, string
from pygame.locals import *

def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key
    else:
      pass

def display_box(screen, message):
  "Print a message in a box in the middle of the screen"
  fontobject = pygame.font.Font(None,36)
  pygame.draw.rect(screen, (255,255,255),
                   ((screen.get_width() / 2) - 250,
                    (screen.get_height() / 2) - 20,
                    500,40), 0)
  pygame.draw.rect(screen, (255,255,255),
                   ((screen.get_width() / 2) - 255,
                    (screen.get_height() / 2) - 24,
                    510,48), 1)
  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, (0,0,0)),
                ((screen.get_width() / 2) - 250, (screen.get_height() / 2) - 25))
  pygame.display.flip()

def ask(screen, question):
  "ask(screen, question) -> answer"
  pygame.font.init()
  current_string = []
  display_box(screen, question + ": " + "".join(current_string))
  while 1:
    inkey = get_key()
    if inkey == K_BACKSPACE:
      current_string = current_string[0:-1]
    elif inkey == K_RETURN:
      break
    elif inkey == K_MINUS:
      current_string.append("_")
    elif inkey <= 127:
      current_string.append(chr(inkey))
    display_box(screen, question + ": " + "".join(current_string))
  return "".join(current_string)

# end inputbox code by Timothy Downs

def showNote(selNote, i, endNum, background, screen):
    selNotePath = "/Users/kaldrich/Documents/Files/Development/Python/GuitarNoteTester/NoteImages/" + selNote + ".png"
    selTrackPath = "/Users/kaldrich/Documents/Files/Development/Python/GuitarNoteTester/NoteTracks/" + selNote + ".ogg"

    # Display progress text
    font = pygame.font.Font(None, 20)
    progressText = font.render(str(i + 1) + " of " + str(endNum), 1, (10, 10, 10))
    progressTextPos = progressText.get_rect()
    progressTextPos.topright = (background.get_rect().topright[0] - 10, background.get_rect().topright[1] + 10)

    # Display note image
    imgNote = pygame.image.load(selNotePath)
    imgNote_rect = imgNote.get_rect()

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    screen.blit(imgNote, (background.get_rect().centerx - imgNote_rect.width / 2, 100))
    screen.blit(progressText, progressTextPos)
    pygame.display.flip()

    #play tone
    pygame.mixer.music.load(selTrackPath)
    #pygame.mixer.music.load('/Users/kaldrich/Documents/Files/Development/Python/GuitarNoteTester/NoteTracks/A#2.ogg')
    pygame.mixer.music.play()

    return imgNote


def showAnswer(imgNote, selNote, background, screen):
    imgNote_rect = imgNote.get_rect()
    selFretPath = "/Users/kaldrich/Documents/Files/Development/Python/GuitarNoteTester/FretboardImages/" + selNote + ".png"

    # Display note name
    font = pygame.font.Font(None, 36)
    text = font.render(selNote, 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    textpos.centery = background.get_rect().centery

    # Display fretboard image
    imgFret = pygame.image.load(selFretPath)
    imgFret_rect = imgFret.get_rect()

    screen.blit(text, textpos)
    screen.blit(imgFret, (background.get_rect().centerx - imgFret_rect.width / 2, background.get_rect().centery + textpos.height + 30))
    pygame.display.update([textpos, imgFret_rect])


def main():
    random.seed()

    noteNames = ["E2","F2","F#2","Gb2","G2","G#2","Ab2","A2","A#2","Bb2","B2","C3","C#3","Db3","D3","D#3","Eb3",
                 "E3","F3","F#3","Gb3","G3","G#3","Ab3","A3","A#3","Bb3","B3","C4","C#4","Db4","D4","D#4","Eb4",
                 "E4","F4","F#4","Gb4","G4","G#4","Ab4","A4","A#4","Bb4","B4","C5","C#5","Db5","D5","D#5","Eb5",
                 "E5"]

    noteFrequencies = [82.407,87.31,92.50,92.50,98.00,103.83,103.83,110.00,116.54,116.54,123.47,130.81,138.59,138.59,146.83,155.56,155.56,
                       164.81,174.61,185.00,185.00,196.00,207.65,207.65,220.00,233.08,233.08,246.94,261.63,277.18,277.18,293.67,311.13,311.13,
                       329.63,349.23,369.99,369.99,392.00,415.30,415.30,440,466.16,466.16,493.88,523.25,554.37,554.37,587.33,622.25,622.25,
                       659.26]

    size = (1366, 720)

    bits = 16

    pygame.init()
    screen = pygame.display.set_mode(size, pygame.SWSURFACE)

    # Initialise screen
    screen.fill((255, 255, 255))
    pygame.display.set_caption('Guitar Note Testing')

    endNum = int(ask(screen,"Enter the number of questions"))
    screen.fill((255, 255, 255))
    pygame.display.flip()
    sleepTime = int(ask(screen,"Enter the seconds between questions"))

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))

    pygame.mixer.init()

    i = 0
    selNote = ""
    selFreq = ""
    imgNote = ""

    #This will keep the sound playing forever, the quit event handling allows the pygame window to close without crashing
    _running = True
    while _running:
        # 1. show the note name
        # 2. show the note on the staff
        # 3. play the note
        # 4. wait X seconds
        # 5. show the note on the fretboard
        # 6. increment X

        #loop for note testing
        if i == endNum * sleepTime:
            _running = False
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _running = False
                break

        # letter = [(0,0,0), (50,50,50), (100,100,100), (150,150,150), (200,200,200), (255, 255, 255)]
        # screen.fill(letter[i % 6])
        # pygame.display.flip()
        # pygame.time.wait(sleepTime * 1000)

        clock = pygame.time.Clock()
        clock.tick(1)
        # pygame.display.flip()
        # pygame.time.wait(1000)

        if (i % sleepTime) == 0:
            screen.fill((255, 255, 255))
            randNum = random.randint(0, len(noteNames)-1)
            selNote = noteNames[randNum]
            selFreq = noteFrequencies[randNum]
            imgNote = showNote(selNote, math.floor(i / endNum), endNum, background, screen)

        if sleepTime > 3:
            if (i % sleepTime) >= (sleepTime - 3):
                showAnswer(imgNote, selNote, background, screen)
        elif (sleepTime <= 3 and sleepTime >= 2):
            if (i % sleepTime) >= (sleepTime - 2):
                showAnswer(imgNote, selNote, background, screen)
        else:
            showAnswer(imgNote, selNote, background, screen)

        pygame.mixer.stop()

        i += 1

    pygame.quit()

if __name__ == "__main__":
    # call your code here
    main()
