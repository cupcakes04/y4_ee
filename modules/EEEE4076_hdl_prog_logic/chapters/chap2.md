# Lecture 2: VHDL Fundamentals



**Subject:** H64HDP/H64HDL — VHDL Fundamentals
**Source:** Lecture 2 VHDL Fundamental.pdf
**Date captured:** October 2, 2026

---

## Overview

This chapter introduces the fundamental building blocks of VHDL (Very High Speed Integrated Circuit Hardware Description Language) used for modelling digital systems. It establishes the structural bifurcation between the primary design units—the entity (interface) and architecture (internal behavior/implementation)—demonstrating behavioral and structural paradigms for combinational and sequential logic. Mastering these mechanics is essential for synthesizing correct gate-level logic, managing signal/data types, and building hierarchical modular hardware designs.

---

## Objectives

After completing this lecture, you will be able to:

* Understand the different design units in VHDL.


* Understand Behavioural and Structural VHDL coding.


* Identify simple VHDL coding errors.


* Write a Behavioural and Structural VHDL code for a simple combinational logic.



---

## What exactly is VHDL?

VHDL is a formal method of describing the operation and structure of a digital system.

An illustrative example is a two-input multiplexer (MUX):

### Diagram Reconstruction: Two-Input Multiplexer (Slide 3)

A vertical rectangular functional block representing a 2-to-1 multiplexer.

* **Inputs:** Two data input lines enter horizontally from the left into the block, labeled `a` (upper input) and `b` (lower input). One control line enters from the bottom, labeled `Sel`.


* **Outputs:** A single data output line exits horizontally from the right edge, labeled `y`.



### Code Example: Two-Input MUX

```vhdl
entity mux2 is
    Port (a:   in std_logic;
          b:   in std_logic;
          sel: in std_logic;
          y:   out std_logic);
end mux2;

architecture Behavioral of mux2 is
begin
    if sel = 1 then
        y <= a;
    else
        y <= b;
    end if;
end Behavioral;

```

(Note: See section "Open / Unresolved" regarding syntax issues in slide behavioral snippets).

---

## VHDL Design Units

VHDL consists of 5 distinct "design units" composed of textual VHDL code:

1. **Entities** (essential)


2. **Architectures** (essential)


3. **Packages** (optional)


4. **Package Bodies** (optional)


5. **Configurations** (optional)



Key mechanical characteristics:

* These five design units can be compiled separately and stored in a design library or the default `WORK` area.


* Primary focus is placed on the essential design units: **Entities** and **Architectures**.



---

## Entity

* Serves as the port declaration interface for inputs and outputs.


* Represents the uppermost level of the component boundary.


* Defines the hardware interface between the design entity and the external environment.



### Diagram Reconstruction: Two-Input Mux Trapezoid (Slide 5)

A standard trapezoidal multiplexer symbol oriented vertically.

* The longer parallel edge is on the left side with two horizontal incoming wires labeled `a` (top) and `b` (bottom).


* The shorter parallel edge is on the right side with a single outgoing wire labeled `y`.


* A control wire enters the slanted bottom edge from below, labeled `Sel`.



### Entity Code: Two-Input Mux

```vhdl
entity mux2 is
    Port (a:   in std_logic;
          b:   in std_logic;
          sel: in std_logic;
          y:   out std_logic);
end mux2;

```

---

## Entity (cont...)

### Formal Syntax

```vhdl
Entity <identifier_name> is
    Port (<identifier> : <mode> <data type>;
          <identifier> : <mode> <data type>);
End <identifiers_name>;

```

### Syntactical and Lexical Rules

* **Reserved Words:** Language keywords (shown in blue in lecture slides) cannot be used as arbitrary identifiers.


* **Comments:** Begin with a double hyphen `--` and extend to the end of the current line.


* **Case Insensitivity:** Identifiers and keywords are case insensitive (e.g., `Rdy` = `rdy` = `RDy`).


* **Statement Termination:** Statements are terminated by a semicolon `;` and may span multiple lines.


* **Delimiters:** A comma `,` is used as a list delimiter.



---

## Architecture

* Describes the internal relationship between design entity inputs and outputs.


