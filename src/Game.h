#pragma once

#include "SFML/Graphics.hpp"
#include "Tile.h"
#include "Player.h"

class Game{
    public:
        Game() : _window(sf::RenderWindow({ 800u, 800u }, "Tresure Hunt")) 
        {
            _window.setFramerateLimit(30);
            initTiles();
        };
        ~Game() = default;

        void run();
        void handleEvents();
        void renderPlayer();
        //void update();
        void render();
        std::string getState();
    private:
        sf::RenderWindow _window;
        std::vector<std::shared_ptr<Tile>> _tiles;
        
        Player _player;

        void initTiles();
        void renderTiles();

};
