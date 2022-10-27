import copy
import random
from threading import Lock


class SingletonMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances or args or kwargs:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class GameOfLife(metaclass=SingletonMeta):
    def __init__(self, width=20, height=20):
        self.__width = width
        self.__height = height
        self.world = self.generate_universe()
        self.old_world = copy.deepcopy(self.world)
        self.counter = 0
        self.previous_states = []   # Список всех предыдущих состояний мира, каждое хранится в виде числа
        self.repeat = False         # Фиксирует наличие повторов

    def form_new_generation(self):
        universe = self.world
        new_world = [[0 for _ in range(self.__width)] for _ in range(self.__height)]

        for i in range(len(universe)):
            for j in range(len(universe[0])):

                if universe[i][j]:
                    if self.__get_near(universe, [i, j]) not in (2, 3):
                        new_world[i][j] = 0
                        continue
                    new_world[i][j] = 1
                    continue

                if self.__get_near(universe, [i, j]) == 3:
                    new_world[i][j] = 1
                    continue
                new_world[i][j] = 0
        self.old_world = copy.deepcopy(self.world)
        self.world = new_world
        self.add_previous_state()

    def generate_universe(self) -> list:
        return [[random.randint(0, 1) for _ in range(self.__width)] for _ in range(self.__height)]

    def get_worlds_dict(self) -> dict:
        """Данные для ответа браузеру"""
        return {
            'old_world': self.old_world,
            'world': self.world,
            'counter': self.counter,
            'repeat': self.repeat
        }

    def add_previous_state(self):
        """Добавляет нынешнее состояние мира в список"""
        world_state = self.__world_state()
        self.repeat = self.__find_repeat(world_state)
        self.previous_states.append(world_state)

    @classmethod
    def destroy_the_world(cls):
        """Очищает данные класса - одиночки"""
        cls._instances = {}

    @staticmethod
    def __get_near(universe, pos, system=None):
        if system is None:
            system = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))

        count = 0
        for i in system:
            if universe[(pos[0] + i[0]) % len(universe)][(pos[1] + i[1]) % len(universe[0])]:
                count += 1
        return count

    def __world_state(self) -> bin:
        """Преобразует двумерный список состоящий из нулей и единиц в число"""
        state = 0
        for i in range(len(self.world)):
            for j in range(len(self.world[0])):
                state <<= 1
                state += self.world[i][j]
        return state

    def __find_repeat(self, world_state) -> bool:
        """Поиск повторных состояний мира"""
        if world_state in self.previous_states:
            return True
        return False
