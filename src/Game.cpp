#include "Game.h"
#include <iostream>
#include <format>
#include <random>
#include "Tile.h"

void Game::handleEvents()
{
    for (auto event = sf::Event(); _window.pollEvent(event);)
    {
        if (event.type == sf::Event::Closed)
        {
            //_done = true;
            _window.close();
        }

        /*if (event.type == sf::Event::KeyReleased) {
            const auto idx = _player.getTileIdx();
            if (event.key.code == sf::Keyboard::Left) {
                if (idx % GRID_SIZE != 0)
                {
                    _player.setTile(_tiles[idx - 1]);
                }
            }
            else if (event.key.code == sf::Keyboard::Right) {
                if ( idx % GRID_SIZE != GRID_SIZE - 1)
                {
                    _player.setTile(_tiles[idx + 1]);
                }
            }
            else if (event.key.code == sf::Keyboard::Up) {
                if (idx - GRID_SIZE >= 0)
                {
                    _player.setTile(_tiles[idx - GRID_SIZE]);
                }
            }
            else if (event.key.code == sf::Keyboard::Down) {
                if (idx + GRID_SIZE < GRID_SIZE * GRID_SIZE)
                {
                    _player.setTile(_tiles[idx + GRID_SIZE]);
                }
            }
            else if (event.key.code == sf::Keyboard::R)
            {
                reset();
            }
        }*/
    }
}

void Game::renderPlayer()
{
	_player.render(_window);
}

std::shared_ptr<EnvReturnValue> Game::step(Action action)
{
    const auto idx = _player.getTileIdx();
    switch (action)
    {
    case LEFT:
        if (idx % GRID_SIZE != 0)
        {
            _player.setTile(_tiles[idx - 1]);
        }
        break;
    case RIGHT:
        if (idx % GRID_SIZE != GRID_SIZE - 1)
        {
            _player.setTile(_tiles[idx + 1]);
        }
        break;
    case UP:
        if (idx - GRID_SIZE >= 0)
        {
            _player.setTile(_tiles[idx - GRID_SIZE]);
        }
    case DOWN:
        if (idx + GRID_SIZE < GRID_SIZE * GRID_SIZE)
        {
            _player.setTile(_tiles[idx + GRID_SIZE]);
        }

    }
    std::shared_ptr<EnvReturnValue> value = std::make_shared<EnvReturnValue>();

    value->nextState = getState();
    value->reward = calculateReward();

    bool coinPresent = false;
    for (auto& tile : _tiles)
    {
        if (tile->hasCoin())
        {
            coinPresent = true;
            break;
        }
    }
    value->isDone = !coinPresent;
    return value;
}

void Game::render()
{
    _window.clear();

    //Render thing here.

    renderTiles();
    renderPlayer();
    //
    _window.display();
}

std::string Game::getState()
{
    std::string state;
    for (auto& tile : _tiles)
    {
        if (tile->hasEnemy())
        {
            state.push_back('E');
        }
        else if (tile->hasCoin())
        {
            state.push_back('C');
        }
        else if (tile->hasPlayer()) {
            state.push_back('P');
        }
        else {
            state.push_back('X');
        }
    }
    return state;
}

std::string Game::reset()
{
    initTiles();
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<int> distrib(0, GRID_SIZE - 1);
    _player.setTile(_tiles[distrib(gen)]);
    return getState();
}

bool Game::isDone()
{
    return _done;
}

int Game::calculateReward()
{
    int reward = 0;
    reward += _player.getReward();

    return reward;
}

void Game::initTiles()
{
    _tiles.clear();
    _tiles.reserve(GRID_SIZE * GRID_SIZE);

    for (int i = 0; i < GRID_SIZE; ++i)
    {
        for (int j = 0; j < GRID_SIZE; ++j)
        {
            std::shared_ptr<Tile> tile = std::make_shared<Tile>();
            tile->setPosition({ j * TILE_SIZE * 1.f, i * TILE_SIZE * 1.f });
            tile->setSize({ TILE_SIZE * 1.f, TILE_SIZE * 1.f });
            const auto idx = static_cast<unsigned char>(i * GRID_SIZE + j);
            tile->setIdx(idx);

            tile->setFillColor(sf::Color::Blue);
            tile->setOutlineColor(sf::Color::Cyan);

            tile->setOutlineThickness(1.f);
            _tiles.push_back(tile);
        }
    }
    _tiles[16]->setCoin(true);
    _tiles[13]->setCoin(true);
    _tiles[1]->setCoin(true);
}

void Game::renderTiles()
{
    for (auto& tile : _tiles)
    {
        tile->render(_window);
    }
}

