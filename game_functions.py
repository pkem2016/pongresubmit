import sys

import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
from ball import Ball


def check_keydown_events(event, ai_settings, screen, paddle1, ai_paddle, bullets):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        # Move the ship to the right.
        paddle1.moving_right = True
    elif event.key == pygame.K_LEFT:
        # Move the ship to the left.
        paddle1.moving_left = True
    elif event.key == pygame.K_a:
        # Move the ai_paddle to the left.
        ai_paddle.moving_left = True
    elif event.key == pygame.K_UP:
        # Move the ai_paddle to the top
        paddle1.moving_up = True
    elif event.key == pygame.K_d:
        # Move the paddle to the right
        ai_paddle.moving_right = True
    elif event.key == pygame.K_DOWN:
        # Move the paddle to the bottom
        paddle1.moving_down = True
    elif event.key == pygame.K_s:
        # Move the paddle to the bottom
        ai_paddle.moving_down = True
    elif event.key == pygame.K_w:
        # Move the paddle to the bottom
        ai_paddle.moving_up = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, paddle1, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet."""
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, paddle, ai_paddle):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        paddle.moving_right = False
    elif event.key == pygame.K_d:
        ai_paddle.moving_right = False
    elif event.key == pygame.K_LEFT:
        paddle.moving_left = False
    elif event.key == pygame.K_a:
        ai_paddle.moving_left = False
    elif event.key == pygame.K_UP:
        paddle.moving_up = False
    elif event.key == pygame.K_DOWN:
        paddle.moving_down = False
    elif event.key == pygame.K_s:
        ai_paddle.moving_down = False
    elif event.key == pygame.K_w:
        ai_paddle.moving_up = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, ai_paddle, aliens, bullets):
    """Respond to key presses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, ai_paddle, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship, ai_paddle)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()
        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)
        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, paddle, ai_paddle,aliens, bullets, play_button, ball):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)

    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    paddle.blitme()
    ai_paddle.blitme()
    ball.blitme()
    # aliens.draw(screen)

    # Draw the score information.
    sb.show_score()

    # Draw a line for the net
    pygame.draw.line(screen, (255, 255, 255), ((ai_settings.screen_width / 2), 0), ((ai_settings.screen_width / 2),
                                                                                    ai_settings.screen_height), 2)

    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship,  aliens, bullets):
    """Update position of bullets and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()

    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    # Check for anu bullets that have hit aliens.
    # If so, get rid of the bullet and the alien.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level.
        bullets.empty()
        ai_settings.increase_speed()

        # Increase level.
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def aiControl(pong_settings, ball, ballDirX, aiPaddle):
    # If ball is moving away from paddle, center bat
    if ballDirX == -1:  # moving left
        if aiPaddle.centerLeft < ball.y:
            aiPaddle.centerLeft += pong_settings.ball_speed + 5  # int here will determine the delay of ai
        elif aiPaddle.centerLeft > ball.y:
            aiPaddle.centerLeft -= pong_settings.ball_speed + 5
        elif aiPaddle.center > ball.x and aiPaddle.rect.left > 0:
            aiPaddle.center -= pong_settings.ball_speed + 20  # int here will determine the delay of ai
        elif aiPaddle.center < ball.x and aiPaddle.rect.right < aiPaddle.pong_settings.screen_width/2:
            aiPaddle.center += pong_settings.ball_speed + 20
    # if ball moving towards bat, track its movement.
    elif ballDirX == 1:  # moving right
        if aiPaddle.centerLeft < ball.y:
            aiPaddle.centerLeft += pong_settings.ball_speed + 5
        else:
            aiPaddle.centerLeft -= pong_settings.ball_speed + 5
    return aiPaddle


def update_ball(pong_settings, ball, paddle1, aiPaddle):
    """Trial"""
    ball.update()
    check_ball_edges(pong_settings, ball)
    # Look for paddle collisions.
    if pygame.Rect.colliderect(ball.rect, paddle1.rect) or pygame.Rect.colliderect(ball.rect, aiPaddle.rect):
        pygame.mixer.Sound.play(ball.ball_hit_paddle)
    if pygame.Rect.colliderect(ball.rect, paddle1.rect2) or pygame.Rect.colliderect(ball.rect, aiPaddle.rect2):
        pygame.mixer.Sound.play(ball.ball_hit_paddle)
    if pygame.Rect.colliderect(ball.rect, paddle1.rect3) or pygame.Rect.colliderect(ball.rect, aiPaddle.rect3):
        pygame.mixer.Sound.play(ball.ball_hit_paddle)


def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """Check if the fleet is at an edge, and then update the position of  all aliens in the fleet"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)


def get_number_aliens_x():
    """Determine the number of aliens that fit in a row."""
    # available_space_x = ai_settings.screen_width - 2 * alien_width
    # number_aliens_x = int(available_space_x / (2 * alien_width))
    number_aliens_x = 1
    return number_aliens_x


def get_number_rows():
    # def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the numver of rows of aliens that fir on the screen."""
    # available_space_y = (ai_settings.screen_height - (3*alien_height) - ship_height)
    # number_rows = int(available_space_y / (2*alien_height))
    number_rows = 1
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row."""
    alien = Alien(ai_settings, screen)
    # alien_width = alien.rect.width
    # alien.x = alien_width + 2 * alien_width * alien_number
    alien.x = (ai_settings.screen_width/2) - 7  # Initial position
    alien.rect.x = alien.x
    # alien.rect.y = alien.rect.height + 2*alien.rect.height * row_number
    alien.rect.y = (ai_settings.screen_height/2) - 7  # Initial position
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):  # deleted ship parameter
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row.
    # Spacing between each alien is equal to one alien width.
    # alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x()
    number_rows = get_number_rows()
    # number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_ball_edges(pong_settings, ball):
    """What to do if we hit an edge"""
    print("hit edge")
    if ball.check_edges():
        change_ball_direction(pong_settings, ball)


def change_ball_direction(pong_settings, ball):
    """Change the ball direction"""
    # if ball is moving as such change the direction when you hit an edge

    pong_settings.ball_direction *= -1

    # if ball.direction == ball.moving_upright and pong_settings.ball_direction == 1 and ball.y == 0:
    #     ball.direction = ball.moving_downright
    #     ball.update()


    # if ball.rect.y < 0 and ball.moving_upleft:
    #     ball.direction = ball.moving_downleft
    #     ball.update()
    # if ball.rect.y < 0 and ball.moving_upright:
    #     ball.direction = ball.moving_downright
    #     ball.update()
    # if ball.rect.y > ball.screen_rect.bottom and ball.moving_upleft:
    #     ball.direction = ball.moving_upleft
    #     ball.update()
    # if ball.rect.y > ball.screen_rect.bottom and ball.moving_downright:
    #     ball.direction = ball.moving_upright
    #     ball.update()
    #pong_settings.ball_direction *= -1


def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


# This makes the ball move
def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    # for alien in aliens.sprites():
    #     alien.rect.y += ai_settings.fleet_drop_speed

    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:
        # Decrement ships_left.
        stats.ships_left -= 1

        # Update scoreboard.
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause.
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


# ball collision
def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break
