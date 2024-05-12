Модуль для работы с векторными полями. Разработал в качестве школьного проекта.

VectorField(\*comps, dim = None)

`	`Векторное поле может быть задано с помощью

проекций векторов в каждой точке поля на

некоторые координатные оси.

\>>> x, y, z, t, p = sympy.symbols("x y z t p")

\>>> v = VectorField(x+y, y\*\*2, z\*y)

\>>> u = VectorField(t - p, p, dim=(t, p))

:param comps: компоненты векторного поля - объекты, переводимые в sympy.Expr

:param dim: кортеж из обозначений координат векторного поля - объектов, переводимых в sympy.Expr



VectorField.\_\_repr\_\_()

Возваращает строку в формате (F1, F2, F3...),

где F1, F2, F3... - проекции векторного поля

\>>> x, y, z = sympy.symbols("x y z")

\>>> v = VectorField(x+y, y\*\*2, z\*y)

\>>> print(v)

(x + y, y\*\*2, y\*z)



VectorField.visualize(image=None, scale=True, density=11, bounds=((-10, 10), (-10, 10), (-10, 10)),

description={"width": False, "length": False, "alpha": False, "color": False},

mode="A", width=0.005, length=1, alpha=1, color="black", imagesize=(10, 10), normalize=False, show=True)

`	`Визуализирует дву- или трёхмерное векторное поле с помощью matplotlib

\>>> x, y = sympy.symbols("x y")

\>>> v = VectorField(x+y, y\*\*2)

\>>> v.visualize(density = 30, color = "blue", width = 0.003)

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

`	`:param show: показывать или не показывать изображение



VectorField.\_\_add\_\_(self, other):

Возвращает VectorField, каждый компонент которого

является суммой соответствующих компонент входных

векторных полей. Размерности входных векторных полей

обязаны совпадать

\>>> x, y, z = sympy.symbols("x y z")

\>>> v = VectorField(x+y, y\*\*2, z\*y)

\>>> u = VectorField(x-y, 1/y, z)

\>>> u + v

(2\*x, y\*\*2 + 1/y, y\*z + z)



VectorField.\_\_mul\_\_(self, other):

В случае если other представлен численным типом данных

возваращает VectorField, каждый компонент которого является

произведением компоненты self и данного скаляра

\>>> x, y = sympy.symbols("x y")

\>>> v = VectorField(x, 1)

\>>> v \* 2

(2\*x, 2)

В случае если other представлен VectorField

возвращает Expr, который представляет собой

скалярное произведение компонент self и other.

Размерности self и other обязаны совпадать

\>>> x, y, z = sympy.symbols("x y z")

\>>> v = VectorField(x+y, y\*\*2, z\*y)

\>>> u = VectorField(x-y, 1/y, z)

\>>> u \* v

y\*z\*\*2 + y + (x - y)\*(x + y)



VectorField.\_\_eq\_\_(self, other):

VectorField равен другому VectorField тогда,

когда совпадают их компоненты и размерности

\>>> x, y = sympy.symbols("x y")

\>>> v = VectorField(x+y, y\*\*2)

\>>> u = VectorField(x+y, y\*\*2)

\>>> t = VectorField(x-y, 1/y)

\>>> u == v

True

\>>> u == t

False



VectorField.\_\_setitem\_\_(self, key, value):

Позволяет вручную задать компоненту векторного поля

\>>> x, y = sympy.symbols("x y")

\>>> v = VectorField(x+y, y\*\*2)

\>>> v[x] = x\*y

\>>> v

(x\*y, y\*\*2)

:param key: координата компоненты векторного поля в виде sympy.Symbol

:param value: задаваемое значение компоненты векторного поля - объекта, переводимого в sympy.Expr



VectorField.\_\_getitem\_\_(self, key):

Позволяет получить компоненту векторного поля по

координате или по индексу в self.\_comps

\>>> x, y = sympy.symbols("x y")

\>>> v = VectorField(x+y, y\*\*2)

\>>> v[x]

x + y

\>>> v[1]

y\*\*2

:param key: координата компоненты векторного поля либо в виде строки, либо в виде числа - индекса в self.\_comps



VectorField.\_\_iter\_\_(self):

Позволяет использовать VectorField в цикле for

при этом должны перебирается кортежи, состоящие из

двух объектов: координаты и компоненты

\>>> x, y = sympy.symbols("x y")

\>>> v = VectorField(x+y, y\*\*2)

\>>> for coordinate, component in v: print(coordinate, component)

x x + y

y y\*\*2



VectorField.\_\_len\_\_(self):

Возвращает длину self.dim

