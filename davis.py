import time
import random
import pygame
import math
import music
from button import Button

pygame.init()


black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
SPOOKY_BIG_FONT = pygame.font.Font("assets/fonts/CHILLER.ttf", 120)
SPOOKY_SMALL_FONT = pygame.font.Font("assets/fonts/CHILLER.ttf", 60)

display_width = 1024
display_height = 768
music_player = music.Music_Player()
music_player.set_volume(1.0)

 
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Davis Hall Escape Simulator 2020')
clock = pygame.time.Clock()

def roundup(x):
    return int(math.ceil(x / 10.0)) * 10

def render_text(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

class Checkbox:
    def __init__(self):
        self.draw()

    def draw(self):
        pygame.draw.circle(gameDisplay, white, (150,150), 75)

def reRenderVol(volDisplay, vol, text):
    volDisplay.text = text
    volDisplay.buttonText()
    gameDisplay.fill(black)
    volDisplay.createButton(gameDisplay)
    vol.createButton(gameDisplay)

def main_menu():

    intro = True
    buttons = [Button("START", white, SPOOKY_SMALL_FONT, ((display_width/2),(display_height/2)), gameDisplay),
    Button("OPTIONS", white, SPOOKY_SMALL_FONT, ((display_width/2),(display_height/1.5)), gameDisplay),
    Button("QUIT", white, SPOOKY_SMALL_FONT, ((display_width/2),(display_height/1.20)), gameDisplay)]
    gameDisplay.fill(black)
    
    TextSurf, TextRect = render_text("Davis Hall", SPOOKY_BIG_FONT, red)
    TextRect.center = ((display_width/2),(display_height/5))
    gameDisplay.blit(TextSurf, TextRect)
    music_player.play_intro()

    while intro:
        
        for event in pygame.event.get():
           
            if (event.type == pygame.QUIT or 
            (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and buttons[2].rect.collidepoint(pygame.mouse.get_pos()))):
                pygame.quit()
                quit()
            
            elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and buttons[1].rect.collidepoint(pygame.mouse.get_pos())):
                music_player.stop()
                options_menu()
                
                
        for button in buttons:
            Button.check_Hover(button, gameDisplay)

        pygame.display.update()
        clock.tick(15)

def options_menu():
    music_player = music.Music_Player()
    music_player.play_normal()

    gameDisplay.fill(black)
    #buttons = [Button("BACK", white, SPOOKY_SMALL_FONT, (0,0))]
    current_volume = music_player.get_volume()
    volumeDisplay = Button(str(roundup(math.trunc(current_volume * 100))), white, SPOOKY_SMALL_FONT, (display_width/2,display_height/2),gameDisplay)
    volume = Button("VOLUME", white, SPOOKY_SMALL_FONT, (volumeDisplay.pos[0] - 200, volumeDisplay.pos[1]),gameDisplay)

    buttons =[Button("BACK", white, pygame.font.Font("assets/fonts/CHILLER.ttf", 70), (90, 60), gameDisplay),
    Button("<", white, SPOOKY_SMALL_FONT, (display_width/2-80,display_height/2), gameDisplay),
    Button(">", white, SPOOKY_SMALL_FONT, (display_width/2+80,display_height/2), gameDisplay),
    Button("MUTE", white, SPOOKY_SMALL_FONT, (display_width/2,display_height/2+100), gameDisplay) ]


    backButton = Button("BACK", white, pygame.font.Font("assets/fonts/CHILLER.ttf", 70), (90, 60), gameDisplay)
    
    while True :
        
        for event in pygame.event.get():
            print(event)
            if (event.type == pygame.QUIT) :
                pygame.quit()
                quit()

            elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and buttons[0].rect.collidepoint(pygame.mouse.get_pos())):
                main_menu()

            elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and buttons[1].rect.collidepoint(pygame.mouse.get_pos())):
                if (buttons[3].text != "UNMUTE"):
                    music_player.set_volume(current_volume - 0.10)
                
                # Subtracting two floats isn't exact so multiply by 100 then truncate
                if (math.trunc(current_volume*100) > 0):
                    current_volume -= 0.10

                #Need to re-render button
                reRenderVol(volumeDisplay, volume, str(roundup(math.trunc(current_volume*100))))

            elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and buttons[2].rect.collidepoint(pygame.mouse.get_pos())):
                if (buttons[3].text != "UNMUTE" and current_volume <= 100):
                    music_player.set_volume(current_volume + 0.10)
                if (math.trunc(current_volume*100) < 100):
                    current_volume += 0.10

                reRenderVol(volumeDisplay, volume, str(roundup(math.trunc(current_volume*100))))

            elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and buttons[3].text == "MUTE" and buttons[3].rect.collidepoint(pygame.mouse.get_pos())):
                music_player.set_volume(0.0)
                buttons[3].text = "UNMUTE"
                reRenderVol(volumeDisplay, volume, str(roundup(math.trunc(current_volume*100))))

            elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and buttons[3].text == "UNMUTE" and buttons[3].rect.collidepoint(pygame.mouse.get_pos())):
                music_player.set_volume(current_volume)
                buttons[3].text = "MUTE"
                reRenderVol(volumeDisplay, volume, str(roundup(math.trunc(current_volume*100))))


        for button in buttons:
            Button.check_Hover(button, gameDisplay)

        pygame.display.update()
        clock.tick(15)

main_menu()


quit()