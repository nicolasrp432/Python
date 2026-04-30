# Cuaderno de Repaso — DataDeck: Abstract Card Architecture

> Objetivo: entender el código al 100%, poder explicar cada línea y cada decisión
> de diseño en voz alta, sin mirar el código.

---

## BLOQUE 0 — Fundamentos que debes dominar antes de empezar

### Preguntas de calentamiento

- ¿Qué es una clase en Python? ¿Qué diferencia hay entre una clase y un objeto?
- ¿Qué es la herencia? ¿Para qué sirve?
- ¿Qué significa que una clase sea "abstracta"?
- ¿Qué hace `from abc import ABC, abstractmethod`?
- ¿Qué pasa si intentas instanciar una clase abstracta directamente?
- ¿Qué es una anotación de tipo (`name: str`, `-> None`)? ¿Por qué las usamos?
- ¿Qué hace `__init__`? ¿Cuándo se llama?
- ¿Qué es `self`?

### Practica esto

```python
# Intenta crear esto desde cero en un fichero aparte:
from abc import ABC, abstractmethod

class Animal(ABC):
    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def speak(self) -> str: ...

    def describe(self) -> str:
        return f"I am {self.name}"

class Dog(Animal):
    def speak(self) -> str:
        return "Woof!"

# ¿Qué pasa si haces Animal("x")?
# ¿Qué pasa si haces una clase que hereda de Animal pero NO implementa speak()?
```

**Respuesta esperada al intentar instanciar Animal:**
```
TypeError: Can't instantiate abstract class Animal
with abstract method speak
```

---

## BLOQUE 1 — Exercise 0: Abstract Factory Pattern

### ¿Qué es el Abstract Factory Pattern?

Es un patrón de diseño que te permite crear **familias** de objetos relacionados
sin depender de sus clases concretas. En vez de hacer `Flameling()` directamente
en tu script, usas una fábrica: `factory.create_base()`.

**Pregunta clave:** ¿Por qué no simplemente hacer `Flameling()` directamente?

> Porque si mañana cambias el nombre de la clase, o quieres crear una familia
> nueva, solo tienes que cambiar la fábrica, no todos los scripts que usan esa
> clase. El código que consume la fábrica ni siquiera sabe qué clase concreta
> se está creando — solo sabe que recibirá algo que es una `Creature`.

---

### Preguntas sobre `ex0/creature.py`

```python
class Creature(ABC):
    def __init__(self, name: str, creature_type: str) -> None:
        self.name = name
        self.creature_type = creature_type

    @abstractmethod
    def attack(self) -> str: ...

    def describe(self) -> str:
        return f"{self.name} is a {self.creature_type} type Creature"
```

1. ¿Por qué `Creature` hereda de `ABC`?
2. ¿Por qué `attack` es abstracto pero `describe` no?
3. Si `describe` es concreto, ¿pueden las subclases sobreescribirlo?
4. ¿Qué pasa si una subclase no implementa `attack`?
5. ¿Qué tipo retorna `attack`? ¿Por qué `str` y no `None`?
6. ¿Qué significa `-> None` en `__init__`?
7. ¿Por qué el atributo se llama `creature_type` y no solo `type`?

**Respuesta a la 7:** `type` es una función built-in de Python. Usar `type`
como nombre de atributo lo sobreescribiría dentro del objeto, lo cual es
confuso y puede causar bugs difíciles de detectar.

---

### Preguntas sobre `ex0/factory.py`

```python
class CreatureFactory(ABC):
    @abstractmethod
    def create_base(self) -> Creature: ...

    @abstractmethod
    def create_evolved(self) -> Creature: ...
```

1. ¿Por qué `CreatureFactory` también es abstracta?
2. ¿Qué le impide al usuario del paquete instanciar `CreatureFactory()` directamente?
3. ¿Qué retorna `create_base`? ¿`Creature` o una subclase concreta?
4. ¿Qué ventaja tiene que el tipo de retorno sea `Creature` (la abstracta)
   en vez de `Flameling`?

