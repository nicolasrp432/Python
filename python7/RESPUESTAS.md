# Respuestas y Explicaciones — DataDeck: Abstract Card Architecture

> Complemento al REPASO.md. Aquí están las respuestas razonadas a cada pregunta,
> con contexto adicional para que puedas entender el "por qué" detrás de cada decisión.

---

## BLOQUE 0 — Fundamentos

**¿Qué es una clase en Python? ¿Qué diferencia hay entre una clase y un objeto?**

Una **clase** es una plantilla o molde que define estructura y comportamiento.
Un **objeto** es una instancia concreta creada a partir de esa plantilla.

```python
class Perro:          # <-- esto es la clase (molde)
    def __init__(self, nombre):
        self.nombre = nombre

rex = Perro("Rex")    # <-- esto es el objeto (instancia concreta)
```

Puedes crear miles de objetos distintos (`rex`, `fido`, `laika`) a partir del mismo molde `Perro`. Cada uno tiene su propio estado (`nombre` distinto) pero comparte la misma estructura.

---

**¿Qué es la herencia? ¿Para qué sirve?**

La herencia permite que una clase **tome todo lo que ya tiene otra clase** y lo extienda o modifique. Es el mecanismo de reutilización más fundamental en OOP.

```python
class Animal:
    def describe(self):
        return "Soy un animal"

class Perro(Animal):   # Perro hereda de Animal
    def hablar(self):
        return "Guau"

rex = Perro()
rex.describe()  # funciona aunque Perro no lo define — lo heredó
```

Sirve para no repetir código y para establecer relaciones "ES-UN": un `Perro` ES UN `Animal`.

---

**¿Qué significa que una clase sea "abstracta"?**

Una clase abstracta es una clase que **no puede instanciarse directamente** — existe solo para ser heredada. Su propósito es definir una interfaz (un contrato): "cualquier clase que herede de mí DEBE implementar estos métodos".

Es como un contrato laboral: define las obligaciones pero no las ejecuta ella misma.

---

**¿Qué hace `from abc import ABC, abstractmethod`?**

- `ABC` (Abstract Base Class): clase de la que heredas para volver tu clase abstracta.
- `@abstractmethod`: decorador que marca un método como "obligatorio para las subclases".

Sin importar esto, Python no tiene forma nativa de forzar que las subclases implementen ciertos métodos.

---

**¿Qué pasa si intentas instanciar una clase abstracta directamente?**

```python
TypeError: Can't instantiate abstract class Animal with abstract method speak
```

Python lanza este error en el momento de la instanciación, no al definir la clase. Es una protección en tiempo de ejecución.

---

**¿Qué es una anotación de tipo (`name: str`, `-> None`)? ¿Por qué las usamos?**

Las anotaciones de tipo son **metadatos** que le dicen a los desarrolladores (y a herramientas como mypy) qué tipo se espera en cada parámetro o valor de retorno.

```python
def saludar(nombre: str) -> str:
    return f"Hola, {nombre}"
```

Python NO las enforza en tiempo de ejecución — si pasas un `int`, no da error. Pero:
- `mypy` sí las verifica estáticamente antes de ejecutar
- Son documentación automática: leyendo la firma sabes exactamente qué recibe y qué devuelve
- Los IDEs las usan para autocompletado y detección de errores

---

**¿Qué hace `__init__`? ¿Cuándo se llama?**

`__init__` es el **inicializador** (comúnmente llamado constructor). Se llama automáticamente justo después de que Python crea el objeto en memoria, permitiéndote inicializar sus atributos.

```python
class Punto:
    def __init__(self, x: int, y: int) -> None:
        self.x = x  # se ejecuta nada más hacer Punto(3, 4)
        self.y = y
```

El objeto ya existe cuando `__init__` se ejecuta — por eso `self` ya está disponible.

---

**¿Qué es `self`?**

`self` es una referencia al **objeto concreto** sobre el que se está llamando el método. Es el primer parámetro de todo método de instancia, y Python lo pasa automáticamente.

```python
p1 = Punto(1, 2)
p2 = Punto(3, 4)
p1.describe()  # Python lo convierte en Punto.describe(p1)
               # dentro, self == p1
```

Cuando haces `self.x = 5`, estás creando un atributo `x` en ESE objeto específico, no en la clase.

---

## BLOQUE 1 — Exercise 0: Abstract Factory Pattern

