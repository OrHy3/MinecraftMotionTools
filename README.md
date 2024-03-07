# MinecraftMotionTools
MinecraftMotionTools is a collection of functions whose purpose is to ease prediction of the velocity and the position of entities simulated into Minecraft.
# How does it work?
Minecraft updates velocity in a different way from real-physics objects, plus it complicates everything just by being a video game and having to update the values in a finite unit of time (the tick).

Minecraft's Wiki got [some information](https://minecraft.wiki/w/Entity#Motion_of_entities) about how it works, but [here](https://hackmd.io/ySiQhr_SSUatNc6qAkbFcw) is the reasoning behind the velocity equations.

Another complication comes from what I, in the functions' arguments, refer to as [slowed down position](https://minecraft.wiki/w/Entity#cite_note-gravityBefore-4), which required forking the formulas for every different case.

Finally, [here](https://hackmd.io/V9oMODQbT5mBA-o4OM76pA) is the formulas' sheet I wrote down. Take in mind that a fair amount of them make use of [Lambert's W function](https://en.wikipedia.org/wiki/Lambert_W_function).

If you don't know what parameters to set for a specific entity, check them on the [wiki's page](https://minecraft.wiki/w/Entity#Motion_of_entities) as well.
# How to install?
Install Python 3 and pip, then run
```
pip install MinecraftMotionTools
```
# How to use?
Check some of the code examples for common uses.