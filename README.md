# ✈️ Flight Routes System (Django Machine Test)

A Django-based web application that models airport routes as a graph and provides traversal and path-finding functionalities.

---

## 📌 Overview

This project represents airports as **nodes** and routes as **edges**, forming a directed graph.

It allows users to:
- Add airports and routes
- Traverse routes (Nth left/right node)
- Find longest route
- Compute shortest path using Dijkstra’s algorithm
- Visualize the airport network as a tree structure

---

## ⚙️ Features

### 🔹 1. Add Airport
Create airport nodes using a simple form.

### 🔹 2. Add Route
Create connections between airports with:
- Source airport
- Destination airport
- Position (Left / Right)
- Duration

### 🔹 3. Nth Node Traversal
Find the Nth node from a starting airport in a given direction.

### 🔹 4. Longest Route
Displays the route with the maximum duration.

### 🔹 5. Shortest Path (Dijkstra)
Finds the shortest path between two airports using **Dijkstra’s algorithm**.

### 🔹 6. Graph Visualization
Displays the airport network as a **tree structure** on every page.

---

## 🧠 Technical Concepts Used

- Django MVC Architecture
- ModelForm & Form validation
- Graph Data Structure
- Tree Representation of Graph
- Dijkstra’s Algorithm (Shortest Path)
- Template Inheritance (`base.html`)
- Recursive template rendering

---

## 🛠️ Installation & Setup

### 1. Clone the repository

```bash
git clone <your-repo-link>
cd flight_system

### 2. Create virtual environment

python -m venv venv

Activate:

venv\Scripts\activate   # Windows


### 3. Install dependencies

pip install -r requirements.txt


### 4. Run migrations

python manage.py migrate


### 5. Run server

python manage.py runserver

🌐 Usage Guide

Go to:
http://127.0.0.1:8000/

Add Airports first
Add Routes
Use features:
Nth Node
Longest Route
Shortest Path