### `ex0/creature.py`

**1. ¿Por qué `Creature` hereda de `ABC`?**

Para que Python sepa que es abstracta y no permita instanciarla directamente. Sin `ABC`, podrías hacer `Creature("algo", "tipo")` y obtener un objeto incompleto (sin `attack` implementado).

---

**2. ¿Por qué `attack` es abstracto pero `describe` no?**

Porque `describe` tiene una implementación genérica que sirve para TODAS las criaturas: siempre devuelve `"X is a Y type Creature"`. No hay razón para que cada subclase la reimplemente.

`attack`, en cambio, es específico de cada criatura: `Flameling` usa fuego, `Aquabub` usa agua. No existe una implementación genérica sensata, así que se fuerza a las subclases a definirla.

**Regla general:** si la implementación es la misma para todos, ponla en la clase base. Si cada subclase necesita su propia versión, hazla abstracta.

---

**3. Si `describe` es concreto, ¿pueden las subclases sobreescribirlo?**

Sí, perfectamente. Una subclase puede redefinir cualquier método concreto heredado:

```python
class Flameling(Creature):
    def describe(self) -> str:
        return "I am a fiery Flameling, fear me!"
```

Si no lo sobreescribe, usa el de `Creature`. Si lo sobreescribe, usa el suyo propio.

---

**4. ¿Qué pasa si una subclase no implementa `attack`?**

Python no permite instanciarla:

```python
class MalaCriatura(Creature):
    pass  # olvidé implementar attack

MalaCriatura("X", "Y")
# TypeError: Can't instantiate abstract class MalaCriatura with abstract method attack
```

Esto es exactamente el valor de `@abstractmethod`: actúa como una red de seguridad.

---

**5. ¿Qué tipo retorna `attack`? ¿Por qué `str` y no `None`?**

Retorna `str`. Porque `attack` describe la acción ("Flameling uses Ember!") — es un mensaje que el código llamante puede imprimir, guardar, enviar, etc.

Si retornara `None` y hacía `print()` internamente, el método decidiría cómo mostrarse. Retornando `str`, el que llama decide qué hacer con el mensaje. Esto es **separación de responsabilidades**.

---

**6. ¿Qué significa `-> None` en `__init__`?**

Indica que `__init__` no retorna nada (retorna `None` implícitamente). Es la convención en Python: los inicializadores siempre devuelven `None`, y anotar `-> None` lo hace explícito para herramientas de análisis estático.

---

**7. ¿Por qué el atributo se llama `creature_type` y no solo `type`?**

`type` es una función built-in de Python que devuelve la clase de un objeto:

```python
type(42)      # <class 'int'>
type("hola")  # <class 'str'>
```

Si usaras `self.type = creature_type` en `Creature`, al hacer `creature.type` obtendrías el string "Fire" en vez de la clase `Flameling`. No rompe nada directamente, pero es confuso y puede ocultar bugs si alguien intenta usar `type()` en el objeto.

---

### `ex0/factory.py`

**1. ¿Por qué `CreatureFactory` también es abstracta?**

Porque `CreatureFactory` es solo un contrato: define qué métodos debe tener una fábrica (`create_base`, `create_evolved`), pero no sabe qué criaturas concretas crear. Cada familia concreta (`FlameFactory`, `AquaFactory`) implementa esa lógica.

Si `CreatureFactory` no fuera abstracta, podrías instanciarla y llamar a `factory.create_base()` — que no está implementada — y obtendrías un `NotImplementedError` en tiempo de ejecución en vez de en tiempo de instanciación.

---

**2. ¿Qué le impide al usuario del paquete instanciar `CreatureFactory()` directamente?**

El mecanismo de `ABC` + `@abstractmethod`. Como `create_base` y `create_evolved` son abstractos, Python lanza `TypeError` si intentas hacer `CreatureFactory()`.

---

**3. ¿Qué retorna `create_base`? ¿`Creature` o una subclase concreta?**

El **tipo declarado** en la firma es `Creature` (la abstracta). El **tipo real** en tiempo de ejecución será una subclase concreta (`Flameling`, `Aquabub`).

```python
factory = FlameFactory()
criatura = factory.create_base()  # tipo real: Flameling
                                  # tipo declarado: Creature
```

Esto es polimorfismo: el tipo de retorno declara la interfaz mínima garantizada.

