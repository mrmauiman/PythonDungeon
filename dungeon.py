#Maui Kelley, Ryan Tigner  12/9/2016
#Ver. 0.2.1
#Controls:
#'W', 'A', 'S', 'D' to move
#'space' to interact, use sword, and close menus
#'m' to open the map
#'p' to open the inventory

import graphics
import sprite
import random

#PRE: hero is the character, entrance is the direction hero came from, room is the new room to generate, controller is a sprite variable that holds many mutable variables
#POST: generates the room
def generate_room(hero, entrance, room, controller):
    if entrance == 'up':
        hero.x = graphics.window_width()/2
        hero.y = tile_size * 2.6
    elif entrance == 'left':
        hero.x = tile_size * 2.6
        hero.y = graphics.window_height()/2
    elif entrance == 'down':
        hero.x = graphics.window_width()/2
        hero.y = graphics.window_height() - (tile_size * 2.6)
    elif entrance == 'right':
        hero.x = graphics.window_width() - (tile_size * 2.6)
        hero.y = graphics.window_height()/2
    elif entrance == 'pit':
        hero.x = graphics.window_width()/2
        hero.y = graphics.window_height()/2
    else:
        hero.x = graphics.window_width()/2
        hero.y = graphics.window_height()/2 + (tile_size*4)

    lock_loc = 0
    if entrance == 'up':
        lock_loc = 0
    elif entrance == 'left':
        lock_loc = 1
    elif entrance == 'down':
        lock_loc = 2
    elif entrance == 'right':
        lock_loc = 3

    if controller.room[controller.current_room[0]][controller.current_room[1]][controller.current_room[2]][2][lock_loc] == True:
        controller.room[controller.current_room[0]][controller.current_room[1]][controller.current_room[2]][2][lock_loc] = False
        
    if controller.room[controller.current_room[0]][controller.current_room[1]][controller.current_room[2]][3][lock_loc] == True:
        controller.room[controller.current_room[0]][controller.current_room[1]][controller.current_room[2]][3][lock_loc] = False
        
    if controller.room[controller.current_room[0]][controller.current_room[1]][controller.current_room[2]][6][lock_loc] == True:
        controller.room[controller.current_room[0]][controller.current_room[1]][controller.current_room[2]][6][lock_loc] = False


    #item Gen
    if len(controller.item_list) > 0:
        controller.item_list = []
    if room[0] != 'none' and room[0] != 'boss':
        item_x = random.randrange(tile_size * 2.5, graphics.window_width() - (tile_size * 2.5))
        item_y = random.randrange(tile_size * 2.5, graphics.window_height() - (tile_size * 2.5))
        controller.item_list.append(sprite.Sprite(item_x, item_y, room[0] + '.gif'))

    
    #lock Gen
    if len(controller.lock_list) > 0:
        controller.lock_list = []
    if room[2] != holes['No']:
        if room[2][0]:
            controller.lock_list.append(sprite.Sprite(graphics.window_width()/2, (tile_size), 'lock_up.gif'))
        if room[2][1]:
            controller.lock_list.append(sprite.Sprite((tile_size), graphics.window_height()/2, 'lock_left.gif'))
        if room[2][2]:
            controller.lock_list.append(sprite.Sprite(graphics.window_width()/2, graphics.window_height() - (tile_size), 'lock_down.gif'))
        if room[2][3]:
            controller.lock_list.append(sprite.Sprite(graphics.window_width() - (tile_size), graphics.window_height()/2, 'lock_right.gif'))

        
    if room[3] != holes['No']:
        if room[3][0]:
            controller.lock_list.append(sprite.Sprite(graphics.window_width()/2, tile_size, 'boss_lock_up.gif'))
        if room[3][1]:
            controller.lock_list.append(sprite.Sprite(tile_size, graphics.window_height()/2, 'boss_lock_left.gif'))
        if room[3][2]:
            controller.lock_list.append(sprite.Sprite(graphics.window_width()/2, graphics.window_height() - (tile_size), 'boss_lock_down.gif'))
        if room[3][3]:
            controller.lock_list.append(sprite.Sprite(graphics.window_width() - (tile_size), graphics.window_height()/2, 'boss_lock_right.gif'))
        
    if room[6] != holes['No']:
        if room[6][0]:
            controller.lock_list.append(sprite.Sprite(graphics.window_width()/2, tile_size, 'switch_lock_up.gif'))
        if room[6][1]:
            controller.lock_list.append(sprite.Sprite(tile_size, graphics.window_height()/2, 'switch_lock_left.gif'))
        if room[6][2]:
            controller.lock_list.append(sprite.Sprite(graphics.window_width()/2, graphics.window_height() - (tile_size), 'switch_lock_down.gif'))
        if room[6][3]:
            controller.lock_list.append(sprite.Sprite(graphics.window_width() - (tile_size), graphics.window_height()/2, 'switch_lock_right.gif'))

    #stairs Gen
    if len(controller.stairs_list) > 0:
        controller.stairs_list = []
    if controller.room[controller.current_room[0]][controller.current_room[1]][controller.current_room[2]][5] == 'UP':
        stairs = sprite.Sprite(graphics.window_width()/2, graphics.window_height()/2, 'stairs_up.gif')
        stairs.og_name = stairs.image_name
        controller.stairs_list.append(stairs)
    elif controller.room[controller.current_room[0]][controller.current_room[1]][controller.current_room[2]][5] == 'DOWN':
        stairs = sprite.Sprite(graphics.window_width()/2, graphics.window_height()/2, 'stairs_down.gif')
        stairs.og_name = stairs.image_name
        controller.stairs_list.append(stairs)
    elif controller.room[controller.current_room[0]][controller.current_room[1]][controller.current_room[2]][5] == 'ITEM_UP':
        fan = sprite.Sprite(graphics.window_width()/2, graphics.window_height()/2, 'fan_1.gif')
        fan.frame = 0
        fan.sprites = ['fan_1.gif', 'fan_2.gif']
        fan.og_name = fan.image_name
        controller.stairs_list.append(fan)
    elif controller.room[controller.current_room[0]][controller.current_room[1]][controller.current_room[2]][5] == 'ITEM_DOWN':
        pit = sprite.Sprite(graphics.window_width()/2, graphics.window_height()/2, 'pit.gif')
        pit.og_name = pit.image_name
        controller.stairs_list.append(pit)
        

    #Enemy Gen
    if len(controller.enemy_list) > 0:
        controller.enemy_list = []
    for i in room[1]:
        enemy = sprite.Sprite(0, 0, i)
        enemy.x = random.randrange(tile_size * 8, graphics.window_width()-(tile_size * 8))
        enemy.y = random.randrange(tile_size * 8, graphics.window_height()-(tile_size * 8))
        enemy.x_speed = 3 * random.randrange(-1, 2, 2)
        enemy.y_speed = 3 * random.randrange(-1, 2, 2)
        enemy.sprite_list = ['none']
        enemy.og_name = enemy.image_name
        enemy.direction = 0
        enemy.frame = 0
        if enemy.image_name == 'enemy_1.gif':
            enemy.x_speed = 2 * random.randrange(-1, 2, 2)
            enemy.y_speed = 2 * random.randrange(-1, 2, 2)
        if enemy.image_name == 'enemy_2.gif':
            enemy.x_speed = 0
            enemy.y_speed = 0
            enemy.speed = 12
            enemy.jumping = False
            enemy.x_dist = 0
            enemy.y_dist = 0
            enemy.dest_x = 0
            enemy.dest_y = 0
        if enemy.image_name == 'enemy_3_up_1.gif':
            enemy.sprite_list = [['enemy_3_up_1.gif', 'enemy_3_up_2.gif'], ['enemy_3_left_1.gif', 'enemy_3_left_2.gif'], ['enemy_3_down_1.gif', 'enemy_3_down_2.gif'], ['enemy_3_right_1.gif', 'enemy_3_right_2.gif']]
            enemy.x_speed = 3 * random.randrange(-1, 2, 1)
            if enemy.x_speed == 0:
                enemy.y_speed = 3 * random.randrange(-1, 2, 2)
            else:
                enemy.y_speed = 0
        if enemy.image_name == 'enemy_4_up_1.gif':
            enemy.sprite_list = [['enemy_4_up_1.gif', 'enemy_4_up_2.gif'], ['enemy_4_left_1.gif', 'enemy_4_left_2.gif'], ['enemy_4_right_1.gif', 'enemy_4_right_2.gif']]
            enemy.firing = 0
        if enemy.image_name == 'enemy_5_up_1.gif':
            enemy.sprite_list = [['enemy_5_up_1.gif', 'enemy_5_up_2.gif'], ['enemy_5_left_1.gif', 'enemy_5_left_2.gif'], ['enemy_5_down_1.gif', 'enemy_5_down_2.gif'], ['enemy_5_right_1.gif', 'enemy_5_right_2.gif']]
            enemy.x_speed = 3 * random.randrange(-1, 2, 1)
            if enemy.x_speed == 0:
                enemy.y_speed = 3 * random.randrange(-1, 2, 2)
            else:
                enemy.y_speed = 0
        controller.enemy_list.append(enemy)



    #Boss Gen
    if len(controller.boss_list) > 0:
        controller.boss_list = []
    if room[0] == 'boss':
        boss = sprite.Sprite(graphics.window_width()/2, tile_size * 4, 'boss_1.gif')
        boss.x_speed = 2
        boss.frame = 0
        boss.health = 20
        boss.damage = 0
        controller.boss_list.append(boss)

    #room variables
    controller.up = room[4][0]
    controller.left = room[4][1]
    controller.down = room[4][2]
    controller.right = room[4][3]

    if not room[7]:
        room[7] = True

