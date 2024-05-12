class VectorField:
    def __init__(self, *comps, dim=None):
        """
        Векторное поле может быть задано с помощью
        проекций векторов в каждой точке поля на
        некоторые координатные оси.

        >>> x, y, z, t, p = sympy.symbols("x y z t p")
        >>> v = VectorField(x+y, y**2, z*y)
        >>> u = VectorField(t - p, p, dim=(t, p))

        :param comps: компоненты векторного поля - объекты, переводимые в sympy.Expr
        :param dim: кортеж из обозначений координат векторного поля - объектов, переводимых в sympy.Expr
        """

        if dim is None:
            x, y, z = sympy.symbols('x y z')
            dim = (x, y, z)[:len(comps)]

        if len(comps) > len(dim):
            raise ValueError("Number of components is bigger than dimension")
        if any([not (isinstance(sympy.sympify(comp), sympy.Expr)) for comp in comps]):
            raise TypeError("Can't subtract component")
        if not (isinstance(dim, tuple)):
            raise TypeError("Dimension must be tuple")
        if any([not (isinstance(var, sympy.Symbol)) for var in dim]):
            raise ValueError("Wrong type of input data (should be able to be turned into Sympy Expression)")

        self._comps = {dim: sympy.sympify(comp) for dim, comp in zip(dim, comps)}
        self.dim = dim

    def __repr__(self):
        """
        Возваращает строку в формате (F1, F2, F3...),
        где F1, F2, F3... - проекции векторного поля

        >>> x, y, z = sympy.symbols("x y z")
        >>> v = VectorField(x+y, y**2, z*y)
        >>> print(v)
        (x + y, y**2, y*z)
        """

        output = []
        for dim, comp in self:
            output.append(str(comp))
        return "(" + ", ".join(output) + ")"

    def visualize(self,
                  image=None,
                  scale=True,
                  density=11,
                  bounds=((-10, 10), (-10, 10), (-10, 10)),
                  description={"width": False, "length": False, "alpha": False, "color": False},
                  mode="A",
                  width=0.005,
                  length=1,
                  alpha=1,
                  color="black",
                  imagesize=(10, 10),
                  normalize=False,
                  show=True):
        """
        Визуализирует дву- или трёхмерное векторное поле с помощью matplotlib

        >>> x, y = sympy.symbols("x y")
        >>> v = VectorField(x+y, y**2)
        >>> v.visualize(density = 30, color = "blue", width = 0.003)

        :param image: изображение (figure), на котором будет отрисовано векторное поле. По умолчанию выведет изображение отдельно
        :param scale: смасштабировать векторное поле на изображение
        :param density: плотность отрисовки стрелок/потоков.
        :param bounds: границы отрисовки векторного поля
        :param description: задаёт настройки отрисовки: динамическая ширина потоков, нормализация длин стрелок, динамическая прозрачность стрелок, динамическая раскраска.
        :param mode: Режим отрисовки векторного поля. Режим отрисовки "A": представляет поле в виде стрелок в каждой точке координатной плоскости/пространства. Режим отрисовки "S": представляет поле в виде потоков (отстутсвует для трёхмерных векторных полей).
        :param width: ширина стрелок или потоков.
        :param length: длина стрелок.
        :param alpha: прозрачность стрелок
        :param color: цвет отрисовки стрелок, потоков.
        :param imagesize: размеры изображения
        :param normalize: нормализация длин векторов в режиме стрелок. Представляет каждый вектор в виде единичного вектора, сохраняя таким образом информацию лишь о нарпавлении вектора
        """

        for option in ("width", "length", "alpha", "color"):
            description[option] = description[option] if option in description else False
        if len(self) <= 1 or 4 <= len(self):
            raise ValueError("Can't visualize VectorField of dimension less than 2 or higher than 3")

        if scale and image is not None:
            if len(self) == 2:
                bounds = (image.axes[0].get_xlim(), image.axes[0].get_ylim())
            if len(self) == 3:
                bounds = (image.axes[0].get_xlim(), image.axes[0].get_ylim(), image.axes[0].get_zlim())

        plane = [numpy.linspace(*bounds[i], density) for i in range(len(self))]
        plane[:len(self)] = numpy.meshgrid(*plane)

        for i in range(len(self)):
            try:
                f = sympy.lambdify(self.dim, self[i], "numpy")
                numpy.seterr(divide='ignore', invalid='ignore')
                plane.append(f(*plane[:len(self)]) * numpy.ones(tuple((len(plane[i]) for i in range(len(self))))))
            except:
                subplane = [numpy.linspace(*bounds[i], density) for i in range(len(self))]
                if len(self) == 2:
                    f = lambda x, y: self[i].subs({self.dim[0]: x, self.dim[1]: y})
                    plane.append(numpy.array([[f(x, y) for x in subplane[0]] for y in subplane[1]], dtype=float))
                else:
                    f = lambda x, y, z: self[i].subs({self.dim[0]: x, self.dim[1]: y, self.dim[2]: z})
                    plane.append(
                        numpy.array([[[f(x, y, z) for x in subplane[0]] for y in subplane[1]] for z in subplane[2]], dtype=float))

        magnitude = numpy.sqrt(sum(plane[i] ** 2 for i in range(len(self), 2 * len(self))))
        if normalize:
            for i in range(len(self), 2 * len(self)):
                plane[i] = plane[i] / magnitude
        norm = None
        submagnitude = magnitude[numpy.nonzero(magnitude)]
        submagnitude = submagnitude[numpy.isfinite(submagnitude)]

        match len(self):
            case 2:
                if image is None:
                    fig, ax = matplotlib.pyplot.subplots(figsize=imagesize)
                    ax.set(xlim=bounds[0], ylim=bounds[1])
                    ax.set_xlabel(str(self.dim[0]))
                    ax.set_ylabel(str(self.dim[1]))
                else:
                    matplotlib.pyplot.figure(image)
                if mode == "A":
                    scale_units = None
                    angles = "uv"
                    scale = None
                    if description["length"]:
                        coef = length * numpy.log10((9 * magnitude / submagnitude.max() + 1)) / magnitude
                        plane[2], plane[3] = plane[2] * coef, plane[3] * coef
                        scale_units = "xy"
                        angles = "xy"
                        scale = (density - 1) / (bounds[0][1] - bounds[0][0])
                    if description["alpha"]:
                        alpha = numpy.nan_to_num(magnitude, 0) / submagnitude.max()
                    if description["color"]:
                        plane.append(magnitude)
                        color = None
                        norm = matplotlib.colors.LogNorm(vmin=submagnitude.min(),
                                       vmax=submagnitude.max())

                    matplotlib.pyplot.quiver(*plane,
                                             color=color,
                                             width=width,
                                             norm=norm,
                                             alpha=alpha,
                                             cmap="coolwarm",
                                             pivot="middle",
                                             scale_units=scale_units,
                                             angles = angles,
                                             scale = scale)
                elif mode == "S":
                    if description["width"]:
                        width *= numpy.log10((9 * magnitude / submagnitude.max() + 1)) / magnitude
                    if description["color"]:
                        color = magnitude
                        norm = matplotlib.colors.LogNorm(vmin=submagnitude.min(),
                                       vmax=submagnitude.max())

                    matplotlib.pyplot.streamplot(*plane,
                                                 density=density/10,
                                                 color=color,
                                                 norm=norm,
                                                 cmap="coolwarm",
                                                 linewidth=width)
                else:
                    raise ValueError("Mode must be A or S")
            case 3:
                if image is None:
                    fig, ax = matplotlib.pyplot.subplots(figsize=imagesize, subplot_kw={"projection": "3d"})
                    ax.set(xlim=bounds[0], ylim=bounds[1], zlim=bounds[2])
                    ax.set_xlabel(str(self.dim[0]))
                    ax.set_ylabel(str(self.dim[1]))
                    ax.set_zlabel(str(self.dim[2]))
                else:
                    matplotlib.pyplot.figure(image)
                if mode == "A":
                    if description["color"]:
                        color = numpy.log10((9 * magnitude.ravel() / submagnitude.max() + 1))
                        color = matplotlib.pyplot.cm.coolwarm(color)
                    if description["alpha"]:
                        alpha = numpy.nan_to_num(magnitude, 0) / submagnitude.max()

                    matplotlib.pyplot.quiver(*plane,
                                             length=length,
                                             color=color,
                                             pivot="middle")
                elif mode == "S":
                    raise ValueError("Can't visualize 3D Vector Field using streams")
                else:
                    raise ValueError("Mode must be A or S")
        if show:
            matplotlib.pyplot.show()

    def __add__(self, other):
        """
        Возвращает VectorField, каждый компонент которого
        является суммой соответствующих компонент входных
        векторных полей. Размерности входных векторных полей
        обязаны совпадать

        >>> x, y, z = sympy.symbols("x y z")
        >>> v = VectorField(x+y, y**2, z*y)
        >>> u = VectorField(x-y, 1/y, z)
        >>> u + v
        (2*x, y**2 + 1/y, y*z + z)
        """

        if self.dim != other.dim:
            raise ValueError("Dimensions of summands don't match")

        output = []
        for comp1, comp2 in zip(self._comps.values(), other._comps.values()):
            output.append(comp1 + comp2)
        return VectorField(*output, dim=self.dim)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        """
        В случае если other представлен численным типом данных
        возваращает VectorField, каждый компонент которого является
        произведением компоненты self и данного скаляра

        >>> x, y = sympy.symbols("x y")
        >>> v = VectorField(x, 1)
        >>> v * 2
        (2*x, 2)

        В случае если other представлен VectorField
        возвращает Expr, который представляет собой
        скалярное произведение компонент self и other.
        Размерности self и other обязаны совпадать

        >>> x, y, z = sympy.symbols("x y z")
        >>> v = VectorField(x+y, y**2, z*y)
        >>> u = VectorField(x-y, 1/y, z)
        >>> u * v
        y*z**2 + y + (x - y)*(x + y)
        """

        if isinstance(other, (int, float)):
            output = []
            for dim, comp in self:
                output.append(other * comp)
            return VectorField(*output, dim=self.dim)

        if isinstance(other, VectorField):
            if self.dim != other.dim:
                raise ValueError("Dimensions of summands don't match")
            output = []
            for dim in self.dim:
                output.append(self[dim] * other[dim])
            return sum(output)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        return 1 / other * self

    def __iadd__(self, other):
        return self + other

    def __isub__(self, other):
        return self - other

    def __imul__(self, other):
        return self * other

    def __pos__(self):
        return self

    def __neg__(self):
        return self * (-1)

    def __eq__(self, other):
        """
        VectorField равен другому VectorField тогда,
        когда совпадают их компоненты и размерности

        >>> x, y = sympy.symbols("x y")
        >>> v = VectorField(x+y, y**2)
        >>> u = VectorField(x+y, y**2)
        >>> t = VectorField(x-y, 1/y)
        >>> u == v
        True
        >>> u == t
        False
        """

        if self._comps == other._comps and self.dim == other.dim:
            return True
        else:
            return False

    def __ne__(self, other):
        return not (self == other)

    def __setitem__(self, key, value):
        """
        Позволяет вручную задать компоненту векторного поля

        >>> x, y = sympy.symbols("x y")
        >>> v = VectorField(x+y, y**2)
        >>> v[x] = x*y
        >>> v
        (x*y, y**2)

        :param key: координата компоненты векторного поля в виде sympy.Symbol
        :param value: задаваемое значение компоненты векторного поля - объекта, переводимого в sympy.Expr
        """

        if not (isinstance(sympy.sympify(value), sympy.Expr)):
            raise TypeError("Can't subtract component")
        if key not in self.dim:
            raise ValueError("Can't assign new component")

        self._comps[key] = sympy.sympify(value)

    def __getitem__(self, key):
        """
        Позволяет получить компоненту векторного поля по
        координате или по индексу в self._comps

        >>> x, y = sympy.symbols("x y")
        >>> v = VectorField(x+y, y**2)
        >>> v[x]
        x + y
        >>> v[1]
        y**2

        :param key: координата компоненты векторного поля либо в виде строки, либо в виде числа - индекса в self._comps
        """

        if isinstance(key, (int, float)):
            return self._comps[self.dim[key]]

        return self._comps[key]

    def __iter__(self):
        """
        Позволяет использовать VectorField в цикле for
        при этом должны перебирается кортежи, состоящие из
        двух объектов: координаты и компоненты

        >>> x, y = sympy.symbols("x y")
        >>> v = VectorField(x+y, y**2)
        >>> for coordinate, component in v: print(coordinate, component)
        x x + y
        y y**2
        """

        return iter(self._comps.items())

    def __len__(self):
        """
        Возвращает длину self.dim

        >>> x, y = sympy.symbols("x y")
        >>> v = VectorField(x+y, y**2)
        >>> len(v)
        2
        """

        return len(self.dim)

    def subs(self, *values):
        """
        Позволяет подставить числа в векторное поле вместо координат.
        Возвращает кортеж из компонент после подстановки значений

        >>> x, y = sympy.symbols("x y")
        >>> v = VectorField(x+y, y**2)
        >>> v.subs(1, 2)
        (3, 4)
        >>> v.subs({x : y, y : x**2})
        (x**2 + y, x**4)

        :param values: выражения, подставляемые в компоненты векторного поля вместо координат. Каждая координата из self.dim будет заменена на соответственное значение в values, которое может быть представлено как кортежом, так и словарём.
        """

        if isinstance(values[0], dict):
            if any([not (isinstance(sympy.sympify(value), sympy.Expr)) for value in values[0].values()]):
                raise ValueError("Can't subtract component")
            scheme = values[0]
        else:
            if any([not (isinstance(sympy.sympify(value), sympy.Expr)) for value in values]):
                raise ValueError("Can't subtract component")
            scheme = list(zip(self.dim, values))
        output = []
        for dim, comp in self:
            output.append(comp.subs(scheme, simultaneous=True))
        return tuple(output)

    def div(self):
        """
        Возвращает ScalarField, который представляет собой
        дивергенцию векторного поля

        >>> x, y = sympy.symbols("x y")
        >>> v = VectorField(x+y, y**2)
        >>> v.div()
        2*y + 1
        """

        output = []
        for dim, comp in self:
            output.append(sympy.diff(comp, dim))
        return ScalarField(sympy.sympify(sum(output)), dim=self.dim)

    def curl(self):
        """
        Возвращает VectorField, который является ротором векторного поля.

        >>> x, y, z = sympy.symbols("x y z")
        >>> v = VectorField(x+y, y**2, z*y)
        >>> v.curl()
        (z, 0, -1)
        """

        match len(self.dim):
            case 2:
                comps = sympy.diff(self[1], self.dim[0]) - sympy.diff(self[0], self.dim[1])
                return VectorField(sympy.simplify(comps), dim=self.dim)
            case 3:
                comps = []
                comps.append(sympy.simplify(sympy.diff(self[2], self.dim[1]) - sympy.diff(self[1], self.dim[2])))
                comps.append(sympy.simplify(sympy.diff(self[0], self.dim[2]) - sympy.diff(self[2], self.dim[0])))
                comps.append(sympy.simplify(sympy.diff(self[1], self.dim[0]) - sympy.diff(self[0], self.dim[1])))
                return VectorField(*comps, dim=self.dim)
            case _:
                raise ValueError("Can't find curl of VectorField with dimensions less than 2 or higher than 3")

    def work(self, curve, bounds, numerical=False):
        """
        Возвращает криволинейный интеграл второго рода вдоль кривой.
        Другими словами, возвращает работу, которую совершает сила,
        представленная векторным полем, при прохождении МТ вдоль кривой.

        >>> x, y, t = sympy.symbols("x y t")
        >>> v = VectorField(0, -10)
        >>> v.work((t**2-1, t), (t, 0, 4))
        -40

        :param curve: кривая, заданная параметрически. Задаётся кортежом из функций от параметра - объектов, переводимых в sympy.Expr.
        :param bounds: границы интегрирования по кривой. Задаётся кортежом из переменной и пределов интегрирования
        :param numerical: численное решение или аналитическое
        """

        if len(curve) != len(self):
            raise ValueError("Dimensions of curve and VectorField don't match")

        function = 0
        scheme = list(zip(self.dim, curve))
        for i in range(len(self)):
            vec = self[i]
            function += vec.subs(scheme) * sympy.diff(curve[i], bounds[0])
        work = sympy.Integral(function, bounds)
        if numerical:
            return work.evalf()
        return work.doit()

    def flux(self, region, *bounds, numerical=True):
        """
        Возвращает поверхностный интеграл второго рода по поверхности.
        Другими словами, возвращает количество жидкости, которое протечёт
        через поверхность, заданной region, поле скоростей которой задано
        векторным полем за единицу времени

        >>> x, y, z, t, p = sympy.symbols("x y z t p")
        >>> v = VectorField(2, 0, 0)
        >>> v.flux((1, t, p), (t, -2, 2), (p, -2, 2))
        32

        :param region: кривая/поверхность, заданная параметрически. Задаётся кортежом из зависящих от нескольких параметров функций - объектов, переводимых в sympy.Expr.
        :param bounds: границы интегрирования по кривой/поверхности. Задаются несколькими кортежами, которые содержат переменную и пределы интегрирования.
        :param numerical: численное решение или аналитическое
        """

        if len(region) != len(self):
            raise ValueError("Dimensions of region and VectorField don't match")

        match len(self):
            case 2:
                normal = (sympy.diff(region[1], bounds[0][0]), -sympy.diff(region[0], bounds[0][0]))
            case 3:
                s = [sympy.diff(region[0], bounds[0][0]), sympy.diff(region[1], bounds[0][0]), sympy.diff(region[2], bounds[0][0]),
                     sympy.diff(region[0], bounds[1][0]), sympy.diff(region[1], bounds[1][0]), sympy.diff(region[2], bounds[1][0])]
                normal = [s[1] * s[5] - s[2] * s[4], s[2] * s[3] - s[0] * s[5], s[0] * s[4] - s[1] * s[3]]
            case _:
                raise ValueError("Can't calculate flux of VectorField of dimension less than 2 or higher than 3")
        function = 0
        scheme = list(zip(self.dim, region))
        for i in range(len(self)):
            vec = self[i]
            function += vec.subs(scheme) * normal[i]
        flux = sympy.Integral(sympy.simplify(function), *bounds)
        if numerical and len(self) == 2:
            return flux.evalf()
        else:
            return flux.doit()

    def potential(self):
        """
        Возвращает потенциал векторного поля, если он имеется.
        Если поле не потенциально, будет вызвано исключение.

        >>> x, y = sympy.symbols("x y")
        >>> v = VectorField(-x, 0)
        >>> v.potential()
        -x**2/2
        """

        if not (self.is_potential()):
            raise ValueError("VectorField is not potential")

        function = sympy.integrate(self[0], (self.dim[0]))
        for i in range(1, len(self)):
            const = self[i] - sympy.diff(function, (self.dim[i]))
            function += sympy.integrate(const, (self.dim[i]))
        return ScalarField(function, dim=self.dim)

    def is_potential(self):
        """
        Возвращает True, если поле потенциально,
        и False в противном случае

        >>> x, y = sympy.symbols("x y")
        >>> v = VectorField(-x, 0)
        >>> v.is_potential()
        True
        >>> u = VectorField(y, -x)
        >>> u.is_potential()
        False
        """

        curl = self.curl()
        if all(comp == 0 for dim, comp in curl):
            return True
        else:
            return False

    def is_solenoid(self):
        """
        Возвращает True, если поле соленоидально,
        и False в противном случае

        >>> x, y = sympy.symbols("x y")
        >>> v = VectorField(x, y)
        >>> v.is_solenoid()
        False
        >>> u = VectorField(y, x)
        >>> u.is_solenoid()
        True
        """

        if self.div().func == 0:
            return True
        else:
            return False


