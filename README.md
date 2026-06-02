# CFD-Simulator

2D Pipe Fluid Dynamics Simulator: A Python-based interactive simulator developed from scratch using computational fluid dynamics (CFD) principles, finite difference methods, and Navier-Stokes equations.

## 2D Pipe Fluid Simulator

This project is the result of my High School Senior Research Project (known in Catalonia as *Treball de Recerca* or *TDR*). It consists of a 2D computational fluid dynamics (CFD) simulator developed from scratch using Python.

---

### 📝 Project Overview

The main objective of this research was to investigate the viability of building a user-friendly tool to model fluid behavior in a 2D pipe section.

> **Important Note:** This project is primarily an exercise in scientific popularization (vulgarization). It is written in Catalan. The focus was on making complex physics and mathematical concepts (such as the Navier-Stokes equations) accessible and understandable, rather than achieving professional-grade code optimization or exact numerical results.

---

### 🛠️ Approach: A "Construction Log"

Rather than a final, polished commercial product, this repository serves as a log of the construction process. It reflects the journey of translating theoretical foundations into a functional simulator:

* **Trial and Error Methodology:** Stability and functionality were achieved through practical testing and iterative adjustments.
* **Accessible Discretization:** The simulator uses the Finite Difference Method to transform complex theoretical equations into calculable algorithms.
* **Educational Focus:** The project prioritizes the explanation of principles like mass conservation and linear momentum over computational performance.
* **Real-time Interaction:** The tool emphasizes the relationship between the user and the simulation, allowing real-time interaction via the mouse.

---

### 🚀 Key Features

* **Interactive Interface:** Built with Tkinter for the GUI and Matplotlib for visual data representation.
* **Multiple Visualization Modes:** Users can toggle between pressure maps, velocity fields (quiver plots), and streamlines.
* **Dynamic Obstacles:** Allows the placement of circular or square obstacles that the fluid interacts with in real-time.

---

### ⚠️ Known Limitations

As this is an educational high school project:

* **Low Reynolds Number:** To maintain stability without excessive computing times, the simulation runs at a very low Reynolds number ($Re=2$).
* **Accuracy vs. Complexity:** While the results show a reasonable approximation of fluid behavior, they are not intended to compete with professional software like SimFlow.
