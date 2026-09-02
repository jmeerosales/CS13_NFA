# CS13_NFA


A formal finite state machine implementation for recognizing C-style comments (`/* ... */`) over the alphabet $\\Sigma = \\{j, *, /\\}$, where symbol `j` serves as a placeholder for any character other than `*` or `/`.

---


- **States ($Q$):** $\\{ q_0, q_1, q_2, q_3, q_4 \\}$
- **Alphabet ($\\Sigma$):** $\\{ j, *, / \\}$
- **Start State ($q_0$):** $q_0$
- **Accept / Final State ($F$):** $\\{ q_4 \\}$

---

## Transition Table

| $\delta$ | $j$ | $*$ | $/$ |
| :---: | :---: | :---: | :---: |
| $\rightarrow q_0$ | $\emptyset$ | $\emptyset$ | $\{q_1\}$ |
| $q_1$ | $\{q_0\}$ | $\{q_2\}$ | $\emptyset$ |
| $q_2$ | $\{q_2\}$ | $\{q_2, q_3\}$ | $\{q_2\}$ |
| $q_3$ | $\emptyset$ | $\{q_3\}$ | $\{q_4\}$ |
| $*q_4$ | $\emptyset$ | $\emptyset$ | $\emptyset$ |

---

## Formal Transition Functions

$$\begin{aligned}
\delta(q_0, /) &= \{q_1\} & \delta(q_2, /) &= \{q_2\} & \delta(q_4, /) &= \emptyset \\
\delta(q_0, *) &= \emptyset & \delta(q_2, *) &= \{q_2, q_3\} & \delta(q_4, *) &= \emptyset \\
\delta(q_0, j) &= \emptyset & \delta(q_2, j) &= \{q_2\} & \delta(q_4, j) &= \emptyset \\
\\
\delta(q_1, /) &= \emptyset & \delta(q_3, /) &= \{q_4\} \\
\delta(q_1, *) &= \{q_2\} & \delta(q_3, *) &= \{q_3\} \\
\delta(q_1, j) &= \{q_0\} & \delta(q_3, j) &= \emptyset
\end{aligned}$$

---

## Full NFA Transition Details
![NFA Transition](handwritten_nfa.jpe)
