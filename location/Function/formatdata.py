def formatdata(data):
    location=None
    photo=None
    if "geometry" in data.keys():
        if "location" in data["geometry"].keys():
            location=data["geometry"]["location"]
        else:
            location=None
    else:
        location=None
    
    if "photos" in data.keys():
        if "photo_reference" in data["photos"][0].keys():
            photo=data["photos"][0]["photo_reference"]
        else:
            photo=None
    else:
        photo=None

    return {
                "name":data["name"],
                "open_now":data["opening_hours"] if "opening_hours" in data.keys() else None,
                "place_id":data["place_id"],
                "price_level":data["price_level"] if "price_level" in data.keys() else None,
                "rating":data["rating"] if "rating" in data.keys() else None,
                "user_ratings_total":data["user_ratings_total"] if "user_ratings_total" in data.keys() else None,
                "destination":location,
                "photo":photo,
                "types":data["types"]
            }
