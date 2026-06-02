# CFD-Simulator

2D Pipe Fluid Dynamics Simulator: A Python-based interactive simulator developed from scratch using computational fluid dynamics (CFD) principles, finite difference methods, and Navier-Stokes equations.

## 2D Pipe Fluid Simulator

This project is the result of my High School Senior Research Project (known in Catalonia as *Treball de Recerca* or *TDR*). It consists of a 2D computational fluid dynamics (CFD) simulator developed from scratch using Python.

---

### 📝 Project Overview

The main objective of this research was to investigate the viability of building a user-friendly tool to model fluid behavior in a 2D pipe section.

> **Important Note:** This project is primarily an exercise in scientific popularization (vulgarization). It is written in Catalan. The focus was on making complex physics and mathematical concepts (such as the Navier-Stokes equations) accessible and understandable, rather than achieving professional-grade code optimization or exact numerical results.

---

### 🔬 Physics Note: Transient vs. Steady State

Although the GUI allows real-time interactive manipulation (moving the mouse or toggling obstacles), a single true simulation setup requires time to yield scientifically reliable results. 

When an obstacle is placed, the visual output represents the **transient state** of the fluid. To obtain physically meaningful data, quantitative analysis, or accurate streamline maps, the simulation must run uninterrupted until the velocity and pressure fields stabilize into their **steady state**.

---

### 🛠️ Technical Stack & Implementation

The project is built entirely from scratch without high-level CFD black-box libraries, showcasing the core mathematical and computational logic behind fluid simulation:

* **Numerical Computation (`NumPy`):** Used to handle 2D structured meshes and solve discretized differential equations efficiently via matrix slicing.
* **CFD Core:** Implements a custom **Pressure-Poisson Equation solver** via iterative relaxation (`cavity_flow` and `pressure_poisson`) alongside the discretized momentum Navier-Stokes equations using the **Finite Difference Method**.
* **GUI & Interaction (`Tkinter`):** The simulator features a lightweight desktop interface that captures mouse movement events dynamically to alter forces and place obstacles on the fly.
* **Data Visualization (`Matplotlib`):** Integrates directly into the Tkinter loop using `FigureCanvasTkAgg` to render real-time contour fields for pressure, vector velocity arrows (`quiver`), and fluid `streamlines`.

---

### 🚀 How to Run

This script is standalone and can be executed either via a standard terminal or directly inside any Python IDE (such as PyCharm, VS Code, Spyder, or Thonny) with an integrated plot viewer.

#### Prerequisites
Make sure you have the required libraries installed:
pip install numpy matplotlib

#### Execution
Simply run the main Python file. The Tkinter GUI window will pop up automatically hosting the interactive Matplotlib plot:
python cfd_pipe_simulator.py

---

### 📐 Approach: A "Construction Log"

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
