# sectionSolver
Code to calculate RC section failure surface, curvature-moment diagrams, bending modulus etc.

Still in development. Currently only able to compute moment-curvature diagram for defined rectangular RC section.
If main.py is run, program will compute and display moment-curvature diagram for 80x40cm section with 22 fi16 bars symetrically arranged around the section (4 corner, 6 left edge, 6 right edge, 3 top edge and 3 bottom edge bars). Diagram is evaluated for axial load state of 2000kN compresion force.

Program takes in account nonlinear material behaviour (both concrete and reinforcement) according to Eurocode 2. Moment - curvature diagram is computed for fixed axial force level using displacement-control (curvature is controlled) using Newton-Raphson method

Solution algorithm is described in SectionSolver.pdf file