---

**4. ¿Qué ventaja tiene que el tipo de retorno sea `Creature` (la abstracta)?**

El código que recibe la criatura solo necesita saber que tiene `.describe()` y `.attack()`. No importa si es `Flameling` o `Aquabub`. Esto permite escribir funciones como:

```python
def test_factory(factory: CreatureFactory) -> None:
    base = factory.create_base()  # no sabe ni le importa qué clase es
    print(base.describe())        # solo usa la interfaz de Creature
    print(base.attack())
```

Si mañana añades `EarthFactory`, esta función funciona sin modificarse. Eso es el **principio Open/Closed**: abierto para extensión, cerrado para modificación.

---

### `ex0/flame.py`

**1. ¿Qué hace `super().__init__("Flameling", "Fire")`?**

Llama al `__init__` de la clase padre (`Creature`) con los argumentos específicos de `Flameling`. Es la forma de inicializar la parte "Creature" del objeto.

Sin esta llamada, `self.name` y `self.creature_type` no existirían, y `describe()` fallaría.

---

**2. ¿Por qué `Flameling.__init__` no necesita parámetros?**

Porque `Flameling` siempre se llama igual: "Flameling", tipo "Fire". Esos valores están hardcodeados. El usuario no puede (ni necesita) personalizar el nombre o tipo — es una criatura específica.

```python
f = Flameling()   # sin argumentos
# vs
f = Flameling("MiFlameling", "Fire")  # esto no tiene sentido
```

---

**3. ¿Qué pasa en memoria cuando haces `f = Flameling()`?**

```
1. Python reserva memoria para un nuevo objeto
2. Llama a Flameling.__init__(self)
3. Dentro, se ejecuta super().__init__("Flameling", "Fire")
4. Que llama a Creature.__init__(self, "Flameling", "Fire")
5. Que ejecuta:
     self.name = "Flameling"
     self.creature_type = "Fire"
6. El objeto queda con:
     f.name          → "Flameling"
     f.creature_type → "Fire"
     f.attack()      → método heredado de Flameling
     f.describe()    → método heredado de Creature
```

---

### `ex0/__init__.py`

**1. ¿Por qué solo expone `FlameFactory` y `AquaFactory`, no `Flameling` o `Pyrodon`?**

El principio de **encapsulación**: el paquete expone solo la API pública. El usuario del paquete no necesita saber que existe `Flameling` — solo necesita usar `FlameFactory().create_base()`. Las clases concretas son detalles de implementación.

Si expusieras `Flameling`, el usuario podría instanciarla directamente y saltarse el patrón de fábrica que tanto cuidaste diseñar.

---

**2. ¿Qué significa `__all__`?**

Es una lista que define qué nombres se exportan cuando alguien hace `from ex0 import *`. También es una señal explícita de cuál es la API pública del módulo.

Sin `__all__`, `from ex0 import *` importaría todo lo que no empiece por `_`. Con `__all__`, solo importa lo que está en la lista.

---

**3. Si hago `from ex0 import Flameling`, ¿qué pasa?**

```
ImportError: cannot import name 'Flameling' from 'ex0'
```

`Flameling` no está en `__init__.py`, así que el paquete `ex0` no la conoce.

---

**4. ¿Puedo hacer `from ex0.flame import Flameling`?**

Técnicamente sí — el archivo `flame.py` existe y `Flameling` está definida ahí. Pero viola el diseño intencionado: estás importando directamente de un módulo interno, no de la API pública del paquete. En una librería real, esto se documenta como "no hagas esto".

---

### `battle.py`

**1. ¿Qué tipo tiene el parámetro `factory`? ¿Por qué no ponemos `FlameFactory`?**

Tipo `CreatureFactory`. Porque la función `test_factory` no le importa QUÉ tipo de fábrica es — solo necesita que tenga `create_base()` y `create_evolved()`. Si pusiera `FlameFactory`, la función solo funcionaría con fuego.

---

**2. ¿Puedo llamar a `test_factory` con `AquaFactory()`? ¿Por qué?**

Sí. `AquaFactory` hereda de `CreatureFactory` — es un `CreatureFactory`. Python acepta cualquier subclase donde se espera la clase base. Esto es el **principio de sustitución de Liskov**: puedes usar una subclase en cualquier lugar donde se usa la clase base.

---

