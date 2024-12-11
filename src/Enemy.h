#pragma once
#include "SFML/Graphics.hpp"
#include "Tile.h"

class Enemy{
public:
    Enemy()
    {
        if (!texture.loadFromFile(std::string("player_sprite.png")))
		{
			throw new std::exception("Couldn't load player sprite...");
		}
		sprite.setTexture(texture);
		sprite.scale(1.2f, 1.2f);
		sprite.setTextureRect(sf::IntRect(128, 0, -128, 100));
		sprite.move(playerOffset);
		sprite.setColor(sf::Color::Red);
		_currentTile = std::make_shared<Tile>();
    }

	void setTile(const std::shared_ptr<Tile>& tile)
	{
		_currentTile->setEnemy(false);
		_currentTile = tile;
		_currentTile->setEnemy(true);
		const auto pos = _currentTile->getPosition();
		sprite.setPosition(pos.x, pos.y);
		sprite.move(playerOffset);

	}
	std::shared_ptr<Tile> getTile()
	{
		return _currentTile;
	}
	unsigned char getTileIdx()
	{
		return _currentTile->getIdx();
	}
	void render(sf::RenderWindow& window)
	{
		window.draw(sprite);

	}
	int x_dir = 1;

    private:
	sf::Sprite sprite;
	sf::Texture texture;
	
	sf::Vector2f position;
	std::shared_ptr<Tile> _currentTile;

	sf::Vector2f playerOffset { 10.f,0.2f };
	int reward = { 0 };
};