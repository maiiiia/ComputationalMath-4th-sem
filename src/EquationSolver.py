import random


class EquationSolver():
    def __init__(self, start, end, func, epsilon, derivative, secondDerivative):
        self.start = start
        self.end = end
        self.func = func
        self.epsilon = epsilon
        self.derivative = derivative
        self.secondDerivative = secondDerivative

    def findRootSegments(self):
        print("----------------------------------------------------------------------")
        stepsize = self.findStepSize()
        print("Отделяем корни методом табулирования. Шаг = ", stepsize)
        rootSegments = []
        tempSegmentStart = self.start
        tempSegmentEnd = self.start + stepsize
        counter = 0
        print("Отрезки перемены знака: ")
        while tempSegmentEnd <= self.end:
            if self.func(tempSegmentStart) * self.func(tempSegmentEnd) <= 0:
                rootSegments.append([tempSegmentStart, tempSegmentEnd])
                counter += 1
                print("[", tempSegmentStart, ", ", tempSegmentEnd, "]")
            tempSegmentStart = tempSegmentEnd
            tempSegmentEnd += stepsize
        print("Всего отрезков: ", counter)
        if stepsize / 2 < self.epsilon:
            print("Середины найденных отрезков находятся на расстоянии не более ", self.epsilon,
                  "от любой точки отрезка. То есть середины отрезков можно считать приближенным значением корня")
        print("----------------------------------------------------------------------")
        return rootSegments

    def findStepSize(self):
        print("----------------------------------------------------------------------")
        print("Введите количество отрезков на которые будет разделён "
              "изначальный отрезок для поиска корней: ")
        n = int(input())
        if n < 2:
            print("Недостаточно отрезков для корректного поиска корней, введите большее число")
            return self.findStepSize()
        stepSize = (self.end - self.start) / n
        if stepSize > 0.01:
            print("Отрезки слишком большие для корректного поиска корней, введите большее число отрезков")
            return self.findStepSize()
        print("----------------------------------------------------------------------")
        return stepSize

    def findRoots(self):
        print("----------------------------------------------------------------------")
        segments = self.findRootSegments()
        print("Уточняем корни на получившихся промежутках")
        for segment in segments:
            print("----------------------------------------------------------------------")
            print("Ищем корни на отрезке: ", segment)
            self.bisectionMethod(segment)
            self.newtonMethod(segment)
            self.modifiedNewtonMethod(segment)
            self.secantMethod(segment)
            print("----------------------------------------------------------------------")

    def ifConverges(self, segment):
        """Проверяет условие сходимости метода Ньютона:
        1)f(a) * f(b) < 0 - выполняется изначально, так как сперва мы отделяем корни
        2)f'(x), f''(x) - сохраняют знаки на [a,b]
        """
        if ((self.derivative(segment[0]) * self.derivative(segment[1])) < 0 or
                (self.secondDerivative(segment[0]) * self.secondDerivative(segment[1])) < 0):
            return False
        else:
            return True

    def newtonMethod(self, segment):
        """Метод Ньютона.
        Проводим касательную к функции в произвольной точке отрезка x0. Она пересечет абциссу в точке x1.
        Продолжаем пока расстояние между xn и xn+1 не станет меньше epsilon
        Формула: xn+1 = xn - f(xn)/f'(xn)
        :param segment: segment to find root in
        :return:
         """
        print("----------------------------------------------------------------------")
        print("Ищем корень методом Ньютона")
        if not self.ifConverges(segment):
            print("Теорема о сходимости не работает,"
                  " так как знак производной функции меняется на концах заданного отрезка")
        else:
            print("Сходится")
            numSteps = 0
            tempSegmentStart = segment[0]
            tempSegmentEnd = segment[1]

            prevRoot = tempSegmentStart + (tempSegmentEnd - tempSegmentStart) * random.random()
            # x_0: f(x_0) * f''(x_0) > 0, x_0 принадлежит [a,b]
            c = 0
            while self.secondDerivative(prevRoot) * self.func(prevRoot) <= 0:
                prevRoot = tempSegmentStart + (tempSegmentEnd - tempSegmentStart) * random.random()
            print("Начальное приближение к корню (x0) = ", prevRoot)

            root = prevRoot - self.func(prevRoot) / self.derivative(prevRoot)
            while abs(root - prevRoot) >= self.epsilon:
                prevRoot = root
                root = prevRoot - self.func(prevRoot) / self.derivative(prevRoot)
                numSteps += 1
            inaccuracy = abs(root - prevRoot)
            print("Приближенное решение x = ", root)
            print("Количество шагов для получения необходимой точности = ", numSteps)
            print("Длина получившегося отрезка = ", inaccuracy)
            print("Абсолютная величина невязки решения: ", abs(self.func(root) - 0))
        print("----------------------------------------------------------------------")

    def modifiedNewtonMethod(self, segment):
        """Модифицированный метод Ньютона.
        Новая формула: xn+1 = xn - f(xn)/f'(x0)
        :param segment: segment to find root in
        :return:
         """
        print("----------------------------------------------------------------------")
        print("Ищем корень модифицированным методом Ньютона")
        if not self.ifConverges(segment):
            print("Теорема о сходимости не работает,"
                  " так как знак производной функции меняется на концах заданного отрезка")
        else:
            numSteps = 0
            tempSegmentStart = segment[0]
            tempSegmentEnd = segment[1]

            prevRoot = tempSegmentStart + (tempSegmentEnd - tempSegmentStart) * random.random()
            # x_0: f(x_0) * f''(x_0) > 0, x_0 принадлежит [a,b]
            while self.secondDerivative(prevRoot) * self.func(prevRoot) <= 0:
                prevRoot = tempSegmentStart + (tempSegmentEnd - tempSegmentStart) * random.random()
            print("Начальное приближение к корню = ", prevRoot)
            derivative_x0 = self.derivative(prevRoot)
            root = prevRoot - self.func(prevRoot) / derivative_x0
            while abs(root - prevRoot) >= self.epsilon:
                prevRoot = root
                root = prevRoot - self.func(prevRoot) / derivative_x0
                numSteps += 1
            inaccuracy = abs(root - prevRoot)
            print("Приближенное решение x = ", root)
            print("Количество шагов для получения необходимой точности = ", numSteps)
            print("Длина получившегося отрезка = ", inaccuracy)
            print("Абсолютная величина невязки решения: ", abs(self.func(root) - 0))
        print("----------------------------------------------------------------------")

    def secantMethod(self, segment):
        """
        Метод секущих. Похож на метод Ньютона, но заменяем производную при подсчете корня ее
        приближенным значением по формулам численного дифференцирования.
        :param segment: segment to find root in
        :return:
        """
        print("----------------------------------------------------------------------")
        print("Ищем корень методом секущих")
        if not self.ifConverges(segment):
            print("Теорема о сходимости не работает,"
                  " так как знак производной функции меняется на концах заданного отрезка")
        else:
            numSteps = 0
            tempSegmentStart = segment[0]
            tempSegmentEnd = segment[1]

            prevRoot = tempSegmentStart + (tempSegmentEnd - tempSegmentStart) * random.random()
            # x_0: f(x_0) * f''(x_0) > 0, x_0 принадлежит [a,b]
            while self.secondDerivative(prevRoot) * self.func(prevRoot) <= 0:
                prevRoot = tempSegmentStart + (tempSegmentEnd - tempSegmentStart) * random.random()
            print("Начальное приближение к корню (x0) = ", prevRoot)

            currentRoot = tempSegmentStart + (tempSegmentEnd - tempSegmentStart) * random.random()
            while currentRoot == prevRoot:
                currentRoot = tempSegmentStart + (tempSegmentEnd - tempSegmentStart) * random.random()

            def approxDerivative(currentRoot, prevRoot):
                return (self.func(currentRoot) - self.func(prevRoot)) / (currentRoot - prevRoot)

            nextRoot = currentRoot - self.func(currentRoot) / approxDerivative(currentRoot, prevRoot)
            while abs(currentRoot - nextRoot) >= self.epsilon:
                prevRoot = currentRoot
                currentRoot = nextRoot
                nextRoot = currentRoot - self.func(currentRoot) / approxDerivative(currentRoot, prevRoot)
                numSteps += 1
            inaccuracy = abs(nextRoot - currentRoot)
            print("Приближенное решение x = ", nextRoot)
            print("Количество шагов для получения необходимой точности = ", numSteps)
            print("Длина получившегося отрезка = ", inaccuracy)
            print("Абсолютная величина невязки решения: ", abs(self.func(nextRoot) - 0))
        print("----------------------------------------------------------------------")

    def bisectionMethod(self, segment):
        """Метод бисекций
            Сходимость метода гарантируется
            Делим отрезок пополам, пока его длина не будет меньше 2*epsilon
            Как только мы достигли этого условия, берем x, который находится на середине получившегося отрезка.
            :param segment: segment to find root in
            :return:
            """
        print("----------------------------------------------------------------------")
        print("Ищем корень методом бисекции (деления пополам)")
        numSteps = 0
        tempSegmentStart = segment[0]
        tempSegmentEnd = segment[1]
        root = (tempSegmentEnd + tempSegmentStart) / 2
        print("Начальное приближение к корню", root)
        pivot = 0
        while (tempSegmentEnd - tempSegmentStart) >= 2 * self.epsilon:
            pivot = (tempSegmentEnd + tempSegmentStart) / 2
            if self.func(pivot) * self.func(tempSegmentStart) <= 0:
                tempSegmentEnd = pivot
            else:
                tempSegmentStart = pivot
            numSteps += 1
        inaccuracy = abs(tempSegmentEnd - tempSegmentStart)
        print("Приближенное решение x = ", pivot)
        print("Количество шагов для получения необходимой точности = ", numSteps)
        print("Длина получившегося отрезка = ", inaccuracy)
        print("Абсолютная величина невязки решения: ", abs(self.func(pivot) - 0))
        print("----------------------------------------------------------------------")
