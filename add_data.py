#!/usr/bin/env python3
""" Test link Many-To-Many Place <> Amenity
"""
from models import *

# creation of a State
state_A = State(name="California")
state_B = State(name="Algeria")
state_A.save()
state_B.save()

# creation of a City
city_A = City(state_id=state_A.id, name="San Francisco")
city_A.save()
city_B = City(state_id=state_B.id, name="Khenchala")
city_B.save()

# creation of a User
user_A = User(email="john@snow.com", password="johnpwd")
user_A.save()
user_B = User(email="kimo@snow.com", password="kasa")
user_B.save()

# creation of 2 Places
place_1 = Place(user_id=user_A.id, city_id=city_A.id, name="House 1")
place_1.save()
place_2 = Place(user_id=user_A.id, city_id=city_A.id, name="House 2")
place_2.save()
place_3 = Place(user_id=user_B.id, city_id=city_B.id, name="Hamam salhin")
place_3.save()


# creation of 3 various Amenity
amenity_1 = Amenity(name="Wifi")
amenity_1.save()
amenity_2 = Amenity(name="Cable")
amenity_2.save()
amenity_3 = Amenity(name="Oven")
amenity_3.save()

# link place_1 with 2 amenities
place_1.amenities.append(amenity_1)
place_1.amenities.append(amenity_2)

# link place_2 with 3 amenities
place_2.amenities.append(amenity_1)
place_2.amenities.append(amenity_2)
place_2.amenities.append(amenity_3)

storage.save()

print("OK")