#PRE: hero is the character
#POST: returns what entrance to the next room you are at
def check_door(hero):
    if hero.y <= (tile_size * 2.5) and controller.up:
        if hero.x > (graphics.window_width()/2) - (tile_size*1.5):
            if hero.x < (graphics.window_width()/2) + (tile_size*1.5):
                if hero.direction == 0:
                    return 'down'
    elif hero.x <= (tile_size * 2.5) and controller.left:
        if hero.y > (graphics.window_height()/2) - (tile_size*1.5):
            if hero.y < (graphics.window_height()/2) + (tile_size*1.5):
                if hero.direction == 1:
                    return 'right'
    elif hero.y >= graphics.window_height() - (tile_size * 2.5) and controller.down:
        if hero.x > (graphics.window_width()/2) - (tile_size*1.5):
            if hero.x < (graphics.window_width()/2) + (tile_size*1.5):
                if hero.direction == 2:
                    return 'up'
    elif hero.x >= graphics.window_width() - (tile_size * 2.5) and controller.right:
        if hero.y > (graphics.window_height()/2) - (tile_size*1.5):
            if hero.y < (graphics.window_height()/2) + (tile_size*1.5):
                if hero.direction == 3:
                    return 'left'
    return 'none'

#PRE: controller is a sprite variable that holds many mutable variables, entrance is the entance to the next room you are at
#POST: returns the next room 
def find_room(controller, entrance):
    if entrance == 'down':
        controller.current_room[2] -= 1
        #print(controller.current_room)
        return controller.room[controller.current_room[0]][controller.current_room[1]][controller.current_room[2]]
    elif entrance == 'right':
        controller.current_room[1] -= 1
        #print(controller.current_room)
        return controller.room[controller.current_room[0]][controller.current_room[1]][controller.current_room[2]]
    elif entrance == 'up':
        controller.current_room[2] += 1
        #print(controller.current_room)
        return controller.room[controller.current_room[0]][controller.current_room[1]][controller.current_room[2]]
    elif entrance == 'left':
        controller.current_room[1] += 1
        #print(controller.current_room)
        return controller.room[controller.current_room[0]][controller.current_room[1]][controller.current_room[2]]
    elif entrance == 'stairs_up' or entrance == 'fan':
        controller.current_room[0] += 1
        return controller.room[controller.current_room[0]][controller.current_room[1]][controller.current_room[2]]
    elif entrance == 'stairs_down' or entrance == 'pit':
        controller.current_room[0] -= 1
        return controller.room[controller.current_room[0]][controller.current_room[1]][controller.current_room[2]]

