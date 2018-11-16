import pygame, math

pygame.init()

win = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Plumber")

angle = [pygame.image.load('angl1.png'), pygame.image.load('angl2.png'), pygame.image.load('angl3.png'),
         pygame.image.load('angl4.png')]
straight = [pygame.image.load('str1.png'), pygame.image.load('str2.png')]
starts = pygame.image.load('start.png')
ends = pygame.image.load('end.png')
bg = pygame.image.load('bgrd.png')
clickSound = pygame.mixer.Sound('pop.ogg')
mouseposition = (0, 0)
moves = 0
# points == squares on screenplay with (possible) pipes, points[i] = k == square number i is in order k'th
points = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# isstr[i] == 1 when we have got staright pipe on point i
isstr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# isang[i] == 1 if on point i we have pipe-angle
isang = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# wsp - which picture we are displaying (straight 0-1, angle 0-3) if we are displaying at point by order
# for example : points[4] = 5 with 3 position of angle, points[5] = 0 -> wsp[4] = 3
wsp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
lev = 1

# level1
points1 = [0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 3, 4, 5, 6, 9, 10, 0, 0, 0, 0, 0, 7, 8, 11, 12, 0, 0, 0,
           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
wsp1 = [0, 3, 0, 1, 1, 0, 2, 0, 2, 2, 3, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
isstr1 = [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
isang1 = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
wsptrue1 = [0, 3, 1, 1, 0, 0, 3, 1, 0, 2, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# level2
points2 = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 5, 6, 0, 0, 17, 18, 19, 3, 4, 7, 0, 0, 16, 0, 20, 0, 9, 8, 13,
           14, 15, 0, 0, 0, 10, 11, 12, 0, 0, 0, 0]
wsp2 = [3, 1, 0, 2, 1, 0, 0, 0, 1, 1, 1, 1, 1, 3, 0, 0, 0, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
isstr2 = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1,
          0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
isang2 = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0,
          1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0]
wsptrue2 = [3, 1, 1, 1, 0, 2, 3, 1, 0, 2, 1, 0, 0, 2, 0, 0, 1, 2, 0, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]



def draw_beginning():
    win.blit(bg, (0, 0))
    global points, isstr, isang, moves
    win.blit(starts, (0, 0))
    win.blit(ends, (900, 300))
    i = 0
    while i < 48:
        print(i)
        if isstr[i] == 1:
            win.blit(straight[wsp[points[i]]], (((i % 8)+1) * 100, (i // 8) * 100))
        elif isang[i] == 1:
            win.blit(angle[wsp[points[i]]], (((i % 8)+1) * 100, (i // 8) * 100))
        i = i + 1
    pygame.display.update()
    moves = 1
    print(wsp)


def redraw():
    # p == number of square clicked on
    global wsp
    p = mouseposition[0] // 100 + 8 * (mouseposition[1] // 100) - 1
    # change == number of square in order
    change = points[p]
    if isstr[p] == 1:
        wsp[change] = (wsp[change] + 1) % 2
        x = (mouseposition[0] // 100) * 100
        y = (mouseposition[1] // 100) * 100
        win.blit(straight[wsp[change]], (x, y))
    elif isang[p] == 1:
        wsp[change] = (wsp[change] + 1) % 4
        x = (mouseposition[0] // 100) * 100
        y = (mouseposition[1] // 100) * 100
        win.blit(angle[wsp[change]], (x, y))
    pygame.display.update()
    print(wsp)

def nextlevel():
    global lev, moves
    print("Hurra!")
    lev = 2
    moves = 0


run = True
while run:
    mouseClicked = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONUP:
            clickSound.play()
            mouseposition = event.pos
            mouseClicked = True
            moves = 1

    if moves == 0:
        # for level1
        if lev == 1:
            points = points1
            wsp = wsp1
            isstr = isstr1
            isang = isang1
            wsptrue = wsptrue1
            draw_beginning()
        if lev == 2:
            points = points2
            wsp = wsp2
            isstr = isstr2
            isang = isang2
            wsptrue = wsptrue2
            draw_beginning()

    elif mouseClicked:
        redraw()
        print(wsp)
        k = 0
        for i in range(48):
            if wsp[i] == wsptrue[i]:
                k = k + 1
        if k == 48:
            nextlevel()

pygame.quit()
