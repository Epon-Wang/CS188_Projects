# Project 3 - Reinforcement Learning
- **Value Iteration**

    Rollout Value Iteration policy for 10 Episodes after 100 Iterations (press any key to begin)
    ```bash
    python gridworld.py -a value -i 100 -k 10
    ```
    Rollout Proritized Sweeping Value Iteration policy for 1 Episode after 1000 Iterations (press any key to begin)
    ```bash
    python gridworld.py -a priosweepvalue -i 1000
    ```
- **Q-Learning**

    Q-Learning Agent, run for 100 Episodes with $\epsilon = 0.9$
    ```bash
    python gridworld.py -a q -k 100 --noise 0.0 -e 0.9
    ```
    Q-Learning Robot Crawler
    ```bash
    python crawler.py
    ```
    Q-Learning Pacman in a small grid
    - run for 2010 Episodes (2000 training + 10 rollout)
        ```bash
        python pacman.py -p PacmanQAgent -x 2000 -n 2010 -l smallGrid
        ```
    - watch 10 Training Episodes
        ```bash
        python pacman.py -p PacmanQAgent -n 10 -l smallGrid -a numTraining=10
        ```
    Approximate Q-Learning Pacman
    - in a small grid, run for 2010 Episodes (2000 training + 10 rollout)
        ```bash
        python pacman.py -p ApproximateQAgent -x 2000 -n 2010 -l smallGrid
        ```
    - in a larger layout, run for 60 Episodes (50 training + 10 rollout)
        ```bash
        python pacman.py -p ApproximateQAgent -a extractor=SimpleExtractor -x 50 -n 60 -l mediumClassic
        ```