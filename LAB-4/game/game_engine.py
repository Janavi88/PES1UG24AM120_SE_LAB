import random
import time
import pygame

# ---------------------------------------------------------------------------
# Coordinate convention: arm_position < 0 is the PLAYER's side,
# arm_position > 0 is the COMPUTER's side.
#   player wins at  -TARGET_LIMIT   (-100.0)
#   computer wins at +TARGET_LIMIT  (+100.0)
# ---------------------------------------------------------------------------
TARGET_LIMIT = 100.0

# --- Player ---------------------------------------------------------------
PLAYER_PUSH_STRENGTH = 4.2          # arm units moved per valid key press
PLAYER_PUSH_STAMINA_COST = 2.0      # stamina spent per valid key press
MAX_STAMINA = 100.0
STAMINA_RECOVERY_PER_SEC = 15.0     # natural recovery (units / second)
EXHAUSTION_THRESHOLD = 10.0         # stamina below this -> exhausted
EXHAUSTION_RECOVER_THRESHOLD = 25.0 # stamina needed to push again

# --- AI -------------------------------------------------------------------
AI_BASE_FORCE_PER_SEC = 21.0        # baseline push (units / second), before variance
AI_VARIANCE_MIN = 0.3
AI_VARIANCE_MAX = 1.0
AI_NORMAL_DURATION = 4.0            # seconds of normal resistance
AI_SURGE_DURATION = 2.0             # seconds of high-power surge
AI_COOLDOWN_DURATION = 3.0          # seconds of reduced resistance
AI_SURGE_MULTIPLIER = 1.8           # force multiplier during surge (> 1)
AI_COOLDOWN_MULTIPLIER = 0.35       # force multiplier during cooldown (< 1)

# --- Counter-surge bonus --------------------------------------------------
COUNTER_SURGE_WINDOW = 0.6          # seconds after surge->cooldown to trigger
COUNTER_SURGE_DURATION = 4.0        # seconds the bonus stays active
COUNTER_SURGE_PUSH_MULTIPLIER = 2.0
COUNTER_SURGE_RECOVERY_MULTIPLIER = 3.0

# --- Misc -----------------------------------------------------------------
MAX_FRAME_DT = 0.05                 # clamp dt so a stall can't skip phases

# AI phases
AI_NORMAL = "NORMAL"
AI_SURGE = "SURGE"
AI_COOLDOWN = "COOLDOWN"


