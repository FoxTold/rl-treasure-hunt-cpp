#include <SFML/Graphics.hpp>
#include <iostream>
#include "Game.h"
#include <format>
#include <random>
#include <map>
#include <fstream>
#include <sstream>

struct Q_LearningAgent
{
	double getEpsilon(int episode, int totalEpisodes, double maxEpsilon, double minEpsilon, double decayRate) {
		// Exponential decay
		double epsilon = minEpsilon + (maxEpsilon - minEpsilon) * exp(-decayRate * episode);
		return epsilon;
	}

	void setQValue(std::string state, int action, double value)
	{
		if (!QTable.contains(state))
		{
			QTable[state] = std::vector<double>(DOWN + 1, 0.f);
		}
		QTable[state][action] = value;
	}

	double getQValue(std::string state, int action)
	{
		if (!QTable.contains(state))
		{
			QTable[state] = std::vector<double>(DOWN + 1, 0.f);
		}
		return QTable[state][action];
	}

	double getValue(std::string state)
	{
		if (!QTable.contains(state))
		{
			QTable[state] = std::vector<double>(DOWN + 1, 0.f);
		}
		auto arr = QTable[state];
		auto max = std::ranges::max_element(arr);
		return *max;
	}
	void update(std::string state, int action, int reward, std::string next_state)
	{
		auto value = (1 - alpha) * getQValue(state, action) + alpha * (reward + gamma * getValue(next_state));
		setQValue(state, action, value);
	}

	int getBestAction(std::string state)
	{
		if (!QTable.contains(state))
		{
			QTable[state] = std::vector<double>(DOWN + 1, 0.f);
		}
		auto vec = QTable[state];
		auto max_it = std::ranges::max_element(vec);
		std::vector<int> idxs;
		for (auto i = 0; i<4 ; i++)
		{
			if (vec[i] == *max_it)
			{
				idxs.push_back(i);
			}
		}
		std::uniform_int_distribution<int> distrib3(0,idxs.size() - 1);

		return idxs[distrib3(gen)];
	}

	int getAction(std::string state)
	{
		int action = 0;
		if (distrib(gen) >= epsilon)
		{
			action = getBestAction(state);
		}
		else
		{
			action = distrib2(gen);
		}
		return action;
	}
	void stopLearning()
	{
		alpha = 0;
		epsilon = 0;
	}
	void saveQTable(const std::string& filename) {
		std::ofstream file(filename);
		if (file.is_open()) {
			for (const auto& pair : QTable) {
				file << pair.first << " ";  // Write the key (state)
				for (double value : pair.second) {
					file << value << " ";   // Write each action value
				}
				file << "\n";  // New line for the next state
			}
			file.close();
			std::cout << "Q-table saved to " << filename << std::endl;
		}
		else {
			std::cerr << "Unable to open file for writing!" << std::endl;
		}
	}

	void loadQTable(const std::string& filename) {
		std::ifstream file(filename);
		if (file.is_open()) {
			QTable.clear();  
			std::string state;
			std::string line;
			double value;
			while (std::getline(file, line)) {  // Read each line
				std::vector<double> vec;
				std::cout << line << std::endl;
				size_t pos = line.find_first_of("0123456789");
				state = line.substr(0, pos - 1);
				std::string numPart = line.substr(pos);
				std::istringstream iss(numPart);
				while (iss >> value) {  // Extract each number from the stream
					vec.push_back(value);
				}
				QTable[state] = vec;
			}
			file.close();
			file.close();
			std::cout << "Q-table loaded from " << filename << std::endl;
		}
		else {
			std::cerr << "Unable to open file for reading!" << std::endl;
		}
	}
	std::random_device rd = std::random_device();
	std::mt19937 gen = std::mt19937(42);
	std::uniform_real_distribution<double> distrib = std::uniform_real_distribution<double>(0, 1);
	std::uniform_int_distribution<int> distrib2 = std::uniform_int_distribution<int>(0, Action::DOWN + 1);
	std::map<std::string, std::vector<double>> QTable;
	double alpha = 0.5;   // Learning rate
	double gamma = 0.9;   // Discount factor
	double epsilon = 0.25; // Exploration rate
};

int main()
{
	if (0)
	{
		auto agent = Q_LearningAgent();
		agent.loadQTable("dupa.txt");
		int actionMax = 100;
		auto env = Game(0);
		for (int episode = 0; episode < 10000; episode++)
		{
			agent.epsilon = agent.getEpsilon(episode, 10000, 1, 0.1, 0.0005);
			int i = 0;
			auto state = env.reset();
			while (false == env.isDone() && i < actionMax)
			{
				env.render();

				auto action = agent.getAction(state);
				env.handleEvents();

				auto envReturn = env.step(static_cast<Action>(action));
				agent.update(state, action, envReturn->reward, envReturn->nextState);
				state = envReturn->nextState;

				std::cout << std::format("epsilon: {}, episode: {}, action: {}, reward: {}, done: {}, state: {}",agent.epsilon, episode, action, envReturn->reward, envReturn->isDone, envReturn->nextState) << "\n";
				if (envReturn->isDone)
				{
					break;
				}
				env.render();
				++i;
			}
		}
		agent.saveQTable("dupa.txt");
	}
	else
	{
		auto agent = Q_LearningAgent();
		agent.loadQTable("dupa.txt");
		agent.stopLearning();

		auto env = Game(1);

		auto state = env.reset();
		while (false == env.isDone())
		{
			auto action = agent.getAction(state);
			env.handleEvents();

			auto envReturn = env.step(static_cast<Action>(action));
			agent.update(state, action, envReturn->reward, envReturn->nextState);
			std::cout << std::format("action: {}, reward: {}, done: {}, state: {}", action, envReturn->reward, envReturn->isDone, envReturn->nextState) << "\n";

			state = envReturn->nextState;
			if (envReturn->isDone)
			{
				break;
			}
			env.render();
		}
		
	}
	



	return 0;
}

