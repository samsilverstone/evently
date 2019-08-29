person={
    "Name":"Sanjay Sajwan",
    "place":"New Delhi",
    "Age":24,
    "Occupation":"web developer"
}


data={
    "name":person["Name"] if person["Name"] else None,
    "hobbies":person["Hobbies"] if "Hobbies" in person.keys() else None
}

print(data)