* Every architecture must be bound to an entity.


* The architecture name cannot be identical to its entity name.


* Two primary types/styles:
1. **Behavioural**

2. **Structural**



* A single entity can have several architectures linked to it.


* Identifier naming constraint: Names of entities and architectures should not conflict with library functions or VHDL reserved keywords.



### Diagram Reconstruction: Entity vs. Architecture Boundary (Slide 8)

A conceptual nested container diagram:

* An outer green rectangular block labeled **Entity** represents the external package.


* A green arrow pointing downward into the top edge is labeled **IN**.


* A green arrow pointing downward out of the bottom edge is labeled **OUT**.




* Inside the green block sits an inner purple rectangular block labeled **Architecture**, demonstrating that architecture logic resides entirely inside the entity boundary.



---

## Architecture (cont...) — Behavioural Architecture

A behavioral architecture specifies algorithms, equations, or sequential logic describing how outputs react to inputs.

### General Syntax

```vhdl
architecture <architecture_name> of <entity_identifier> is
    [<architecture_declarative_part>]
begin
    <architecture_statement_part>
end [<architecture_name>];

```

### Declarative vs. Statement Section Structure

```vhdl
architecture Behavioral of mux2 is
    -- signal and variable declaration (declarative part)
begin
    -- statement part: defines relationship between I/Os
end Behavioral;

```

### Example: Behavioural Two-Input MUX Code

```vhdl
architecture Behavioral of mux2 is
begin
    if sel = 1 then
        y <= a;
    else
        y <= b;
    end if;
end Behavioral;

```

---

## Behavioral Examples

### 1. Half Adder Circuit

⚠️ DEPENDS ON: Boolean Logic (Half Adder truth table: $\text{Sum} = A \oplus B$, $\text{Carry} = A \cdot B$)

#### Diagram Reconstruction: Half Adder Logic Diagram (Slide 10)

Two logic gates arranged in parallel driven by two inputs:

* Inputs `a` and `b` on the left branch out:
* Branch 1 routes into a 2-input XOR gate (`XOR2`), producing output `Sum` on the right.


* Branch 2 routes into a 2-input AND gate (`AND2`), producing output `Carry` on the right.





#### Code

```vhdl
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

Entity ha is
    port (a, b: in std_logic;
          sum, carry: out std_logic);
end ha;

Architecture ha_behav of ha is
begin
    sum <= a xor b;
    carry <= a and b;
end ha_behav;

```

### 2. RS Flip Flop

⚠️ DEPENDS ON: Cross-coupled NOR latch feedback mechanics and bistable multivibrators

#### Diagram Reconstruction: Cross-Coupled NOR Latch (Slide 11)

A cross-coupled NOR gate schematic:

* Top NOR gate (`NOR2`): Primary upper input is terminal `R`. Output is labeled `Q`.


* Bottom NOR gate (`NOR2`): Primary lower input is terminal `S`. Output is labeled `Qbar`.


* Feedback routing:
* Output `Q` connects back down to the second input of the bottom NOR gate.


* Output `Qbar` connects back up to the second input of the top NOR gate.





#### Code

```vhdl
Library ieee;
Use ieee.std_logic_1164.all;

Entity rsff is
    port (s, r: in std_logic;
          q, qbar: out std_logic);
end rsff;

Architecture rsff_behav of rsff is
    signal x, y: std_logic;
begin
    y <= s nor x;
    x <= r nor y;
    q <= x;
    qbar <= y;
end rsff_behav;

```

---

## Entity Modes

Port modes define the data directionality relative to the entity boundary:

* `in`: The component can only read the signal.


* `out`: The component can only write to the signal (cannot read back internally).


* `inout`: Bidirectional; the component can read or write to the signal.


* `buffer`: The component can write to and read back the signal; strictly non-bidirectional.


* `linkage`: Used only for documentation or non-VHDL subprogram linkage.



---

## Entity Data Types

### Standard Built-In Types

* **Boolean type:** `True` or `False`.


* **Integer type:** 32-bit signed integer ranging from `-2147483648` to `+2147483647` (slide states `+2147483648`).


* Binary literal: `B"10101"`

* Octal literal: `O"721"`

