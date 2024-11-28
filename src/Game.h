#pragma once

#include "SFML/Graphics.hpp"

namespace{
    constexpr int GRID_SIZE = 5;

    struct Position{
        int x;
        int y;
    };
}
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
        sf::VertexArray grid();
        
        //void initGrid();
};