import pygame
import random
import math
import sys
import time

# ---------------------------------------------------------------------------
#  CONSTANTS & THEME
# ---------------------------------------------------------------------------
SCREEN_W, SCREEN_H = 1000, 720

COLORS = {
    "bg":           (10,  12,  30),
    "bg2":          (18,  22,  48),
    "panel":        (22,  28,  60),
    "card_back":    (35,  45,  95),
    "card_face":    (20,  26,  55),
    "card_border":  (70,  90, 200),
    "accent":       (100, 160, 255),
    "accent2":      (60, 220, 180),
    "matched":      (40,  80,  60),
    "matched_bdr":  (60, 220, 130),
    "wrong":        (120, 30,  40),
    "wrong_bdr":    (255, 80,  80),
    "text":         (220, 230, 255),
    "text_dim":     (100, 120, 180),
    "timer_ok":     (60,  220, 180),
    "timer_warn":   (255, 200,  60),
    "timer_crit":   (255,  80,  80),
    "btn":          (40,  55, 130),
    "btn_hover":    (60,  80, 180),
    "btn_text":     (200, 220, 255),
    "overlay":      (5,   8,  20),
}

FPS         = 60
CARD_RADIUS = 10

FLIP_SPEED = 0.045

SHAPE_PALETTES = [
    (255, 100, 100), (100, 200, 255), (255, 220,  60),
    (100, 255, 160), (255, 140, 255), (255, 160,  80),
    (80,  255, 220), (200, 130, 255), (255, 255, 100),
    (255,  90, 150), (130, 255, 130), (100, 180, 255),
    (255, 180,  60), (180, 255, 100), (255, 100, 200),
    (60,  220, 255), (255, 210, 130), (160, 100, 255),
]

# ---------------------------------------------------------------------------
#  SMOOTH SHAPE DRAWING  (gfxdraw for anti-aliased outlines + filled polys)
# ---------------------------------------------------------------------------
try:
    import pygame.gfxdraw
    HAS_GFX = True
except ImportError:
    HAS_GFX = False


def _aa_polygon(surf, pts, color):
    """Filled + anti-aliased polygon."""
    if HAS_GFX and len(pts) >= 3:
        pygame.gfxdraw.filled_polygon(surf, pts, color)
        pygame.gfxdraw.aapolygon(surf, pts, color)
    else:
        pygame.draw.polygon(surf, color, pts)


def _aa_circle(surf, cx, cy, r, color):
    if HAS_GFX and r > 0:
        pygame.gfxdraw.filled_circle(surf, cx, cy, r, color)
        pygame.gfxdraw.aacircle(surf, cx, cy, r, color)
    else:
        pygame.draw.circle(surf, color, (cx, cy), r)


def _pts_polygon(cx, cy, n, radius, angle_offset=0):
    return [
        (int(cx + radius * math.cos(math.radians(360 * i / n + angle_offset - 90))),
         int(cy + radius * math.sin(math.radians(360 * i / n + angle_offset - 90))))
        for i in range(n)
    ]


