class GameData:
    """Tracks the mutable state of a single game session."""

    def __init__(self, total_lives: int,
                 total_time: int,
                 points_per_pacgum: int,
                 points_per_super_pacgum: int,
                 points_per_ghost: int,
                 seed: int
                 ):
        """Initialize the game session's state.

        Args:
            total_lives (int): Starting lives.
            total_time (int): Level time limit, in seconds.
            points_per_pacgum (int): Points per regular pac-gum.
            points_per_super_pacgum (int): Points per super pac-gum.
            points_per_ghost (int): Points per ghost eaten.
            seed (int): Maze generation seed.

        Returns:
            None.
        """
        self._setup_lives = total_lives
        self._lives = total_lives
        self._toggle_infinite_lives = False
        self._game_time = total_time
        self._saved_time = total_time
        self._points_per_pacgum_config = points_per_pacgum
        self._points_per_super_pacgum_config = points_per_super_pacgum
        self._points_per_ghost_config = points_per_ghost
        self._death_malus = 100
        self._kill = 0
        self._nb_death = 0
        self._score = 0
        self._seed_config = seed
        self._is_lose = False
        self._level_num = 1

    @property
    def lives(self) -> int:
        """int: Number of lives the player currently has remaining."""
        return self._lives

    @property
    def level_num(self) -> int:
        """int: The current level number (starting at 1)."""
        return self._level_num

    @property
    def score(self) -> int:
        """int: The player's current score."""
        return self._score

    @property
    def game_time(self) -> int:
        """int: Remaining time for the current level, in seconds."""
        return self._game_time

    @property
    def points_per_pacgum_config(self) -> int:
        """int: Points awarded for eating a regular pac-gum."""
        return self._points_per_pacgum_config

    @property
    def points_per_super_pacgum_config(self) -> int:
        """int: Points awarded for eating a super pac-gum."""
        return self._points_per_super_pacgum_config

    @property
    def points_per_ghost_config(self) -> int:
        """int: Points awarded for eating a ghost."""
        return self._points_per_ghost_config

    @property
    def death_malus(self) -> int:
        """int: Points deducted from the score when the player dies."""
        return self._death_malus

    @property
    def kill(self) -> int:
        """int: Number of ghosts eaten by the player so far."""
        return self._kill

    @property
    def nb_death(self) -> int:
        """int: Number of times the player has died so far."""
        return self._nb_death

    @property
    def toggle_infinite_lives(self) -> bool:
        """bool: Whether the infinite-lives cheat is currently enabled."""
        return self._toggle_infinite_lives

    @property
    def seed_config(self) -> int:
        """int: The seed used for maze generation."""
        return self._seed_config

    def addLives(self, amount: int = 1) -> None:
        """Increase the player's life count.

        Args:
            amount (int): Lives to add.

        Returns:
            None.
        """
        if amount > 0:
            self._lives += amount

    def addLevel(self, amount: int = 1) -> None:
        """Increase the current level number.

        Args:
            amount (int): Levels to advance by.

        Returns:
            None.
        """
        if amount > 0:
            self._level_num += amount

    def addScore(self, amount: int = 1) -> None:
        """Increase the player's score.

        Args:
            amount (int): Points to add.

        Returns:
            None.
        """
        if amount > 0:
            self._score += amount

    def addKill(self, amount: int = 1) -> None:
        """Increase the player's ghost-kill count.

        Args:
            amount (int): Kills to add.

        Returns:
            None.
        """
        if amount > 0:
            self._kill += amount

    def removeLives(self, amount: int = 1) -> None:
        """Decrease the life count and record the death(s).

        Args:
            amount (int): Lives to remove.

        Returns:
            None.
        """
        if amount > 0:
            self._lives = max(0, self._lives - amount)
            self._nb_death += amount
            if not self._toggle_infinite_lives:
                self._setup_lives -= amount

    def removeScore(self, amount: int = 1) -> None:
        """Decrease the player's score.

        Args:
            amount (int): Points to subtract.

        Returns:
            None.
        """
        if amount > 0:
            self._score -= amount

    def removeTime(self, amount: int = 1) -> None:
        """Decrease the remaining level time.

        Args:
            amount (int): Seconds to subtract.

        Returns:
            None.
        """
        if amount > 0:
            self._game_time -= amount

    def playerDead(self) -> None:
        """Record a player death, removing one life.

        Returns:
            None.
        """
        self.removeLives(1)

    def eatGhost(self) -> None:
        """Award a kill and points for eating a ghost.

        Returns:
            None.
        """
        self.addKill()
        self.addScore(self.points_per_ghost_config)

    def infiniteLives(self) -> None:
        """Toggle the infinite-lives cheat on or off.

        Returns:
            None.
        """
        self._toggle_infinite_lives = not self._toggle_infinite_lives
        if self._toggle_infinite_lives:
            self._lives = 9999999999999999
        else:
            self._lives = self._setup_lives

    def resetTimer(self) -> None:
        """Reset the remaining level time to its saved starting value.

        Returns:
            None.
        """
        self._game_time = self._saved_time