* Hexadecimal literal: `X"AF14"`



* **Character type:** `'0'` to `'9'`, `'A'` to `'Z'`, `'a'` to `'z'`, and special characters (`+`, `-`, `*`, `/`, etc.).


* **Bit type:** Logic levels `'0'`, `'1'` (slide lists `0, 1, X, Z`, conflating it with multivalued logic).



### Standard Logic: `std_logic` (IEEE 1164 9-Valued System)

* `'U'`: Uninitialized


* `'X'`: Forcing Unknown (contention)


* `'0'`: Forcing Zero


* `'1'`: Forcing One


* `'Z'`: High Impedance (floating/tri-state)


* `'W'`: Weak Unknown


* `'L'`: Weak Zero (pull-down)


* `'H'`: Weak One (pull-up)


* `'-'`: Don't care



*Syntax Rule:* Single quotes (`'0'`) define a single bit (`std_logic`). Double quotes (`"1010"`) define an array/vector (`std_logic_vector`).

### Array / Vector Types

* `to`: Ascending index ordering.


* `downto`: Descending index ordering.



Examples:

* `A: in std_logic_vector (9 downto 0);`

* Assignment: `A <= "1101110010";`
* Mapping: $A(9)=1, A(8)=1, A(7)=0, \dots, A(0)=0$ (slide writes $A(0)=1$).




* `B: out std_logic_vector (0 to 3);`

* Ordered as $B(0), B(1), B(2), B(3)$.




* *Guideline:* Mixing `to` and `downto` directions within the same system is strongly discouraged.



### Array Slicing

Allows assigning a scalar bit or a slice of an array:

```vhdl
B(0) <= '0';
B(2 to 3) <= "10";
A(1) <= B(0);

```

*Rule:* Slice index direction must strictly match the direction specified in the signal declaration.

### Physical Type: Time

Time units: `1ms`, `9ns`, `100ps`.

### User-Defined Enumerated Types

Enables user-defined state encoding and symbolic states:

```vhdl
TYPE color IS (red, blue, green, orange);

type stateType is (stIdle, stData, stStop, stTxdCompleted);
attribute enum_encoding of statetype: type is "00 01 11 10";
signal presState: stateType;
signal nextState: stateType;

```

---

## VHDL Keywords

The complete set of reserved language keywords presented:
`abs`, `access`, `after`, `alias`, `all`, `and`, `architecture`, `array`, `assert`, `attribute`, `begin`, `block`, `body`, `buffer`, `bus`, `case`, `component`, `configuration`, `constant`, `disconnect`, `downto`, `else`, `elsif`, `end`, `entity`, `exit`, `file`, `for`, `function`, `generate`, `generic`, `group`, `guarded`, `if`, `impure`, `in`, `inertial`, `inout`, `is`, `label`, `library`, `linkage`, `literal`, `loop`, `map`, `mod`, `nand`, `new`, `next`, `nor`, `not`, `null`, `of`, `on`, `open`, `or`, `others`, `out`, `package`, `port`, `postponed`, `procedure`, `process`, `pure`, `range`, `record`, `register`, `reject`, `rem`, `report`, `rol`, `ror`, `select`, `severity`, `shared`, `signal`, `sla`, `sll`, `sra`, `srl`, `subtype`, `then`, `to`, `transport`, `type`, `unaffected`, `units`, `until`, `use`, `variable`, `wait`, `when`, `while`, `with`, `xnor`, `xor`.

---

## Structural Architecture

* Models a circuit as an interconnection of pre-defined hardware components (netlist representation).


* Produces clean, directly synthesizable code.


* Forms the foundation for hierarchical VHDL designs.


* Typically used when designing systems with complexities exceeding 1000 gates.


* **Mechanism:**
* Uses `component` declarations to declare sub-module interfaces within the architecture declarative block.


* Uses internal `signal` lines to wire entity ports to component ports.





### Diagram Reconstruction: Two-Input Mux Structural Gate Level (Slide 9, 19, 20)

* **Inputs:** Ports `A`, `B`, and `Sel`.


* **Gates:**
* Inverter `INV`: Input connected to `Sel`, output generates internal net `Int 1`.


