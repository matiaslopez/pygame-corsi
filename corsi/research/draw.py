import os
import sys
import json
import pygame
import measurements
# import trials_raw_fede as trials_raw

surf = None

multiplier = 4
margin = 12 * multiplier
box_side = 20 * multiplier
w = 6 * box_side + 6 * margin
h = 4 * box_side + 5 * margin + 20



def make_empty_board():
    global surf
    surf.fill((100,100,100),
                pygame.Rect(0,0,w,h))
    surf.fill((255,255,255),
                pygame.Rect(0+margin/2.0,
                            0+margin/2.0,
                            w-2*margin/2.0,
                            h-2*margin/2.0))

def make_boxes():
    global surf
    pygame.font.init()
    f = pygame.font.get_default_font()
    font = pygame.font.Font(f, 20)

    for (k, (x,y)) in measurements.box_positions.items():
        # print((k,(x,y)))
        (left, top, width, height) = (
                            1.5*margin + (margin + box_side) * (y-1),
                            1.5*margin + (margin + box_side) * (x-1),
                            box_side, box_side)
        surf.fill((0,0,180),
                pygame.Rect((left, top, width, height)))

        text = font.render(k, 1, (225, 225, 225))
        surf.blit(text, (left + (box_side/2.0) - text.get_width()/2.0,
                          top + (box_side/2.0) - text.get_height()/2.0))

    pygame.display.flip()

def draw_sequence(sequence):
    for i in range(len(sequence)-1):
        draw_segment(sequence[i],sequence[i+1])

def draw_segment(s, d):
    global surf
    s = measurements.box_positions[s]
    d = measurements.box_positions[d]
    s = (1.5*margin + (margin + box_side) * (s[1]-1) + box_side/2.0, 1.5*margin + (margin + box_side) * (s[0]-1) + box_side/2.0)
    d = (1.5*margin + (margin + box_side) * (d[1]-1) + box_side/2.0, 1.5*margin + (margin + box_side) * (d[0]-1) + box_side/2.0)

    pygame.draw.line(surf, (180, 0, 0), s, d, 4)
    pygame.display.flip()

def init_draw():
    global surf
    pygame.display.init()
    surf = pygame.display.set_mode((w, h),32)

def end_draw():
    pygame.display.quit()


def save_board(file_name):
    if not os.path.exists("output"):
        os.makedirs("output")
    pygame.image.save(surf, "output/%s.png" % (file_name,))

def write_name(num, seq, protocol_str=""):
    pygame.font.init()
    f = pygame.font.get_default_font()
    font = pygame.font.Font(f, 12)

    msg = "Protcolo: %s - Trial: %02d - Secuencia:  %s" % (protocol_str, num, seq)
    text = font.render(msg, 1, (250, 250, 250))
    textrec = text.get_width()
    surf.blit(text, (w/2.0-(textrec/2.0),
                    h - text.get_height() - 5))

    pygame.display.flip()


def generate_all_boards(b, protocol_str=""):
    # for (group, exp) in enumerate(b): # b=trials_raw.trials_group
    for (num, seq) in b:
        init_draw()
        make_empty_board()
        draw_sequence(seq)
        make_boxes()
        write_name(num, "".join(seq), protocol_str)

        file_name = "{0}-{1:02d}_{2}".format(protocol_str, num, "".join(seq))

        save_board(file_name)


pygame.display.quit()

init_draw()

def main():
    if len(sys.argv) == 2:
        print "Cargando protocolo de ", sys.argv[1]

        prot_f=open(sys.argv[1]).read()
        prot_data = json.loads(prot_f)
        prot_trials = prot_data["trials"]
        prot_name = "protocoloSN"
        if prot_data.has_key("protocolo"):
            if prot_data["protocolo"].has_key("nombre"):
                prot_name = prot_data["protocolo"]["nombre"]

        struct = [ (int(x), y[0]) for (x,y) in prot_trials.iteritems()]

        generate_all_boards(struct, prot_name)

        pygame.quit()


if __name__ == '__main__':
    main()