class ScalarField:
    def __init__(self, func=0, dim=None):
        """
        Скалярное поле может быть задано с помощью функции
        нескольких переменных, являющихся координатами точки.

        >>> x, y, z, v, t = sympy.symbols("x y z v t")
        >>> s = ScalarField(x**2 + y**2 + z**2)
        >>> p = ScalarField(v + t, dim=(t, v))

        :param func: функция нескольких переменных, задающая скалярное поле - объект, переводимый в sympy.Expr.
        :param dim: кортеж из обозначений координат скалярного поля - объектов, переводимых в sympy.Expr.
        """

        if not (isinstance(sympy.sympify(func), sympy.Expr)):
            raise ValueError("Wrong type of input data (should be able to be turned into Sympy Expression)")
        func = sympy.sympify(func)

        if dim is None:
            x, y, z = sympy.symbols("x y z")
            symbols = [x, y, z] + [i for i in func.free_symbols if str(i) not in ["x", "y", "z"]]
            dim = tuple(i for i in symbols if i in func.free_symbols)

        if not (isinstance(dim, tuple)):
            raise TypeError("Dimension must be tuple")
        if any([not (isinstance(var, sympy.Symbol)) for var in dim]):
            raise ValueError("Wrong type of input data (should be able to be turned into Sympy Expression)")

        self.func = sympy.sympify(func)
        self.dim = dim

    def __repr__(self):
        """
        Возваращает строку, содержащую функцию ScalarField

        >>> x, y = sympy.symbols("x y")
        >>> s = ScalarField(x**2 + y**2)
        >>> print(s)
        x**2 + y**2
        """

        return str(self.func)

    def visualize(self,
                  image=None,
                  scale=True,
                  bounds=((-10, 10), (-10, 10), None),
                  density=256,
                  levels=10,
                  mode="G",
                  color=None,
                  showgrid=True,
                  show=True,
                  imagesize=(10, 10)):
        """
        Визуализирует одно- или двумерное скалярное поле с помощью matplotlib

        >>> x, y = sympy.symbols("x y")
        >>> s = ScalarField(x**2 + y**2)
        >>> s.visualize()

        :param image: изображение (figure), на котором будет отриосвано векторное поле
        :param scale: смасштабировать скалярное поле на изображение
        :param bounds: границы отрисовки скалярного поля
        :param density: точность прорисовки скалярного поля
        :param levels: количество эквипотенциальных поверхностей в режиме эквипотенциальных поверхностей
        :param mode: режим отрисовки скалярного поля. В режиме "G" отрисовывает скалярное поле как график. В режиме "S" отрисовывает скалярное поле с помощью эквипотенциальных поверхностей. Отсутствует для одномерных скалярных полей.
        :param color: цвет отрисовки графика скалярного поля. В режиме эквипотенциальных поверхностей может принимать особое значение "D". В таком случае каждый уровень будет иметь свой цвет в зависимости от значения функции на этом уровне.
        :param showgrid: отрисовка сетки для координатной плоскости.
        :param imagesize: размеры изображения
        """

        if scale and image is not None:
            if len(self) == 1:
                bounds = (image.axes[0].get_xlim(),)
            if len(self) == 3:
                bounds = (image.axes[0].get_xlim(), image.axes[0].get_ylim())

        if len(self) <= 0 or 4 <= len(self):
            raise ValueError("Can't visualize ScalarField of dimension less than 1 or higher than 2")

        plane = [numpy.linspace(*bounds[i], density) for i in range(len(self))]
        if len(self) == 2:
            plane[0], plane[1] = numpy.meshgrid(*plane)

        try:
            one = numpy.ones(tuple((len(plane[i]) for i in range(len(self)))))
            f = sympy.lambdify(self.dim, self.func, "numpy")
            numpy.seterr(divide='ignore', invalid='ignore')
            plane.append(f(*plane[:len(self)]) * one)
        except:
            subplane = [numpy.linspace(*bounds[i], density) for i in range(len(self))]
            if len(self) == 1:
                f = lambda x: self.func.subs({self.dim[0]: x})
                plane.append(numpy.array([f(x) for x in subplane[0]], dtype=float))
            else:
                f = lambda x, y: self.func.subs({self.dim[0]: x, self.dim[1]: y})
                plane.append(numpy.array([[f(x, y) for x in subplane[0]] for y in subplane[1]], dtype=float))
        cmap = None

        match len(self):
            case 1:
                match mode:
                    case "G":
                        if image is None:
                            fig, ax = matplotlib.pyplot.subplots(figsize=imagesize)
                            ax.set(xlim=bounds[0])
                            if bounds[1] is not None:
                                ax.set(ylim=bounds[1])
                            ax.set_xlabel(str(self.dim[0]))
                        else:
                            matplotlib.pyplot.figure(image)
                        matplotlib.pyplot.plot(*plane, color=color)
                    case "S":
                        raise ValueError("Can't visualize 1D Vector Field using isosurfaces")
            case 2:
                match mode:
                    case "G":
                        if image is None:
                            fig, ax = matplotlib.pyplot.subplots(figsize=imagesize, subplot_kw={"projection": "3d"})
                            ax.set(xlim=bounds[0], ylim=bounds[1])
                            if bounds[2] is not None:
                                ax.set(ylim=bounds[2])
                            ax.set_xlabel(str(self.dim[0]))
                            ax.set_ylabel(str(self.dim[1]))
                            ax.plot_surface(*plane, color=color)
                        else:
                            matplotlib.pyplot.figure(image)
                            image.get_axes()[0].plot_surface(*plane, color=color)
                    case "S":
                        if color == "D":
                            color = None
                            cmap = "viridis"
                        if image is None:
                            fig, ax = matplotlib.pyplot.subplots(figsize=imagesize)
                            ax.set(xlim=bounds[0], ylim=bounds[1])
                            ax.set_xlabel(str(self.dim[0]))
                            ax.set_ylabel(str(self.dim[1]))
                            ax.contour(*plane, levels, colors=color, cmap=cmap)
                        else:
                            matplotlib.pyplot.figure(image)
                            matplotlib.pyplot.contour(*plane, levels, colors=color, cmap=cmap)
        if showgrid:
            matplotlib.pyplot.grid()
        if show:
            matplotlib.pyplot.show()

    def __add__(self, other):
        """
        Возвращает ScalarField, функция которого является
        суммой функций self и other. Размерности скалярных
        полей должны совпадать

        >>> x, y = sympy.symbols("x y")
        >>> s = ScalarField(x**2 + y**2)
        >>> p = ScalarField(x - y**2)
        >>> s + p
        x**2 + x
        """

        return ScalarField(self.func + other.func, dim=self.dim)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        """
        Возвращает ScalarField, функция которого является
        произвдением функции self и other. other при помещении
        в sympify() обязан возвращать объект класса Expr

        >>> x, y = sympy.symbols("x y")
        >>> s = ScalarField(x + y)
        >>> s * 2
        2*x + 2*y
        >>> s * x
        x*(x + y)
        """

        if not (isinstance(sympy.sympify(other), sympy.Expr)):
            raise ValueError("Wrong type of input data (should be able to be turned into Sympy Expression)")

        if isinstance(other, ScalarField):
            return ScalarField(self.func * other.func, dim=self.dim)
        return ScalarField(self.func * sympy.sympify(other), dim=self.dim)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if not (isinstance(sympy.sympify(other), sympy.Expr)):
            raise ValueError("Wrong type of input data (should be able to be turned into Sympy Expression)")

        if isinstance(other, ScalarField):
            return ScalarField(self.func * other.func, dim=self.dim)
        return ScalarField(self.func / sympy.sympify(other), dim=self.dim)

    def __iadd__(self, other):
        return self + other

    def __isub__(self, other):
        return self - other

    def __imul__(self, other):
        return self * other

    def __pos__(self):
        return self

    def __neg__(self):
        return self * (-1)

    def __eq__(self, other):
        """
        ScalarField равен другому ScalarField тогда
        когда, когда функция первого ScalarField
        равна функции второго ScalarField

        >>> x, y = sympy.symbols("x y")
        >>> s = ScalarField(x**2 + y**2)
        >>> i = ScalarField(y**2 + x**2)
        >>> s == i
        True
        >>> p = ScalarField(x + y)
        >>> s == p
        False
        """

        if self.func == other.func:
            return True
        return False

    def __ne__(self, other):
        return not (self == other)

    def __len__(self):
        """
        Возвращает длину размерности векторного поля

        >>> x, y = sympy.symbols("x y")
        >>> s = ScalarField(x**2 + y**2)
        >>> len(s)
        2
        """

        return len(self.dim)

    def subs(self, *values):
        """
        Подставляет в функцию скалярного поля значения

        >>> x, y = sympy.symbols("x y")
        >>> s = ScalarField(x**2 + y**2)
        >>> s.subs(2, 2)
        8

        :param values: выражения, подставляемые в компоненты скалярного поля вместо координат. Каждая координата из self.dim будет заменена на соответственное значение в values, котороме может быть представлено как кортежом, так и словарём.

        """

        if any([not (isinstance(sympy.sympify(value), sympy.Expr)) for value in values]):
            raise ValueError("Can't subtract component")

        if isinstance(values[0], dict):
            if any([not (isinstance(sympy.sympify(value), sympy.Expr)) for value in values[0].values()]):
                raise ValueError("Can't subtract component")
            scheme = values[0]
        else:
            if any([not (isinstance(sympy.sympify(value), sympy.Expr)) for value in values]):
                raise ValueError("Can't subtract component")
            scheme = list(zip(self.dim, values))
        output = self.func.subs(scheme, simultaneous=True)
        return output

    def work(self, curve, bounds, numerical=False):
        """
        Возвращает криволинейный интеграл второго рода вдоль кривой.
        Другими словами, возвращает работу, которую совершает сила,
        представленная векторным полем, при прохождении МТ вдоль кривой.

        >>> x, y, t = sympy.symbols("x y t")
        >>> v = ScalarField(x+y)
        >>> v.work((t, 0), (t, 0, 2))
        2

        :param curve: кривая, заданная параметрически. Задаётся кортежом из функций от параметра - объектов, переводимых в sympy.Expr.
        :param bounds: границы интегрирования по кривой. Задаётся кортежом из переменной и пределов интегрирования
        :param numerical: численное решение или аналитическое
        """

        if len(curve) != len(self):
            raise ValueError("Dimensions of curve and VectorField don't match")

        function = 0
        scheme = list(zip(self.dim, curve))
        for i in range(len(self)):
            function += sympy.diff(curve[i], bounds[0]) ** 2
        function = function ** (1 / 2) * self.func.subs(scheme)
        line = sympy.Integral(function, bounds)
        if numerical:
            return line.evalf()
        else:
            return line.doit()

    def grad(self):
        """
        Возвращает VectorField, являющийся градиентом
        скалярного поля

        >>> x, y = sympy.symbols("x y")
        >>> s = ScalarField(x**2/2 + y**2/2)
        >>> s.grad()
        (x, y)
        """

        output = []
        for dim in self.dim:
            output.append(sympy.diff(self.func, dim))
        return VectorField(*output, dim=self.dim)

    def laplacian(self):
        return self.grad().div()

    def ordiff(self, *vector):
        """
        Возвращает значение производной по направлению в
        каждой точке скалярного поля

        >>> x, y = sympy.symbols("x y")
        >>> s = ScalarField(x**2 + y**2)
        >>> s.ordiff(3, 4)
        1.2*x + 1.6*y

        :param vector: вектор, задающий направление производной, состоящий из объектов, переводимых в sympy.Expr.
        """

        if any([not (isinstance(i, (int, float))) for i in vector]):
            raise ValueError("Wrong type of input data: vector components can be only numbers")

        length = sum(map(lambda x: x ** 2, vector)) ** .5
        return VectorField(*vector, dim=self.dim) * self.grad() / length
