
import pygame
from math_functions import split_the_string, parse_to_tree, evaluate_tree

# --- Button Class ---
class Button:
    def __init__(
        self, x, y, width, height, text, font,
        bg_color, text_color, hover_color=None, border_radius=8
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.hover_color = hover_color if hover_color is not None else bg_color
        self.border_radius = border_radius

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            color = self.hover_color
        else:
            color = self.bg_color

        pygame.draw.rect(
            surface,
            color,
            self.rect,
            border_radius=self.border_radius
        )

        if self.text:
            text_surface = self.font.render(
                self.text, True, self.text_color
            )
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)

    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


# --- Button Setup ---
def buttons_setup(font):
    buttons_texts = [
        "7", "8", "9", "/", "^",
        "4", "5", "6", "*", "√",
        "1", "2", "3", "-", "3√",
        "0", ".", "=", "+", "C"
    ]

    buttons = {}

    button_width = 85
    button_height = 55
    gap = 8
    columns = 5

    # RGB colors: each value is between 0 and 255
    bg_color = (15, 0, 255)
    text_color = (255, 255, 255)
    hover_color = (15, 100, 255)

    for i, text in enumerate(buttons_texts):
        row = i // columns
        col = i % columns

        x = 20 + col * (button_width + gap)
        y = 130 + row * (button_height + gap)

        buttons[i] = Button(
            x=x,
            y=y,
            width=button_width,
            height=button_height,
            text=text,
            font=font,
            bg_color=bg_color,
            text_color=text_color,
            hover_color=hover_color,
            border_radius=8
        )

    return buttons


# --- Pygame Setup ---
def initCalc():
    pygame.init()

    window = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Graphic Calculator")

    clock = pygame.time.Clock()
    FPS = 60

    font = pygame.font.Font(None, 30)
    text_font = pygame.font.Font(None, 40)

    buttons = buttons_setup(font)

    return window, clock, FPS, buttons, text_font


# --- Main ---
def main():
    window, clock, FPS, buttons, text_font = initCalc()

    run = True
    math_string = ""

    result_shown = False

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            for button in buttons.values():
                if button.is_clicked(event):
                    if button.text == "C":
                        math_string = ""

                    elif button.text == "=":
                        try:
                            tokens = split_the_string(math_string)
                            root_node = parse_to_tree(tokens)
                            result = evaluate_tree(root_node)
                            math_string = str(result)
                            result_shown = True

                        except (ValueError, ZeroDivisionError, OverflowError) as error:
                            math_string = "Error"
                            print(error)

                    else:
                        if result_shown:
                            math_string = button.text
                            result_shown = False
                        else:
                            math_string += button.text

        window.fill((25, 25, 35))

        title = text_font.render(
            "Graphic Calculator", True, (255, 255, 255)
        )
        window.blit(title, (20, 25))

        math_text = text_font.render(
            math_string, True, (255, 255, 255)
        )
        window.blit(math_text, (20, 75))

        for button in buttons.values():
            button.draw(window)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
