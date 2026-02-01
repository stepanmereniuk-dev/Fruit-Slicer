"""
GameScene - Main game screen.
Handles gameplay: fruits, bombs, ice flowers, score, hearts, freeze.
"""

import pygame
import os
from typing import List, Union, Optional

from scenes.base_scene import BaseScene
from config import (
    IMAGES_DIR, FONTS_DIR, WINDOW_WIDTH, WINDOW_HEIGHT,
    Images, Layout, TextColors, GameConfig, DIFFICULTY, FONT_FILE
)
from core import lang_manager
from core.scoring import ScoringManager, BonusGauge
from core.spawner import Spawner
from core.input_handler import InputHandler
from core.achievements import AchievementManager
from entities import Fruit, Bomb, Ice
from entities.splash import Splash
from ui.buttons import ImageButton


Entity = Union[Fruit, Bomb, Ice]


class GameScene(BaseScene):
    """Game scene - classic and challenge modes."""
    
    # Font size for score
    SCORE_FONT_SIZE = 40
    
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        
        # Resources
        self.background = None
        self.font_score = None
        self.font_letter = None
        
        # HUD images
        self.coin_img = None  # TODO: add coin image
        self.heart_full_img = None
        self.heart_empty_img = None
        self.gauge_img = None
        self.gauge_segments = []  # [yellow, orange, red, purple, blue]
        self.timer_frame_img = None  # Timer frame (challenge mode)
        
        # Buttons
        self.btn_gear: Optional[ImageButton] = None
        self.btn_cross: Optional[ImageButton] = None
        
        # Components
        self.scoring = ScoringManager()
        self.bonus_gauge = BonusGauge()
        self.spawner = None
        self.input_handler = None
        self.achievement_manager = None
        
        # Game state
        self.entities: List[Entity] = []
        self.splashes: List[Splash] = []  # Active splashes
        self.hearts = GameConfig.MAX_HEARTS
        self.game_time = 0.0
        self.is_frozen = False
        self.freeze_timer = 0.0
        self.game_over = False
        self.exploded = False  # Game over by bomb
        
        # Accumulation of fruits sliced during a mouse stroke
        self._stroke_sliced_fruits: List[Fruit] = []
        self._was_slicing = False
        
        # Game mode
        self.mode = 'classic'  # 'classic' or 'challenge'
        self.difficulty = 'normal'
        self.challenge_timer = 0.0
    
    def setup(self):
        """Initializes the game."""
        # Retrieve data from scene_manager
        self.mode = self.scene_manager.shared_data.get('mode', 'classic')
        self.difficulty = self.scene_manager.shared_data.get('difficulty', 'normal')
        control_mode = self.scene_manager.shared_data.get('control_mode', 'mouse')
        
        # Load resources
        self._load_resources()
        
        # Initialize components
        if self.mode == 'challenge':
            self.spawner = Spawner('challenge')
            self.challenge_timer = DIFFICULTY['challenge']['duration']
        else:
            self.spawner = Spawner(self.difficulty)
        
        self.input_handler = InputHandler(control_mode)
        
        # Reset state
        self.entities.clear()
        self.splashes.clear()
        self.scoring.reset()
        self.bonus_gauge.reset()
        self.hearts = GameConfig.MAX_HEARTS
        self.game_time = 0.0
        self.is_frozen = False
        self.freeze_timer = 0.0
        self.game_over = False
        self.exploded = False
        self._stroke_sliced_fruits.clear()
        self._was_slicing = False
        
        # Start achievement tracking
        if self.achievement_manager:
            self.achievement_manager.start_new_game(control_mode)
    
    def _load_resources(self):
        """Loads images and fonts."""
        # Background depending on mode
        if self.mode == 'challenge':
            bg_path = os.path.join(IMAGES_DIR, Images.CHALLENGE_BG)
        else:
            bg_path = os.path.join(IMAGES_DIR, Images.GAME_BG)
        self.background = pygame.image.load(bg_path).convert()
        
        # Fonts
        font_path = os.path.join(FONTS_DIR, FONT_FILE)
        self.font_score = pygame.font.Font(font_path, self.SCORE_FONT_SIZE)
        self.font_letter = pygame.font.Font(font_path, 24)
        
        # Hearts
        self.heart_full_img = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.HEART_FULL)
        ).convert_alpha()
        self.heart_empty_img = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.HEART_EMPTY)
        ).convert_alpha()
        
        # Gauge
        self.gauge_img = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.GAUGE)
        ).convert_alpha()
        
        # Gauge segments
        segment_paths = [
            Images.GAUGE_YELLOW,
            Images.GAUGE_ORANGE,
            Images.GAUGE_RED,
            Images.GAUGE_PURPLE,
            Images.GAUGE_BLUE,
        ]
        self.gauge_segments = []
        for path in segment_paths:
            img = pygame.image.load(os.path.join(IMAGES_DIR, path)).convert_alpha()
            self.gauge_segments.append(img)
        
        # Timer frame (challenge mode only)
        if self.mode == 'challenge':
            self.timer_frame_img = pygame.image.load(
                os.path.join(IMAGES_DIR, Images.CHALLENGE_TIMER_FRAME)
            ).convert_alpha()
        
        # Buttons (gear and cross)
        self.btn_gear = ImageButton(
            image_path=Images.GEAR,
            center=Layout.GAME_GEAR,
            on_click=self._on_settings
        )
        self.btn_cross = ImageButton(
            image_path=Images.CROSS,
            center=Layout.GAME_CROSS,
            on_click=self._on_quit
        )
    
    def set_achievement_manager(self, manager: AchievementManager):
        """Sets the achievement manager."""
        self.achievement_manager = manager
    
    # Button callbacks
    def _on_settings(self):
        # TODO: open settings in pause
        pass
    
    def _on_quit(self):
        # Back to menu
        self.scene_manager.change_scene('menu')
    
    def handle_events(self, events: List[pygame.event.Event]):
        if self.game_over:
            return
        
        for event in events:
            # HUD buttons
            self.btn_gear.handle_event(event)
            self.btn_cross.handle_event(event)
            
            # Pass to input handler
            self.input_handler.handle_event(event)
            
            # Escape shortcut to quit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self._on_quit()
    
    def update(self, dt: float):
        if self.game_over:
            return
        
        self.game_time += dt
        
        # Challenge mode: countdown timer
        if self.mode == 'challenge':
            self.challenge_timer -= dt
            if self.challenge_timer <= 0:
                self._end_game()
                return
        
        # Freeze handling
        if self.is_frozen:
            self.freeze_timer -= dt
            if self.freeze_timer <= 0:
                self._unfreeze_all()
        
        # Update multiplier
        self.scoring.update(dt)
        
        # Spawn new entities (unless frozen)
        if not self.is_frozen:
            keyboard_mode = self.input_handler.mode == "keyboard"
            new_entities = self.spawner.update(dt, keyboard_mode)
            self.entities.extend(new_entities)
        
        # Update entities
        for entity in self.entities:
            entity.update(dt)
        
        # Update splashes
        for splash in self.splashes:
            splash.update(dt)
        
        # Detect slices
        sliced = self.input_handler.get_sliced_entities(self.entities)
        if sliced:
            self._process_sliced(sliced)
        
        # Check end of mouse stroke to calculate combo score
        is_slicing = self.input_handler.is_slicing()
        if self._was_slicing and not is_slicing:
            # End of stroke: calculate score for all accumulated fruits
            self._finalize_stroke()
        self._was_slicing = is_slicing
        
        # Check if freeze should end (no more frozen fruits)
        self._check_freeze_end()
        
        # Check entities that went off-screen
        self._check_missed_entities()
        
        # Clean up dead entities and finished splashes
        self._cleanup_entities()
        self.splashes = [s for s in self.splashes if not s.finished]
        
        # Update time for achievements
        if self.achievement_manager:
            self.achievement_manager.on_time_update(self.game_time)
    
    def _finalize_stroke(self):
        """Finalizes a mouse stroke: calculates score and bonuses."""
        if not self._stroke_sliced_fruits:
            return
        
        fruits = self._stroke_sliced_fruits
        count = len(fruits)
        
        # Calculate points (combo if multiple fruits)
        points = self.scoring.add_sliced_fruits(count)
        
        # Check identical pairs for bonus gauge
        fruit_types = [f.fruit_type for f in fruits]
        for fruit_type in set(fruit_types):
            if fruit_types.count(fruit_type) >= 2:
                if self.bonus_gauge.add_cran():
                    self._activate_multiplier()
        
        # Achievements
        if self.achievement_manager:
            self.achievement_manager.on_fruit_sliced(count)
            self.achievement_manager.on_score_update(self.scoring.score)
        
        # Reset for next stroke
        self._stroke_sliced_fruits.clear()
    
    def _process_sliced(self, sliced: List[Entity]):
        """Processes sliced entities."""
        fruits_sliced = []
        bomb_sliced = False
        ice_sliced = False
        
        for entity in sliced:
            entity.slice()
            
            # Release the letter
            if entity.letter:
                self.spawner.release_letter(entity.letter)
            
            if isinstance(entity, Fruit):
                fruits_sliced.append(entity)
            elif isinstance(entity, Bomb):
                bomb_sliced = True
            elif isinstance(entity, Ice):
                ice_sliced = True
        
        # Priority: bomb > ice > fruits
        if bomb_sliced:
            self._on_bomb_sliced()
            return
        
        if ice_sliced:
            self._on_ice_sliced()
        
        if fruits_sliced:
            self._on_fruits_sliced(fruits_sliced)
    
    def _on_fruits_sliced(self, fruits: List[Fruit]):
        """Called when fruits are sliced (accumulates for stroke)."""
        # Create splashes immediately
        for fruit in fruits:
            cx, cy = fruit.center
            splash = Splash(fruit.fruit_type, cx, cy)
            self.splashes.append(splash)
        
        # Mouse mode: accumulate for end-of-stroke combo
        if self.input_handler.mode == "mouse":
            self._stroke_sliced_fruits.extend(fruits)
        else:
            # Keyboard mode: process immediately (one key = one group)
            count = len(fruits)
            self.scoring.add_sliced_fruits(count)
            
            # Check identical pairs for bonus gauge
            fruit_types = [f.fruit_type for f in fruits]
            for fruit_type in set(fruit_types):
                if fruit_types.count(fruit_type) >= 2:
                    if self.bonus_gauge.add_cran():
                        self._activate_multiplier()
            
            # Achievements
            if self.achievement_manager:
                self.achievement_manager.on_fruit_sliced(count)
                self.achievement_manager.on_score_update(self.scoring.score)
    
    def _on_bomb_sliced(self):
        """Called when a bomb is sliced."""
        if self.mode == 'challenge':
            # Challenge mode: point penalty
            penalty = DIFFICULTY['challenge']['bomb_penalty']
            self.scoring.apply_bomb_penalty(penalty)
        else:
            # Classic mode: instant game over
            self.exploded = True
            self._end_game()
    
    def _on_ice_sliced(self):
        """Called when an ice flower is sliced."""
        # Get freeze duration based on difficulty
        if self.mode == 'challenge':
            return  # No ice flowers in challenge mode
        
        freeze_duration = DIFFICULTY.get(self.difficulty, DIFFICULTY['normal']).get('freeze_duration', 4.0)
        self._freeze_all(freeze_duration)
        
        if self.achievement_manager:
            self.achievement_manager.on_ice_sliced()
    
    def _freeze_all(self, duration: float):
        """Freezes all fruits (not bombs or ice flowers)."""
        self.is_frozen = True
        self.freeze_timer = duration
        
        # Freeze only unsliced fruits
        for entity in self.entities:
            if isinstance(entity, Fruit) and not entity.sliced:
                entity.freeze()
    
    def _unfreeze_all(self):
        """Unfreezes all entities."""
        self.is_frozen = False
        self.freeze_timer = 0.0
        
        for entity in self.entities:
            if isinstance(entity, Fruit):
                entity.unfreeze()
    
    def _check_freeze_end(self):
        """Checks if freeze should end (no more frozen fruits)."""
        if not self.is_frozen:
            return
        
        # Count still-frozen (unsliced) fruits
        frozen_fruits = [
            e for e in self.entities 
            if isinstance(e, Fruit) and e.frozen and not e.sliced
        ]
        
        if len(frozen_fruits) == 0:
            self._unfreeze_all()
    
    def _activate_multiplier(self):
        """Activates multiplier when gauge is full."""
        if self.scoring.has_multiplier:
            # Increase existing multiplier
            self.scoring.increase_multiplier(
                BonusGauge.MULTIPLIER_INCREMENT,
                BonusGauge.MULTIPLIER_DURATION
            )
        else:
            # First multiplier
            self.scoring.activate_multiplier(2, BonusGauge.MULTIPLIER_DURATION)
    
    def _check_missed_entities(self):
        """Checks entities that exited bottom of game zone."""
        for entity in self.entities:
            if entity.sliced or entity.missed:
                continue
            
            # Fruit is missed if it exits bottom of game zone
            if entity.y > GameConfig.GAME_ZONE_BOTTOM:
                entity.missed = True
                
                if isinstance(entity, Fruit):
                    self._on_fruit_missed()
                elif isinstance(entity, Bomb):
                    # Bomb avoided
                    if self.achievement_manager:
                        self.achievement_manager.on_bomb_avoided()
    
    def _on_fruit_missed(self):
        """Called when a fruit is missed."""
        if self.mode == 'challenge':
            return  # No penalty in challenge mode
        
        self.hearts -= 1
        
        if self.achievement_manager:
            self.achievement_manager.on_heart_lost()
        
        if self.hearts <= 0:
            self._end_game()
    
    def _cleanup_entities(self):
        """Removes entities that left the game zone."""
        self.entities = [
            e for e in self.entities
            if not (e.missed or e.y > GameConfig.GAME_ZONE_BOTTOM)
        ]
    
    def _end_game(self):
        """Ends the game."""
        self.game_over = True
        
        # Finalize achievements
        if self.achievement_manager:
            self.achievement_manager.end_game(self.exploded)
        
        # Save score
        self.scene_manager.shared_data['last_score'] = self.scoring.score
        self.scene_manager.shared_data['exploded'] = self.exploded
        # TODO: check for new record
        
        # Transition to game over
        self.scene_manager.change_scene('game_over')
    
    def render(self, screen: pygame.Surface):
        # Background
        screen.blit(self.background, (0, 0))
        
        # Set clip zone for entities (game zone only)
        game_zone_rect = pygame.Rect(
            GameConfig.GAME_ZONE_LEFT,
            GameConfig.GAME_ZONE_TOP,
            GameConfig.GAME_ZONE_SIZE[0],
            GameConfig.GAME_ZONE_SIZE[1]
        )
        screen.set_clip(game_zone_rect)
        
        # Splashes (behind entities)
        for splash in self.splashes:
            splash.render(screen)
        
        # Entities (clipped to game zone)
        for entity in self.entities:
            entity.render(screen, self.font_letter if self.input_handler.mode == "keyboard" else None)
        
        # Mouse trail (also clipped)
        if self.input_handler.mode == "mouse" and self.input_handler.is_slicing():
            self._render_trail(screen)
        
        # Remove clip for HUD
        screen.set_clip(None)
        
        # HUD (not clipped)
        self._render_hud(screen)
    
    def _render_trail(self, screen: pygame.Surface):
        """Renders the mouse trail."""
        points = self.input_handler.get_trail_points()
        if len(points) < 2:
            return
        
        # White line with fade effect
        for i in range(1, len(points)):
            alpha = int(255 * (i / len(points)))
            color = (255, 255, 255)
            pygame.draw.line(screen, color, points[i-1], points[i], 3)
    
    def _render_hud(self, screen: pygame.Surface):
        """Renders HUD (score, hearts/timer, gauge, buttons)."""
        # Score (top left, left-justified)
        self._render_score(screen)
        
        # Hearts or Timer (top center)
        if self.mode == 'challenge':
            self._render_timer(screen)
        else:
            self._render_hearts(screen)
        
        # Buttons (top right)
        self.btn_gear.render(screen)
        self.btn_cross.render(screen)
        
        # Bonus gauge (bottom center)
        self._render_gauge(screen)
    
    def _render_score(self, screen: pygame.Surface):
        """Renders score with multiplier if active."""
        # Format: "140387 x2 (10s)" or just "140387"
        score_text = f"{self.scoring.score}"
        
        if self.scoring.has_multiplier:
            score_text += f" x{self.scoring.multiplier}"
            timer_left = int(self.scoring.multiplier_timer)
            score_text += f" ({timer_left}s)"
        
        score_surface = self.font_score.render(score_text, True, TextColors.GAME_SCORE)
        
        # Same position for classic and challenge (left-justified)
        score_rect = score_surface.get_rect(left=Layout.GAME_SCORE_POS_CLASSIC[0], centery=Layout.GAME_SCORE_POS_CLASSIC[1])
        screen.blit(score_surface, score_rect)
    
    def _render_hearts(self, screen: pygame.Surface):
        """Renders the 3 hearts (classic mode)."""
        heart_positions = [
            Layout.GAME_HEART_1,
            Layout.GAME_HEART_2,
            Layout.GAME_HEART_3,
        ]
        
        for i, pos in enumerate(heart_positions):
            if i < self.hearts:
                img = self.heart_full_img
            else:
                img = self.heart_empty_img
            
            rect = img.get_rect(center=pos)
            screen.blit(img, rect)
    
    def _render_timer(self, screen: pygame.Surface):
        """Renders the timer with its frame (challenge mode)."""
        # Timer frame
        if self.timer_frame_img:
            frame_rect = self.timer_frame_img.get_rect(center=Layout.GAME_TIMER)
            screen.blit(self.timer_frame_img, frame_rect)
        
        # Timer text
        minutes = int(self.challenge_timer) // 60
        seconds = int(self.challenge_timer) % 60
        timer_text = f"{minutes}:{seconds:02d}"
        
        timer_surface = self.font_score.render(timer_text, True, TextColors.GAME_SCORE)
        timer_rect = timer_surface.get_rect(center=Layout.GAME_TIMER)
        screen.blit(timer_surface, timer_rect)
    
    def _render_gauge(self, screen: pygame.Surface):
        """Renders the bonus gauge with its segments."""
        # Gauge background
        gauge_rect = self.gauge_img.get_rect(center=Layout.GAME_GAUGE)
        screen.blit(self.gauge_img, gauge_rect)
        
        # Filled segments based on gauge level
        crans = self.bonus_gauge.crans
        for i in range(crans):
            if i < len(self.gauge_segments):
                segment_img = self.gauge_segments[i]
                segment_pos = Layout.GAME_GAUGE_SEGMENTS[i]
                segment_rect = segment_img.get_rect(center=segment_pos)
                screen.blit(segment_img, segment_rect)
    
    def cleanup(self):
        """Cleanup on scene exit."""
        self.entities.clear()
        if self.input_handler:
            self.input_handler.reset()