**Respuesta a la 4:** El código que recibe la criatura no necesita saber
si es `Flameling` o `Aquabub`. Solo sabe que tiene `.describe()` y `.attack()`.
Esto se llama **polimorfismo**: tratar objetos distintos de forma uniforme
mediante una interfaz común.

---

### Preguntas sobre `ex0/flame.py`

```python
class Flameling(Creature):
    def __init__(self) -> None:
        super().__init__("Flameling", "Fire")

    def attack(self) -> str:
        return "Flameling uses Ember!"
```

1. ¿Qué hace `super().__init__("Flameling", "Fire")`?
2. ¿Por qué `Flameling.__init__` no necesita parámetros?
3. ¿Qué pasa en memoria cuando haces `f = Flameling()`?
   Traza los pasos: qué se llama, en qué orden, qué atributos se crean.

**Traza mental:**
```
Flameling()
  └─ Flameling.__init__(self)
       └─ super().__init__("Flameling", "Fire")
            └─ Creature.__init__(self, "Flameling", "Fire")
                 └─ self.name = "Flameling"
                 └─ self.creature_type = "Fire"
# Resultado: objeto con .name="Flameling", .creature_type="Fire", .attack()
```

---

### Preguntas sobre `ex0/__init__.py`

```python
from ex0.flame import FlameFactory
from ex0.aqua import AquaFactory

__all__ = ["FlameFactory", "AquaFactory"]
```

1. ¿Por qué el `__init__.py` solo expone `FlameFactory` y `AquaFactory`,
   y no `Flameling` o `Pyrodon`?
2. ¿Qué significa `__all__`?
3. Si yo hago `from ex0 import Flameling`, ¿qué pasa?
4. ¿Puedo hacer `from ex0.flame import Flameling`? ¿Está prohibido?

**Respuesta a la 3:** `ImportError` — Flameling no está en `__init__.py`.

**Respuesta a la 4:** Técnicamente sí se puede (el archivo existe), pero
viola el espíritu del ejercicio: el paquete no debe *exponer* las clases
concretas. En una librería real, documentarías solo la API pública.

---

### Preguntas sobre `battle.py`

```python
def test_factory(factory: CreatureFactory) -> None:
    print("Testing factory")
    base = factory.create_base()
    evolved = factory.create_evolved()
    print(base.describe())
    print(base.attack())
    print(evolved.describe())
    print(evolved.attack())
```

1. ¿Qué tipo tiene el parámetro `factory`? ¿Por qué no ponemos `FlameFactory`?
2. ¿Puedo llamar a `test_factory` con `AquaFactory()`? ¿Por qué?
3. ¿Qué es el polimorfismo aquí? Da el ejemplo concreto.
4. ¿Qué hace `print(base.describe())` paso a paso?

```python
def test_battle(factory1: CreatureFactory, factory2: CreatureFactory) -> None:
    creature1 = factory1.create_base()
    creature2 = factory2.create_base()
    ...
    print(creature1.attack())
    print(creature2.attack())
```

5. ¿Sabemos, dentro de `test_battle`, qué clase concreta son `creature1` y `creature2`?
6. ¿Qué pasaría si `attack()` estuviera en `CreatureFactory` en vez de `Creature`?

---

## BLOQUE 2 — Exercise 1: Capabilities (Mixins con herencia múltiple)

### ¿Qué es un Mixin?

Un Mixin es una clase que **aporta funcionalidad extra** sin ser una clase
base completa. No representa una entidad ("un Animal"), sino una capacidad
("algo que puede curarse"). En Python se implementan con herencia múltiple.

**Analogía:** Piensa en interfaces de Java o en traits de Rust.
Un `Sproutling` ES una `Creature` Y TIENE la capacidad de `HealCapability`.

---

### Preguntas sobre `ex1/capabilities.py`

