#include <SFML/Graphics.hpp>
#include "Game.h"
int main()
{
	auto env = Game();
	
	env.run();

	return 0;
}