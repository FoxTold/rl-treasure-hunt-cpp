#pragma once

#include "SFML/Graphics.hpp"

namespace{
    constexpr int GRID_SIZE = 6;

    struct Position{
        int x;
        int y;
    };
}
class Game{
    public:
        Game() : _window(sf::RenderWindow({ 800u, 800u }, "Tresure Hunt")) 
        {

        };
        ~Game();

        void run();
        void handleEvents();
        void update();
        void render();
    
    private:
        sf::RenderWindow _window;
        sf::RectangleShape _grid[GRID_SIZE][GRID_SIZE];
        
        void initGrid();
};