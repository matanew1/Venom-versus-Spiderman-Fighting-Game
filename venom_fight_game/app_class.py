import sys
from player_class import *

pygame.init()
vec = pygame.math.Vector2


def draw_text(txt, screen, pos, size, colour, font_name):
    font = pygame.font.SysFont(name=font_name, size=size, bold=True)
    text = font.render(txt, False, colour)
    text_size = text.get_size()
    pos[0] = pos[0] - text_size[0] // 2
    pos[1] = pos[1] - text_size[1] // 2
    screen.blit(text, pos)


class App:
    def __init__(self, state_default='start', pos_p=PLAYER_START_POS, pos_e=ENEMY_START_POS):
        self.end = False
        self.loser = None
        self.winner = None
        self.attack_p = False
        self.attack_e = False
        self.set_window()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = state_default
        self.cell_width = WIDTH // 8
        self.cell_height = HEIGHT // 8
        self.player_pos = PLAYER_START_POS
        self.enemy_pos = ENEMY_START_POS
        self.player = Player(self, 100, self.screen, PLAYER_NAME, pos_p)
        self.enemy = Player(self, 100, self.screen, ENEMY_NAME, pos_e)
        self.userInput_p = None
        self.userInput_e = None

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_draw()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_draw()
                if self.end is True:
                    self.end_play()
            else:
                self.running = False
        pygame.quit()
        sys.exit()

    # help functions

    @staticmethod
    def load_image(image_name, screen, size, pos):
        img = pygame.image.load(image_name)
        img = pygame.transform.scale(img, size)
        screen.blit(img, pos)

    @staticmethod
    def set_window():
        icon = pygame.image.load('venom.png')
        pygame.display.set_icon(icon)
        pygame.display.set_caption('venom_fight_game')

    #  start functions
    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
                self.state = 'playing'
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                self.running = False

    def start_draw(self):
        # self.screen.fill(GREEN)
        # self.video.draw(self.screen, (0, 0))
        self.load_image(f'venom_background.png', self.screen, (700, 700), BACKGROUND_CENTER)
        draw_text('PLEASE PRESS Y BUTTON TO START', self.screen, [WIDTH // 2, HEIGHT // 2 + 120], START_TEXT_SIZE, RED,
                  START_FONT)
        draw_text('PLEASE PRESS N BUTTON TO EXIT', self.screen, [WIDTH // 2, HEIGHT // 2 + 170], START_TEXT_SIZE, RED,
                  START_FONT)
        pygame.display.update()

    #  playing functions
    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        self.userInput_p = pygame.key.get_pressed()
        self.player.move(self.userInput_p, 'p')
        self.userInput_e = pygame.key.get_pressed()
        self.enemy.move(self.userInput_e, 'e')

    def playing_draw(self):
        self.screen.fill(RED)
        self.load_image(MAZE_IMAGE, self.screen, (WIDTH, HEIGHT), (0, HEIGHT - BOTTOM_PANEL))
        self.player.draw_player(self.player.pos)
        self.enemy.draw_enemy(self.enemy.pos)

        if self.attack_p is True:
            self.player.update(self.attack_p)
        else:
            self.player.update(self.attack_p)

        if self.attack_e is True:
            self.enemy.update(self.attack_e)
        else:
            self.enemy.update(self.attack_e)

        draw_text(f'{self.player.name} - HP', self.screen, [WIDTH // 2 - 150, HEIGHT // 2 + 200],
                  START_TEXT_SIZE - 3, WHITE, START_FONT)
        draw_text(f'{self.enemy.name} - HP', self.screen, [WIDTH // 2 + 150, HEIGHT // 2 + 200],
                  START_TEXT_SIZE - 3, WHITE, START_FONT)
        draw_text(str(self.player.hp), self.screen, [WIDTH // 2 - 150, HEIGHT // 2 + 250],
                  START_TEXT_SIZE, GREEN, START_FONT)
        draw_text(str(self.enemy.hp), self.screen, [WIDTH // 2 + 150, HEIGHT // 2 + 250],
                  START_TEXT_SIZE, GREEN, START_FONT)

        if self.player.alive is False or self.enemy.alive is False:
            if self.winner is not None and self.loser is not None:
                draw_text(f'{str.upper(self.winner)} DEFEATED {str.upper(self.loser)}', self.screen,
                          [WIDTH // 2, HEIGHT // 2 - 220],
                          START_TEXT_SIZE + 5, RED, START_FONT)
            draw_text('PRESS Y BUTTON FOR A NEW GAME', self.screen, [WIDTH // 2, HEIGHT // 2 - 140],
                      START_TEXT_SIZE, GREEN, START_FONT)
            draw_text('PRESS N BUTTON TO EXIT', self.screen, [WIDTH // 2, HEIGHT // 2 - 100],
                      START_TEXT_SIZE, GREEN, START_FONT)

        pygame.display.update()

    def end_play(self):
        self.__init__(state_default='playing')
        self.player.pos = vec(PLAYER_STATIC_POS)
        self.enemy.pos = vec(ENEMY_STATIC_POS)
        self.run()
        self.end = False