* Upper AND Gate `AND2`: Inputs connected to `A` and `Sel`, output generates internal net `Int 2`.


* Lower AND Gate `AND2`: Inputs connected to `Int 1` and `B`, output generates internal net `Int 3`.


* OR Gate `OR2`: Inputs connected to `Int 2` and `Int 3`, output drives system output `Y`.





### Structural MUX Implementation

```vhdl
entity mux2 is
    Port (a:   in std_logic;
          b:   in std_logic;
          sel: in std_logic;
          y:   out std_logic);
end mux2;

architecture Structure of mux2 is
    -- Component declarations
    component AND2 is
        port (a, b: in std_logic; f: out std_logic);
    end component;

    component OR2 is
        port (a, b: in std_logic; f: out std_logic);
    end component OR2;

    component INV is
        port (a: in std_logic; f: out std_logic);
    end component;

    -- Internal net declarations
    signal int1, int2, int3: std_logic;

begin
    U1: INV  port map (sel, int1);
    U2: AND2 port map (sel, a, int2);
    U3: AND2 port map (int1, b, int3);
    U4: OR2  port map (int2, int3, y);
end Structure;

```

### Component Declaration & Port Map Syntax

* **Declaration Syntax:**

```vhdl
component <name>
    [generic (<generic_associated_list>);]
    port (<port_associated_list>);
end component <name>;

```

* **Port Map Association Styles:**
* **Positional Association:** Ordered by component port declaration:
```vhdl
U2: AND2 port map (sel, a, int2);

```


* **Named Association:** Explicit mapping using formal parameter arrows `=>`:
```vhdl
U2: AND2 port map (a => sel, b => a, f => int2);

```





---

## Hierarchical Design of a Full Adder Circuit

⚠️ DEPENDS ON: Full adder digital logic decomposition ($S = A \oplus B \oplus C_{in}$, $C_{out} = AB + C_{in}(A \oplus B)$)

### Diagram Reconstruction: Full Adder Composed of Two Half Adders (Slide 22)

A top-level bounding box represents a 1-bit Full Adder:

* **External Pins:** Input ports `A`, `B`, `Cin` on the left; output ports `S` (Sum) and `C` (Carry out) on the right.


* **Sub-blocks:**
* Half Adder 1 (`HA`, left): Inputs `A` and `B` connect directly to external ports `A` and `B`.


* Sum output `S` generates intermediate wire `S1`.


* Carry output `C` generates intermediate wire `C1`.




* Half Adder 2 (`HA`, right):
* Input `A` connects to wire `S1`.


* Input `B` connects to external port `Cin`.


* Sum output `S` connects directly to external output `S`.


* Carry output `C` generates intermediate wire `C2`.




* OR Gate: Inputs connect to `C1` and `C2`; output connects directly to external output `C`.





### Slide Full Adder Code Implementation

```vhdl
entity full_adder is
    Port (a:     in STD_LOGIC;
          b:     in STD_LOGIC;
          c:     in STD_LOGIC;
          sum:   out STD_LOGIC;
          carry: out STD_LOGIC);
end full_adder;

architecture Behavioral of full_adder is
    component half_adder is
        Port (a:     in STD_LOGIC;
              b:     in STD_LOGIC;
              sum:   out STD_LOGIC;
              carry: out STD_LOGIC);
    end half_adder;

    signal int_sum, int_carry1, int_carry2: std_logic;

begin
    u1: half_adder port map (
        a     => a,
        b     => b,
        sum   => int_sum,
        carry => int_carry1
    );

    u2: half_adder port map (
        a     => int_sum,
        b     => c,
        sum   => sum,
        carry => int_carry2
    );

    carry <= int_carry1 and int_carry2; -- Note: Error in slide; should logically be OR
end Behavioral;

```

---

## IEEE Libraries and Packages

Standard package header template recommended for designs:

```vhdl
library IEEE;                     -- Library declaration
use IEEE.STD_LOGIC_1164.ALL;      -- Logic value system package
use IEEE.STD_LOGIC_ARITH.ALL;     -- Arithmetic operations package
use IEEE.STD_LOGIC_UNSIGNED.ALL;  -- Unsigned operations package

```

---

## Exercises

