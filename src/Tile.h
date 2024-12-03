#pragma once

#include "SFML/Graphics.hpp"
#include "Vector2f.h"
#include <format>
namespace
{
    const int GRID_SIZE = 5;
    const int SCREEN_SIZE = 800;
    const int TILE_SIZE = SCREEN_SIZE / GRID_SIZE;
}

class Tile{
public:
    Tile()
    {
        if (!_font.loadFromFile("Roboto.ttf"))
        {
            throw new std::exception("Couldnt load font");
        }
    };
    ~Tile() = default;

    void setPosition(const Vector2f& pos)
    {
        _position.x = pos.x;
        _position.y = pos.y;
        _shape.setPosition({ pos.x,pos.y });
    }

    void setSize(const Vector2f& size)
    {
        _size = size;
        _shape.setSize({ size.x,size.y });
    }

    void setIdx(const unsigned char& idx)
    {
        _idx = idx;
        _text.setFont(_font);
        _text.setString(std::format("{}", _idx));
        _text.setCharacterSize(12);
        _text.setPosition(_shape.getPosition());
    }

    void setFillColor(const sf::Color& color)
    {
        _shape.setFillColor(color);
    }

    void setOutlineColor(const sf::Color& color)
    {
        _shape.setOutlineColor(color);
    }

    void setOutlineThickness(float thick)
    {
        _shape.setOutlineThickness(thick);
    }

    Vector2f getPosition() const
    {
        return _position;
    }

    sf::RectangleShape& getShape()
    {
        return _shape;
    }

    unsigned char getIdx() {
        return _idx;
    }
    
    bool hasCoin() {
        return _hasCoin;
    }

    bool hasPlayer() {
        return _hasPlayer;
    }

    bool hasEnemy()
    {
        return _hasEnemy;
    }
    void setCoin(const bool hasCoin)
    {
        _hasCoin = hasCoin;
    }
    void setPlayer(const bool hasPlayer)
    {
        _hasPlayer = hasPlayer;
    }
    void setEnemy(const bool hasEnemy)
    {
        _hasEnemy = hasEnemy;
    }

    void drawCoin(sf::RenderWindow& window)
    {
        const auto coinSize = 20;
        sf::CircleShape coin(coinSize);
        coin.setFillColor(sf::Color::Yellow);
        sf::Vector2f vec;
        sf::Vector2f currVec = _shape.getPosition();
        vec.x = currVec.x + (TILE_SIZE / 2) - coinSize;
        vec.y = currVec.y + (TILE_SIZE / 2) - coinSize;
        coin.setPosition(vec);
        window.draw(coin);
    }

    void render(sf::RenderWindow& window)
    {
        window.draw(_shape);
        if (1 == _hasCoin)
        {
            drawCoin(window);
        }
        window.draw(_text);
    }

private:
    sf::RectangleShape _shape;
    Vector2f _position;
    Vector2f _size;

    bool _hasCoin { false };
    bool _hasPlayer{ false };
    bool _hasEnemy{ false };

    unsigned char _idx = 0;

    sf::Font _font;
    sf::Text _text;
};