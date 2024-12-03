#include "Game.h"
#include <iostream>
#include <format>
#include <random>

namespace {
    constexpr int N_COINS = 15;
}

void Game::run()
{
	while (_window.isOpen())
	{
        handleEvents();
        
        std::cout << "State: " << getState() << '\n';
        render();
	}
}

void Game::handleEvents()
{
    for (auto event = sf::Event(); _window.pollEvent(event);)
    {
        if (event.type == sf::Event::Closed)
        {
            _window.close();
        }

        if (event.type == sf::Event::KeyReleased) {
            const auto idx = _player.getTileIdx();
            if (event.key.code == sf::Keyboard::Left) {
                _player.setTile(_tiles[idx - 1]);
            }
            else if (event.key.code == sf::Keyboard::Right) {
                _player.setTile(_tiles[idx + 1]);
            }
            else if (event.key.code == sf::Keyboard::Up) {
                _player.setTile(_tiles[idx - GRID_SIZE]);
            }
            else if (event.key.code == sf::Keyboard::Down) {
                _player.setTile(_tiles[idx + GRID_SIZE]);
            }
        }
    }
}

void Game::renderPlayer()
{
	_player.render(_window);
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
            state.push_back(' ');
        }
    }
    return state;
}

void Game::initTiles()
{
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

    std::mt19937 gen(42);
    std::uniform_int_distribution<> dist(1, 98);

    for (int i = 0; i < N_COINS; ++i)
    {
        int idx = dist(gen);
        _tiles[idx]->setCoin(true);
    }
}

void Game::renderTiles()
{
    for (auto& tile : _tiles)
    {
        tile->render(_window);
    }
}
