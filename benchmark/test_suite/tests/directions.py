import random

class Directions:
    def __init__(self, total_locations, total_queries) -> None:
        self.name = "Directions"
        self.total_locations = total_locations
        self.total_queries = total_queries
        self.sample_locations, self.query_messages = self.generate_sample_locations()

    def generate_sample_locations(self):
        assert self.total_queries <= 4, "Can only do 4 query questions."
        assert self.total_locations >= self.total_queries, "total_locations should be greater than or equal to total_queries."

        locations = [
            "Hospital", "Library", "Retail Area", "Park", "Museum",
            "Playground", "Statue of Founder", "Town Hall", "High Street"
        ]

        directions = [
            "is a location in my hometown, it is {} KM, {} from {}.",
            "is a place located {} KM, {} from {}.",
            "{} is located {} KM, {} from {}."
        ]

        sample_locations = []
        points_of_interest = []

        # Generate points of interest with distances
        start_location = random.choice(locations)
        points_of_interest.append(start_location)
        sample_locations.append(f"There is a {start_location} in the center of my hometown.")

        for _ in range(self.total_locations - 1):
            previous_location = points_of_interest[-1]
            new_location = random.choice(locations)
            distance = random.randint(1, 5)  # Random distance between 1 and 5 KM
            direction = random.choice(["North", "South", "East", "West"])
            sample_locations.append(directions[random.randint(0, 2)].format(new_location, distance, direction, previous_location))
            points_of_interest.append(new_location)

        query_choices = [
            (points_of_interest[0], points_of_interest[-1]),  # from first to last
            (points_of_interest[1], points_of_interest[-1]),  # from second to last
            (points_of_interest[2], points_of_interest[-1]),  # from third to last
            (points_of_interest[3], points_of_interest[-1]),  # from fourth to last
        ]

        # Generate query messages
        query_messages = []
        for i in range(self.total_queries):
            start_point, end_point = query_choices[i]
            query_messages.append(f"Given the points of interest that I have told you about, how would I travel from {start_point} to {end_point} following those interesting points?")

        return sample_locations, query_messages


# Example initialization
if __name__ == "__main__":
    directions_instance = Directions(total_locations=7, total_queries=4)
    print("Sample Locations:")
    for location in directions_instance.sample_locations:
        print(location)

    print("\nQuery Messages:")
    for query in directions_instance.query_messages:
        print(query)