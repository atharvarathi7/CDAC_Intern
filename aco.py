import requests
import folium
import random
import numpy as np

# Function to calculate distance between two points
def distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) * 2 + (point1[1] - point2[1]) * 2)

# Function to perform Ant Colony Optimization (ACO) to find the closest city
def ant_colony_optimization(points, central_point, n_ants, n_iterations, alpha):
    n_points = len(points)
    pheromone = np.ones(n_points)
    closest_city = None
    min_distance = np.inf
    
    for iteration in range(n_iterations):
        for ant in range(n_ants):
            visited = [False] * n_points
            current_point = np.random.randint(n_points)
            visited[current_point] = True
            
            while False in visited:
                unvisited = np.where(np.logical_not(visited))[0]
                probabilities = np.zeros(len(unvisited))
                
                for i, unvisited_point in enumerate(unvisited):
                    dist = distance(points[current_point], points[unvisited_point])
                    if dist == 0:  # Prevent division by zero
                        probabilities[i] = 0
                    else:
                        probabilities[i] = pheromone[unvisited_point] / dist
                
                total_prob = np.sum(probabilities)
                
                if total_prob == 0 or np.isnan(total_prob):  # Handle zero probabilities or NaN
                    probabilities = np.ones(len(unvisited))
                    probabilities /= len(unvisited)
                else:
                    probabilities /= total_prob
                
                next_point = np.random.choice(unvisited, p=probabilities)
                visited[next_point] = True
                current_point = next_point
            
            route_distance = distance(points[current_point], central_point)
            if route_distance < min_distance:
                closest_city = current_point
                min_distance = route_distance
        
        # Update pheromone levels based on the closest city found
        pheromone *= (1 - alpha)
        pheromone[closest_city] += alpha / min_distance
    
    return closest_city

# Function to fetch route information between locations using OpenRouteService API
def get_route_between_locations(api_key, start_coords, end_coords):
    url = f'https://api.openrouteservice.org/v2/directions/driving-car?api_key={api_key}&start={start_coords[1]},{start_coords[0]}&end={end_coords[1]},{end_coords[0]}'
    response = requests.get(url)
    
    if response.status_code == 200:
        route_data = response.json()
        return route_data
    else:
        print("Failed to fetch route data.")
        return None

# Replace 'your_api_key' with your actual API key from OpenRouteService
api_key = '5b3ce3597851110001cf62487bce7868e6f44aa9addaae751aa29402'

# Latitude and longitude coordinates for Central City
central_location = (40.7128, -74.0060)  # Central City (e.g., New York)

# Generate four random spots around the central location
random_spots = [
    (central_location[0] + random.uniform(-0.1, 0.1), central_location[1] + random.uniform(-0.1, 0.1))  # Random spots
    for _ in range(4)
]

# Create a map centered on the central location
mymap = folium.Map(location=central_location, zoom_start=5)

# Add marker for the central location
folium.Marker(location=central_location, popup='Central City', icon=folium.Icon(color='red')).add_to(mymap)

# Add markers for all random spots
for idx, spot in enumerate(random_spots, start=1):
    folium.Marker(location=spot, popup=f'Random Spot {idx}', icon=folium.Icon(color='blue')).add_to(mymap)

# Run ACO to find the closest city to the central location
closest_city_idx = ant_colony_optimization(random_spots, central_location, n_ants=10, n_iterations=100, alpha=1.0)
closest_city = random_spots[closest_city_idx]

# Get route information from the closest city to the central location
route_info = get_route_between_locations(api_key, closest_city, central_location)
if route_info:
    # Extract route geometry (coordinates) from route_info
    route_geometry = route_info['features'][0]['geometry']['coordinates']
    
    # Add route polyline to the map (in green color)
    folium.PolyLine(locations=[(lat, lon) for lon, lat in route_geometry], color='green', weight=3).add_to(mymap)
else:
    print("Failed to fetch route data for the closest city to the central location")

# Save map as HTML
map_file = "new_route.html"
mymap.save(map_file)

# Provide a link to the HTML file
print(f"Map saved as '{map_file}'. Click the link to view the map: ")
print(f'<a href="{map_file}" target="_blank">Open Route Map</a>')