### Exercise 1

* **Prompt:** Assume the assigning condition:
`A: in std_logic_vector (4 downto 0);`
`B: in std_logic_vector (0 to 4);`
If $A \Leftarrow \text{"10010"}$ and $B \Leftarrow A$, determine the value of $B(4)$.


* **Analysis:**
$A$ is indexed `(4 downto 0)` with value `"10010"`:
$A(4) = 1, A(3) = 0, A(2) = 0, A(1) = 1, A(0) = 0$.
When assigning $A$ to $B$ (where $B$ is declared `0 to 4`), VHDL assigns positional bit-by-bit from left to right:
$B(0) \Leftarrow A(4) = 1$
$B(1) \Leftarrow A(3) = 0$
$B(2) \Leftarrow A(2) = 0$
$B(3) \Leftarrow A(1) = 1$
$B(4) \Leftarrow A(0) = 0$.
Therefore, $B(4) = 0$.

### Exercise 2

* **Prompt:** Write a structural VHDL code for the schematic diagram shown in Figure (Slide 25).



#### Diagram Reconstruction (Slide 25)

Cross-coupled SR latch formed from two OR gates each followed by an inverter (discrete NOR structure):

* Top stage: OR gate with inputs `Set` and feedback wire `Q`. Output feeds into an inverter (`INV`), producing output `Qbar`.


* Bottom stage: OR gate with inputs `Reset` and feedback wire `Qbar`. Output feeds into an inverter (`INV`), producing output `Q`.



#### Structural Solution

```vhdl
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity sr_latch_structural is
    Port (Set, Reset: in STD_LOGIC;
          Q, Qbar:    inout STD_LOGIC); -- or buffer / intermediate signals
end sr_latch_structural;

architecture Structural of sr_latch_structural is
    component OR2 is
        port (a, b: in STD_LOGIC; f: out STD_LOGIC);
    end component;

    component INV is
        port (a: in STD_LOGIC; f: out STD_LOGIC);
    end component;

    signal or1_out, or2_out: STD_LOGIC;
    signal q_int, qbar_int: STD_LOGIC;

begin
    U1: OR2 port map (a => Set,   b => q_int,    f => or1_out);
    U2: INV port map (a => or1_out, f => qbar_int);
    U3: OR2 port map (a => qbar_int, b => Reset, f => or2_out);
    U4: INV port map (a => or2_out, f => q_int);

    Q    <= q_int;
    Qbar <= qbar_int;
end Structural;

```

### Exercise 3

* **Prompt:** Identify any TWO errors in the provided VHDL code and correct them (Slide 26).


* **Analysis of Errors:**
1. `Sum in Integer range 0 to 5);` inside `casewhen_err` entity declaration has mode `in`; it is assigned to in line 36/37/38, so it must be `out` (or `buffer`).


2. `Sum` is declared as an `Integer`, but assigned vector literals (`"001"` and `"110"`) instead of integers.


3. Comma delimiters used at ends of assignment lines (`sum <= "001",`) instead of semicolons (`;`).


4. Concatenation `A & B` yields a 6-bit vector (`3 downto 0` & `1 downto 0`), but choices `"00001"` and `"00010"` are only 5 bits wide.


5. `Case` statement is written concurrently within `architecture` without an enclosing `process` block.





### Exercise 5

* **Prompt:** Write the hierarchical design of a 4-bit Ripple Carry Adder circuit using four full adders (Slide 27).



#### Diagram Reconstruction (Slide 27)

A block diagram depicting a 4-bit ripple carry adder:

* Input buses: `A` (4-bit bus) and `B` (4-bit bus) feed an upper block labeled `process_read_inputs()`.


* Sliced into single lines: $(A_3, B_3)$, $(A_2, B_2)$, $(A_1, B_1)$, and $(A_0, B_0)$.




* Four full adder blocks arranged horizontally from right to left: `FA0`, `FA1`, `FA2`, `FA3`.


* External carry input `Cin` enters `FA0` from the right.


* `FA0` takes $(A_0, B_0, C_{in})$, outputs sum $S_0$ downward and carry $C_1$ leftward into `FA1`.


