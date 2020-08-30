from app import app
from models import db, connect_db, get_gravity, num_with_commas, add_km_mi_to_diameter, add_hours_to_rotation, add_days_to_orbit, add_percent_to_water, User, Flight, Itinerary, ItineraryFlight, ItineraryPlanet, ItineraryTour, Planet, PlanetImage, Tour, TourImage
import requests

db.drop_all()
db.create_all()

planet_ids = [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]                                                                                                                              

base_url = "https://swapi.dev/api/planets/"                                                                                                                                                        

resp_dicts = []                                                                                                                                                                                    

for id in planet_ids:
    resp = requests.get(f"{base_url}{id}")    
    resp_dicts.append(resp.json()) 

resp_dicts[0]['description'] = "The most famous planet in the galaxy!  Birthplace of Anakin Skywalker, who later became Lord Vader, the most feared leader of the dreaded Empire.  Home of Rebel hero, Luke Skywalker!  Take a tour of either of their homes, rent one of your own and watch the beautiful twin sunset, or visit the galaxy-famous Mos Eisley Cantina!"
resp_dicts[1]['description'] = "A beautiful, jungle-covered moon orbiting the gas giant Yavin, Yavin IV was made famous from the Battle of Yavin.  It was from a base on Yavin IV that the Rebel Alliance launched an attack that destroyed the first Death Star.  You can still tour this famous base, and after, explore the giant rainforests!  Adventure awaits at Yavin IV!"
resp_dicts[2]['description'] = "Make sure to dress in three or more layers here!  It's downright cold year-round on Hoth, but the sights you can see here are incredible!  You can visit the remnants of Echo Base, a famous Rebel stronghold that was nearly destroyed by the Empire at the Battle of Hoth.  If you can brave the cold, take a scenic ride on a Tauntaun through the mountains of Hoth!"
resp_dicts[3]['description'] = "A damp, dark, quiet planet, Dagobah offers one thing and one thing only - a chance to visit the home of galaxy-famous Master Jedi Yoda!  His modest hut has been preserved over the years by conservationists and is open to the public!  See where the most famous Jedi ever called home and where he trained the second most famous Jedi ever, Luke Skywalker!  Book now!"
resp_dicts[4]['description'] = "Bespin's Cloud City is a sight to behold.  A spectacle of intelligent engineering, the entire city sits above the crushing pressure of the interior of Bespin, giving you a safe and spectacular view of the gigantic clouds.  Known for its opulent dining, hotels, and night life, there are no shortage of things to do.  You can also visit the famous carbon-freezing facility where Rebel hero Han Solo was frozen in carbonite and where Lord Vader told Luke Skywalker that he was his father.  Such history here in Bespin!"
resp_dicts[5]['description'] = "Made famous from the Battle of Endor, where the Rebel Alliance defeated the dreaded Empire for good and destroyed the second Death Star, the forest moon of Endor is rich with history and natural beauty.  You can visit a part original/part recreation of the Empire bunker and base, you can spend a few nights in a beautiful Ewok village, or you can simply explore the beautiful forests.  No shortage of things to do here on Endor!"
resp_dicts[6]['description'] = "Oozing with history and natural beauty, Naboo is a sight to behold.  Come tour the beautiful royal palace of Queen Amidala, Anakin Skywalker's wife, at Theed.  Take a tour of the hangar at Theed, where Naboo forces took their city back with the help of Jedis Qui-Gon-Jinn and Obi-Wan Kenobi from the Trade Federation.  Tour the generator complex where the two Jedis fought evil Sith apprentice, Darth Maul.  Visit the underwater city of Otoh Gunga in a Tribubble Bongo and spend a few nights under the sea!  Or stay above water in a beautiful lake home.  Naboo has plenty to offer!"
resp_dicts[7]['description'] = "Calling all city-people!  If you're looking for breathtaking skyscrapers and luxury shopping, hotels, dining, and nightlife, then Coruscant is the place for you!  And if you're a history buff, check out the galaxy-famous Jedi Temple and Galactic Senate building!  Into opera?  Coruscant's famous Galaxies Opera House in the Uscru District is the place for you!  There is truly something for everyone in Coruscant.  Book today!"
resp_dicts[8]['description'] = "Love the ocean?  Love rain?  Then you'll love Kamino!  It is almost always raining on this planet and it is completely covered in water.  Thanks to the ingenious Kaminoans though, there are many facilities you can sleep comfortably in and stay dry in.  You can visit the famous cloning facility where the Republic got its clone army from.  If you're feeling really adventurous and brave, try going for a ride on an Aiwha, a flying creature that the Kaminoans use to get around a lot!"
resp_dicts[9]['description'] = "Move over, Mars!  There's a new red planet in town, and it's called Geonosis!  You can tour the Petranaki Arena, the site where the famous Clone Wars began, you can tour numerous Separatists facilities that have survived throughout the years, and you can simply tour the land in a speeder.  Get red today!"
resp_dicts[10]['description'] = "A unique planet where all sentient life lives in enormous sinkholes below the surface of the planet, Utapau has to be seen to be believed!  A remarkable feat of Utapauan engineering and ingenuity, Utapauans transformed these sinkholes into vibrant cities.  You can visit the most famous of these sinkhole cities, Pau City, and explore what it has to offer!  This is where General Grievous was killed by Master Jedi Obi-Wan Kenobi near the end of the Clone Wars.  Explore the city on the back of a Varactyl or in a TSMEU-6 Wheel Bike!"
resp_dicts[11]['description'] = "Make sure to bring a portable fan to this planet, because it is hot, hot, hot!  Explore the abandoned Klegger Corp. Mining Facility, where Obi-Wan Kenobi and Darth Vader battled each other with lightsabers until Obi-Wan came out victorious.  Ironically, this is also the planet where Vader healed himself from those wounds in his castle, which you can also visit!  You can also take a tour of the many lava rivers that flow through the planet.  Steamy adventures await on Mustafar!"
resp_dicts[12]['description'] = "Home of the gentle giants, the Wookies, Kashyyyk is a beautiful and welcoming planet.  Spend a few nights in a Wookie village and tour the land in a Wookie flying catamaran!  For you history buffs, you can visit the site of the Battle of Kashyyyk, where the Republic and Wookie forces drove out the invading Separatist droid army in the Clone Wars."
resp_dicts[13]['description'] = "An asteroid colonized by the Kallidahin, Polis Massa offers spectacular views of the surrounding asteroid belt and advanced facilities that will take your breath away!  One of the facilities that you can visit is the medical facility where Rebel heroes Luke Skywalker and Leia Organa were born and where their mother, Padme Amidala passed away giving birth.  Sights and history - what more do you want??  Visit Polis Massa today!"
resp_dicts[14]['description'] = "A war-torn planet for most of its recent history, Mygeeto is finally at peace now.  You can tour its war-torn cities and contribute to its revitalized economy.  The native Lurmen species have reclaimed their planet and welcome visitors to their new, thriving, and vibrant home!"
resp_dicts[15]['description'] = "A planet covered in the most beautiful plant life the galaxy has ever known!  It's a treasure you have to see for yourself.  Visit Felucia today!"

