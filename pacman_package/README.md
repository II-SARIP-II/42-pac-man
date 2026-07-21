# Pacman
## How to use

```sh
./pac-man.bin config.json
```

Example config:

```json
{
  "highscore_filename": "config/highscores.json",
  "levels": [
    {
      "width": 15,
      "height": 15
    },
    {
      "width": 6,
      "height": 6
    },
    {
      "width": 8,
      "height": 8
    },
    {
      "width": 10,
      "height": 10
    },
    {
      "width": 12,
      "height": 10
    },
    {
      "width": 14,
      "height": 12
    },
    {
      "width": 16,
      "height": 12
    },
    {
      "width": 18,
      "height": 14
    },
    {
      "width": 20,
      "height": 16
    },
    {
      "width": 22,
      "height": 18
    }
  ],
  "lives": 3,
  "points_per_pacgum": 10,
  "points_per_super_pacgum": 50,
  "points_per_ghost": 200,
  "seed": 42,
  "level_max_time": 120
}
```
