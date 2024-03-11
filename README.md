# MinecraftMotionTools
MinecraftMotionTools is a collection of functions whose purpose is to ease prediction of the velocity and the position of entities simulated into Minecraft.
# How does it work?
Minecraft updates velocity in a different way from real-physics objects, plus it complicates everything just by being a video game and having to update the values in a finite unit of time (the tick).

Minecraft's Wiki got [some information](https://minecraft.wiki/w/Entity#Motion_of_entities) about how it works, but [here](https://hackmd.io/ySiQhr_SSUatNc6qAkbFcw) is the reasoning behind the velocity equations.

Another complication comes from what I, in the code, refer to as [acceleration drag](https://minecraft.wiki/w/Entity#cite_note-gravityBefore-4), which initially required forking the formulas for every different case (see [old sheet](https://hackmd.io/V9oMODQbT5mBA-o4OM76pA)), before I decided to generalize the formulas, introducing the coefficient `k`.

Acceleration drag works the following way:

$\text{position}\_{new}=\text{position}_{old}+\text{velocity}-k\cdot\text{acceleration}$

Finally, [here](https://hackmd.io/1t0ACyplTDKSgo-a1jA7nQ) is the formulas' sheet I wrote down. Take in mind that a fair amount of them make use of [Lambert's W function](https://en.wikipedia.org/wiki/Lambert_W_function).
# Entities' parameter table
|Type|Acceleration|Vertical drag|Horizontal drag|Applies drag|k coefficient|
|-|-|-|-|-|-|
|Players, mobs and armor stands|0.08|0.019999980926513672|0.0899999737739563|After|0|
|Entities with slow falling|0.01|0.019999980926513672|0.0899999737739563|After|0|
|Items, falling blocks and TNTs|0.04|0.02|0.02|After|1|
|Minecarts|0.04|0.05|0.05|After|1|
|Boats|0.03999999910593033|0|0.10000002384185791|-|1|
|Thrown eggs, snowballs and ender pearls|0.029999999329447746|0.009999990463256836|0.009999990463256836|Before|0|
|Thrown potions|0.05000000074505806|0.009999990463256836|0.009999990463256836|Before|0|
|Thrown experience bottles|0.07000000029802322|0.009999990463256836|0.009999990463256836|Before|0|
|Experience orbs|0.03|0.02|0.019999980926513672|After|1|
|Thrown fishing bobbers|0.03|0.08|0.08|After|1|
|Llama spit|0.05999999865889549|0.009999990463256836|0.009999990463256836|Before|0|
|Fired arrows and thrown tridents|0.05000000074505806|0.009999990463256836|0.009999990463256836|Before|0|
|Fireballs, wither skulls and dragon fireballs|0.1|0.050000011920928955|0.050000011920928955|After|0|
|Dangerous wither skulls|0.1|0.26999998092651367|0.26999998092651367|After|0|

NOTE: For fireballs and alike, use negative velocity and position, since "opposite acceleration" [would be negative for them](https://minecraft.wiki/w/Entity#cite_ref-boom_5-0).
# How to install?
Install Python 3 and pip, then run
```
pip install MinecraftMotionTools
```
# How to use?
Check some of the code examples for common uses.

Functions' parameters are set to Falling Blocks by default.
