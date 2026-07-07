class GameData:
    def __init__(self, total_lives: int,
                 total_time: int,
                 points_per_pacgum: int,
                 points_per_super_pacgum: int,
                 points_per_ghost: int,
                 seed: int
                 ):
        self._lives = total_lives
        self._game_time = total_time
        self._points_per_pacgum_config = points_per_pacgum
        self._points_per_super_pacgum_config = points_per_super_pacgum
        self._points_per_ghost_config = points_per_ghost
        self._death_malus = 100
        self._kill = 0
        self._nb_death = 0
        self._score = 0
        self._seed_config = seed
        self._is_lose = False

    @property
    def lives(self) -> int:
        return self._lives

    @property
    def score(self) -> int:
        return self._score

    @property
    def game_time(self) -> int:
        return self._game_time

    @property
    def points_per_pacgum_config(self) -> int:
        return self._points_per_pacgum_config

    @property
    def points_per_super_pacgum_config(self) -> int:
        return self._points_per_super_pacgum_config

    @property
    def points_per_ghost_config(self) -> int:
        return self._points_per_ghost_config

    @property
    def death_malus(self) -> int:
        return self._death_malus

    @property
    def kill(self) -> int:
        return self._kill

    @property
    def nb_death(self) -> int:
        return self._nb_death

    @property
    def seed_config(self) -> int:
        return self._seed_config

    def addLives(self, amount: int = 1) -> None:
        if amount > 0:
            self._lives += amount

    def addScore(self, amount: int = 1) -> None:
        if amount > 0:
            self._score += amount

    def addKill(self, amount: int = 1) -> None:
        if amount > 0:
            self._kill += amount

    def removeLives(self, amount: int = 1) -> None:
        if amount > 0:
            self._lives = max(0, self._lives - amount)
            self._nb_death += amount

    def removeScore(self, amount: int = 1) -> None:
        if amount > 0:
            self._score -= amount

    def removeTime(self, amount: int = 1) -> None:
        if amount > 0:
            self._game_time -= amount

    def playerDead(self) -> None:
        self.removeLives(1)
        self.removeScore(self.death_malus)
