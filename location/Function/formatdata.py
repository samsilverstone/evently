def formatdata(data):
    return {
                "name":data["name"],
                "open_now":data["opening_hours"] if "opening_hours" in data.keys() else None,
                "place_id":data["place_id"],
                "price_level":data["price_level"] if "price_level" in data.keys() else None,
                "rating":data["rating"] if "rating" in data.keys() else None,
                "user_ratings_total":data["user_ratings_total"] if "user_ratings_total" in data.keys() else None,
                "types":data["types"]
            }