**3. ¿Qué es el polimorfismo aquí? Da el ejemplo concreto.**

`test_factory` llama a `base.attack()` sin saber si `base` es `Flameling` o `Aquabub`. Cada uno ejecuta SU versión de `attack`. La misma llamada produce resultados distintos según el tipo real del objeto:

```python
# con FlameFactory: base.attack() → "Flameling uses Ember!"
# con AquaFactory:  base.attack() → "Aquabub uses Water Splash!"
```

---

**4. ¿Qué hace `print(base.describe())` paso a paso?**

```
1. base es un objeto Flameling (por ejemplo)
2. Python busca describe() en Flameling — no la tiene
3. Sube al MRO: busca en Creature — sí la tiene
4. Ejecuta Creature.describe(self):
     return f"{self.name} is a {self.creature_type} type Creature"
     → "Flameling is a Fire type Creature"
5. print() recibe ese string y lo muestra en consola
```

---

**5. ¿Sabemos, dentro de `test_battle`, qué clase concreta son `creature1` y `creature2`?**

No. Solo sabemos que son `Creature`. Y eso es exactamente el punto: no necesitamos saberlo. Confiamos en que tienen `attack()` porque `Creature` lo garantiza.

---

**6. ¿Qué pasaría si `attack()` estuviera en `CreatureFactory` en vez de `Creature`?**

No tendría sentido. Una fábrica crea objetos; no ataca. Mezclaría responsabilidades. Además, `test_battle` recibe criaturas, no fábricas — no tendría acceso a `attack()`.

---

## BLOQUE 2 — Exercise 1: Capabilities (Mixins)

### `ex1/capabilities.py`

**1. ¿Por qué `HealCapability` NO hereda de `Creature`?**

Porque `HealCapability` no ES una criatura — es una **capacidad**. Si heredara de `Creature`, cualquier clase que usara `HealCapability` tendría que inicializar también `name` y `creature_type`, creando conflictos de herencia múltiple innecesarios.

Un mixin debe ser lo más ligero posible: solo la capacidad, nada más.

---

**2. ¿Qué pasaría si heredara de `Creature`? ¿Qué problemas crearía?**

El "diamante de la muerte": `Sproutling` heredaría de `Creature` (directamente) y de `HealCapability` (que también hereda de `Creature`). Habría dos caminos para llegar a `Creature.__init__`, y decidir cuál llamar se vuelve ambiguo y frágil.

```
         Creature
        /        \
  Creature    HealCapability   ← HealCapability hereda de Creature
        \        /
         Sproutling            ← ¡dos caminos al mismo padre!
```

---

**3. ¿Puede existir una clase que herede solo de `HealCapability` sin ser `Creature`?**

Técnicamente sí. Pero en el contexto de este diseño, no tiene sentido — las estrategias esperan `Creature`. Un objeto que solo sea `HealCapability` no podría usarse en las batallas.

---

**4. ¿Por qué `TransformCapability` tiene `__init__` pero `HealCapability` no?**

Porque `TransformCapability` necesita **estado**: el atributo `_transformed` que registra si la criatura se ha transformado. `HealCapability` no tiene estado propio — solo define el método `heal()`.

Regla: un mixin solo necesita `__init__` si tiene atributos propios que inicializar.

---

**5. ¿Qué significa el guion bajo en `_transformed`?**

Es una convención en Python para indicar "atributo privado por convención". No es privado a nivel del lenguaje (Python no fuerza privacidad), pero es un acuerdo entre desarrolladores: "no accedas a esto directamente desde fuera de la clase".

`__transformed` (doble guion bajo) activaría el *name mangling* de Python, haciéndolo más difícil de acceder pero no imposible. El guion simple es más común en la práctica.

---

**6. ¿Por qué el estado `_transformed` está en `TransformCapability` y no en `Shiftling`?**

Porque el estado pertenece a la **capacidad**, no a la criatura específica. Si mañana creas otra criatura transformable (`Morphling`), no necesitas redefinir `_transformed` — lo hereda de `TransformCapability`.

Es encapsulación: el estado y los métodos que lo manipulan van juntos.

---

**7. ¿Qué pasa si dos instancias de `Shiftling` comparten el mismo estado?**

No lo comparten. Cada instancia tiene su propio `__dict__` (diccionario de atributos). Cuando haces `s1 = Shiftling()`, Python crea un objeto nuevo en memoria con su propio `_transformed = False`. `s2 = Shiftling()` crea otro objeto independiente.