#PRE: hero is the character, controller is a sprite variable that holds many mutable variables
#POST: updates the hero sprite
def update_hero(hero, controller):
    #Because you can't stab and move to make game feel more retro lol
    if not hero.stabbing:
        #Movement
        hero.x_speed = 0
        hero.y_speed = 0

        if hero.y >= (tile_size * 2.5) and hero.x >= (tile_size * 2.5) and hero.y <= graphics.window_height() - (tile_size * 2.5) and hero.x <= graphics.window_width() - (tile_size * 2.5):
            new_order = [controls[controls.index(hero.last_pressed)]] + controls[:controls.index(hero.last_pressed)] + controls[controls.index(hero.last_pressed) + 1:]
            for i in new_order:
                if graphics.key_down(i):
                    if i == controls[0]:
                        hero.x_speed = 0
                        hero.y_speed = -4
                        hero.direction = 0
                        if graphics.key_up(hero.last_pressed):
                            hero.last_pressed = controls[0]
                        hero.moving = True
                    if i == controls[1]:
                        hero.x_speed = -4
                        hero.y_speed = 0
                        hero.direction = 1
                        if graphics.key_up(hero.last_pressed):
                            hero.last_pressed = controls[1]
                        hero.moving = True
                    if i == controls[2]:
                        hero.x_speed = 0
                        hero.y_speed = 4
                        hero.direction = 2
                        if graphics.key_up(hero.last_pressed):
                            hero.last_pressed = controls[2]
                        hero.moving = True
                    if i == controls[3]:
                        hero.x_speed = 4
                        hero.y_speed = 0
                        hero.direction = 3
                        if graphics.key_up(hero.last_pressed):
                            hero.last_pressed = controls[3]
                        hero.moving = True
                        
        if hero.y <= (tile_size * 2.5):
            hero.y = tile_size * 2.5
        if hero.x <= (tile_size * 2.5):
            hero.x = tile_size * 2.5
        if hero.y >= graphics.window_height() - (tile_size * 2.5):
            hero.y = graphics.window_height() - (tile_size * 2.5)
        if hero.x >= graphics.window_width() - (tile_size * 2.5):
            hero.x = graphics.window_width() - (tile_size * 2.5)
        
        if hero.x + hero.x_speed >= (tile_size * 2.5) and hero.x + hero.x_speed <= graphics.window_width() - (tile_size * 2.5):
            hero.x += hero.x_speed
        else:
            if hero.direction == 1:
                diff = hero.x - (tile_size * 2.5)
            else:
                diff = graphics.window_width() - (hero.x + (tile_size * 2.5))
            hero.x += (diff/abs(hero.x_speed))*hero.x_speed
        if hero.y + hero.y_speed >= (tile_size * 2.5) and hero.y + hero.y_speed <= graphics.window_height() - (tile_size * 2.5):
            hero.y += hero.y_speed
        else:
            if hero.direction == 0:
                diff = hero.y - (tile_size * 2.5)
            else:
                diff = graphics.window_height() - (hero.y + (tile_size * 2.5))
            hero.y += (diff/abs(hero.y_speed))*hero.y_speed

        count = 0
        for i in range(len(controls)-1):
            if not graphics.key_down(controls[i]):
                count += 1
            if count == 4:
                hero.moving = False

        
        #animating hero
        speed = 4
        if hero.moving:
            hero.frame += 1
            if hero.frame == len(hero.walking_sprites[hero.direction]) * speed:
                hero.frame = 0
            if hero.frame % speed == 0:
                hero.image_name = hero.walking_sprites[hero.direction][hero.frame // speed]

    #Collision with items
    for i in range(len(controller.item_list)-1, -1, -1):
        if hero.collides(controller.item_list[i]):
            temp = controller.item_list[i].image_name 
            if temp == 'chest.gif':
                prize = loot[random.randrange(2)]
                if prize == 'gold':
                    hero.gold += 500
                elif prize == 'health':
                    hero.hp += 2
                    if hero.hp > maxHP:
                        hero.hp = maxHP
                controller.room[controller.current_room[0]][controller.current_room[1]][controller.current_room[2]][0] = 'none'
            elif temp == 'leaf.gif':
                hero.item = True
                controller.room[controller.current_room[0]][controller.current_room[1]][controller.current_room[2]][0] = 'none'
            else:
                hero.keys.append(temp[:temp.find('.')])
                controller.room[controller.current_room[0]][controller.current_room[1]][controller.current_room[2]][0] = 'none'
            del controller.item_list[i]

    #Collision with locks
    for i in range(len(controller.lock_list)-1, -1, -1):
        if hero.collides(controller.lock_list[i]):
            if len(hero.keys) > 0 and graphics.key_down(controls[4]):
                lock_x = controller.lock_list[i].x
                lock_y = controller.lock_list[i].y
                lock_images = ['lock_up.gif', 'lock_left.gif', 'lock_down.gif', 'lock_right.gif']
                boss_lock_images = ['boss_lock_up.gif', 'boss_lock_left.gif', 'boss_lock_down.gif', 'boss_lock_right.gif']
                switch_lock_images = ['switch_lock_up.gif', 'switch_lock_left.gif', 'switch_lock_down.gif', 'switch_lock_right.gif']
                lock_image = 0
                lock_loc = 0
                correct_key = False

                #Remove lock from current room 
                if lock_y == tile_size:
                    lock_loc = 0
                elif lock_x == tile_size:
                    lock_loc = 1
                elif lock_y == graphics.window_height() - (tile_size):
                    lock_loc = 2
                else:
                    lock_loc = 3

                if controller.lock_list[i].image_name in lock_images and 'key' in hero.keys:
                    lock_image = 2
                    correct_key = True
                elif controller.lock_list[i].image_name in boss_lock_images and 'boss_key' in hero.keys:
                    lock_image = 3
                    correct_key = True
                elif controller.lock_list[i].image_name in switch_lock_images and 'a_switch' in hero.keys:
                    if 'b_switch' in hero.keys:
                        lock_image = 6
                        correct_key = True
                if correct_key:   
                    controller.room[controller.current_room[0]][controller.current_room[1]][controller.current_room[2]][lock_image][lock_loc] = False
                    del controller.lock_list[i]
                    if lock_image == 2:
                        del(hero.keys[hero.keys.index('key')])
                    if lock_image == 3:
                        del(hero.keys[hero.keys.index('boss_key')])
                    if lock_image == 6:
                        del(hero.keys[hero.keys.index('a_switch')])
                        del(hero.keys[hero.keys.index('b_switch')])
                else:
                    hero.uncollide(controller.lock_list[i])
                
            else:
                hero.uncollide(controller.lock_list[i])

    #Collision with stairs
    for i in range(len(controller.stairs_list)-1, -1, -1):
        if (hero.collides(controller.stairs_list[i])):
            if controller.stairs_list[i].image_name == 'stairs_up.gif' or controller.stairs_list[i].image_name == 'stairs_down.gif':
                hero.uncollide(controller.stairs_list[i])
                if graphics.key_down(controls[4]):
                    if hero.y <= graphics.window_height()/2 + (tile_size*4) and hero.y > graphics.window_height()/2:
                        if hero.x > (graphics.window_width()/2) - (tile_size*1.5):
                            if hero.x < (graphics.window_width()/2) + (tile_size*1.5):
                                direction = controller.stairs_list[i].image_name
                                direction = direction[:direction.find('.')]
                                del(controller.stairs_list[i])
                                graphics.clear()
                                graphics.draw_image('Black.gif', graphics.window_width()/2, graphics.window_height()/2)
                                graphics.wait()
                            
                                generate_room(hero, direction, find_room(controller, direction), controller)
            elif controller.stairs_list[i].og_name == 'fan_1.gif':
                if graphics.key_down(controls[4]) and hero.item == True:
                    direction = controller.stairs_list[i].image_name
                    direction = direction[:direction.find('_')]
                    del(controller.stairs_list[i])
                    graphics.clear()
                    graphics.draw_image('Black.gif', graphics.window_width()/2, graphics.window_height()/2)
                    graphics.wait()
                    
                    generate_room(hero, direction, find_room(controller, direction), controller)
            else:
                direction = controller.stairs_list[i].image_name
                direction = direction[:direction.find('.')]
                del(controller.stairs_list[i])
                graphics.clear()
                graphics.draw_image('Black.gif', graphics.window_width()/2, graphics.window_height()/2)
                graphics.wait()
                
                generate_room(hero, direction, find_room(controller, direction), controller)

        #Animate Fan
        if controller.stairs_list[i].og_name == 'fan_1.gif':
            fan = controller.stairs_list[i]
            speed = 4
            fan.frame += 1
            if fan.frame == len(fan.sprites) * speed:
                fan.frame = 0
            if fan.frame % speed == 0:
                fan.image_name = fan.sprites[fan.frame//speed]
                    
    
    #Moveing to the next room
    check = check_door(hero)
    if (check != 'none' and graphics.key_down(controls[4])):
        graphics.clear()
        graphics.draw_image('Black.gif', graphics.window_width()/2, graphics.window_height()/2)
        graphics.wait()
            
        generate_room(hero, check, find_room(controller, check), controller)

    #sword
    if graphics.key_down(controls[4]) and hero.sword_list == [] and not hero.recharge:
        if hero.direction == 0:
            sword = sprite.Sprite(hero.x, hero.y - ((tile_size/2) + (graphics.image_height(hero.sword_sprite_list[hero.direction]))/2), hero.sword_sprite_list[hero.direction])
        elif hero.direction == 1:
            sword = sprite.Sprite(hero.x - ((tile_size/2) + (graphics.image_width(hero.sword_sprite_list[hero.direction]))/2), hero.y, hero.sword_sprite_list[hero.direction])
        elif hero.direction == 2:
            sword = sprite.Sprite(hero.x, hero.y + ((tile_size/2) + (graphics.image_height(hero.sword_sprite_list[hero.direction]))/2), hero.sword_sprite_list[hero.direction])
        else:
            sword = sprite.Sprite(hero.x + ((tile_size/2) + (graphics.image_width(hero.sword_sprite_list[hero.direction]))/2), hero.y, hero.sword_sprite_list[hero.direction])
        sword.life = 10
        hero.stabbing = True
        hero.image_name = hero.attack_sprites[hero.direction]
        hero.sword_list.append(sword)

    for i in range(len(hero.sword_list)-1, -1, -1):
        sword = hero.sword_list[i]
        
        if hero.direction == 0:
            sword.x = hero.x
            sword.y = hero.y - ((tile_size/2) + (graphics.image_height(hero.sword_sprite_list[hero.direction]))/2)
        elif hero.direction == 1:
            sword.x = hero.x - ((tile_size/2) + (graphics.image_width(hero.sword_sprite_list[hero.direction]))/2)
            sword.y = hero.y
        elif hero.direction == 2:
            sword.x = hero.x
            sword.y = hero.y + ((tile_size/2) + (graphics.image_height(hero.sword_sprite_list[hero.direction]))/2)
        else:
            sword.x = hero.x + ((tile_size/2) + (graphics.image_width(hero.sword_sprite_list[hero.direction]))/2)
            sword.y = hero.y
        sword.image_name = hero.sword_sprite_list[hero.direction]
        
        graphics.draw_sprite(sword)
        sword.life -= 1
        if sword.life == 0:
            del(hero.sword_list[i])
            hero.stabbing = False
            hero.image_name = hero.walking_sprites[hero.direction][0]
            hero.recharge = True

    if graphics.key_up(controls[4]):
        hero.recharge = False

    #DEATH
    if hero.hp < 1:
        controller.current_room = [0, 4, 4]
        controller.starting = True
        controller.block_1.x = graphics.window_width()/4
        controller.block_2.x = 3*(graphics.window_width()/4)
        generate_room(hero, 'down', controller.room[controller.current_room[0]][controller.current_room[1]][controller.current_room[2]], controller)
        hero.hp = maxHP
    

    #drawing the character
    graphics.draw_sprite(hero)

    #drawing the healthbox
    graphics.draw_rectangle(85, 25, 140, 20, fill='white')
    graphics.draw_text('HP', 30, 25)
    if hero.hp > (maxHP/2):
        r = 255 - int(255 * ((hero.hp / maxHP) - 0.5) * 2)
        g = 255
        b = 0
    elif hero.hp < (maxHP/2):
        r = 255
        g = int(255 * (hero.hp / (maxHP / 2)))
        b = 0
    else:
        r = 255
        g = 255
        b = 0
    color = '#%02x%02x%02x' % (r, g, b)
    graphics.draw_line(50, 25, 50 + ((hero.hp / maxHP) * 100), 25, fill=color, thickness=16)
    graphics.draw_rectangle(100, 25, 100, 16)
    for i in range(hero.hp):
        width = 100 / maxHP
        graphics.draw_rectangle(50 + (width * (i + 1)) - (width/2), 25, width, 16)
    
#PRE: controller is a sprite variable that holds many mutable variables, hero is the hero sprite object
#POST: updates the enemy sprites in the room
def update_enemies(controller, hero):
    for i in range(len(controller.enemy_list)-1, -1, -1):
        enemy = controller.enemy_list[i]

        #Slime Logic
        if enemy.image_name == 'enemy_1.gif':
            if random.randrange(50) == 15:
                if random.randrange(2) == 1:
                    enemy.x_speed = enemy.x_speed * -1
                else:
                    enemy.y_speed = enemy.y_speed * -1
            if enemy.collides(hero):
                dist = 15
                hero.x += enemy.x_speed * dist
                hero.y += enemy.y_speed * dist
                enemy.x -= enemy.x_speed * dist
                enemy.y -= enemy.y_speed * dist
                hero.hp -= 1

        #Blitzers Logic
        if enemy.image_name == 'enemy_2.gif':
            if random.randrange(50) == 15 and enemy.jumping == False:
                enemy.dest_x = random.randrange(tile_size * 2.5, graphics.window_width() - (tile_size * 2.5))
                enemy.dest_y = random.randrange(tile_size * 2.5, graphics.window_height() - (tile_size * 2.5))
                enemy.x_dist = enemy.dest_x - enemy.x
                enemy.y_dist = enemy.dest_y - enemy.y
                enemy.x_speed = enemy.x_dist/((((enemy.x_dist**2) + (enemy.y_dist**2))**.5)/enemy.speed)
                enemy.y_speed = enemy.y_dist/((((enemy.x_dist**2) + (enemy.y_dist**2))**.5)/enemy.speed)
                enemy.jumping = True
            elif enemy.jumping == True:
                if enemy.dest_x - 6 < enemy.x and enemy.dest_x + 6 > enemy.x:
                    enemy.x_speed = 0
                    enemy.y_speed = 0
                    enemy.jumping = False
            if enemy.collides(hero):
                dist = 8
                if enemy.x_speed == 0 and enemy.y_speed == 0:
                    hero.x -= hero.x_speed * dist * 2
                    hero.y -= hero.y_speed * dist * 2
                else:
                    hero.x += enemy.y_speed * dist
                    hero.y += -enemy.x_speed * dist
                hero.hp -= 1

        #Boomerang Thrower Logic
        if enemy.og_name == 'enemy_3_up_1.gif':
            if random.randrange(50) == 15:
                if enemy.x_speed == 0:
                    enemy.x_speed = 3 * random.randrange(-1, 2, 2)
                    enemy.y_speed = 0
                    if enemy.x_speed < 0:
                        enemy.direction = 1
                    else:
                        enemy.direction = 3
                else:
                    enemy.y_speed = 3 * random.randrange(-1, 2, 2)
                    enemy.x_speed = 0
                    if enemy.y_speed < 0:
                        enemy.direction = 0
                    else:
                        enemy.direction = 2
            if enemy.collides(hero):
                dist = 15
                hero.x += enemy.x_speed * dist
                hero.y += enemy.y_speed * dist
                enemy.x -= enemy.x_speed * dist
                enemy.y -= enemy.y_speed * dist
                hero.hp -= 1

            if random.randrange(100) == 15:
                enemy.rang = (sprite.Sprite(enemy.x, enemy.y, 'boomerang_1.gif'))
                enemy.rang.master = i
                enemy.rang.sending = False
                enemy.rang.returning = False
                enemy.rang.speed = 7
                enemy.rang.frame = 0
                enemy.rang.sprite_list = ['boomerang_1.gif', 'boomerang_2.gif', 'boomerang_3.gif', 'boomerang_4.gif']
                enemy.rang.og_name = enemy.rang.image_name
                controller.enemy_list.append(enemy.rang)

            #animating enemy
            speed = 4
            enemy.frame += 1
            if enemy.frame == len(enemy.sprite_list[enemy.direction]) * speed:
                enemy.frame = 0
            if enemy.frame % speed == 0:
                enemy.image_name = enemy.sprite_list[enemy.direction][enemy.frame // speed]

        #Boomerang Logic
        if enemy.og_name == 'boomerang_1.gif':
            enemy.range = 32
            if enemy.sending == False and enemy.returning == False:
                enemy.dest_x = hero.x
                enemy.dest_y = hero.y
                enemy.x_dist = (enemy.dest_x - enemy.x)
                enemy.y_dist = (enemy.dest_y - enemy.y)
                if ((((enemy.x_dist**2) + (enemy.y_dist**2))**.5)/enemy.speed) != 0:
                    enemy.x_speed = enemy.x_dist/((((enemy.x_dist**2) + (enemy.y_dist**2))**.5)/enemy.speed)
                    enemy.y_speed = enemy.y_dist/((((enemy.x_dist**2) + (enemy.y_dist**2))**.5)/enemy.speed)
                enemy.sending = True
            if enemy.sending == True:
                if enemy.dest_x - 4 < enemy.x and enemy.dest_x + 4 > enemy.x:
                    enemy.sending = False
                    enemy.returning = True
            if enemy.returning == True and enemy.master < len(controller.enemy_list):
                enemy.dest_x = controller.enemy_list[enemy.master].x
                enemy.dest_y = controller.enemy_list[enemy.master].y
                enemy.x_dist = enemy.dest_x - enemy.x
                enemy.y_dist = enemy.dest_y - enemy.y
                if ((((enemy.x_dist**2) + (enemy.y_dist**2))**.5)/enemy.speed) != 0:
                    enemy.x_speed = enemy.x_dist/((((enemy.x_dist**2) + (enemy.y_dist**2))**.5)/enemy.speed)
                    enemy.y_speed = enemy.y_dist/((((enemy.x_dist**2) + (enemy.y_dist**2))**.5)/enemy.speed)
                if enemy.collides(controller.enemy_list[enemy.master]):
                    del(controller.enemy_list[i])
                    continue
            if enemy.collides(hero):
                dist = 8
                hero.x += enemy.y_speed * dist
                hero.y += -enemy.x_speed * dist
                hero.hp -= 1

            #animating boomerang 
            speed = 4
            enemy.frame += 1
            if enemy.frame == len(enemy.sprite_list) * speed:
                enemy.frame = 0
            if enemy.frame % speed == 0:
                enemy.image_name = enemy.sprite_list[enemy.frame // speed]

        #Mage Logic
        if enemy.og_name == 'enemy_4_up_1.gif':
            enemy.x_speed = 0
            enemy.y_speed = 0
            if random.randrange(50) == 15 and enemy.firing != 1:
                enemy.x = random.randrange(tile_size * 2.5, graphics.window_width() - (tile_size * 2.5))
                enemy.y = random.randrange(tile_size * 2.5, graphics.window_height() - (tile_size * 2.5))
            if enemy.collides(hero):
                dist = 15
                hero.x -= hero.x_speed * dist
                hero.y -= hero.y_speed * dist
                hero.hp -= 1

            if random.randrange(100) == 15:
                enemy.firing = 1

            #animating enemy
            if hero.y < enemy.y + (tile_size / 2):
                enemy.direction = 0
            elif hero.x < enemy.x:
                enemy.direction = 1
            else:
                enemy.direction = 2

            if enemy.firing == 1:
                enemy.frame += 1
                if enemy.frame == 8:
                    enemy.firing = 0
                    enemy.frame = 0
                    enemy.fire = (sprite.Sprite(enemy.x, enemy.y, 'fireball_1.gif'))
                    enemy.fire.sending = False
                    enemy.fire.speed = 7
                    enemy.fire.frame = 0
                    enemy.fire.sprite_list = ['fireball_1.gif', 'fireball_2.gif', 'fireball_3.gif', 'fireball_4.gif']
                    enemy.fire.og_name = enemy.fire.image_name
                    controller.enemy_list.append(enemy.fire)
                
            enemy.image_name = enemy.sprite_list[enemy.direction][enemy.firing]

            

        #Fireball Logic
        if enemy.og_name == 'fireball_1.gif':
            enemy.range = 32
            if enemy.sending == False:
                enemy.dest_x = hero.x
                enemy.dest_y = hero.y
                enemy.x_dist = (enemy.dest_x - enemy.x)
                enemy.y_dist = (enemy.dest_y - enemy.y)
                enemy.x_speed = enemy.x_dist/((((enemy.x_dist**2) + (enemy.y_dist**2))**.5)/enemy.speed)
                enemy.y_speed = enemy.y_dist/((((enemy.x_dist**2) + (enemy.y_dist**2))**.5)/enemy.speed)
                enemy.sending = True
                
            if enemy.collides(hero):
                dist = 8
                hero.x += enemy.y_speed * dist
                hero.y += -enemy.x_speed * dist
                hero.hp -= 1

            #animating fireball
            speed = 4
            enemy.frame += 1
            if enemy.frame == len(enemy.sprite_list) * speed:
                enemy.frame = 0
            if enemy.frame % speed == 0:
                enemy.image_name = enemy.sprite_list[enemy.frame // speed]

        #Knight Logic
        if enemy.og_name == 'enemy_5_up_1.gif':
            if random.randrange(50) == 15:
                if enemy.x_speed == 0:
                    enemy.x_speed = 3 * random.randrange(-1, 2, 2)
                    enemy.y_speed = 0
                else:
                    enemy.y_speed = 3 * random.randrange(-1, 2, 2)
                    enemy.x_speed = 0
            if enemy.collides(hero):
                dist = 15
                hero.x += enemy.x_speed * dist
                hero.y += enemy.y_speed * dist
                enemy.x -= enemy.x_speed * dist
                enemy.y -= enemy.y_speed * dist
                hero.hp -= 1

            
            if enemy.x_speed < 0:
                enemy.direction = 1
            elif enemy.x_speed > 0:
                enemy.direction = 3
            elif enemy.y_speed < 0:
                enemy.direction = 0
            else:
                enemy.direction = 2

            #animating enemy
            speed = 4
            enemy.frame += 1
            if enemy.frame == len(enemy.sprite_list[enemy.direction]) * speed:
                enemy.frame = 0
            if enemy.frame % speed == 0:
                enemy.image_name = enemy.sprite_list[enemy.direction][enemy.frame // speed]

        #Boss Fireball
        if enemy.og_name == 'boss_fireball_1.gif':
            enemy.y_speed = enemy.speed
            enemy.x_speed = (enemy.angle//45)*enemy.speed
            
            if enemy.collides(hero):
                dist = 16
                thing = random.randrange(-1, 2, 2)
                hero.x += thing * (enemy.y_speed * dist)
                hero.y += thing * (-enemy.x_speed * dist)
                hero.hp -= 1

            #animating boss_fireball_1
            speed = 4
            enemy.frame += 1
            if enemy.frame == len(enemy.sprite_list) * speed:
                enemy.frame = 0
            if enemy.frame % speed == 0:
                enemy.image_name = enemy.sprite_list[enemy.frame // speed]
            

        #Base Enemy Logic
        if enemy.x < tile_size * 2.5 and enemy.image_name != 'enemy_2.gif':
            if enemy.og_name != 'fireball_1.gif' and enemy.og_name != 'boomerang_1.gif' and enemy.og_name != 'boss_fireball_1.gif':
                enemy.x = tile_size * 2.5
                enemy.x_speed = enemy.x_speed * -1
                enemy.direction = 3
            elif enemy.og_name == 'fireball_1.gif' or enemy.og_name == 'boss_fireball_1.gif':
                del(controller.enemy_list[i])
                continue
        if enemy.y < tile_size * 2.5 and enemy.image_name != 'enemy_2.gif':
            if enemy.og_name != 'fireball_1.gif' and enemy.og_name != 'boomerang_1.gif' and enemy.og_name != 'boss_fireball_1.gif':
                enemy.y = tile_size * 2.5
                enemy.y_speed = enemy.y_speed * -1
                enemy.direction = 2
            elif enemy.og_name == 'fireball_1.gif' or enemy.og_name == 'boss_fireball_1.gif':
                del(controller.enemy_list[i])
                continue
        if enemy.x > graphics.window_width() - (tile_size * 2.5) and enemy.image_name != 'enemy_2.gif':
            if enemy.og_name != 'fireball_1.gif' and enemy.og_name != 'boomerang_1.gif' and enemy.og_name != 'boss_fireball_1.gif':
                enemy.x = graphics.window_width() - (tile_size * 2.5)
                enemy.x_speed = enemy.x_speed * -1
                enemy.direction = 1
            elif enemy.og_name == 'fireball_1.gif' or enemy.og_name == 'boss_fireball_1.gif':
                del(controller.enemy_list[i])
                continue
        if enemy.y > graphics.window_height() - (tile_size * 2.5) and enemy.image_name != 'enemy_2.gif':
            if enemy.og_name != 'fireball_1.gif' and enemy.og_name != 'boomerang_1.gif' and enemy.og_name != 'boss_fireball_1.gif':
                enemy.y = graphics.window_height() - (tile_size * 2.5)
                enemy.y_speed = enemy.y_speed * -1
                enemy.direction = 0
            elif enemy.og_name == 'fireball_1.gif' or enemy.og_name == 'boss_fireball_1.gif':
                del(controller.enemy_list[i])
                continue
        #collision with sword    
        for sword in hero.sword_list:
            if enemy.collides(sword) and enemy.og_name != 'fireball_1.gif' and enemy.og_name != 'boomerang_1.gif' and enemy.og_name != 'boss_fireball_1.gif':
                if enemy.og_name != 'enemy_5_up_1.gif':
                    prize = loot[random.randrange(2)]
                    if prize == 'gold':
                        hero.gold += 200
                    elif prize == 'health':
                        hero.hp += 1
                        if hero.hp > maxHP:
                            hero.hp = maxHP
                    del(controller.enemy_list[i])
                    del(controller.room[controller.current_room[0]][controller.current_room[1]][controller.current_room[2]][1][controller.room[controller.current_room[0]][controller.current_room[1]][controller.current_room[2]][1].index(enemy.og_name)])
                    continue
                else:
                    if enemy.direction == hero.direction:
                        prize = loot[random.randrange(2)]
                        if prize == 'gold':
                            hero.gold += 500
                        elif prize == 'health':
                            hero.hp += 2
                        if hero.hp > maxHP:
                            hero.hp = maxHP
                        del(controller.enemy_list[i])
                        del(controller.room[controller.current_room[0]][controller.current_room[1]][controller.current_room[2]][1][controller.room[controller.current_room[0]][controller.current_room[1]][controller.current_room[2]][1].index(enemy.og_name)])
                        continue
                    else:
                        enemy.x -= enemy.x_speed * 16
                        enemy.y -= enemy.y_speed * 16
                
        enemy.x += enemy.x_speed
        enemy.y += enemy.y_speed

    #Boss Logic
    for i in range(len(controller.boss_list)-1, -1, -1):
        boss = controller.boss_list[i]
        boss.frame += 1
        if boss.frame == boss.damage:
            boss.image_name = 'boss_1.gif'
        
        #Movement
        if boss.x <= tile_size * 4 or boss.x >= graphics.window_width() - (tile_size * 4):
            boss.x_speed = boss.x_speed * -1

        #3 Fireball Attack
        if boss.frame % 60 == 0:
            for i in range(3):
                fireball = sprite.Sprite(boss.x, boss.y + (tile_size * 2), 'boss_fireball_1.gif')
                if i == 0:
                    fireball.angle = -45
                elif i == 1:
                    fireball.angle = 0
                else:
                    fireball.angle = 45

                fireball.og_name = fireball.image_name
                fireball.speed = 6
                fireball.frame = 0
                fireball.sprite_list = ['boss_fireball_1.gif', 'boss_fireball_2.gif', 'boss_fireball_3.gif', 'boss_fireball_4.gif', 'boss_fireball_5.gif', 'boss_fireball_6.gif', 'boss_fireball_7.gif', 'boss_fireball_8.gif']
                
                controller.enemy_list.append(fireball)

        #Collision with player
        if boss.collides(hero):
            hero.hp -= 1
            if hero.y > boss.y + (tile_size * 2):
                hero.y += 32
            else:
                hero.x += boss.x_speed * 24
                

        #Collides with sword
        for sword in hero.sword_list:
            if boss.collides(sword):
                boss.health -= 1
                boss.image_name = 'boss_2.gif'
                boss.damage = boss.frame + 4
                if hero.direction == 0:
                    hero.y += 64
                elif hero.direction == 1:
                    hero.x += 64
                elif hero.direction == 2:
                    hero.y -= 64
                else:
                    hero.x -= 64

        #Killing Boss
        if boss.health <= 0:
            del(boss)
            graphics.draw_sprite(hero)
            graphics.wait(1)
            width = 200
            for i in range (20):
                graphics.draw_rectangle(0, graphics.window_height()/2, width, graphics.window_height(), fill='black')
                graphics.draw_rectangle(graphics.window_width(), graphics.window_height()/2, width, graphics.window_height(), fill='black')
                graphics.wait()
                width += 100
            controller.game_state = controller.game_state_list[5]
            continue
        #Drawing Health Bar
        graphics.draw_rectangle(graphics.window_width() - 85, 25, 140, 20, fill='white')
        graphics.draw_text('HP', graphics.window_width() - 30, 25)
        graphics.draw_rectangle(graphics.window_width() - 100, 25, (boss.health / 20) * 100, 16, fill='red')
        
        boss.x += boss.x_speed

#=========Controller Creation=======#
controller = sprite.Sprite(0, 0, 'controller.gif')

#==============Enemy List===========#
controller.enemy_type_list = ['enemy_1.gif', 'enemy_2.gif', 'enemy_3_up_1.gif', 'enemy_4_up_1.gif', 'enemy_5_up_1.gif']

#====================================dungeon creation===========================================#
controller.room = []
for f in range(3):
    controller.room.append([])
    for x in range (9):
        controller.room[f].append([])
        for y in range (5):
            controller.room[f][x].append([])

#controller.room[floor][x][y] = ['objects', int:enemies, [bool:locks; Up, Left, Down, Right], [bool:boss_locks; Up, Left, Down, Right], [bool:exits; Up, Left, Down, Right], 'stairs',
                    #[bool:a+b_locks; Up, Left, Down, Right]]
holes = {'All':[True, True, True, True],
            'No':[False, False, False, False],
            'Top':[True, False, False, False],
            'Left':[False, True, False, False],
            'Bottom':[False, False, True, False],
            'Right':[False, False, False, True],
            'Top_left':[True, True, False, False],
            'Top_bottom':[True, False, True, False],
            'Top_right':[True, False, False, True],
            'Left_bottom':[False, True, True, False],
            'Left_right':[False, True, False, True],
            'Bottom_right':[False, False, True, True],
            'Not_top':[False, True, True, True],
            'Not_left':[True, False, True, True],
            'Not_bottom':[True, True, False, True],
            'Not_right':[True, True, True, False]}

#PRE: floor is the floor the room is on
#POST: returns a list of monsters for that floor
def get_enemy_list(floor):
    a_list = []
    for i in range(random.randrange(5)):
        if floor == 0:
            a_list.append(controller.enemy_type_list[random.randrange(2)])
        elif floor == 1:
            a_list.append(controller.enemy_type_list[random.randrange(4)])
        else:
            a_list.append(controller.enemy_type_list[random.randrange(5)])
    return a_list

#Floor 1======================================================================================================
controller.room[0][0][0] = ['chest', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Bottom_right'][:], 'none', holes['No'][:], False]
controller.room[0][0][1] = ['none', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Not_left'][:], 'none', holes['No'][:], False]
controller.room[0][0][2] = ['none', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Not_left'][:], 'none', holes['No'][:], False]
controller.room[0][0][3] = ['none', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Not_left'][:], 'none', holes['No'][:], False]
controller.room[0][0][4] = ['none', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Top_right'][:], 'none', holes['No'][:], False]

controller.room[0][1][0] = ['none', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Not_top'][:], 'none', holes['No'][:], False]
controller.room[0][1][1] = ['none', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Top_left'][:], 'none', holes['No'][:], False]
controller.room[0][1][2] = ['key', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Left_bottom'][:], 'none', holes['No'][:], False]
controller.room[0][1][3] = ['chest', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Top_left'][:], 'none', holes['No'][:], False]
controller.room[0][1][4] = ['none', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Left_right'][:], 'none', holes['No'][:], False]

controller.room[0][2][0] = ['none', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Left_bottom'][:], 'none', holes['No'][:], False]
controller.room[0][2][1] = ['chest', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Top_bottom'][:], 'none', holes['No'][:], False]
controller.room[0][2][2] = ['none', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Top_bottom'][:], 'none', holes['No'][:], False]
controller.room[0][2][3] = ['none', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Not_left'][:], 'none', holes['No'][:], False]
controller.room[0][2][4] = ['none', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Top_left'][:], 'none', holes['No'][:], False]

controller.room[0][3][0] = ['b_switch', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Bottom'][:], 'none', holes['No'][:], False]
controller.room[0][3][1] = ['none', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Top_bottom'][:], 'none', holes['No'][:], False]
controller.room[0][3][2] = ['none', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Top_bottom'][:], 'none', holes['No'][:], False]
controller.room[0][3][3] = ['none', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Not_right'][:], 'none', holes['No'][:], False]
controller.room[0][3][4] = ['none', ['enemy_2.gif'], holes['Right'][:], holes['No'][:], holes['Top_right'][:], 'none', holes['No'][:], False]

controller.room[0][4][0] = ['none', [], holes['No'][:], holes['No'][:], holes['Bottom'][:], 'UP', holes['No'][:], False]
controller.room[0][4][1] = ['none', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Top_bottom'][:], 'none', holes['No'][:], False]
controller.room[0][4][2] = ['none', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Top_bottom'][:], 'none', holes['Bottom'][:], False]
controller.room[0][4][3] = ['key', ['enemy_1.gif'], holes['No'][:], holes['No'][:], holes['Top_bottom'][:], 'none', holes['Top'][:], False]
controller.room[0][4][4] = ['none', [], holes['Left_right'][:], holes['No'][:], holes['Not_bottom'][:], 'none', holes['No'][:], False]

controller.room[0][5][0] = ['a_switch', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Right'][:], 'none', holes['No'][:], False]
controller.room[0][5][1] = ['chest', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Bottom'][:], 'none', holes['No'][:], False]
controller.room[0][5][2] = ['none', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Not_left'][:], 'none', holes['No'][:], False]
controller.room[0][5][3] = ['none', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Top_bottom'][:], 'none', holes['No'][:], False]
controller.room[0][5][4] = ['none', ['enemy_2.gif'], holes['Left'][:], holes['No'][:], holes['Not_bottom'][:], 'none', holes['No'][:], False]

controller.room[0][6][0] = ['none', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Left_right'][:], 'none', holes['No'][:], False]
controller.room[0][6][1] = ['none', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Bottom_right'][:], 'none', holes['No'][:], False]
controller.room[0][6][2] = ['none', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Not_bottom'][:], 'none', holes['No'][:], False]
controller.room[0][6][3] = ['none', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Bottom_right'][:], 'none', holes['No'][:], False]
controller.room[0][6][4] = ['none', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Top_left'][:], 'none', holes['No'][:], False]

controller.room[0][7][0] = ['none', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Left_right'][:], 'none', holes['No'][:], False]
controller.room[0][7][1] = ['none', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Not_top'][:], 'none', holes['No'][:], False]
controller.room[0][7][2] = ['key', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Top_left'][:], 'none', holes['No'][:], False]
controller.room[0][7][3] = ['none', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Left_bottom'][:], 'none', holes['No'][:], False]
controller.room[0][7][4] = ['none', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Top_right'][:], 'none', holes['No'][:], False]

controller.room[0][8][0] = ['none', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Left_bottom'][:], 'none', holes['No'][:], False]
controller.room[0][8][1] = ['none', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Not_right'][:], 'none', holes['No'][:], False]
controller.room[0][8][2] = ['none', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Top_bottom'][:], 'none', holes['No'][:], False]
controller.room[0][8][3] = ['none', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Top_bottom'][:], 'none', holes['No'][:], False]
controller.room[0][8][4] = ['none', get_enemy_list(0), holes['No'][:], holes['No'][:], holes['Top_left'][:], 'none', holes['No'][:], False]

#Floor 2=======================================================================================================
controller.room[1][0][0] = ['chest', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['Right'][:], 'none', holes['No'][:], False]
controller.room[1][0][1] = ['none', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['Bottom_right'][:], 'none', holes['No'][:], False]
controller.room[1][0][2] = ['none', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['Not_left'][:], 'none', holes['No'][:], False]
controller.room[1][0][3] = ['none', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['Not_left'][:], 'none', holes['No'][:], False]
controller.room[1][0][4] = ['none', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['Top_right'][:], 'none', holes['No'][:], False]

controller.room[1][1][0] = ['none', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['Not_top'][:], 'none', holes['No'][:], False]
controller.room[1][1][1] = ['none', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['All'][:], 'none', holes['No'][:], False]
controller.room[1][1][2] = ['none', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['Top_left'][:], 'none', holes['No'][:], False]
controller.room[1][1][3] = ['chest', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['Left'][:], 'none', holes['No'][:], False]
controller.room[1][1][4] = ['none', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['Left_right'][:], 'none', holes['No'][:], False]

controller.room[1][2][0] = ['chest', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['Left'][:], 'none', holes['No'][:], False]
controller.room[1][2][1] = ['none', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['Not_top'][:], 'none', holes['No'][:], False]
controller.room[1][2][2] = ['none', [], holes['No'][:], holes['No'][:], holes['Top'][:], 'ITEM_UP', holes['No'][:], False]
controller.room[1][2][3] = ['none', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['Bottom_right'][:], 'none', holes['No'][:], False]
controller.room[1][2][4] = ['none', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['Top_left'][:], 'none', holes['No'][:], False]

controller.room[1][3][0] = ['none', ['enemy_3_up_1.gif'], holes['No'][:], holes['No'][:], holes['Bottom_right'][:], 'none', holes['No'][:], False]
controller.room[1][3][1] = ['none', ['enemy_4_up_1.gif'], holes['No'][:], holes['No'][:], holes['Not_right'][:], 'none', holes['No'][:], False]
controller.room[1][3][2] = ['none', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['Top_bottom'][:], 'none', holes['No'][:], False]
controller.room[1][3][3] = ['none', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['Not_right'][:], 'none', holes['No'][:], False]
controller.room[1][3][4] = ['none', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['Top_right'][:], 'none', holes['No'][:], False]

controller.room[1][4][0] = ['none', [], holes['Right'][:], holes['No'][:], holes['Left_right'][:], 'DOWN', holes['No'][:], False]
controller.room[1][4][1] = ['none', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['Bottom_right'][:], 'none', holes['No'][:], False]
controller.room[1][4][2] = ['none', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['Top_right'][:], 'none', holes['No'][:], False]
controller.room[1][4][3] = ['chest', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['Bottom'][:], 'none', holes['No'][:], False]
controller.room[1][4][4] = ['none', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['Not_bottom'][:], 'none', holes['No'][:], False]

controller.room[1][5][0] = ['none', ['enemy_3_up_1.gif'], holes['Bottom'][:], holes['No'][:], holes['Not_top'][:], 'none', holes['No'][:], False]
controller.room[1][5][1] = ['none', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['Top_left'][:], 'none', holes['No'][:], False]
controller.room[1][5][2] = ['none', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['Left_bottom'][:], 'none', holes['No'][:], False]
controller.room[1][5][3] = ['none', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['Top_right'][:], 'none', holes['No'][:], False]
controller.room[1][5][4] = ['none', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['Left_right'][:], 'none', holes['No'][:], False]

controller.room[1][6][0] = ['none', ['enemy_4_up_1.gif'], holes['No'][:], holes['No'][:], holes['Not_top'][:], 'none', holes['No'][:], False]
controller.room[1][6][1] = ['none', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['Top_bottom'][:], 'none', holes['No'][:], False]
controller.room[1][6][2] = ['none', [], holes['No'][:], holes['No'][:], holes['Top'][:], 'ITEM_UP', holes['No'][:], False]
controller.room[1][6][3] = ['none', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['Left_right'][:], 'none', holes['No'][:], False]
controller.room[1][6][4] = ['chest', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['Left'][:], 'none', holes['No'][:], False]

controller.room[1][7][0] = ['none', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['Left_right'][:], 'none', holes['No'][:], False]
controller.room[1][7][1] = ['none', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['Bottom_right'][:], 'none', holes['No'][:], False]
controller.room[1][7][2] = ['none', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['Top_right'][:], 'none', holes['No'][:], False]
controller.room[1][7][3] = ['none', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['Left_right'][:], 'none', holes['No'][:], False]
controller.room[1][7][4] = ['leaf', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['Right'][:], 'none', holes['No'][:], False]

controller.room[1][8][0] = ['none', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['Left_bottom'][:], 'none', holes['No'][:], False]
controller.room[1][8][1] = ['none', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['Top_left'][:], 'none', holes['No'][:], False]
controller.room[1][8][2] = ['key', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['Left'][:], 'none', holes['No'][:], False]
controller.room[1][8][3] = ['none', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['Left_bottom'][:], 'none', holes['No'][:], False]
controller.room[1][8][4] = ['none', get_enemy_list(1), holes['No'][:], holes['No'][:], holes['Top_left'][:], 'none', holes['No'][:], False]

#Floor 3=======================================================================================================
controller.room[2][0][0] = ['none', get_enemy_list(2), holes['No'][:], holes['Bottom'][:], holes['Bottom_right'][:], 'none', holes['No'][:], False]
controller.room[2][0][1] = ['none', get_enemy_list(2), holes['No'][:], holes['Top'][:], holes['Top_bottom'][:], 'none', holes['No'][:], False]
controller.room[2][0][2] = ['none', get_enemy_list(2), holes['No'][:], holes['No'][:], holes['Top_bottom'][:], 'none', holes['No'][:], False]
controller.room[2][0][3] = ['none', get_enemy_list(2), holes['No'][:], holes['No'][:], holes['Top_bottom'][:], 'none', holes['No'][:], False]
controller.room[2][0][4] = ['chest', get_enemy_list(2), holes['No'][:], holes['No'][:], holes['Top_right'][:], 'none', holes['No'][:], False]

controller.room[2][1][0] = ['none', get_enemy_list(2), holes['No'][:], holes['No'][:], holes['Not_top'][:], 'none', holes['No'][:], False]
controller.room[2][1][1] = ['none', get_enemy_list(2), holes['No'][:], holes['No'][:], holes['Top_bottom'][:], 'none', holes['No'][:], False]
controller.room[2][1][2] = ['none', get_enemy_list(2), holes['No'][:], holes['No'][:], holes['Top_bottom'][:], 'none', holes['No'][:], False]
controller.room[2][1][3] = ['none', get_enemy_list(2), holes['No'][:], holes['No'][:], holes['Top_right'][:], 'none', holes['No'][:], False]
controller.room[2][1][4] = ['none', get_enemy_list(2), holes['No'][:], holes['No'][:], holes['Left_right'][:], 'none', holes['No'][:], False]

controller.room[2][2][0] = ['none', get_enemy_list(2), holes['No'][:], holes['No'][:], holes['Left_bottom'][:], 'none', holes['No'][:], False]
controller.room[2][2][1] = ['none', ['enemy_5_up_1.gif'], holes['No'][:], holes['No'][:], holes['Top_bottom'][:], 'none', holes['No'][:], False]
controller.room[2][2][2] = ['none', [], holes['No'][:], holes['No'][:], holes['Top'][:], 'ITEM_DOWN', holes['No'][:], False]
controller.room[2][2][3] = ['key', get_enemy_list(2), holes['No'][:], holes['No'][:], holes['Left'][:], 'none', holes['No'][:], False]
controller.room[2][2][4] = ['none', get_enemy_list(2), holes['No'][:], holes['No'][:], holes['Left_right'][:], 'none', holes['No'][:], False]

controller.room[2][3][0] = ['none', get_enemy_list(2), holes['No'][:], holes['No'][:], holes['Bottom_right'][:], 'none', holes['No'][:], False]
controller.room[2][3][1] = ['none', get_enemy_list(2), holes['No'][:], holes['No'][:], holes['Top_bottom'][:], 'none', holes['No'][:], False]
controller.room[2][3][2] = ['none', get_enemy_list(2), holes['Right'][:], holes['No'][:], holes['Top_right'][:], 'none', holes['No'][:], False]
controller.room[2][3][3] = ['none', get_enemy_list(2), holes['No'][:], holes['No'][:], holes['Bottom_right'][:], 'none', holes['No'][:], False]
controller.room[2][3][4] = ['chest', [], holes['No'][:], holes['No'][:], holes['Top_left'][:], 'none', holes['No'][:], False]

controller.room[2][4][0] = ['none', get_enemy_list(2), holes['No'][:], holes['No'][:], holes['Not_top'][:], 'none', holes['No'][:], False]
controller.room[2][4][1] = ['none', get_enemy_list(2), holes['Right'][:], holes['No'][:], holes['Top_right'][:], 'none', holes['No'][:], False]
controller.room[2][4][2] = ['none', get_enemy_list(2), holes['Left'][:], holes['No'][:], holes['Left_right'][:], 'none', holes['No'][:], False]
controller.room[2][4][3] = ['chest', [], holes['No'][:], holes['No'][:], holes['Left_bottom'][:], 'none', holes['No'][:], False]
controller.room[2][4][4] = ['none', get_enemy_list(2), holes['No'][:], holes['No'][:], holes['Top_right'][:], 'none', holes['No'][:], False]

controller.room[2][5][0] = ['none', get_enemy_list(2), holes['No'][:], holes['No'][:], holes['Left_right'][:], 'none', holes['No'][:], False]
controller.room[2][5][1] = ['none', get_enemy_list(2), holes['Left'][:], holes['No'][:], holes['Left_right'][:], 'none', holes['No'][:], False]
controller.room[2][5][2] = ['none', ['enemy_5_up_1.gif'], holes['No'][:], holes['No'][:], holes['Left_right'][:], 'none', holes['No'][:], False]
controller.room[2][5][3] = ['boss', [], holes['No'][:], holes['No'][:], holes['Bottom'][:], 'none', holes['No'][:], False]
controller.room[2][5][4] = ['chest', [], holes['No'][:], holes['No'][:], holes['Top_left'][:], 'none', holes['No'][:], False]

controller.room[2][6][0] = ['none', get_enemy_list(2), holes['No'][:], holes['No'][:], holes['Left_right'][:], 'none', holes['No'][:], False]
controller.room[2][6][1] = ['none', get_enemy_list(2), holes['No'][:], holes['No'][:], holes['Left_right'][:], 'none', holes['No'][:], False]
controller.room[2][6][2] = ['none', [], holes['No'][:], holes['No'][:], holes['Left'][:], 'ITEM_DOWN', holes['No'][:], False]
controller.room[2][6][3] = ['none', get_enemy_list(2), holes['No'][:], holes['No'][:], holes['Bottom_right'][:], 'none', holes['No'][:], False]
controller.room[2][6][4] = ['boss_key', get_enemy_list(2), holes['No'][:], holes['No'][:], holes['Top'][:], 'none', holes['No'][:], False]

controller.room[2][7][0] = ['none', get_enemy_list(2), holes['No'][:], holes['No'][:], holes['Left_right'][:], 'none', holes['No'][:], False]
controller.room[2][7][1] = ['none', get_enemy_list(2), holes['No'][:], holes['No'][:], holes['Left_right'][:], 'none', holes['No'][:], False]
controller.room[2][7][2] = ['none', get_enemy_list(2), holes['No'][:], holes['No'][:], holes['Bottom_right'][:], 'none', holes['No'][:], False]
controller.room[2][7][3] = ['none', get_enemy_list(2), holes['No'][:], holes['No'][:], holes['All'][:], 'none', holes['No'][:], False]
controller.room[2][7][4] = ['none', get_enemy_list(2), holes['No'][:], holes['No'][:], holes['Top_right'][:], 'none', holes['No'][:], False]

controller.room[2][8][0] = ['key', get_enemy_list(2), holes['No'][:], holes['No'][:], holes['Left'][:], 'none', holes['No'][:], False]
controller.room[2][8][1] = ['none', get_enemy_list(2), holes['No'][:], holes['No'][:], holes['Left_bottom'][:], 'none', holes['No'][:], False]
controller.room[2][8][2] = ['none', get_enemy_list(2), holes['No'][:], holes['No'][:], holes['Not_right'][:], 'none', holes['No'][:], False]
controller.room[2][8][3] = ['none', get_enemy_list(2), holes['No'][:], holes['No'][:], holes['Not_right'][:], 'none', holes['No'][:], False]
controller.room[2][8][4] = ['chest', get_enemy_list(2), holes['No'][:], holes['No'][:], holes['Top_left'][:], 'none', holes['No'][:], False]

#==============Variables============#
tile_size = 32
graphics.window_width(704)
graphics.window_height(704)
boss_talking = True
almost = -1
controls = ['w', 'a', 's', 'd', 'space']
loot = ['gold', 'health']
maxHP = 10
health_upgrade_cost = 5000
sword_upgrade_cost = 10000
controller.starting = True
buying = False

#=============Controller============#
controller.up = False
controller.left = False
controller.down = False
controller.right = False
controller.current_room = [0, 4, 4] #0, 4 , 4
controller.item_list = []
controller.lock_list = []
controller.enemy_list = []
controller.stairs_list = []
controller.boss_list = []
controller.block_1 = sprite.Sprite(graphics.window_width()/4, graphics.window_height()/2, 'black_block.gif')
controller.block_2 = sprite.Sprite(3*(graphics.window_width()/4), graphics.window_height()/2, 'black_block.gif')
controller.game_state_list = ['title', 'game', 'pause', 'map', 'lose', 'win']
controller.game_state = controller.game_state_list[1]
controller.room[controller.current_room[0]][controller.current_room[1]][controller.current_room[2]][7] = True

#==================Hero=============#
hero = sprite.Sprite(100, 100, 'hero_up_1.gif')
hero.keys = []
hero.gold = 0
hero.hp = 10
hero.item = False
hero.x_speed = 0
hero.y_speed = 0
hero.direction = 0
hero.recharge = False
hero.sword_list = []
hero.sword_sprite_list = ['sword_up_1.gif', 'sword_left_1.gif', 'sword_down_1.gif', 'sword_right_1.gif']
hero.walking_sprites = [['hero_up_1.gif', 'hero_up_2.gif'], ['hero_left_1.gif', 'hero_left_2.gif'], ['hero_down_1.gif', 'hero_down_2.gif'], ['hero_right_1.gif', 'hero_right_2.gif']]
hero.attack_sprites = ['hero_sword_up.gif', 'hero_sword_left.gif', 'hero_sword_down.gif', 'hero_sword_right.gif']
hero.frame = 0
hero.moving = False
hero.stabbing = False
hero.last_pressed = controls[0]
hero.sword_range = 1

#============First Room Gen=========#
generate_room(hero, 'down', controller.room[controller.current_room[0]][controller.current_room[1]][controller.current_room[2]], controller)

#==============Game Loop============#
while graphics.window_open():
    graphics.clear()
    controller.room[controller.current_room[0]][controller.current_room[1]][controller.current_room[2]][7] = True
    #Game
    if (controller.game_state == controller.game_state_list[1]):
    
        #Draw Background and doors
        if controller.room[controller.current_room[0]][controller.current_room[1]][controller.current_room[2]][0] != 'boss':
            graphics.draw_image('background_floor_' + str(controller.current_room[0]) + '.gif', graphics.window_width()/2, graphics.window_height()/2)
        else:
            graphics.draw_image('background_floor_0.gif', graphics.window_width()/2, graphics.window_height()/2)
        if controller.up:
            graphics.draw_image('Door_up.gif', graphics.window_width()/2, tile_size)
        if controller.left:
            graphics.draw_image('Door_left.gif', tile_size, graphics.window_height()/2)
        if controller.down:
            graphics.draw_image('Door_down.gif', graphics.window_width()/2, graphics.window_height() - (tile_size))
        if controller.right:
            graphics.draw_image('Door_right.gif', graphics.window_width() - (tile_size), graphics.window_height()/2)
        
        #Draw Items
        for i in controller.item_list:
            graphics.draw_sprite(i)

        #Draw Locks
        for i in controller.lock_list:
            graphics.draw_sprite(i)

        #Draw Stairs
        for i in controller.stairs_list:
            graphics.draw_sprite(i)
            
        #Draw Enemies
        for i in controller.enemy_list:
            graphics.draw_sprite(i)
            
        #Draw Boss
        for i in controller.boss_list:
            graphics.draw_sprite(i)
        if controller.block_1.x < -graphics.window_width()/4:
            controller.starting = False
        
        if controller.starting:
            graphics.draw_sprite(controller.block_1)
            graphics.draw_sprite(controller.block_2)
            controller.block_1.x -= 25
            controller.block_2.x += 25
            graphics.wait()
            
        else:
            #update enemies
            update_enemies(controller, hero)
            if controller.game_state != controller.game_state_list[1]:
                continue
        
            #update hero
            update_hero(hero, controller)
            if controller.game_state != controller.game_state_list[1]:
                continue
            if controller.room[controller.current_room[0]][controller.current_room[1]][controller.current_room[2]][0] == 'boss' and almost:
                almost = False
                graphics.wait()
                continue

            #Menus
            if graphics.key_down('e'):
                controller.game_state = controller.game_state_list[2]

            if graphics.key_down('q'):
                controller.game_state = controller.game_state_list[3]
            
            if controller.room[controller.current_room[0]][controller.current_room[1]][controller.current_room[2]][0] == 'boss' and boss_talking:
                graphics.draw_sprite(hero)
                graphics.wait(1)
                graphics.wait(1)
                graphics.draw_text('I DONT', graphics.window_width()/2, 300, color='purple', size=50)
                graphics.wait(1)
                graphics.wait(1)
                graphics.draw_text('WANT', graphics.window_width()/2, 400, color='purple', size=50)
                graphics.wait(1)
                graphics.wait(1)
                graphics.draw_text('SPAGHETTI!', graphics.window_width()/2, 500, color='purple', size=50)
                graphics.wait(1)
                graphics.wait(1)
                boss_talking = False

        

    #Pause Menu
    if controller.game_state == controller.game_state_list[2]:
        graphics.draw_image('menu.gif', graphics.window_width()/2, graphics.window_height()/2)
        keys = 0
        boss_keys = 0
        a_switch = False
        b_switch = False
        for i in hero.keys:
            if i == 'key':
                keys += 1
            elif i == 'boss_key':
                boss_keys += 1
            elif i == 'a_switch':
                a_switch = True
            else:
                b_switch = True
        graphics.draw_text('X ' + str(keys), 200, 100, size=30)
        graphics.draw_text('X ' + str(boss_keys), 200, 250, size=30)
        graphics.draw_text('X ' + str(hero.gold), 550, 100, size=30)
        if maxHP < 20:
            graphics.draw_text(str(health_upgrade_cost) + ' g', 580, 410, size=20)
        if hero.sword_range < 3:
            graphics.draw_text(str(sword_upgrade_cost) + ' g', 580, 515, size=20)


        if a_switch:
            graphics.draw_image('a_switch_menu.gif', 478, 257)
        if b_switch:
            graphics.draw_image('b_switch_menu.gif', 439, 257)

        if hero.item:
            graphics.draw_image('item_menu.gif', 200, 450)

        #buttons
        if graphics.button_down(1):
            380, 567
            640, 669
            if graphics.mouse_x() >= 59 and graphics.mouse_x() <= 319 and graphics.mouse_y() >= 567 and graphics.mouse_y() <= 669:
                controller.game_state = controller.game_state_list[1]
            if graphics.mouse_x() >= 380 and graphics.mouse_x() <= 640 and graphics.mouse_y() >= 567 and graphics.mouse_y() <= 669:
                break
        
        if graphics.key_down('space'):
            controller.game_state = controller.game_state_list[1]

        #shop
        if not buying:
            if graphics.key_down('z') and hero.gold >= health_upgrade_cost and maxHP < 20:
                hero.gold -= health_upgrade_cost
                maxHP += 5
                hero.hp += 5
                health_upgrade_cost = int(health_upgrade_cost * 1.5)
                buying = True
            elif graphics.key_down('x') and hero.gold >= sword_upgrade_cost and hero.sword_range < 3:
                hero.gold -= sword_upgrade_cost
                hero.sword_range += 1
                for i in range(len(hero.sword_sprite_list)):
                    sword = hero.sword_sprite_list[i]
                    sword = sword[:sword.find(str(hero.sword_range - 1))] + str(hero.sword_range) + '.gif'
                    hero.sword_sprite_list[i] = sword
                sword_upgrade_cost = int(sword_upgrade_cost * 1.5)
                buying = True
        if graphics.key_released('z') or graphics.key_released('x'):
            buying = False
        #Map
    if controller.game_state == controller.game_state_list[3]:
        floor = controller.current_room[0] + 1
        graphics.draw_rectangle(graphics.window_width()/2, graphics.window_height()/2,graphics.window_width(), graphics.window_height(), fill='black')
        graphics.draw_image('floor_1.gif', 200, 100)
        graphics.draw_image('floor_2.gif', graphics.window_width()/2, 100)
        graphics.draw_image('floor_3.gif', graphics.window_width() - 200, 100)
        
        if floor == 1:
            graphics.draw_image('cursor.gif', 200, 100)
            graphics.draw_image('map_floor_1.gif', graphics.window_width()/2, graphics.window_height()/2)
        elif floor == 2:
            graphics.draw_image('cursor.gif', graphics.window_width()/2, 100)
            graphics.draw_image('map_floor_2.gif', graphics.window_width()/2, graphics.window_height()/2)
        else:
            graphics.draw_image('cursor.gif', graphics.window_width() - 200, 100)
            graphics.draw_image('map_floor_3.gif', graphics.window_width()/2, graphics.window_height()/2)

        
        for f in range(len(controller.room)):
            for x in range(len(controller.room[f])):
                for y in range(len(controller.room[f][x])):
                    if floor - 1 == f:
                        grid_x = ((graphics.window_width()/2) - 288) + ((64*x) + 32)
                        grid_y = ((graphics.window_width()/2) - 160) + ((64*y) + 32)
                            
                        if controller.room[f][x][y][2][0]:
                            graphics.draw_image('grey_lock_horizontal.gif', grid_x, grid_y - 32)
                        if controller.room[f][x][y][2][1]:
                            graphics.draw_image('grey_lock_vertical.gif', grid_x - 32, grid_y)
                        if controller.room[f][x][y][2][2]:
                            graphics.draw_image('grey_lock_horizontal.gif', grid_x, grid_y + 32)
                        if controller.room[f][x][y][2][3]:
                            graphics.draw_image('grey_lock_vertical.gif', grid_x + 32, grid_y)

                        if controller.room[f][x][y][3][0]:
                            graphics.draw_image('gold_lock_horizontal.gif', grid_x, grid_y - 32)
                        if controller.room[f][x][y][3][1]:
                            graphics.draw_image('gold_lock_vertical.gif', grid_x - 32, grid_y)
                        if controller.room[f][x][y][3][2]:
                            graphics.draw_image('gold_lock_horizontal.gif', grid_x, grid_y + 32)
                        if controller.room[f][x][y][3][3]:
                            graphics.draw_image('gold_lock_vertical.gif', grid_x + 32, grid_y)

                        if controller.room[f][x][y][6][0]:
                            graphics.draw_image('purple_lock_horizontal.gif', grid_x, grid_y - 32)
                        if controller.room[f][x][y][6][1]:
                            graphics.draw_image('purple_lock_vertical.gif', grid_x - 32, grid_y)
                        if controller.room[f][x][y][6][2]:
                            graphics.draw_image('purple_lock_horizontal.gif', grid_x, grid_y + 32)
                        if controller.room[f][x][y][6][3]:
                            graphics.draw_image('purple_lock_vertical.gif', grid_x + 32, grid_y)

        for f in range(len(controller.room)):
            for x in range(len(controller.room[f])):
                for y in range(len(controller.room[f][x])):
                    if floor - 1 == f:
                        grid_x = ((graphics.window_width()/2) - 288) + ((64*x) + 32)
                        grid_y = ((graphics.window_width()/2) - 160) + ((64*y) + 32)
                        
                        if not controller.room[f][x][y][7]:
                            graphics.draw_image('map_black.gif', grid_x, grid_y)

                        if controller.room[f][x][y][0] != 'none':
                            graphics.draw_image('map_' + controller.room[f][x][y][0] + '.gif', grid_x, grid_y)

                        if controller.room[f][x][y][5] != 'none':
                            if controller.room[f][x][y][5] == 'UP':
                                graphics.draw_image('map_up.gif', grid_x, grid_y)
                            if controller.room[f][x][y][5] == 'ITEM_UP':
                                graphics.draw_image('map_up.gif', grid_x, grid_y)
                            if controller.room[f][x][y][5] == 'DOWN':
                                graphics.draw_image('map_down.gif', grid_x, grid_y)
                            if controller.room[f][x][y][5] == 'ITEM_DOWN':
                                graphics.draw_image('map_down.gif', grid_x, grid_y)

                        if x == controller.current_room[1] and y == controller.current_room[2]:
                            graphics.draw_rectangle(grid_x, grid_y, 16, 16, fill='green')

        if graphics.key_down('space'):
            controller.game_state = controller.game_state_list[1]
            
        #SUPER SECRET HACK FOR DEMONSTRATION PURPOSES AND NOD TO DEVELOPERS
        if graphics.key_down('m'):
            if graphics.key_down('k'):
                if graphics.key_down('r'):
                    if graphics.key_down('t'):
                        controller.current_room = [2, 5, 4]
                        controller.starting = True
                        controller.block_1.x = graphics.window_width()/4
                        controller.block_2.x = 3*(graphics.window_width()/4)
                        generate_room(hero, 'down', controller.room[controller.current_room[0]][controller.current_room[1]][controller.current_room[2]], controller)

    #Win
    if (controller.game_state == controller.game_state_list[5]):
        graphics.draw_image('black.gif', graphics.window_width()/2, graphics.window_height()/2)
        graphics.draw_text('CONGRATULATIONS!', graphics.window_width()/2, graphics.window_height()/2, color='white', size=50)
            
    graphics.wait()
