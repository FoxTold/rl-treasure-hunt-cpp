#include "Game.h"
#include <chrono>
void Game::run()
{
	while (_window.isOpen())
	{
        handleEvents();
        

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
    }
}

void Game::render()
{
    _window.clear();

    //Render thing here.

    _window.display();
}
