
import mesa
import random
import math
import statistics

def compute_resistance(model):
    agent_resistance = []
    for agent in model.schedule.agents:
        if agent.type == 'bacteria':
            agent_resistance.append(agent.resistance)
    if len(agent_resistance) != 0:
        mean1 = statistics.mean(agent_resistance)
    else:
        mean1 = 0
    return mean1

def compute_number_of_bacteria(model):
    agent_resistance = []
    for agent in model.schedule.agents:
        if agent.type == 'bacteria':
            agent_resistance.append(agent.resistance)
    
    return len(agent_resistance)

class Food(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.size = 0.7 + random.random()/10
        self.type = 'food'
    
   #food will disappear 
    def consumed(self):
        self.model.kill_agents.append(self)


class Bacteria(mesa.Agent):
    """An agent with some resistance"""

    def calculate_speed(self):
        return 1/math.pow(self.size,1/3)

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = 'bacteria'
        self.resistance = random.random()
        self.hunger = 1 + random.random()
        self.size = 1 + random.random()/10
        self.biodegradation = random.random()/10
        self.speed = self.calculate_speed()
        self.sense =  1 + random.random()

    def move(self):
        the_activated_cell = 0

        food_cells = []
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        print(possible_steps)
        for possible_step in possible_steps:
            cellcontent = self.model.grid.get_cell_list_contents([possible_step])
            for inside_cell in cellcontent:
                print(inside_cell.type)
                if inside_cell.type == 'food':
                    food_cells.append((inside_cell, possible_step))
        
        new_position = self.random.choice(possible_steps)
        if len(food_cells) == 0:
            self.hunger += 1
        else:
            for food_cell in food_cells:
                print(food_cell)
                if food_cell[0] not in self.model.kill_agents:
                    best_pos = food_cell[1]
                    the_activated_cell = food_cell[0].size
                    new_position = best_pos
                    food_cell[0].consumed()

        self.model.grid.move_agent(self, new_position)
        self.hunger -= the_activated_cell
        self.hunger += 1/self.speed + self.resistance*0.5
        self.size += the_activated_cell
        self.speed = self.calculate_speed()


        if self.hunger > 9 or self.model.power_of_antibiotic > self.resistance + random.random()/10 - random.random()/10:
            self.model.kill_agents.append(self)
        else:
            if self.size > 3:
                #time to reproduce
                self.model.num_agents += 2
                b = Bacteria(self.model.num_agents, self.model) 
                self.model.grid.place_agent(b, new_position)
                self.model.schedule.add(b)
                self.size = self.size/2
                self.hunger = 1
                b.hunger = 1
                b.size = self.size
                b.resistance = self.resistance + random.random()/10 - random.random()/10
                b.sense = self.sense + random.random()/10 - random.random()/10
                b.speed = self.calculate_speed()
                self.speed = self.calculate_speed()


    def step(self):
        # The agent's step will go here.
        self.move()    

class ARModel(mesa.Model):
    def place_agent_randomly(self, a):
        x = self.random.randrange(self.grid.width)
        y = self.random.randrange(self.grid.height)
        self.grid.place_agent(a, (x, y))

    """A model with some number of agents."""
    def __init__(self, bacteria_number, food_number, antibiotic_number, power_of_antibiotic, width, height):
        self.num_agents = 0
        self.power_of_antibiotic = power_of_antibiotic
        self.food_number = food_number
        self.antibiotic_number = antibiotic_number
        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.MultiGrid(width, height, True)
        # Create agents
        for i in range(self.num_agents, bacteria_number):
            a = Bacteria(i, self)
            self.schedule.add(a)
            self.place_agent_randomly(a)
            self.num_agents += bacteria_number

        for i in range(self.num_agents, self.num_agents + food_number):
            a = Food(i, self)
            self.schedule.add(a)
            self.place_agent_randomly(a)
            self.num_agents += food_number
        
        self.datacollector = mesa.DataCollector(
            model_reporters={"Resistance": compute_resistance}, agent_reporters={"Resistance": lambda x: x.resistance if x.type == 'bacteria' else None}
        )
        self.datacollector_bacteria = mesa.DataCollector(
            model_reporters={"Count": compute_number_of_bacteria}, agent_reporters={"Count": lambda x: x.resistance if x.type == 'bacteria' else None}
        )


    def step(self):
        self.datacollector.collect(self)
        self.datacollector_bacteria.collect(self)
        #self.power_of_antibiotic += 0.01
        self.kill_agents = []  #killing agents
        self.schedule.step()

        print(self.kill_agents)
        for i in self.kill_agents:  
            print(i.unique_id)
            
            self.grid.remove_agent(i)
            self.schedule.remove(i)
            self.kill_agents.remove(i)        

        for i in range(self.num_agents + 1, self.num_agents + self.food_number + 1):
            a = Food(i, self)
            self.schedule.add(a)
            self.place_agent_randomly(a)
            self.num_agents += self.food_number + 1
        