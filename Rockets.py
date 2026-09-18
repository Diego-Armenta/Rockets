import pygame as p

def main():
    p.init()
    screen = p.display.set_mode((800, 600))
    clock = p.time.Clock()
    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
        screen.fill((255, 255, 255))
        p.draw.rect(screen,(240,0,0),(100,100,200,100))
        p.display.flip()
    p.quit()

main()
