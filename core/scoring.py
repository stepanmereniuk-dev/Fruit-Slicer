"""
Scoring - Point calculation and combo management.

Rules:
- 1 fruit = 1 point
- N fruits in one stroke = N + (N-1) points
- Multiplier (x2, x4, x6...) applies to the total
"""


class ScoringManager:
    """Manages the score and multipliers."""
    
    def __init__(self):
        self.score = 0
        self.multiplier = 1
        self.multiplier_timer = 0.0
        
        # Stats for achievements
        self.total_fruits_sliced = 0
        self.total_combos = 0
        self.max_combo = 0
    
    def reset(self):
        """Resets the score to zero for a new game."""
        self.score = 0
        self.multiplier = 1
        self.multiplier_timer = 0.0
        self.total_fruits_sliced = 0
        self.total_combos = 0
        self.max_combo = 0
    
    def add_sliced_fruits(self, count: int) -> int:
        """
        Adds points for sliced fruits.
        Returns the points earned.
        """
        if count <= 0:
            return 0
        
        # Point calculation: N fruits = N + (N-1)
        base_points = count + (count - 1) if count > 1 else 1
        
        # Apply multiplier
        points = base_points * self.multiplier
        
        self.score += points
        self.total_fruits_sliced += count
        
        # Combo stats
        if count >= 3:
            self.total_combos += 1
            self.max_combo = max(self.max_combo, count)
        
        return points
    
    def apply_bomb_penalty(self, penalty: int):
        """Deducts points (challenge mode)."""
        self.score = max(0, self.score - penalty)
    
    def activate_multiplier(self, multiplier: int, duration: float):
        """Activates a temporary multiplier."""
        self.multiplier = multiplier
        self.multiplier_timer = duration
    
    def increase_multiplier(self, increment: int, duration: float):
        """Increases the existing multiplier."""
        self.multiplier += increment
        self.multiplier_timer = duration
    
    def update(self, dt: float):
        """Updates the multiplier timer."""
        if self.multiplier_timer > 0:
            self.multiplier_timer -= dt
            if self.multiplier_timer <= 0:
                self.multiplier = 1
                self.multiplier_timer = 0.0
    
    @property
    def has_multiplier(self) -> bool:
        return self.multiplier > 1


class BonusGauge:
    """
    Bonus gauge that fills with identical fruit pairs.
    5 notches = multiplier activation.
    """
    
    MAX_CRANS = 5
    MULTIPLIER_DURATION = 10.0
    MULTIPLIER_INCREMENT = 2
    
    def __init__(self):
        self.crans = 0
    
    def reset(self):
        self.crans = 0
    
    def add_cran(self) -> bool:
        """
        Adds a notch to the gauge.
        Returns True if the gauge is full.
        """
        self.crans += 1
        if self.crans >= self.MAX_CRANS:
            self.crans = 0
            return True
        return False
    
    def get_fill_ratio(self) -> float:
        """Returns the fill ratio (0.0 to 1.0)."""
        return self.crans / self.MAX_CRANS