* `FA1` takes $(A_1, B_1, C_1)$, outputs sum $S_1$ downward and carry $C_2$ leftward into `FA2`.


* `FA2` takes $(A_2, B_2, C_2)$, outputs sum $S_2$ downward and carry $C_3$ leftward into `FA3`.


* `FA3` takes $(A_3, B_3, C_3)$, outputs sum $S_3$ downward and carry $C_{out}$ exiting out the left.




* A lower block labeled `process_generate_sum()` collects $S_0, S_1, S_2, S_3$ and bundles them into the 4-bit `Sum` bus.



### Exercise 6 (Q&A Drill)

1. **What is meant by mode in an entity?**
* The direction of data flow for a port relative to the entity boundary (`in`, `out`, `inout`, `buffer`, or `linkage`).




2. **Name the built-in data types used in an entity?**
* `Boolean`, `Integer`, `Character`, `Bit`.




3. **Which of these are valid identifiers: `behav2; myfriend_4; 2go_home; x; all; after_8;`?**
* `behav2`: Valid.
* `myfriend_4`: Valid.
* `2go_home`: Invalid (cannot begin with a numeric digit in standard VHDL).


* `x`: Valid.
* `all`: Invalid (reserved VHDL keyword).


* `after_8`: Invalid (starts with reserved keyword prefix, or if treated as pure identifier, valid; but `after` itself is a reserved keyword).




4. **Where would you use `port map` and where would you use `port`?**
* `port` is used in entity and component declarations to define interface boundaries.


* `port map` is used in architecture statement bodies during component instantiation to bind actual signals to formal ports.




5. **Name the three levels used in an architecture body.**
* Declarative part, statement part (`begin ... end`), and component/process execution level.




6. **Within `port map`, what does `=>` signify?**
* Named formal parameter association linking a component port on the left to an actual architecture signal/port on the right.




7. **What mode will be used if no mode applies in port list?**
* Default mode is `in`.



### Exercise 7 (True/False Drill)

1. **An entity defines behaviour?** False (it defines the interface/ports; architecture defines behavior).


2. **An entity is equivalent to a symbol?** True (it specifies external pins similar to a schematic symbol).


3. **You can place behaviour inside an entity?** False (in standard hardware modeling, behavioral code resides within an architecture).


4. **An entity must have only one architecture?** False (an entity can be linked with multiple architectures).


5. **In VHDL '87 an identifier can begin with a number?** False.


6. **External signals are declared in an architecture body?** False (external ports are declared in the entity; architecture declares internal signals).


7. **Mode is specified on internal signals?** False (internal signals do not have modes; modes belong strictly to entity/component ports).


8. **`++` is used to define a comment statement?** False (VHDL comments begin with `--`).


9. **Component declaration can be in an entity declaration?** False (placed within architecture declarative regions or packages).


10. **Signals can be declared within an entity declaration?** False (ports are declared in the entity; internal interconnect signals are declared in architectures/packages).



---

## More on syntax (Slide 30)

* `::=` : Means definition (e.g., `entity declaration ::=`).


* `<>` : Means default value of the port / non-terminal placeholder.


* `{}` : Means optional and repeating.


* `[]` : Means optional.


* `|`  : Means alternative ("or", e.g., `constant | variable`).



---

## Key Equations

**Half Adder Boolean Sum**


$$\text{Sum} = a \oplus b$$

* **Variables:**
* $a$: Single-bit logic input [dimensionless, type `std_logic`]


* $b$: Single-bit logic input [dimensionless, type `std_logic`]


* $\text{Sum}$: Single-bit logic output representing least significant sum bit [dimensionless, type `std_logic`]




* **Assumes:** Binary Boolean algebra; ideal logic transitions without gate propagation delay.


* **Breaks when:** Inputs assume invalid logic levels (e.g., `'U'`, `'X'`, `'Z'`) under multi-valued IEEE 1164 evaluation resulting in unresolvable output states.



---

**Half Adder Boolean Carry**


$$\text{Carry} = a \cdot b$$

* **Variables:**
* $a$: Single-bit logic input [dimensionless, type `std_logic`]


* $b$: Single-bit logic input [dimensionless, type `std_logic`]


