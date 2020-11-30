import pygame
import invClassHelpers
import equipClassHelpers
import battle_UIClassHelpers
from config import *
import config
from player import Player
from sprites import *
from render import ray_casting
from drawing import Drawing
import health
import activities
import encounter
from character_selection import character_selection
import options_menu
from items import Item
from button import Button
import enemies
from battle import Battle


def GameMain(sc, playername):
    print("i have started the game")
    #If the player is in battle, it will bring up battle UI instead of Inventory
    #global in_battle
    #If the player clicks their inventory while in battle this should be True
    battleInvClicked = False
    exited = 0
    sc = pygame.display.set_mode((display_width, display_height))
    sc_map = pygame.Surface(MINIMAP_RES)

    clock = pygame.time.Clock()
    sprites = Sprites()

    #Initialize Player, Inventory, Equipment, Battle UI
    player = Player(playername)
    inventory = invClassHelpers.Inventory(player.startingItems)
    equipment = equipClassHelpers.Equipment()
    battleUI = battle_UIClassHelpers.BattleUI(player,inventory)
    heldItem = None
    # config.text1.append(player.pos)
    drawing = Drawing(sc, sc_map, None)
    second_screen = pygame.Surface((400, 300))
    second_screen.fill(black)
    healthBar = health.Bar(config.white, config.CHAR_DETAIL_FONT_LARGE, (1285, 500), sc)

    while True:
        mouseX, mouseY = pygame.mouse.get_pos()
        sc.fill(black)
        player.movement()
        walls = ray_casting(player, drawing.textures)
        drawing.background(player.angle)
        drawing.world(walls + [obj.object_locate(player, healthBar) for obj in sprites.list_of_objects])
        sc.blit(second_screen, (0, 0))
        # second_screen.blit(second_screen, (0, config.scroll_y))
        drawing.mini_map(player)
        drawing.ui_elements(player,sc)
        drawing.activities_panel(second_screen)
        healthBar.updateBar()
        equipment.createEquip()
        activities.iterate_over_input(second_screen, 20)

        if encounter.in_battle:
            encounter.enemy_trigger(sc)

        if (battleInvClicked):
            inventory.createInventory()
            if (battleInvClicked):
                Button.check_Hover(inventory.back, sc)
            drawing.blitHeldItem(heldItem, mouseX, mouseY)
            drawing.blitMenuInfoBoxes(inventory, equipment)
            
        else: #The player is in battle
                battleUI.createBattleUI()
                
                #the hover check is what's blitting the actions to the screen each time also
                #battleUI.actions[0] to [3] is the player's moves. [4] is "Open Inventory"
                for button in battleUI.actions:
                    Button.check_Hover(button, sc)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and ( battleInvClicked):
                #If they clicked "Back" in the Inventory
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and inventory.back.rect.collidepoint(pygame.mouse.get_pos()):
                    battleInvClicked = False
                    break

                heldItem, healthBar, player = drawing.inventoryEquipmentUI(inventory, equipment, sc, event.type, event.button, mouseX, mouseY, heldItem, healthBar, player)
                drawing.blitMenuInfoBoxes(inventory, equipment)

                if event.button == 4:
                    config.scroll_y = min(config.scroll_y + 20, 0) #what happens when you scroll is that the activities panel goes
                                                                   #black and then the text are repeated
                                                                   #so you should use the second_screen recursively
                    print('up')
                if event.button == 5:
                    config.scroll_y = max(config.scroll_y - 20, -300)
                    print('down')
                    print(config.scroll_y)

            #If they left-click
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                #If they clicked "Open Inventory" in the Battle UI
                if battleUI.actions[4].rect.collidepoint(pygame.mouse.get_pos()):
                    battleInvClicked = True  

                
        if exited == 1:
            gameDisplay_input = pygame.display.set_mode((config.display_width, config.display_height))
            game_over_text = config.SPOOKY_BIG_FONT.render('Game Over', True, config.red)
            gameDisplay_input.blit(game_over_text,(config.display_width/3, config.display_height/3))
            buttons = [
                Button("Return to Character Selection Screen", config.white, pygame.font.Font("assets/fonts/CHILLER.ttf", 50), (4*config.display_width/5, 4*config.display_height/5), gameDisplay_input)]
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and buttons[0].rect.collidepoint(
                pygame.mouse.get_pos())):
                character_selection(gameDisplay_input)
                # options_menu.options_menu(gameDisplay_input)



            # options_menu.lost(gameDisplay_input)

            # print("You suck")



        pygame.display.flip()
        clock.tick(60)