import socket
import time
import pygame
import pickle
from bullet import Bullet

SERVER = "192.168.29.71"  # Enter your server host
PORT = 9999
ADDRESS = (SERVER, PORT)

pygame.init()
size = (888, 500)
Screen = pygame.display.set_mode(size)
pygame.display.set_caption("Dino Fight")
icon = pygame.image.load("./dino/icon.png")
pygame.display.set_icon(icon)
p1_walk_rt = [pygame.image.load(f"./dino/Walk ({i}).png") for i in range(1, 11)]
p2_walk_rt = [pygame.image.load(f"./dino2/Walk ({i}).png") for i in range(1, 11)]
p1_walk_lt = [pygame.image.load(f"./dino/LWalk ({i}).png") for i in range(1, 11)]
p2_walk_lt = [pygame.image.load(f"./dino2/LWalk ({i}).png") for i in range(1, 11)]
bkg = pygame.image.load("./dino/bkg.jpg")
p1_idle = [pygame.image.load("./dino/Idle.png"), pygame.image.load("./dino/L_Idle.png")]
p2_idle = [pygame.image.load("./dino2/Idle.png"), pygame.image.load("./dino2/L_Idle.png")]
p1_fireball = [pygame.image.load("./dino/Bullet.png"), pygame.image.load("./dino/LBullet.png")]
p2_fireball = [pygame.image.load("./dino2/Bullet.png"), pygame.image.load("./dino2/LBullet.png")]
menu_icon = pygame.image.load("./dino/Menu.png")
clock = pygame.time.Clock()

main = True
menu = True
waiting_for_player = True
font_of_start_game = pygame.font.SysFont("arial", 50, True)
font_of_quit_game = pygame.font.SysFont("arial", 50, True)
font_of_waiting_for_player = pygame.font.SysFont("arial", 100, True)


def fade():
    fade = pygame.Surface(size)
    fade.fill((0, 0, 0))
    for alpha in range(0, 256, 7):
        fade.set_alpha(alpha)
        Redraw_Screen()
        Screen.blit(fade, (0, 0))
        pygame.display.update()