```python
class HealCapability(ABC):
    @abstractmethod
    def heal(self) -> str: ...
```

1. ¿Por qué `HealCapability` NO hereda de `Creature`?
2. ¿Qué pasaría si heredara de `Creature`? ¿Qué problemas crearía?
3. ¿Puede existir una clase que herede solo de `HealCapability` sin ser `Creature`?
   ¿Tendría sentido en el diseño?

```python
class TransformCapability(ABC):
    def __init__(self) -> None:
        self._transformed: bool = False
```

4. ¿Por qué `TransformCapability` tiene `__init__` pero `HealCapability` no?
5. ¿Qué significa el guion bajo en `_transformed`?
6. ¿Por qué el estado `_transformed` está en `TransformCapability` y no en
   la criatura (`Shiftling`)?
7. ¿Qué pasa si dos instancias de `Shiftling` comparten el mismo estado?
   (Spoiler: no lo comparten — ¿por qué?)

**Respuesta a la 5:** El guion bajo es una convención que indica que el
atributo es "privado por convención" — no debe accederse desde fuera de la
clase directamente. No es privado forzado (como en Java), es un acuerdo.

**Respuesta a la 7:** Cada instancia tiene su propio `__dict__`, su propia
memoria. `s1 = Shiftling()` y `s2 = Shiftling()` son objetos distintos con
`_transformed` independiente.

---

### Preguntas sobre herencia múltiple en `ex1/healing.py`

```python
class Sproutling(Creature, HealCapability):
    def __init__(self) -> None:
        Creature.__init__(self, "Sproutling", "Grass")
```

1. ¿Qué es el MRO (Method Resolution Order)? ¿Cuál es el MRO de `Sproutling`?
2. ¿Por qué llamamos `Creature.__init__` explícitamente en vez de `super().__init__`?
3. ¿`Sproutling` es una instancia de `Creature`? ¿Y de `HealCapability`?
4. ¿`isinstance(Sproutling(), Creature)` da `True`?
5. ¿`isinstance(Sproutling(), HealCapability)` da `True`?

**Respuesta a la 2 (MRO):**
```
Sproutling → Creature → HealCapability → ABC → object
```
Si usaras `super().__init__("Sproutling", "Grass")` dentro de `Sproutling`,
llamaría a `Creature.__init__`. Dentro de `Creature.__init__`, si usara
`super().__init__()`, el MRO indicaría que debe llamar a
`HealCapability.__init__()` — pero `HealCapability` no tiene `__init__`,
así que iría a `ABC.__init__()` que tampoco acepta `name`/`creature_type`.
Para evitar esta ambigüedad, llamamos explícitamente.

**Practica esto:**
```python
print(Sproutling.__mro__)
# Debes poder predecir el resultado antes de ejecutarlo
```

---

### Preguntas sobre `Shiftling` y estado de transformación

```python
class Shiftling(Creature, TransformCapability):
    def attack(self) -> str:
        if self._transformed:
            return "Shiftling performs a boosted strike!"
        return "Shiftling attacks normally."

    def transform(self) -> str:
        self._transformed = True
        return "Shiftling shifts into a sharper form!"
```

1. ¿Qué devuelve `Shiftling().attack()` sin llamar a `transform()` antes?
2. ¿Qué devuelve `Shiftling().attack()` después de llamar a `transform()`?
3. ¿Qué pasa si llamas a `transform()` dos veces seguidas?
4. ¿Qué pasa si llamas a `revert()` sin haber llamado a `transform()` antes?
5. ¿Por qué `transform()` RETORNA un string en vez de solo cambiar el estado?
6. ¿Por qué no hacemos `print()` dentro de `transform()`?

**Respuesta a la 5 y 6:** Separación de responsabilidades. El método
hace su trabajo (cambiar estado, describir la acción) y retorna el mensaje.
Quien lo llama decide si imprimirlo, guardarlo en un log, enviarlo por red,
etc. Si hiciéramos `print()` dentro, estaríamos forzando que SIEMPRE se
imprima en consola — eso limita el reutilizable del código.