def draw_shape(surf, shape_id, cx, cy, size, color):
    """Draw one of 18 distinct geometric icons centred at (cx, cy)."""
    r  = size // 2
    s  = shape_id % 18
    bg = COLORS["card_face"]

    if s == 0:
        _aa_circle(surf, cx, cy, r, color)
    elif s == 1:
        pts = [(cx, cy-r), (cx+r, cy), (cx, cy+r), (cx-r, cy)]
        _aa_polygon(surf, pts, color)
    elif s == 2:
        _aa_polygon(surf, _pts_polygon(cx, cy, 3, r), color)
    elif s == 3:
        pygame.draw.rect(surf, color, (cx-r, cy-r, r*2, r*2), border_radius=4)
    elif s == 4:
        outer = _pts_polygon(cx, cy, 5, r)
        inner = _pts_polygon(cx, cy, 5, int(r*0.45), 36)
        star = []
        for i in range(5):
            star += [outer[i], inner[i]]
        _aa_polygon(surf, star, color)
    elif s == 5:
        _aa_polygon(surf, _pts_polygon(cx, cy, 5, r), color)
    elif s == 6:
        _aa_polygon(surf, _pts_polygon(cx, cy, 6, r), color)
    elif s == 7:
        t = max(2, r // 3)
        pygame.draw.rect(surf, color, (cx-t, cy-r, t*2, r*2), border_radius=3)
        pygame.draw.rect(surf, color, (cx-r, cy-t, r*2, t*2), border_radius=3)
    elif s == 8:
        pts = []
        for angle in range(0, 361, 4):
            a = math.radians(angle)
            x = r * 0.8 * (16 * math.sin(a)**3)
            y = -r * 0.8 * (13*math.cos(a) - 5*math.cos(2*a) - 2*math.cos(3*a) - math.cos(4*a))
            pts.append((int(cx + x/16), int(cy + y/16)))
        if len(pts) > 2:
            _aa_polygon(surf, pts, color)
    elif s == 9:
        pts = [
            (cx-r, cy-r//3), (cx, cy-r//3), (cx, cy-r),
            (cx+r, cy),
            (cx, cy+r), (cx, cy+r//3), (cx-r, cy+r//3)
        ]
        _aa_polygon(surf, pts, color)
    elif s == 10:
        _aa_circle(surf, cx, cy, r, color)
        _aa_circle(surf, cx + r//3, cy - r//5, int(r*0.80), bg)
    elif s == 11:
        _aa_polygon(surf, _pts_polygon(cx, cy, 8, r), color)
    elif s == 12:
        _aa_circle(surf, cx, cy, r, color)
        _aa_circle(surf, cx, cy, r//2, bg)
    elif s == 13:
        pts = [
            (cx+r//3, cy-r), (cx-r//4, cy-r//8),
            (cx+r//4, cy-r//8), (cx-r//3, cy+r)
        ]
        _aa_polygon(surf, pts, color)
    elif s == 14:
        outer = _pts_polygon(cx, cy, 6, r)
        inner = _pts_polygon(cx, cy, 6, int(r*0.45), 30)
        star = []
        for i in range(6):
            star += [outer[i], inner[i]]
        _aa_polygon(surf, star, color)
    elif s == 15:
        for i in range(6):
            a  = math.radians(60 * i)
            px = cx + int(r * 0.6 * math.cos(a))
            py = cy + int(r * 0.6 * math.sin(a))
            _aa_circle(surf, px, py, r//3, color)
        _aa_circle(surf, cx, cy, r//3, color)
    elif s == 16:
        t = max(2, r // 3)
        for angle in (45, -45):
            rad = math.radians(angle)
            ca, sa = math.cos(rad), math.sin(rad)
            corners = [(-t, -r), ( t, -r), ( t,  r), (-t,  r)]
            rotated = [
                (int(cx + dx*ca - dy*sa), int(cy + dx*sa + dy*ca))
                for dx, dy in corners
            ]
            _aa_polygon(surf, rotated, color)
    elif s == 17:
        prev = None
        for i in range(0, 360, 4):
            a  = math.radians(i)
            rr = r * i / 360
            x  = int(cx + rr * math.cos(a))
            y  = int(cy + rr * math.sin(a))
            if prev:
                pygame.draw.line(surf, color, prev, (x, y), 3)
            prev = (x, y)
            
# ---------------------------------------------------------------------------
#  CARD CLASS
# ---------------------------------------------------------------------------
class Card:
    def __init__(self, shape_id, rect):
        self.shape_id  = shape_id
        self.color     = SHAPE_PALETTES[shape_id % len(SHAPE_PALETTES)]
        self.rect      = pygame.Rect(rect)
        self.matched   = False
        self.revealed  = False

        self.flip_progress = 0.0
        self.flip_target   = 0.0
        self.wrong_flash   = 0

    def start_flip(self, to_front: bool):
        self.flip_target = 1.0 if to_front else 0.0

    def update(self):
        if self.wrong_flash > 0:
            self.wrong_flash -= 1

        diff = self.flip_target - self.flip_progress
        if abs(diff) <= FLIP_SPEED:
            self.flip_progress = self.flip_target
        else:
            self.flip_progress += FLIP_SPEED if diff > 0 else -FLIP_SPEED

    def is_animating(self):
        return abs(self.flip_progress - self.flip_target) > 0.001

    def draw(self, surf):
        r = self.rect
        angle_deg = self.flip_progress * 180.0
        scale     = abs(math.cos(math.radians(angle_deg)))
        w_draw    = max(2, int(r.width * scale))
        x_off     = (r.width - w_draw) // 2
        draw_r    = pygame.Rect(r.x + x_off, r.y, w_draw, r.height)

        showing_front = self.flip_progress >= 0.5

        if self.wrong_flash > 0:
            bg_c  = COLORS["wrong"]
            bdr_c = COLORS["wrong_bdr"]
        elif self.matched:
            bg_c  = COLORS["matched"]
            bdr_c = COLORS["matched_bdr"]
        elif showing_front:
            bg_c  = COLORS["card_face"]
            bdr_c = COLORS["accent"]
        else:
            bg_c  = COLORS["card_back"]
            bdr_c = COLORS["card_border"]

        pygame.draw.rect(surf, bg_c,  draw_r, border_radius=CARD_RADIUS)
        pygame.draw.rect(surf, bdr_c, draw_r, width=2, border_radius=CARD_RADIUS)

        if showing_front and w_draw > 20:
            cx       = draw_r.centerx
            cy       = draw_r.centery
            icon_size = int(min(draw_r.width, draw_r.height) * 0.52)
            draw_shape(surf, self.shape_id, cx, cy, icon_size, self.color)
        elif not showing_front and w_draw > 20:
            dot_c = (50, 65, 140)
            step  = 10
            for dx in range(step, draw_r.width - step // 2, step):
                for dy in range(step, draw_r.height - step // 2, step):
                    pygame.draw.circle(surf, dot_c,
                                       (draw_r.x + dx, draw_r.y + dy), 1)
                    
# ---------------------------------------------------------------------------
#  BUTTON WIDGET
# ---------------------------------------------------------------------------
class Button:
    def __init__(self, rect, label, font):
        self.rect    = pygame.Rect(rect)
        self.label   = label
        self.font    = font
        self.hovered = False

    def draw(self, surf):
        c = COLORS["btn_hover"] if self.hovered else COLORS["btn"]
        pygame.draw.rect(surf, c, self.rect, border_radius=8)
        pygame.draw.rect(surf, COLORS["accent"], self.rect, width=2, border_radius=8)
        txt = self.font.render(self.label, True, COLORS["btn_text"])
        surf.blit(txt, txt.get_rect(center=self.rect.center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False


# ---------------------------------------------------------------------------
#  INPUT FIELD WIDGET
# ---------------------------------------------------------------------------
class InputField:
    def __init__(self, rect, default, label, font, min_val=2, max_val=18):
        self.rect    = pygame.Rect(rect)
        self.value   = str(default)
        self.label   = label
        self.font    = font
        self.active  = False
        self.min_val = min_val
        self.max_val = max_val

    def get_int(self):
        try:
            return max(self.min_val, min(self.max_val, int(self.value)))
        except ValueError:
            return self.min_val

    def draw(self, surf, label_font):
        lbl = label_font.render(self.label, True, COLORS["text_dim"])
        surf.blit(lbl, (self.rect.x, self.rect.y - 24))
        border_c = COLORS["accent"] if self.active else COLORS["card_border"]
        pygame.draw.rect(surf, COLORS["card_back"], self.rect, border_radius=6)
        pygame.draw.rect(surf, border_c, self.rect, width=2, border_radius=6)
        txt = self.font.render(self.value, True, COLORS["text"])
        surf.blit(txt, txt.get_rect(center=self.rect.center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.value = self.value[:-1]
            elif event.unicode.isdigit() and len(self.value) < 3:
                self.value += event.unicode