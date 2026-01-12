# Nodes-Movement
A Plugin for [Glyphs.app](https://glyphsapp.com) that shows the movement of path nodes between masters with arrows representation.

![Nodes Movement](images/Screenshot.png)

**Nodes Movement** is a Glyphs Reporter Plugin for the Glyphs that visualizes how path nodes move between compatible masters using arrows.  
It is developed for variable fonts consistency, interpolation debugging, and design analysis.

## Features
- Visualizes node movement between masters using directional arrows  
- Shows the previous master as a lightly tinted layer
- Uses arrows to clearly indicate direction  
- Helps spot interpolation issues

## Usfull for
- Understanding interpolation direction
- Debugging variable font axes  
- Comparing structural changes between masters 


## How to use
- After installation enable the plugin via: `View > Show Nodes Movement`.
- Make sure your font has at least **2 masters**.
- Select the master Layer you want to see the transition **from the previous master**.  
- Only the nodes movement from the **previous master to the selected master** will be visualized, to reduce complixity and have a clear visulistion. 

## License
Copyright 2026 Yazeed Omar (@yazeedomar).
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
See the License file included in this repository for further details.