"""
Scoring - Calcul des points et gestion des combos.

Règles :
- 1 fruit = 1 point
- N fruits en un coup = N + (N-1) points
- Multiplicateur (x2, x4, x6...) s'applique au total
"""


class ScoringManager:
    """Gère le score et les multiplicateurs."""
    
    def __init__(self):
        self.score = 0
        self.multiplier = 1
        self.multiplier_timer = 0.0
        
        # Stats pour les succès
        self.total_fruits_sliced = 0
        self.total_combos = 0
        self.max_combo = 0
    
    def reset(self):
        """Remet le score à zéro pour une nouvelle partie."""
        self.score = 0
        self.multiplier = 1
        self.multiplier_timer = 0.0
        self.total_fruits_sliced = 0
        self.total_combos = 0
        self.max_combo = 0
    
    def add_sliced_fruits(self, count: int) -> int:
        """
        Ajoute des points pour les fruits tranchés.
        Retourne les points gagnés.
        """
        if count <= 0:
            return 0
        
        # Calcul des points : N fruits = N + (N-1)
        base_points = count + (count - 1) if count > 1 else 1
        
        # Application du multiplicateur
        points = base_points * self.multiplier
        
        self.score += points
        self.total_fruits_sliced += count
        
        # Stats combos
        if count >= 3:
            self.total_combos += 1
            self.max_combo = max(self.max_combo, count)
        
        return points
    
    def apply_bomb_penalty(self, penalty: int):
        """Retire des points (mode challenge)."""
        self.score = max(0, self.score - penalty)
    
    def activate_multiplier(self, multiplier: int, duration: float):
        """Active un multiplicateur temporaire."""
        self.multiplier = multiplier
        self.multiplier_timer = duration
    
    def increase_multiplier(self, increment: int, duration: float):
        """Augmente le multiplicateur existant."""
        self.multiplier += increment
        self.multiplier_timer = duration
    
    def update(self, dt: float):
        """Met à jour le timer du multiplicateur."""
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
    Jauge de bonus qui se remplit avec des paires de fruits identiques.
    5 crans = activation du multiplicateur.
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
        Ajoute un cran à la jauge.
        Retourne True si la jauge est pleine.
        """
        self.crans += 1
        if self.crans >= self.MAX_CRANS:
            self.crans = 0
            return True
        return False
    
    def get_fill_ratio(self) -> float:
        """Retourne le ratio de remplissage (0.0 à 1.0)."""
        return self.crans / self.MAX_CRANS