---

### Preguntas sobre `capacitor.py`

```python
if isinstance(creature, HealCapability):
    print(creature.heal())
```

1. ¿Por qué usamos `isinstance` aquí?
2. ¿Podríamos evitar el `isinstance` con un mejor diseño? ¿Cómo?
3. ¿Qué pasaría si no tuviéramos el `isinstance` y llamáramos `creature.heal()`
   en un `Shiftling`?

**Respuesta a la 3:** `AttributeError: 'Shiftling' object has no attribute 'heal'`
porque `Shiftling` hereda de `TransformCapability`, no de `HealCapability`.

---

## BLOQUE 3 — Exercise 2: Strategy Pattern

### ¿Qué es el Strategy Pattern?

Es un patrón que permite **cambiar el comportamiento de un objeto en tiempo
de ejecución** sin modificar su código. En vez de usar `if/elif` para decidir
cómo actúa una criatura, encapsulamos cada comportamiento en una clase separada.

**Sin Strategy Pattern (malo):**
```python
def act(creature, strategy_name):
    if strategy_name == "normal":
        print(creature.attack())
    elif strategy_name == "aggressive":
        print(creature.transform())
        print(creature.attack())
        print(creature.revert())
    elif strategy_name == "defensive":
        print(creature.attack())
        print(creature.heal())
```

**Problema:** si añades una nueva estrategia, tienes que modificar esta función.
Viola el principio Open/Closed: "abierto para extensión, cerrado para modificación".

**Con Strategy Pattern (bueno):**
```python
strategy.act(creature)  # No importa qué estrategia es — simplemente actúa
```

---

### Preguntas sobre `ex2/strategy.py`

```python
class BattleStrategy(ABC):
    @abstractmethod
    def is_valid(self, creature: Creature) -> bool: ...

    @abstractmethod
    def act(self, creature: Creature) -> None: ...
```

1. ¿Por qué `act` retorna `None` en vez de `str`?
2. ¿Qué hace `is_valid`? ¿Por qué existe por separado de `act`?
3. ¿Para qué sirve tener la clase abstracta `BattleStrategy` si podríamos
   usar duck typing directamente?

**Respuesta a la 3:** Con la clase abstracta:
- mypy puede verificar que se pasan objetos correctos
- Python lanza error si alguien crea una estrategia sin implementar `is_valid` o `act`
- Es documentación viva: cualquiera que lea `BattleStrategy` sabe exactamente
  qué métodos debe implementar una estrategia nueva

```python
class AggressiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, TransformCapability)

    def act(self, creature: Creature) -> None:
        if not self.is_valid(creature):
            raise InvalidStrategyError(
                f"Invalid Creature '{creature.name}'"
                " for this aggressive strategy"
            )
        assert isinstance(creature, TransformCapability)
        print(creature.transform())
        print(creature.attack())
        print(creature.revert())
```

4. ¿Por qué `is_valid` usa `isinstance(creature, TransformCapability)`?
5. ¿Para qué sirve el `assert isinstance(creature, TransformCapability)`
   después del `if not self.is_valid`? ¿No es redundante?
6. ¿Qué es `InvalidStrategyError`? ¿Por qué no usamos `ValueError` genérico?
7. ¿Qué ventaja tiene crear tu propia excepción?
8. ¿Qué hace el `f"..."` con `'{creature.name}'`?

**Respuesta a la 5:** El `assert` le dice a mypy (y a cualquier lector del
código) que en ese punto ya sabemos con certeza que `creature` tiene los
métodos de `TransformCapability`. Sin él, mypy daría error porque `creature`
está tipado como `Creature`, que no tiene `transform()`.