class GameEngine:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.target_limit = TARGET_LIMIT
        self.max_stamina = MAX_STAMINA
        self.ai_strength = AI_BASE_FORCE_PER_SEC

        self.font_big = pygame.font.SysFont(None, 44)
        self.font_med = pygame.font.SysFont(None, 26)

        self._last_tick = None
        self.reset()

    # ------------------------------------------------------------------ state
    def reset(self):
        """Reset every piece of round-specific state."""
        self.arm_position = 0.0
        self.last_key = None

        self.stamina = self.max_stamina
        self.exhausted = False

        self.winner = None
        self.game_state = "PLAYING"

        self.ai_state = AI_NORMAL
        self.ai_phase_time = 0.0        # seconds spent in current AI phase

        self.counter_window_time = 0.0  # remaining time of the counter window
        self.counter_bonus_time = 0.0   # remaining time of the active bonus

        self._last_tick = None          # avoid a huge dt after a pause/rematch

    # ------------------------------------------------------------------ input
    def handle_event(self, event):
        if self.game_state != "PLAYING":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()
            return

        if event.type != pygame.KEYDOWN:
            return
        if event.key not in (pygame.K_LEFT, pygame.K_RIGHT):
            return
        # Ignore auto-repeat style duplicates: a key must differ from the last.
        if event.key == self.last_key:
            return
        # Exhausted players cannot push (and the press is not remembered).
        if self.exhausted or self.stamina < EXHAUSTION_THRESHOLD:
            self.exhausted = True
            return

        self.last_key = event.key

        # Counter-surge: valid push inside the window right after surge ends.
        if self.counter_window_time > 0.0 and self.counter_bonus_time <= 0.0:
            self.counter_bonus_time = COUNTER_SURGE_DURATION
            self.counter_window_time = 0.0   # one activation per transition

        strength = PLAYER_PUSH_STRENGTH
        if self.counter_bonus_time > 0.0:
            strength *= COUNTER_SURGE_PUSH_MULTIPLIER

        # Player pushes toward the NEGATIVE (player) side.
        self.arm_position -= strength
        self.stamina = max(0.0, self.stamina - PLAYER_PUSH_STAMINA_COST)
        if self.stamina < EXHAUSTION_THRESHOLD:
            self.exhausted = True

        self._clamp_and_check_winner()

    # ----------------------------------------------------------------- update
    def update(self, dt=None):
        if self.game_state != "PLAYING":
            self._last_tick = None
            return

        if dt is None:
            now = time.perf_counter()
            dt = 0.0 if self._last_tick is None else now - self._last_tick
            self._last_tick = now
        dt = max(0.0, min(dt, MAX_FRAME_DT))

        self._update_ai_cycle(dt)
        self._update_counter_timers(dt)

        # AI force (uses existing strength + random variance), scaled by phase.
        ai_variance = random.uniform(AI_VARIANCE_MIN, AI_VARIANCE_MAX)
        self.arm_position += (
            self.ai_strength * ai_variance * self._ai_multiplier() * dt
        )

        # Stamina recovery (faster during the counter-surge bonus).
        recovery = STAMINA_RECOVERY_PER_SEC
        if self.counter_bonus_time > 0.0:
            recovery *= COUNTER_SURGE_RECOVERY_MULTIPLIER
        self.stamina = min(self.max_stamina, self.stamina + recovery * dt)

        if self.exhausted and self.stamina >= EXHAUSTION_RECOVER_THRESHOLD:
            self.exhausted = False

        self._clamp_and_check_winner()

    def _ai_multiplier(self):
        if self.ai_state == AI_SURGE:
            return AI_SURGE_MULTIPLIER
        if self.ai_state == AI_COOLDOWN:
            return AI_COOLDOWN_MULTIPLIER
        return 1.0

    def _ai_phase_duration(self):
        return {
            AI_NORMAL: AI_NORMAL_DURATION,
            AI_SURGE: AI_SURGE_DURATION,
            AI_COOLDOWN: AI_COOLDOWN_DURATION,
        }[self.ai_state]

    def _update_ai_cycle(self, dt):
        self.ai_phase_time += dt
        # while-loop so a long dt still performs every transition in order
        while self.ai_phase_time >= self._ai_phase_duration():
            self.ai_phase_time -= self._ai_phase_duration()
            if self.ai_state == AI_NORMAL:
                self.ai_state = AI_SURGE
            elif self.ai_state == AI_SURGE:
                self.ai_state = AI_COOLDOWN
                # Surge just ended: open the counter-surge timing window.
                self.counter_window_time = COUNTER_SURGE_WINDOW
            else:
                self.ai_state = AI_NORMAL
                self.counter_window_time = 0.0

    def _update_counter_timers(self, dt):
        if self.counter_window_time > 0.0:
            self.counter_window_time = max(0.0, self.counter_window_time - dt)
        if self.counter_bonus_time > 0.0:
            self.counter_bonus_time = max(0.0, self.counter_bonus_time - dt)

    def _clamp_and_check_winner(self):
        if self.game_state != "PLAYING":
            return
        if self.arm_position <= -self.target_limit:
            self.arm_position = -self.target_limit
            self.winner = "PLAYER"
            self.game_state = "GAME_OVER"
        elif self.arm_position >= self.target_limit:
            self.arm_position = self.target_limit
            self.winner = "COMPUTER"
            self.game_state = "GAME_OVER"

        if self.game_state == "GAME_OVER":
            # Nothing temporary should linger on the post-game screen.
            self.counter_window_time = 0.0
            self.counter_bonus_time = 0.0

    # ----------------------------------------------------------------- render
    def render(self, screen):
        screen.fill((25, 28, 35))

        title_surf = self.font_big.render("ARM WRESTLE SHOWDOWN", True, (240, 240, 240))
        screen.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 12))

        player_header = self.font_med.render("PLAYER", True, (80, 160, 255))
        computer_header = self.font_med.render("COMPUTER", True, (255, 100, 80))
        screen.blit(player_header, (60, 55))
        screen.blit(computer_header, (self.width - 150, 55))

        table_rect = pygame.Rect(40, 100, self.width - 80, 310)
        pygame.draw.rect(screen, (110, 50, 15), table_rect, border_radius=14)
        pygame.draw.rect(screen, (70, 30, 8), table_rect, width=5, border_radius=14)

        pygame.draw.line(screen, (45, 18, 4), (self.width // 2, 100), (self.width // 2, 410), 4)

        offset_x = (self.arm_position / self.target_limit) * 95
        hand_x = (self.width // 2) + int(offset_x)
        hand_y = 235

        p_shoulder = (70, 330)
        p_elbow = (140, 215)
        c_shoulder = (self.width - 70, 330)
        c_elbow = (self.width - 140, 215)

        pygame.draw.line(screen, (200, 145, 110), p_shoulder, p_elbow, 32)
        pygame.draw.line(screen, (215, 160, 125), p_elbow, (hand_x, hand_y), 26)
        pygame.draw.circle(screen, (185, 130, 95), p_elbow, 18)

        pygame.draw.line(screen, (170, 110, 85), c_shoulder, c_elbow, 32)
        pygame.draw.line(screen, (185, 125, 95), c_elbow, (hand_x, hand_y), 26)
        pygame.draw.circle(screen, (150, 95, 70), c_elbow, 18)

        pygame.draw.circle(screen, (225, 175, 140), (hand_x, hand_y), 24)
        pygame.draw.circle(screen, (160, 115, 85), (hand_x, hand_y), 24, width=3)

        stamina_label = self.font_med.render("STAMINA", True, (220, 220, 220))
        screen.blit(stamina_label, (40, 445))

        stamina_bg = pygame.Rect(140, 448, 240, 22)
        stamina_fill = pygame.Rect(140, 448, int(240 * (self.stamina / self.max_stamina)), 22)
        pygame.draw.rect(screen, (45, 50, 60), stamina_bg, border_radius=6)
        bar_color = (60, 210, 100) if self.stamina > 25 else (220, 60, 60)
        if self.counter_bonus_time > 0.0:
            bar_color = (255, 210, 60)
        pygame.draw.rect(screen, bar_color, stamina_fill, border_radius=6)

        self._render_indicators(screen)

        if self.game_state == "GAME_OVER":
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))

            win_text = "PLAYER WINS THE MATCH!" if self.winner == "PLAYER" else "COMPUTER WINS!"
            color = (80, 240, 100) if self.winner == "PLAYER" else (240, 80, 80)
            text_surf = self.font_big.render(win_text, True, color)
            screen.blit(
                text_surf,
                (self.width // 2 - text_surf.get_width() // 2, self.height // 2 - 45)
            )

            restart_surf = self.font_med.render(
                "Press [R] to Rematch", True, (240, 240, 240)
            )
            screen.blit(
                restart_surf,
                (self.width // 2 - restart_surf.get_width() // 2, self.height // 2 + 10)
            )

    def _render_banner(self, screen, text, y, fg, bg):
        surf = self.font_med.render(text, True, fg)
        rect = pygame.Rect(0, 0, self.width - 80, 34)
        rect.midtop = (self.width // 2, y)
        pygame.draw.rect(screen, bg, rect, border_radius=8)
        screen.blit(
            surf,
            (rect.centerx - surf.get_width() // 2, rect.centery - surf.get_height() // 2),
        )

    def _render_indicators(self, screen):
        """AI-state, exhaustion and counter-surge indicators (below the bar)."""
        if self.game_state != "PLAYING":
            return

        # AI state banner (always visible so states are clearly distinguished)
        remaining = max(0.0, self._ai_phase_duration() - self.ai_phase_time)
        if self.ai_state == AI_SURGE:
            blink = int(self.ai_phase_time * 6) % 2 == 0
            bg = (200, 30, 30) if blink else (140, 20, 20)
            self._render_banner(
                screen, f"!! WARNING: AI SURGE !!  {remaining:.1f}s", 490,
                (255, 255, 255), bg)
        elif self.ai_state == AI_COOLDOWN:
            self._render_banner(
                screen, f"AI COOLDOWN - weakened  {remaining:.1f}s", 490,
                (255, 255, 255), (40, 100, 190))
        else:
            self._render_banner(
                screen, "AI: normal resistance", 490,
                (210, 210, 210), (50, 55, 65))

        # Player exhaustion
        if self.exhausted:
            self._render_banner(
                screen, "EXHAUSTED - recovering, cannot push!", 535,
                (30, 20, 0), (255, 160, 30))
        # Counter-surge bonus (or the 'push now!' prompt during the window)
        elif self.counter_bonus_time > 0.0:
            self._render_banner(
                screen,
                f"COUNTER-SURGE! x{COUNTER_SURGE_PUSH_MULTIPLIER:g} PUSH + FAST RECOVERY  "
                f"{self.counter_bonus_time:.1f}s",
                535, (40, 30, 0), (255, 210, 60))
        elif self.counter_window_time > 0.0:
            self._render_banner(
                screen, "PUSH NOW for COUNTER-SURGE!", 535,
                (255, 255, 255), (60, 160, 90))