```python
s1 = Shiftling()
s2 = Shiftling()
s1.transform()
print(s1._transformed)  # True
print(s2._transformed)  # False — completamente independiente
```

---

### Herencia múltiple en `ex1/healing.py`

**1. ¿Qué es el MRO? ¿Cuál es el MRO de `Sproutling`?**

El MRO (Method Resolution Order) es el orden en que Python busca métodos cuando hay herencia múltiple. Se calcula con el algoritmo C3 Linearization.

```
Sproutling → Creature → HealCapability → ABC → object
```

Cuando llamas a `sproutling.describe()`, Python busca en `Sproutling` (no está), luego en `Creature` (está) — y para ahí.

```python
print(Sproutling.__mro__)
# (<class 'Sproutling'>, <class 'Creature'>, <class 'HealCapability'>, <class 'ABC'>, <class 'object'>)
```

---

**2. ¿Por qué llamamos `Creature.__init__` explícitamente en vez de `super().__init__`?**

Para evitar ambigüedad con el MRO. Si usaras `super().__init__("Sproutling", "Grass")` en `Sproutling`, llamaría a `Creature.__init__`. Pero si `Creature` usara `super().__init__()` internamente, el MRO llevaría esa llamada a `HealCapability.__init__()` — que no existe — y luego a `ABC.__init__()`, que no espera `name` ni `creature_type`.

Llamando explícitamente `Creature.__init__(self, ...)`, controlamos exactamente qué se inicializa, sin sorpresas del MRO.

---

**3 y 4 y 5. ¿`Sproutling` es instancia de `Creature`? ¿Y de `HealCapability`?**

```python
isinstance(Sproutling(), Creature)       # True — hereda directamente
isinstance(Sproutling(), HealCapability) # True — también hereda de ella
isinstance(Sproutling(), ABC)            # True — ABC es ancestro de ambas
```

`isinstance` verifica toda la cadena de herencia, no solo el padre inmediato.

---

### `Shiftling` y estado de transformación

**1. ¿Qué devuelve `Shiftling().attack()` sin llamar a `transform()` antes?**

```
"Shiftling attacks normally."
```

Porque `_transformed` es `False` por defecto (inicializado en `TransformCapability.__init__`).

---

**2. ¿Qué devuelve `Shiftling().attack()` después de llamar a `transform()`?**

```
"Shiftling performs a boosted strike!"
```

`transform()` pone `_transformed = True`, y `attack()` comprueba ese valor.

---

**3. ¿Qué pasa si llamas a `transform()` dos veces seguidas?**

Nada especial: `_transformed` ya es `True`, vuelve a ponerse `True`. El mensaje de retorno es el mismo. No hay error, pero es idempotente (llamarlo una o veinte veces tiene el mismo efecto).

---

**4. ¿Qué pasa si llamas a `revert()` sin haber llamado a `transform()` antes?**

`revert()` pone `_transformed = False` (que ya era `False`). Devuelve su mensaje normalmente. No hay error — simplemente no tiene efecto visible.

---

**5 y 6. ¿Por qué `transform()` RETORNA un string en vez de hacer `print()`?**

**Separación de responsabilidades.** El método hace su trabajo (cambiar estado) y reporta la acción como string. Quien lo llama decide qué hacer con ese string: imprimirlo, guardarlo en un log, enviarlo por red, ignorarlo.

Si el método llamara a `print()` internamente:
- No podrías usarlo en un contexto donde no quieres output en consola (tests, servidores)
- No podrías capturar el mensaje para procesarlo
- Forzarías una dependencia con `stdout` que no tiene nada que ver con la lógica del juego

---

### `capacitor.py`

**1. ¿Por qué usamos `isinstance` aquí?**

Porque en tiempo de ejecución recibimos un objeto `Creature` genérico y no sabemos si tiene `heal()` o no. `isinstance(creature, HealCapability)` verifica si el objeto concreto tiene esa capacidad antes de llamar al método.

---

**2. ¿Podríamos evitar el `isinstance` con un mejor diseño? ¿Cómo?**

Sí. Una alternativa es el patrón **Null Object**: dar a `Creature` un método `heal()` base que devuelve "no puedo curarme" o simplemente no hace nada. Así todos los objetos responden al mismo mensaje sin necesitar `isinstance`.

