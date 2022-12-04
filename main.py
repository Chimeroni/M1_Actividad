import mesa
import random
import time

class robot_agent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        self.move()
        self.clean()

    def clean(self):
        if not self.model.esta_limpio(self.pos):
            self.model.cambiar_limpio(self.pos)
            print("Celda Limpia: ", self.pos, "\n")

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)


class robot_model(mesa.Model):
    def __init__(self, N, width, height, percent, tiempo_max):
        self.num_agents = N
        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.MultiGrid(height, width, True)
        self.init_time = time.time()
        self.final_time = tiempo_max
        self.total_mov = 0

        self.celdas_suc = int((width * height) * percent)
        self.celdas_lim = int((width * height) * (1 - percent))
        self.dirty_matrix = [([True]*width) for i in range(height)]
        self.cant_celdas_suc_inicializar = self.celdas_suc
        while (self.cant_celdas_suc_inicializar > 0): 
            for i in range(height):
                for j in range(width):
                    sucio_o_limpio = random.randint(0, 1)
                    if self.cant_celdas_suc_inicializar > 0 and self.dirty_matrix[i][j]:
                        self.dirty_matrix[i][j] = False
                        self.cant_celdas_suc_inicializar -= 1

        for i in range(self.num_agents):
            a = robot_agent(i, self)
            self.schedule.add(a)
            self.grid.place_agent(a, (1, 1))

    def step(self):
        self.total_mov += 1
        self.schedule.step()

    def total_movimientos(self):
        return self.total_mov * self.num_agents

    def porcentaje_celdas_limpias(self):
        return self.celdas_lim / (self.celdas_lim + self.celdas_suc)
    
    def esta_limpio(self, new_position):
        x, y = new_position
        return self.dirty_matrix[x][y]

    def cambiar_limpio(self, new_position):
        x, y = new_position
        self.dirty_matrix[x][y] = True
        self.celdas_suc -= 1
        self.celdas_lim += 1
        if self.celdas_suc == 0:
            self.final_time = time.time() - self.init_time 
            self.total_movimientos()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -



    
    

# Main - Ejemplo de Entrada
M = int(input("M: ")) 
N = int(input("N: ")) 

cant = int(input("# de agentes: "))

suciedad = float(input("% de las celdas sucias: "))
while (suciedad > 1):
    suciedad = float(input("Error: Escribe un numero entre 0 y 1: "))

tiempo_max = int(input("\n\n\nIntroduce el tiempo máximo de ejecución (segundos): "))

model = robot_model(cant, N, M, suciedad, tiempo_max)
while (model.celdas_suc > 0 and ((time.time() - model.init_time) < model.final_time)):
    model.step()
    # [print(*line) for line in model.dirty_matrix]
    
    for line in model.dirty_matrix:
        str = ""
        for l in line:
            if l == True:
                str += " 1"
            else:
                str += " 0"
        print(str)
    print("\nPorcentaje de celdas limpias:", model.porcentaje_celdas_limpias(), "\n\n")

print("Movimientos totales de los agentes:", model.total_movimientos())
print("Tiempo:", model.final_time, "(s)")
