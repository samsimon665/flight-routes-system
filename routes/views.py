from django.shortcuts import render
from .models import Airport, Route
from .forms import RouteForm, NthNodeForm, ShortestPathForm

import heapq


# -------------------------------
# ADD ROUTE
# -------------------------------
def add_route(request):
    form = RouteForm(request.POST or None)

    if form.is_valid():
        form.save()
        form = RouteForm()  # reset form after save

    return render(request, 'add_route.html', {'form': form})


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

        # Safe fetch
        current = Airport.objects.filter(code=code).first()
        if not current:
            return render(request, 'nth_node.html', {
                'form': form,
                'result': "Invalid airport"
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
        'result': result
    })


# -------------------------------
# Q2: LONGEST ROUTE
# -------------------------------
def longest_route_view(request):
    route = Route.objects.order_by('-duration').first()

    return render(request, 'longest.html', {
        'route': route
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

        # Safe fetch
        source = Airport.objects.filter(code=source_code).first()
        destination = Airport.objects.filter(code=dest_code).first()

        if not source or not destination:
            return render(request, 'shortest.html', {
                'form': form,
                'result': "Invalid airport"
            })

        # Dijkstra setup
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
        'result': result
    })
