from django.shortcuts import render
from .models import Airport, Route
from .forms import AirportForm, RouteForm, NthNodeForm, ShortestPathForm

import heapq


# -------------------------------
# TREE BUILDER (GRAPH → TREE)
# -------------------------------
def build_tree(node, visited=None):
    if visited is None:
        visited = set()

    # Prevent infinite loops
    if node.id in visited:
        return {"code": node.code, "children": []}

    visited.add(node.id)

    children = Route.objects.filter(from_airport=node)

    return {
        "code": node.code,
        "children": [
            build_tree(route.to_airport, visited.copy())
            for route in children
        ]
    }


def get_tree():
    root = Airport.objects.first()
    return build_tree(root) if root else None


# -------------------------------
# ADD AIRPORT
# -------------------------------
def add_airport(request):
    form = AirportForm(request.POST or None)

    if form.is_valid():
        form.save()
        form = AirportForm()

    return render(request, 'add_airport.html', {
        'form': form,
        'tree': get_tree()
    })


# -------------------------------
# ADD ROUTE
# -------------------------------
def add_route(request):
    form = RouteForm(request.POST or None)

    if form.is_valid():
        form.save()
        form = RouteForm()

    return render(request, 'add_route.html', {
        'form': form,
        'tree': get_tree()
    })


# -------------------------------
# Q1: Nth LEFT/RIGHT NODE
# -------------------------------
def nth_node_view(request):
    form = NthNodeForm(request.POST or None)
    result = None

    if form.is_valid():
        code = form.cleaned_data['start_airport']
        direction = form.cleaned_data['direction']
        steps = form.cleaned_data['steps']

        current = Airport.objects.filter(code=code).first()

        if not current:
            return render(request, 'nth_node.html', {
                'form': form,
                'result': "Invalid airport",
                'tree': get_tree()
            })

        for _ in range(steps):
            route = Route.objects.filter(
                from_airport=current,
                position=direction
            ).first()

            if not route:
                result = "No such node found"
                break

            current = route.to_airport

        else:
            result = current

    return render(request, 'nth_node.html', {
        'form': form,
        'result': result,
        'tree': get_tree()
    })


# -------------------------------
# Q2: LONGEST ROUTE
# -------------------------------
def longest_route_view(request):
    route = Route.objects.order_by('-duration').first()

    return render(request, 'longest.html', {
        'route': route,
        'tree': get_tree()
    })


# -------------------------------
# Q3: SHORTEST PATH (DIJKSTRA)
# -------------------------------
def shortest_path_view(request):
    form = ShortestPathForm(request.POST or None)
    result = None

    if form.is_valid():
        source_code = form.cleaned_data['source']
        dest_code = form.cleaned_data['destination']

        source = Airport.objects.filter(code=source_code).first()
        destination = Airport.objects.filter(code=dest_code).first()

        if not source or not destination:
            return render(request, 'shortest.html', {
                'form': form,
                'result': "Invalid airport",
                'tree': get_tree()
            })

        queue = [(0, source)]
        visited = set()

        while queue:
            cost, node = heapq.heappop(queue)

            if node == destination:
                result = cost
                break

            if node.id in visited:
                continue

            visited.add(node.id)

            routes = Route.objects.filter(
                from_airport=node
            ).select_related('to_airport')

            for route in routes:
                heapq.heappush(
                    queue,
                    (cost + route.duration, route.to_airport)
                )

        if result is None:
            result = "No path found"

    return render(request, 'shortest.html', {
        'form': form,
        'result': result,
        'tree': get_tree()
    })
