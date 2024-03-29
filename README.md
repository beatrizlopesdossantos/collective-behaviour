# Model of collective behavior based purely on vision
![Simulation](images/simulation.gif)
![Simulation with predator](images/predator.gif)

## Team members
- [Beatriz Lopes dos Santos](https://github.com/beatrizlopesdossantos)
- [Juraj Kulich](https://github.com/jurajkulich)
- [Ricardo Ferreira](https://github.com/rickyfer305)
- [Tomas Marek](https://github.com/realkuresryzi)

## Presentation
[Canva presentation](https://www.canva.com/design/DAF5MPtnm1A/xUs_hnICXeDpUTCL1cy6gQ/view?utm_content=DAF5MPtnm1A&utm_campaign=designshare&utm_medium=link&utm_source=editor)

## Paper to be explored
### [A model of collective behavior based purely on vision](https://www.science.org/doi/10.1126/sciadv.aay0792)

This paper explores a model of collective behavior in animal groups based **purely on vision**. The model is based on the idea that animals use their vision to perceive the positions and orientations of their neighbors, and then use this information to adjust their own movement.

It is a model without spacial representation and collision, meaning that it does not explicitly track the positions of the individuals in the group. Instead of it, it assumes that each individual are aware of the positions and orientations of its neighbors within a certain range.

## Plan
### 1st Milestone (20 November 2023, 12:00 AM)
- Review of concepts and existing models
- Understand the vision-based interaction approach and how it differs
- General overview of the problem and general idea on how the problem will be approached
- Summarize the various collective behaviors produced by the model

### 2nd Milestone (18 December 2023, 12:00 AM)
- Polishing of the previous report based on the received comments
- Details about the methods and the proposed methodology for verification
- Choose a programming language/environment like Python or JavaScript
- Decide on 2D vs 3D implementation
- Select metrics to analyze like neighbor distance, collisions
- Implement the model based on selected criteria

### 3rd Milestone (8 January 2024, 12:00 AM)
- Tweek the implementation
- Analyze metrics for different parameters
- Compare emergent behaviors to paper
- Write the final report with every detailed processe and results

## Goals
- Recreate the model
- Implement the raycast vision
- Add predator simulation

We were able to implement all of the goals 

## Instructions
To run the model without the predator, go to simulation.py and run on the terminal:

`python3 simulation.py
`    

To run the model with the predator, go to simulation_with_predator.py and run on the terminal:

`python3 simulation_with_predator.py
`    
