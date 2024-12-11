#pragma once

#include "SFML/Graphics.hpp"
#include "Tile.h"
#include "Player.h"
#include "Enemy.h"
enum Action
{
	LEFT,
    RIGHT,
    UP,
    DOWN
};
struct EnvReturnValue
{
    int reward;
    std::string nextState;
    bool isDone;

};
class Game{
    public:
        Game(int fps) : _window(sf::RenderWindow({ 800u, 800u }, "Tresure Hunt")) 
        {
            _window.setFramerateLimit(fps);
            initTiles();
            _player.setTile(_tiles[0]);
        };
        ~Game() = default;

        void handleEvents();
        void renderPlayer();
        //void update();
        std::shared_ptr<EnvReturnValue> step(Action action);
        void render();
        std::string reset();
        bool isDone();
        int calculateReward();
    private:
        sf::RenderWindow _window;
        std::vector<std::shared_ptr<Tile>> _tiles;
        
        Player _player;
        Enemy _enemy;
        bool _done { false };
        void initTiles();
        void renderTiles();
        std::string getState();
        int pendingReward = { 0 };

};
