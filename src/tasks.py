from src.EquationSolver import EquationSolver
import math


def task1():
    print("Задание №1: численные методы решения нелинейных уравнений, 18 вариант")
    print("Ищем корни уравнения f(x) = x**2 - sin(5x)")
    print("[A, B] = [-2, 1]")
    print("epsilon = 1e-08")

    def func(x): return x ** 2 - math.sin(5 * x)

    def funcDerivative(x): return 2 * x - 5 * math.cos(5 * x)

    def funcSecondDerivative(x): return 2 + 25 * math.sin(5 * x)

    start = -2
    end = 1
    epsilon = 10 ** -12
    solver = EquationSolver(start, end, func, epsilon, funcDerivative, funcSecondDerivative)
    solver.findRoots()


def task2():
    print("Задание №2: численные методы решения нелинейных уравнений, 18 вариант")
    print("Ищем корни уравнения f(x) = x**2 - sin(5x)")
    print("[A, B] = [-2, 1]")
    print("epsilon = 1e-08")

    def func(x): return x ** 2 - math.sin(5 * x)

    def funcDerivative(x): return 2 * x - 5 * math.cos(5 * x)

    def funcSecondDerivative(x): return 2 + 25 * math.sin(5 * x)

    start = -2
    end = 1
    epsilon = 10 ** -12
    solver = EquationSolver(start, end, func, epsilon, funcDerivative, funcSecondDerivative)
    solver.findRoots()