for resp_dict in resp_dicts:
    new_gravity = get_gravity(resp_dict['diameter'])
    pretty_population = num_with_commas(resp_dict['population'])
    pretty_diameter = add_km_mi_to_diameter(resp_dict['diameter'])
    pretty_rotation = add_hours_to_rotation(resp_dict['rotation_period'])
    pretty_orbit = add_days_to_orbit(resp_dict['orbital_period'])
    pretty_water = add_percent_to_water(resp_dict['surface_water'])

    new_planet = Planet(name=resp_dict['name'], description=resp_dict['description'], diameter=pretty_diameter, rotation_period=pretty_rotation, orbital_period=pretty_orbit, gravity=new_gravity, population=pretty_population, climate=resp_dict['climate'], terrain=resp_dict['terrain'], surface_water=pretty_water)
    db.session.add(new_planet)
    db.session.commit()

scarif = Planet(name='Scarif', description="Can you imagine the most battle-hardened stormtroopers of the Empire stripping down to their boxers every day after 'work' and going swimming in the ocean?  Well, I bet that really happened here on Scarif!  How could you not take a dip in these perfect waters?  Even if you are a stormtrooper!  The entire planet is like the Imperial Security Complex.  Nothing but a bunch of small, tropical islands with perfect sandy beaches and crystal clear blue waters.  This planet is an absolute paradise.  Book now!", diameter="12,000 km / 7,456.44 mi", rotation_period="30 Earth hours", orbital_period="289 Earth days", gravity="0.94 Standard Earth Gs", population="150,000,000", climate="tropical", terrain="islands, ocean", surface_water="85%")
db.session.add(scarif)
db.session.commit()