\>>> x, y = sympy.symbols("x y")

\>>> v = VectorField(x+y, y\*\*2)

\>>> len(v)

2



vecfield.VectorField,subs(self, \*values):

Позволяет подставить числа в векторное поле вместо координат.

Возвращает кортеж из компонент после подстановки значений

\>>> x, y = sympy.symbols("x y")

\>>> v = VectorField(x+y, y\*\*2)

\>>> v.subs(1, 2)

(3, 4)

\>>> v.subs({x : y, y : x\*\*2})

(x\*\*2 + y, x\*\*4)

:param values: выражения, подставляемые в компоненты векторного поля вместо координат. Каждая координата из self.dim будет заменена на соответственное значение в values, которое может быть представлено как кортежом, так и словарём.



vecfield.VectorField,div(self):

Возвращает ScalarField, который представляет собой

дивергенцию векторного поля

\>>> x, y = sympy.symbols("x y")

\>>> v = VectorField(x+y, y\*\*2)

\>>> v.div()

2\*y + 1



vecfield.VectorField,curl(self):

Возвращает VectorField, который является ротором векторного поля.

\>>> x, y, z = sympy.symbols("x y z")

\>>> v = VectorField(x+y, y\*\*2, z\*y)

\>>> v.curl()

(z, 0, -1)



vecfield.VectorField,work(self, curve, bounds, numerical=False):

Возвращает криволинейный интеграл второго рода вдоль кривой.

Другими словами, возвращает работу, которую совершает сила,

представленная векторным полем, при прохождении МТ вдоль кривой.

\>>> x, y, t = sympy.symbols("x y t")

\>>> v = VectorField(0, -10)

\>>> v.work((t\*\*2-1, t), (t, 0, 4))

- 40

:param curve: кривая, заданная параметрически. Задаётся кортежом из функций от параметра - объектов, переводимых в sympy.Expr.

:param bounds: границы интегрирования по кривой. Задаётся кортежом из переменной и пределов интегрирования

:param numerical: численное решение или аналитическое



vecfield.VectorField,flux(self, region, \*bounds, numerical=True):

Возвращает поверхностный интеграл второго рода по поверхности.

Другими словами, возвращает количество жидкости, которое протечёт

через поверхность, заданной region, поле скоростей которой задано

векторным полем за единицу времени

\>>> x, y, z, t, p = sympy.symbols("x y z t p")

\>>> v = VectorField(2, 0, 0)

\>>> v.flux((1, t, p), (t, -2, 2), (p, -2, 2))

32

:param region: кривая/поверхность, заданная параметрически. Задаётся кортежом из зависящих от нескольких параметров функций - объектов, переводимых в sympy.Expr.

:param bounds: границы интегрирования по кривой/поверхности. Задаются несколькими кортежами, которые содержат переменную и пределы интегрирования.

:param numerical: численное решение или аналитическое



vecfield.VectorField,potential(self):

Возвращает потенциал векторного поля, если он имеется.

Если поле не потенциально, будет вызвано исключение.

\>>> x, y = sympy.symbols("x y")

\>>> v = VectorField(-x, 0)

\>>> v.potential()

- x\*\*2/2



vecfield.VectorField,is\_potential(self):

Возвращает True, если поле потенциально,

и False в противном случае

\>>> x, y = sympy.symbols("x y")

\>>> v = VectorField(-x, 0)

\>>> v.is\_potential()

True

\>>> u = VectorField(y, -x)

\>>> u.is\_potential()

False



vecfield.VectorField,is\_solenoid(self):

Возвращает True, если поле соленоидально,

и False в противном случае

\>>> x, y = sympy.symbols("x y")

\>>> v = VectorField(x, y)

\>>> v.is\_solenoid()

False

\>>> u = VectorField(y, x)

\>>> u.is\_solenoid()

True





vecfield.ScalarField.\_\_init\_\_(self, func=0, dim=None):

Скалярное поле может быть задано с помощью функции

нескольких переменных, являющихся координатами точки.

\>>> x, y, z, v, t = sympy.symbols("x y z v t")

\>>> s = ScalarField(x\*\*2 + y\*\*2 + z\*\*2)

\>>> p = ScalarField(v + t, dim=(t, v))

:param func: функция нескольких переменных, задающая скалярное поле - объект, переводимый в sympy.Expr.

:param dim: кортеж из обозначений координат скалярного поля - объектов, переводимых в sympy.Expr.



vecfield.ScalarField.\_\_repr\_\_(self):

Возваращает строку, содержащую функцию ScalarField

\>>> x, y = sympy.symbols("x y")

\>>> s = ScalarField(x\*\*2 + y\*\*2)

