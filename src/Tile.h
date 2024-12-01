#pragma once
#include "SFML/Graphics.hpp"
#include "Vector2f.h"

class Tile{
public:
    Tile() = default;
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

private:
    sf::RectangleShape _shape;
    Vector2f _position;
    Vector2f _size;
    unsigned char _idx = 0;
};