* $\text{Carry}$: Single-bit logic output representing generated carry bit [dimensionless, type `std_logic`]




* **Assumes:** Binary Boolean operations.


* **Breaks when:** Multi-valued non-forcing states are evaluated without resolution functions.



---

**Full Adder Carry Generation Logic (Slide 22 vs Slide 23 Implementation)**


$$C_{\text{out}} = C_1 + C_2 = (A \cdot B) + (C_{\text{in}} \cdot (A \oplus B))$$

* **Variables:**
* $A, B$: Primary 1-bit input operands [dimensionless, type `std_logic`]


* $C_{\text{in}}$: Primary incoming carry bit [dimensionless, type `std_logic`]


* $C_1$: Intermediate carry generated by first half adder ($A \cdot B$) [dimensionless, type `std_logic`]


* $C_2$: Intermediate carry generated by second half adder ($C_{\text{in}} \cdot (A \oplus B)$) [dimensionless, type `std_logic`]


* $C_{\text{out}}$: Final composite carry-out bit [dimensionless, type `std_logic`]




* **Assumes:** Mutually exclusive generation where $C_1$ and $C_2$ are never simultaneously 1, allowing Carry generation via OR gate ($C_1 \lor C_2$).


* **Breaks when:** Hardware description erroneously models the combination using an `AND` operator (as typed on slide 23: `carry <= int_carry1 and int_carry2;`), forcing $C_{\text{out}}$ to remain stuck low.



---

## Concept Index

* Design Unit


* Entity


* Architecture


* Package


* Package Body


* Configuration


* WORK Library


* Port Declaration


* Behavioural Architecture


* Structural Architecture


* Case Insensitivity


* Comment Syntax (`--`)


* Mode `in`

* Mode `out`

* Mode `inout`

* Mode `buffer`

* Mode `linkage`

* Data Type `Boolean`

* Data Type `Integer`

* Data Type `Character`

* Data Type `Bit`

* IEEE `std_logic_1164`

* 9-Valued Logic (`U`, `X`, `0`, `1`, `Z`, `W`, `L`, `H`, `-`)


* `std_logic_vector`

* Range Specification `to`

* Range Specification `downto`

* Array Slicing


* Physical Type `Time`

* Enumerated Type


* User-Defined Type


* Attribute `enum_encoding`

* Component Declaration


* Component Instantiation


* Port Map


* Positional Association


* Named Association (`=>`)


* Hierarchical Design


* Half Adder


* Full Adder


* Ripple Carry Adder


* Cross-Coupled RS Latch


* Backus-Naur Syntax Notation



---

## Open / Unresolved

* ❓ **Slide 3 & Slide 9 syntax illegality:** The snippet uses `if sel = 1 then` without placing the `if` construct inside an explicit `process` statement. In synthesizable VHDL, `if` is a sequential statement forbidden directly inside a concurrent architecture body. Additionally, integer `1` is compared against `std_logic` without quotes (should be `'1'`).
* ❓ **Slide 13 Integer Range Typo:** Slide specifies 32-bit integer range as `-2147483648 to +2147483648`. In standard two's complement 32-bit math, the upper bound is $+2147483647$ ($2^{31} - 1$).
* ❓ **Slide 15 Vector Assignment Vector Size Mismatch:** Slide states for `A <= "110111001"` that `A(0) = 1`, but the literal contains 9 bits while `(9 downto 0)` requires 10 bits.
* ❓ **Slide 20 Syntax Typos in Component Ports:** Semicolons are placed immediately prior to closing parentheses in port lists (e.g., `port (a,b: in std_logic; f: out std_logic;);`), which is invalid VHDL grammar.
* ❓ **Slide 23 Logic Bug in Full Adder Carry Output:** Line `carry <= int_carry1 and int_carry2;` uses `and` instead of `or`. Because `int_carry1` ($A \cdot B$) and `int_carry2` ($C_{\text{in}} \cdot (A \oplus B)$) can never be simultaneously true, `carry` will evaluate to `0` at all times.
* ❓ **Slide 27 Exercise 5 Left Unimplemented:** The 4-bit Ripple Carry Adder schematic was given as a structural composition exercise without code provided in the lecture material.