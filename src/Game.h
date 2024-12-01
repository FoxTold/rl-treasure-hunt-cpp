#pragma once

#include "SFML/Graphics.hpp"
#include "Map.h"
class Game{
    public:
        Game() : _window(sf::RenderWindow({ 800u, 800u }, "Tresure Hunt")) 
        {
            _window.setFramerateLimit(30);
        };
        ~Game() {};

        void run();
        void handleEvents();
        //void update();
        void render();
    
    private:
        sf::RenderWindow _window;
        Map _map;
        //void initGrid();
};