Otra opción: usar el patrón **Visitor**. Pero para este proyecto, `isinstance` es la solución más directa y legible.

---

**3. ¿Qué pasaría si no tuviéramos el `isinstance` y llamáramos `creature.heal()` en un `Shiftling`?**

```
AttributeError: 'Shiftling' object has no attribute 'heal'
```

`Shiftling` hereda de `TransformCapability`, no de `HealCapability`. No tiene el método `heal`. El programa crashearía.

---

## BLOQUE 3 — Exercise 2: Strategy Pattern

### `ex2/strategy.py`

**1. ¿Por qué `act` retorna `None` en vez de `str`?**

Porque `act` es el punto de entrada que **orquesta** la batalla: llama a varios métodos y hace `print()` con sus resultados. No tiene un único string que retornar — produce múltiples líneas de output. Retornar `None` e imprimir directamente es la decisión de diseño aquí.

(Un diseño alternativo sería retornar `list[str]` y dejar que el llamante imprima — cada enfoque tiene sus trade-offs.)

---

**2. ¿Qué hace `is_valid`? ¿Por qué existe por separado de `act`?**

`is_valid` permite verificar ANTES de actuar si una estrategia puede aplicarse a una criatura. Esto permite:

```python
if strategy.is_valid(creature):
    strategy.act(creature)
else:
    # manejar el caso inválido de otra forma
```

Si solo existiera `act` (que lanza excepción si es inválido), el llamante no podría comprobar antes. Tener ambos da más flexibilidad.

---

**3. ¿Para qué sirve tener la clase abstracta `BattleStrategy` con duck typing?**

Con duck typing, cualquier objeto con `is_valid` y `act` funcionaría. Pero la clase abstracta aporta:

1. **Garantía en tiempo de definición**: si creas `class MiStrategy(BattleStrategy)` y olvidas `is_valid`, Python te avisa al instanciar — no al llamar.
2. **Verificación con mypy**: mypy puede comprobar que pasas un `BattleStrategy` correcto.
3. **Documentación estructural**: la clase abstracta dice exactamente qué contrato debe cumplir cualquier estrategia.

---

**4. ¿Por qué `is_valid` usa `isinstance(creature, TransformCapability)`?**

Porque `AggressiveStrategy` llama a `transform()` y `revert()`, que son métodos de `TransformCapability`. Solo criaturas que hereden de `TransformCapability` (como `Shiftling`) tienen esos métodos. La comprobación previene el `AttributeError`.

---

**5. ¿Para qué sirve el `assert isinstance(creature, TransformCapability)` después del `if not self.is_valid`?**

No es para Python en tiempo de ejecución (ya sabemos que llegamos ahí porque `is_valid` fue `True`). Es para **mypy** (el analizador estático).

Dentro de `act`, `creature` está tipado como `Creature`. `Creature` no tiene `transform()`. Sin el `assert`, mypy daría error: "Creature doesn't have attribute transform". El `assert` le dice a mypy: "en este punto, te garantizo que creature también es TransformCapability" — y mypy confía en eso.

---

**6 y 7. ¿Qué es `InvalidStrategyError`? ¿Por qué no usamos `ValueError`?**

`InvalidStrategyError` es una excepción personalizada para el dominio del proyecto. La ventaja:

```python
try:
    strategy.act(creature)
except InvalidStrategyError:
    # sabemos exactamente qué salió mal: estrategia inválida
    # no confundimos esto con un ValueError de otra parte del código
except ValueError:
    # esto podría venir de CUALQUIER parte — demasiado genérico
```

Las excepciones propias permiten `except` precisos, haciendo el manejo de errores más claro y menos propenso a capturar errores no relacionados.

---

**8. ¿Qué hace el `f"..."` con `'{creature.name}'`?**

Es un f-string. Python evalúa `{creature.name}` en tiempo de ejecución, insertando el valor del atributo `name` del objeto `creature`. Las comillas simples alrededor son parte del mensaje literal (para que aparezca como `'Sproutling'` en el error).

```python
creature.name = "Sproutling"
f"Invalid Creature '{creature.name}'"
# → "Invalid Creature 'Sproutling'"
```

---

### `tournament.py`

**1. ¿Qué tipo tiene `opponents`? Explícalo en palabras simples.**

`list[tuple[CreatureFactory, BattleStrategy]]`

