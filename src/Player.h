#pragma once
#include "SFML/Graphics.hpp"


class Player {
public: 
	Player() {
		
		if (!texture.loadFromFile(std::string("player_sprite.png")))
		{
			throw new std::exception("Couldn't load player sprite...");
		}
		sprite.setTexture(texture);
		sprite.scale(1.2f, 1.2f);
		sprite.setTextureRect(sf::IntRect(128, 0, -128, 100));
		sprite.move(playerOffset);
		_currentTile = std::make_shared<Tile>();

	};
	~Player() = default;

	void draw(sf::RenderWindow& window)
	{
		window.draw(sprite);
	}

	void setTile(const std::shared_ptr<Tile>& tile)
	{
		_currentTile->setPlayer(false);
		_currentTile = tile;
		_currentTile->setPlayer(true);
		const auto pos = _currentTile->getPosition();
		sprite.setPosition(pos.x,pos.y);
		sprite.move(playerOffset);
		if (_currentTile->hasCoin())
		{
			_currentTile->setCoin(false);
			// GIVE REWARD
			reward = 10;
		}
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
	int getReward()
	{
		auto rew = reward;
		reward = 0;
		return rew;
	}
private:
	sf::Sprite sprite;
	sf::Texture texture;
	
	sf::Vector2f position;
	std::shared_ptr<Tile> _currentTile;

	sf::Vector2f playerOffset { 10.f,0.2f };
	int reward = { 0 };
};