**Respuesta a la 6-7:** Crear una excepción propia (`InvalidStrategyError`)
permite que el código que la captura (`except InvalidStrategyError`) sea
preciso: solo captura ESE error específico, no cualquier error genérico que
pudiera venir de otro lugar.

---

### Preguntas sobre `tournament.py`

```python
def battle(opponents: list[tuple[CreatureFactory, BattleStrategy]]) -> None:
    creatures = [
        (fac.create_base(), strat)
        for fac, strat in opponents
    ]
    for i in range(len(creatures)):
        for j in range(i + 1, len(creatures)):
```

1. ¿Qué tipo tiene `opponents`? Explícalo en palabras simples.
2. ¿Por qué usamos `list[tuple[...]]` en vez de solo `list`?
3. ¿Por qué el bucle interno empieza en `i + 1` y no en `0`?
4. Si hay 3 oponentes (A, B, C), ¿cuántos battles habrá? ¿Cuáles son los pares?
5. ¿Por qué creamos las criaturas ANTES de los bucles y no dentro de ellos?

```python
try:
    strategy_i.act(creature_i)
    strategy_j.act(creature_j)
except InvalidStrategyError as e:
    print(f"Battle error, aborting tournament: {e}")
    return
```

6. ¿Qué hace `return` dentro de esta función? ¿Termina el battle o el torneo?
7. ¿Por qué capturamos `InvalidStrategyError` y no `Exception`?
8. ¿Qué pasa con los battles restantes si hay un error?
9. ¿Qué imprime `{e}` en el f-string?

**Respuesta a la 3:** Si no pusiéramos `i + 1`, tendríamos:
- (0,0): una criatura contra sí misma — sin sentido
- (0,1) y (1,0): el mismo par dos veces — duplicado
Con `j` empezando en `i + 1`, solo procesamos cada par una vez.

**Respuesta a la 5:** Porque si las creáramos dentro del bucle, cada criatura
se recrearía en cada batalla — perdería el estado (por ejemplo, `_transformed`
quedaría reseteado).

**Respuesta a la 9:** Python llama a `str(e)` automáticamente en el f-string,
que a su vez llama a `Exception.__str__`, que retorna el mensaje con el que
se construyó la excepción.

---

## BLOQUE 4 — Preguntas de diseño (las más difíciles en la defensa)

Estas preguntas no tienen respuesta en el código — requieren que PIENSES.

1. **¿Por qué separar `Creature` de `CreatureFactory`?**
   > ¿Qué pasaría si mezcláramos la lógica de creación dentro de `Creature`?

2. **¿Por qué hay un `__init__.py` en cada paquete?**
   > ¿Qué hace Python con un directorio que NO tiene `__init__.py`?

3. **¿Qué pasaría si quisieras añadir una nueva familia, por ejemplo `EarthFactory`
   con `Rockling` (base) y `Boulderax` (evolucionada)?**
   > ¿Qué archivos tendrías que crear? ¿Qué archivos existentes tendrías que modificar?

4. **¿Qué pasaría si quisieras añadir una nueva estrategia `StealthStrategy`
   que requiera una nueva capability `StealthCapability`?**
   > ¿Dónde meterías la nueva capability? ¿En ex1 o en ex2?

5. **¿Por qué `battle.py`, `capacitor.py` y `tournament.py` están en la raíz
   y no dentro de sus respectivos paquetes?**
   > ¿Cómo afecta esto a los imports?

6. **¿Qué pasaría si `Flameling` heredara también de `HealCapability`?**
   > ¿Qué cambiaría en la lógica de validación de `DefensiveStrategy`?

7. **¿Qué es el Principio de Responsabilidad Única y cómo se aplica aquí?**

---

## BLOQUE 5 — Exercicios prácticos de repaso

### Ejercicio A — Reconstrucción de memoria
Sin mirar el código, intenta escribir desde cero:
1. La clase `Creature` completa
2. La clase `CreatureFactory` completa
3. Una criatura concreta cualquiera con su factory

