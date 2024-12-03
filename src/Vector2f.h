#pragma once

struct Vector2f{
    float x = 0;
    float y = 0;

    Vector2f() = default;
    Vector2f(float x, float y) : x(x), y(y) {};
    Vector2f(const Vector2f& pos) : x(pos.x), y(pos.y) {};
    
    ~Vector2f() = default;


};
