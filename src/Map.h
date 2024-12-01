#pragma once

#include "SFML/Graphics.hpp"
#include "Tile.h"
namespace
{
    const int GRID_SIZE = 10;
    const int SCREEN_SIZE = 800;
}
class Map{
public:
    Map()
    {
        _tiles.reserve(GRID_SIZE * GRID_SIZE);
        initTiles();
    }
    ~Map() = default;


    void render(sf::RenderWindow& window);
private:
    void initTiles();
    std::vector<Tile> _tiles;

};