### Ejercicio B — Extiende el sistema
Añade una nueva familia sin modificar ningún archivo existente:
```
LightningFamily:
  - Zaplet (base): tipo "Electric", attack: "Zaplet uses Thunder Shock!"
  - Volthorn (evolved): tipo "Electric/Steel", attack: "Volthorn uses Discharge!"
```
Crea `ex0/lightning.py` con la factory, y añádela al `__init__.py`.

### Ejercicio C — Nueva capability
Añade una `FlyCapability` en `ex1/capabilities.py`:
```python
class FlyCapability(ABC):
    @abstractmethod
    def fly(self) -> str: ...
```
Crea una criatura `Winglet` que herede de `Creature` y `FlyCapability`.

### Ejercicio D — Nueva estrategia
Añade una `FlightStrategy` en `ex2/strategy.py`:
- Solo válida para criaturas con `FlyCapability`
- `act`: primero `fly()`, luego `attack()`
- Si la criatura no tiene `FlyCapability`, lanza `InvalidStrategyError`

### Ejercicio E — Preguntas en voz alta
Siéntate con un compañero y pídele que señale cualquier línea del código.
Tú debes explicar:
- ¿Qué hace esa línea?
- ¿Por qué está ahí?
- ¿Qué pasaría si la quitáramos?

---

## BLOQUE 6 — Conceptos clave para memorizar

| Concepto | Definición en una frase | Dónde aparece en el proyecto |
|----------|------------------------|------------------------------|
| Clase abstracta | Clase que NO puede instanciarse directamente | `Creature`, `CreatureFactory`, `BattleStrategy` |
| Método abstracto | Método sin implementación que las subclases DEBEN implementar | `attack()`, `create_base()`, `act()` |
| Abstract Factory | Patrón que crea familias de objetos sin exponer las clases concretas | `FlameFactory`, `AquaFactory` |
| Herencia múltiple | Una clase hereda de dos o más clases | `Sproutling(Creature, HealCapability)` |
| Mixin | Clase que aporta capacidades extras, no una entidad completa | `HealCapability`, `TransformCapability` |
| MRO | Orden en que Python busca métodos en la jerarquía de herencia | Afecta a `Sproutling`, `Shiftling`, etc. |
| Strategy Pattern | Encapsular comportamientos intercambiables en clases separadas | `NormalStrategy`, `AggressiveStrategy`, `DefensiveStrategy` |
| Polimorfismo | Tratar objetos distintos de forma uniforme por su tipo común | `factory: CreatureFactory`, `strategy.act(creature)` |
| isinstance | Verificar en runtime si un objeto es de cierta clase | `isinstance(creature, TransformCapability)` |
| Excepción propia | Clase de error personalizada para errores específicos del dominio | `InvalidStrategyError` |

---

## BLOQUE 7 — Checklist de defensa

Marca cada punto cuando puedas hacerlo sin mirar el código:

- [ ] Puedo dibujar el diagrama de clases completo (ex0, ex1, ex2)
- [ ] Puedo explicar qué es ABC y @abstractmethod con un ejemplo propio
- [ ] Puedo explicar el Abstract Factory Pattern en 2 frases
- [ ] Puedo decir el MRO de Sproutling y Shiftling de memoria
- [ ] Puedo explicar por qué HealCapability no hereda de Creature
- [ ] Puedo explicar por qué usamos `isinstance` en las estrategias
- [ ] Puedo explicar qué es el Strategy Pattern con una analogía propia
- [ ] Puedo explicar por qué `j` empieza en `i+1` en el bucle del torneo
- [ ] Puedo añadir una nueva familia de criaturas sin ayuda
- [ ] Puedo añadir una nueva estrategia sin ayuda
- [ ] Puedo explicar qué pasaría si eliminara cualquier línea del código
- [ ] Puedo ejecutar los tres scripts de memoria y predecir el output exacto