Es una lista de pares. Cada par contiene una fábrica (para crear una criatura) y una estrategia (para definir cómo lucha esa criatura). Ejemplo:

```python
opponents = [
    (FlameFactory(), AggressiveStrategy()),
    (AquaFactory(), DefensiveStrategy()),
]
```

---

**2. ¿Por qué usamos `list[tuple[...]]` en vez de solo `list`?**

Las anotaciones de tipo concretas permiten a mypy verificar que el contenido de la lista es correcto. `list` sin anotar acepta cualquier cosa — podrías meter strings por accidente y el error aparecería solo en tiempo de ejecución. Con `list[tuple[CreatureFactory, BattleStrategy]]`, mypy detecta el error antes.

---

**3. ¿Por qué el bucle interno empieza en `i + 1` y no en `0`?**

Para evitar dos problemas:
- **(0,0)**: una criatura luchando contra sí misma — no tiene sentido
- **(0,1) y (1,0)**: el mismo par dos veces — duplicado

Con `j` empezando en `i+1`, solo procesamos cada combinación única una vez.

```
i=0, j=1  → par (A, B)
i=0, j=2  → par (A, C)
i=1, j=2  → par (B, C)
```

---

**4. Si hay 3 oponentes (A, B, C), ¿cuántos battles habrá?**

3 battles: (A,B), (A,C), (B,C). La fórmula general es `n*(n-1)/2`.

---

**5. ¿Por qué creamos las criaturas ANTES de los bucles y no dentro de ellos?**

Si las creáramos dentro del bucle interno, cada criatura se recrearía en cada batalla. Eso significa:
- `_transformed` se resetearía a `False` en cada batalla
- El estado acumulado entre batallas se perdería
- Cada batalla empezaría con criaturas "nuevas"

Crear antes del bucle garantiza que el estado persiste durante todo el torneo.

---

**6. ¿Qué hace `return` dentro de esta función? ¿Termina el battle o el torneo?**

Termina **el torneo completo** — la función `battle` retorna inmediatamente, abortando todos los battles pendientes. Si quisieras solo cancelar el battle actual y continuar con los demás, usarías `continue`.

---

**7. ¿Por qué capturamos `InvalidStrategyError` y no `Exception`?**

`except Exception` capturaría CUALQUIER error: bugs de Python, `IndexError`, `AttributeError` por errores en el código. Eso ocultaría bugs reales haciéndolos difíciles de detectar.

`except InvalidStrategyError` solo captura el error de negocio específico que sabemos que puede ocurrir y que queremos manejar. Los bugs siguen propagándose como errores no capturados — que es exactamente lo que quieres durante el desarrollo.

---

**8. ¿Qué pasa con los battles restantes si hay un error?**

Se abortan todos. El `return` dentro del `except` sale de la función completa. Los battles que venían después no se ejecutan.

---

**9. ¿Qué imprime `{e}` en el f-string?**

Python llama `str(e)` automáticamente, que invoca `Exception.__str__`, que devuelve el mensaje con el que se creó la excepción. Es decir, el string que pasaste al crear el error:

```python
raise InvalidStrategyError("Invalid Creature 'Sproutling' for this aggressive strategy")
# {e} → "Invalid Creature 'Sproutling' for this aggressive strategy"
```

---

## BLOQUE 4 — Preguntas de diseño

**1. ¿Por qué separar `Creature` de `CreatureFactory`?**

Si mezcláramos creación dentro de `Creature`, la clase haría dos cosas: ser una entidad del juego Y saber cómo construirse a sí misma. Eso viola el **Principio de Responsabilidad Única** (SRP): cada clase debe tener una sola razón para cambiar.

Separando:
- `Creature` cambia si cambia la lógica del juego (stats, ataques)
- `CreatureFactory` cambia si cambia cómo se crean las criaturas

---

**2. ¿Por qué hay un `__init__.py` en cada paquete?**

`__init__.py` le dice a Python que ese directorio es un paquete importable. Sin él, Python 3 lo trataría como un "namespace package" (más limitado) o simplemente no encontraría los módulos con imports normales.

También es el lugar para definir la API pública del paquete (qué exportar en `__all__`).

---

**3. ¿Qué archivos necesitarías para añadir `EarthFactory`?**

Archivos a CREAR:
- `ex0/earth.py` — con `Rockling`, `Boulderax`, y `EarthFactory`

