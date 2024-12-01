#include "Map.h"

namespace {
	const int TILE_SIZE = SCREEN_SIZE / GRID_SIZE;
}
void Map::render(sf::RenderWindow& window)
{
	for (auto& tile : _tiles)
	{
		window.draw(tile.getShape());
	}
}
void Map::initTiles()
{
    for (int i = 0; i < GRID_SIZE; ++i)
    {
        for (int j = 0; j < GRID_SIZE; ++j)
        {
            Tile tile; 
            tile.setPosition({i * TILE_SIZE * 1.f, j * TILE_SIZE * 1.f});
            tile.setSize({ TILE_SIZE * 1.f, TILE_SIZE * 1.f });
            const auto idx = static_cast<unsigned char>(i * GRID_SIZE + j);
            tile.setIdx(idx);
            
            tile.setFillColor(sf::Color::Black);
            tile.setOutlineColor(sf::Color::White);

            tile.setOutlineThickness(1.f);
            _tiles.push_back(tile);
        }
    }
}