\>>> print(s)

x\*\*2 + y\*\*2



vecfield.ScalarField.visualize(self,

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

Визуализирует одно- или двумерное скалярное поле с помощью matplotlib

\>>> x, y = sympy.symbols("x y")

\>>> s = ScalarField(x\*\*2 + y\*\*2)

\>>> s.visualize()

:param image: изображение (figure), на котором будет отриосвано векторное поле

:param scale: смасштабировать скалярное поле на изображение

:param bounds: границы отрисовки скалярного поля

:param density: точность прорисовки скалярного поля

:param levels: количество эквипотенциальных поверхностей в режиме эквипотенциальных поверхностей

:param mode: режим отрисовки скалярного поля. В режиме "G" отрисовывает скалярное поле как график. В режиме "S" отрисовывает скалярное поле с помощью эквипотенциальных поверхностей. Отсутствует для одномерных скалярных полей.

:param color: цвет отрисовки графика скалярного поля. В режиме эквипотенциальных поверхностей может принимать особое значение "D". В таком случае каждый уровень будет иметь свой цвет в зависимости от значения функции на этом уровне.

:param showgrid: отрисовка сетки для координатной плоскости.

:param imagesize: размеры изображения



vecfield.ScalarField.\_\_add\_\_(self, other):

Возвращает ScalarField, функция которого является

суммой функций self и other. Размерности скалярных

полей должны совпадать

\>>> x, y = sympy.symbols("x y")

\>>> s = ScalarField(x\*\*2 + y\*\*2)

\>>> p = ScalarField(x - y\*\*2)

\>>> s + p

x\*\*2 + x



vecfield.ScalarField.\_\_mul\_\_(self, other):

Возвращает ScalarField, функция которого является

произвдением функции self и other. other при помещении

в sympify() обязан возвращать объект класса Expr

\>>> x, y = sympy.symbols("x y")

\>>> s = ScalarField(x + y)

\>>> s \* 2

2\*x + 2\*y

\>>> s \* x

x\*(x + y)



vecfield.ScalarField.\_\_eq\_\_(self, other):

ScalarField равен другому ScalarField тогда

когда, когда функция первого ScalarField

равна функции второго ScalarField

\>>> x, y = sympy.symbols("x y")

\>>> s = ScalarField(x\*\*2 + y\*\*2)

\>>> i = ScalarField(y\*\*2 + x\*\*2)

\>>> s == i

True

\>>> p = ScalarField(x + y)

\>>> s == p

False



vecfield.ScalarField.\_\_len\_\_(self):

Возвращает длину размерности векторного поля

\>>> x, y = sympy.symbols("x y")

\>>> s = ScalarField(x\*\*2 + y\*\*2)

\>>> len(s)

2



vecfield.ScalarField.subs(self, \*values):

Подставляет в функцию скалярного поля значения

\>>> x, y = sympy.symbols("x y")

\>>> s = ScalarField(x\*\*2 + y\*\*2)

\>>> s.subs(2, 2)

8

:param values: выражения, подставляемые в компоненты скалярного поля вместо координат. Каждая координата из self.dim будет заменена на соответственное значение в values, котороме может быть представлено как кортежом, так и словарём.



vecfield.ScalarField.work(self, curve, bounds, numerical=False):

Возвращает криволинейный интеграл второго рода вдоль кривой.

Другими словами, возвращает работу, которую совершает сила,

представленная векторным полем, при прохождении МТ вдоль кривой.

\>>> x, y, t = sympy.symbols("x y t")

\>>> v = ScalarField(x+y)

\>>> v.work((t, 0), (t, 0, 2))

2

:param curve: кривая, заданная параметрически. Задаётся кортежом из функций от параметра - объектов, переводимых в sympy.Expr.

:param bounds: границы интегрирования по кривой. Задаётся кортежом из переменной и пределов интегрирования

:param numerical: численное решение или аналитическое



vecfield.ScalarField.grad(self):

Возвращает VectorField, являющийся градиентом

скалярного поля

\>>> x, y = sympy.symbols("x y")

\>>> s = ScalarField(x\*\*2/2 + y\*\*2/2)

\>>> s.grad()

(x, y)



vecfield.ScalarField.ordiff(self, \*vector):

Возвращает значение производной по направлению в

каждой точке скалярного поля

\>>> x, y = sympy.symbols("x y")

\>>> s = ScalarField(x\*\*2 + y\*\*2)

\>>> s.ordiff(3, 4)

1. 2\*x + 1.6\*y

:param vector: вектор, задающий направление производной, состоящий из объектов, переводимых в sympy.Expr.