Archivos a MODIFICAR:
- `ex0/__init__.py` — añadir `from ex0.earth import EarthFactory` y añadir `"EarthFactory"` a `__all__`

Eso es todo. `battle.py` y `tournament.py` no necesitan modificarse — funcionan con cualquier `CreatureFactory`. Ese es el poder del patrón.

---

**4. ¿Dónde metería `StealthCapability`?**

En `ex1/capabilities.py`, junto con `HealCapability` y `TransformCapability`. Las capabilities son agnósticas a las estrategias — son rasgos de las criaturas. La estrategia (`StealthStrategy`) iría en `ex2/strategy.py`.

---

**5. ¿Por qué `battle.py`, `capacitor.py` y `tournament.py` están en la raíz?**

Son scripts de demostración/uso, no parte de los paquetes. Estar en la raíz les permite importar de los paquetes limpiamente:

```python
from ex0 import FlameFactory       # importa del paquete ex0
from ex1.healing import Sproutling # importa del submodulo
from ex2.strategy import AggressiveStrategy
```

Si estuvieran dentro de `ex0/`, los imports relativos se complicarían.

---

**6. ¿Qué pasaría si `Flameling` heredara también de `HealCapability`?**

`DefensiveStrategy.is_valid` usa `isinstance(creature, HealCapability)`. Si `Flameling` heredara de `HealCapability`:
- `isinstance(Flameling(), HealCapability)` devolvería `True`
- `DefensiveStrategy` consideraría válido actuar con un `Flameling`
- Se llamaría `flameling.heal()` — pero `Flameling` tendría que implementar `heal()` o ser abstracta

El diseño lo permitiría, pero necesitarías implementar `heal()` en `Flameling`.

---

**7. ¿Qué es el Principio de Responsabilidad Única (SRP)?**

Una clase debe tener **una sola razón para cambiar**. En este proyecto:
- `Creature`: solo cambia si cambia la lógica de ser una criatura
- `CreatureFactory`: solo cambia si cambia cómo se crean criaturas
- `BattleStrategy`: solo cambia si cambia la lógica de batalla
- `HealCapability`: solo cambia si cambia la lógica de curación

Si una clase hace demasiadas cosas, un cambio en un área puede romper otra área no relacionada.

---

## Resumen visual — Diagrama de clases

```
ABC
 ├── Creature (abstracta)
 │    ├── Flameling          (ex0/flame.py)
 │    ├── Pyrodon            (ex0/flame.py)
 │    ├── Aquabub            (ex0/aqua.py)
 │    ├── Tidalfin           (ex0/aqua.py)
 │    ├── Sproutling         (ex1/healing.py)   ← también HealCapability
 │    └── Shiftling          (ex1/transform.py) ← también TransformCapability
 │
 ├── CreatureFactory (abstracta)
 │    ├── FlameFactory       (ex0/flame.py)
 │    └── AquaFactory        (ex0/aqua.py)
 │
 ├── HealCapability (mixin abstracta)
 │    └── (implementada por Sproutling)
 │
 ├── TransformCapability (mixin con estado)
 │    └── (implementada por Shiftling)
 │
 └── BattleStrategy (abstracta)
      ├── NormalStrategy     (ex2/strategy.py)
      ├── AggressiveStrategy (ex2/strategy.py)
      └── DefensiveStrategy  (ex2/strategy.py)

Exception
 └── InvalidStrategyError   (ex2/strategy.py)
```

---

## Trampas comunes en la defensa

1. **"ABC no hace nada"** — Sí hace: impide instanciar clases abstractas y fuerza implementación de métodos abstractos.

2. **"`super()` siempre llama al padre"** — Llama al siguiente en el MRO, que en herencia múltiple puede no ser el padre directo.

3. **"El tipo anotado es el tipo real"** — No. `Creature` como tipo de retorno no significa que el objeto sea `Creature` — es una subclase concreta. La anotación es la interfaz mínima garantizada.

4. **"`isinstance` y `type()` son lo mismo"** — No. `type(obj) == Creature` es `False` para `Flameling`. `isinstance(obj, Creature)` es `True` para `Flameling`.

5. **"Los atributos se comparten entre instancias"** — Solo los atributos de CLASE se comparten. Los de instancia (definidos con `self.x`) son independientes por objeto.