def player_draw(player, screen):
    if player.walk_count + 1 >= 30:
        player.walk_count = 0

    if not player.standing:
        if player.left:
            if player.id == 1:
                screen.blit(p1_walk_lt[player.walk_count // 3], (player.x, player.y))  # 1 pic for 3 frames
            else:
                screen.blit(p2_walk_lt[player.walk_count // 3], (player.x, player.y))
            player.walk_count += 1
        elif player.right:
            if player.id == 1:
                screen.blit(p1_walk_rt[player.walk_count // 3], (player.x, player.y))
            else:
                screen.blit(p2_walk_rt[player.walk_count // 3], (player.x, player.y))
            player.walk_count += 1
    else:
        if player.id == 1:
            if player.left:
                screen.blit(p1_idle[1], (player.x, player.y))
            else:
                screen.blit(p1_idle[0], (player.x, player.y))
        else:
            if player.right:
                screen.blit(p2_idle[0], (player.x, player.y))
            else:
                screen.blit(p2_idle[1], (player.x, player.y))

    player.hitbox = (player.x + 18, player.y + 3, 40, 65)  # HITBOX HERE FOR DINO
    pygame.draw.rect(screen, (255, 0, 0), (player.hitbox[0] - 10, player.hitbox[1] - 10, 60, 7))  # Red
    if player.health != 0:
        pygame.draw.rect(screen, (0, 200, 0),
                         (player.hitbox[0] - 10, player.hitbox[1] - 10, 60 - (12 * (5 - player.health)),
                          7))  # Green
    pl_name = font_of_player_name.render(player.name[:7], True, (0, 0, 0))
    screen.blit(pl_name, (player.hitbox[0] - 5, player.hitbox[1] - 35))


def bullet_draw(bullet, screen):
    if bullet.facing == 1:
        if bullet.owner_id == 1:
            screen.blit(p1_fireball[0], (bullet.x, bullet.y))
        else:
            screen.blit(p2_fireball[0], (bullet.x, bullet.y))
    else:
        if bullet.owner_id == 1:
            screen.blit(p1_fireball[1], (bullet.x, bullet.y))
        else:
            screen.blit(p2_fireball[1], (bullet.x, bullet.y))


def Redraw_Screen():
    Screen.blit(bkg, (0, 0))
    player_draw(player1, Screen)
    player_draw(player2, Screen)
    for bullet in p1_bullets:
        bullet_draw(bullet, Screen)
    for bullet in p2_bullets:
        bullet_draw(bullet, Screen)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

player1 = pickle.loads(client.recv(2048))

# ||-----MAIN LOOP-----||#

while menu:  # Main Menu
    start_game = font_of_start_game.render("START", True, (255, 255, 255))
    quit_game = font_of_quit_game.render("QUIT", True, (255, 255, 255))
    Screen.fill((255, 255, 255))

    # Start button
    pygame.draw.rect(Screen, (0, 0, 0), (40, 425, 175, 60))
    pygame.draw.rect(Screen, (255, 0, 0), (40, 425, 175, 60), 2)
    Screen.blit(start_game, (60, 425))

    # Quit button
    pygame.draw.rect(Screen, (0, 0, 0), (660, 425, 175, 60))
    pygame.draw.rect(Screen, (255, 0, 0), (660, 425, 175, 60), 2)
    Screen.blit(quit_game, (700, 425))

    Screen.blit(menu_icon, (235, 0))

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            main, waiting_for_player, menu = False, False, False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if 40 <= pos[0] <= 215 and 425 <= pos[1] <= 485:  # Start
                player1.ready_to_play = True
                menu = False

            if 660 <= pos[0] <= 835 and 425 <= pos[1] <= 485:  # Quit
                main, waiting_for_player, menu = False, False, False

    client.send(pickle.dumps(player1))
    player2 = pickle.loads(client.recv(2048))
    pygame.display.update()

while waiting_for_player:
    print("Waiting For Player to Join")
    client.send(pickle.dumps(player1))
    player2 = pickle.loads(client.recv(2048))

    waiting_for_player_font = font_of_waiting_for_player.render("Waiting for Player...", True, (0, 0, 0))
    Screen.fill((255, 255, 255))
    Screen.blit(waiting_for_player_font, (75, 150))

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            main, waiting_for_player = False, False
            player1.is_game_over = True
            client.send(pickle.dumps(player1))
            player2 = pickle.loads(client.recv(2048))

    print(f"Opponent status : {player2.ready_to_play}")
    if player2.ready_to_play:
        waiting_for_player = False

    pygame.display.update()


while main:
    print("Game Started")
    fps = 30
    run = True
    p1_bullets = player1.bullets
    bullet_count = 0
    player1.score = 0
    font_of_player_name = pygame.font.SysFont("arial", 17, True, True)
    font_of_game_over = pygame.font.SysFont("arial", 100, True)

    # Game screen starts here
    while run:
        print("Game Started")

        clock.tick(fps)
        p2_bullets = player2.bullets
        client.send(pickle.dumps(player1))
        player2 = pickle.loads(client.recv(2048))

        Redraw_Screen()

        if not player2.is_connected:
            fade()
            break

        if bullet_count > 0:
            bullet_count += 1  # So we can shoot once per 10 frames(iteration)
        if bullet_count > 10:
            bullet_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run, main = False, False

        if player1.health == 0 or player1.score == 5:
            fade()
            break

        for bullet in p1_bullets:  # width 25px height 20px
            if bullet.y < player2.hitbox[1] + player2.hitbox[3] and bullet.y + 20 > player2.hitbox[1]:
                if bullet.x + 25 > player2.hitbox[0] and bullet.x < player2.hitbox[0] + player2.hitbox[2]:
                    player1.score += 1
                    p1_bullets.remove(bullet)

            if 0 < bullet.x < 888:
                bullet.x += bullet.velocity
            else:
                p1_bullets.remove(bullet)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            run, main = False, False

        # This bullet_count makes to shoot 1 fire ball for 1 loop...
        if keys[pygame.K_SPACE] and bullet_count == 0:
            if player1.left:
                facing = -1
            else:
                facing = 1

            if len(p1_bullets) < 3:
                if facing == 1:
                    p1_bullets.append(Bullet(player1.x + 55, player1.y + 10, facing, player1.id))
                else:
                    p1_bullets.append(Bullet(player1.x - 10, player1.y + 10, facing, player1.id))
            bullet_count = 0.5

        if keys[pygame.K_RIGHT]:
            if player1.x <= 888 - player1.width + 5:
                player1.x += player1.velocity
            player1.right = True
            player1.left = False
            player1.standing = False

        elif keys[pygame.K_LEFT]:
            if player1.x >= 0 - 5:
                player1.x -= player1.velocity
            player1.right = False
            player1.left = True
            player1.standing = False

        else:
            player1.standing = True
            player1.walk_count = 0

        # Should not go up or down while jumping...
        if not (player1.isjumping):
            if keys[pygame.K_UP]:
                player1.isjumping = True
                # This if-else makes the jump facing left also & removes blinking while jump
                if player1.right:
                    player1.left = False
                    pass
                elif player1.left:
                    player1.right = False
                    pass

                player1.walk_count = 0

        else:
            if player1.jump_pos >= -10:
                neg = 1
                if player1.jump_pos < 0:
                    neg = -1
                # Sq.Func to make a jump...You can also use cubic or linear func...
                player1.y -= (player1.jump_pos ** 2) // 2 * neg
                player1.jump_pos -= 2
            else:
                player1.jump_pos = 10
                player1.isjumping = False

        player1.health = 5 - player2.score
        pygame.display.update()

    # Game Over screen starts here
    while run:
        player1.is_game_over = True
        client.send(pickle.dumps(player1))
        player2 = pickle.loads(client.recv(2048))

        if player1.health > (5 - player1.score) or not player2.is_connected:
            game_over = font_of_game_over.render("YOU WON", True, (255, 255, 255))
            Screen.blit(game_over, (200, 150))
        else:
            game_over = font_of_game_over.render("YOU LOSE", True, (255, 255, 255))
            Screen.blit(game_over, (200, 150))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run, main = False, False

        pygame.display.update()
        time.sleep(2)
        run, main = False, False

pygame.quit()
