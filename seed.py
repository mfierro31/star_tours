from app import app
from models import *
from secrets import *
import requests


db.drop_all()
db.create_all()

# Adding planets

# Planet IDs taken from the SWAPI

planet_ids = [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]                                                                                                                              

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
resp_dicts[13]['diameter'] = "8"
resp_dicts[13]['description'] = "An asteroid colonized by the Kallidahin, Polis Massa offers spectacular views of the surrounding asteroid belt and advanced facilities that will take your breath away!  One of the facilities that you can visit is the medical facility where Rebel heroes Luke Skywalker and Leia Organa were born and where their mother, Padme Amidala passed away giving birth.  Sights and history - what more do you want??  Visit Polis Massa today!"
resp_dicts[14]['description'] = "A war-torn planet for most of its recent history, Mygeeto is finally at peace now.  You can tour its war-torn cities and contribute to its revitalized economy.  The native Lurmen species have reclaimed their planet and welcome visitors to their new, thriving, and vibrant home!"
resp_dicts[15]['description'] = "A planet covered in the most beautiful plant life the galaxy has ever known!  It's a treasure you have to see for yourself.  Visit Felucia today!"
resp_dicts[16]['diameter'] = "13500"
resp_dicts[16]['description'] = "Neimoidians have shown off their incredible engineering skills on this planet.  A colony planet of the Neimoidians, Cato Neimoidia is populated with two major cities - Zarra, the capital city, and Tarko-se.  Each are nestled in between gigantic rock formations springing out of their acidic oceans.  The cities are built upon arches and bridges connected to these rock formations and are truly a sight to behold.  The former base of operations for the Trade Federation, Cato Neimoidia has enjoyed wealth and prosperity over the years and still attracts visitors to this day.  Take advantage of the fine dining, nightlife, and hotels.  Watch a beautiful Cato Neimoidian sunset or sunrise from atop one of these arch cities, take an aerial tour of the city, or backpack through the grasslands atop the giant rock structures.  Adventure and beauty awaits at Cato Neimoidia!"

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

# Adding images to planets

pi1 = PlanetImage(image_name="Tatooine_planet.png", planet_name="Tatooine")
pi2 = PlanetImage(image_name="Tatooine_twin_sunset.jpg", planet_name="Tatooine")
pi3 = PlanetImage(image_name="Tatooine_Mos_Eisley_cantina.jpg", planet_name="Tatooine")
pi4 = PlanetImage(image_name="Tatooine_Luke.jpg", planet_name="Tatooine")
pi5 = PlanetImage(image_name="Tatooine_anakins_home.jpg", planet_name="Tatooine")
pi6 = PlanetImage(image_name="Yavin4.png", planet_name="Yavin IV")
pi7 = PlanetImage(image_name="Yavin4_Great_Temple.png", planet_name="Yavin IV")
pi8 = PlanetImage(image_name="Yavin4_forest.jpeg", planet_name="Yavin IV")
pi9 = PlanetImage(image_name="Hoth.png", planet_name="Hoth")
pi10 = PlanetImage(image_name="Hoth_Echo_Base.png", planet_name="Hoth")
pi11 = PlanetImage(image_name="Hoth_tauntaun.jpeg", planet_name="Hoth")
pi12 = PlanetImage(image_name="Dagobah.jpg", planet_name="Dagobah")
pi13 = PlanetImage(image_name="Dagobah_yodas_hut.jpg", planet_name="Dagobah")
pi14 = PlanetImage(image_name="Dagobah_yodas_hut_interior.jpg", planet_name="Dagobah")
pi15 = PlanetImage(image_name="Bespin.png", planet_name="Bespin")
pi16 = PlanetImage(image_name="Bespin_cloud_city.jpg", planet_name="Bespin")
pi17 = PlanetImage(image_name="Bespin_cloud_city_room.jpg", planet_name="Bespin")
pi18 = PlanetImage(image_name="Bespin_carbon_freezing_chamber.jpeg", planet_name="Bespin")
pi19 = PlanetImage(image_name="Bespin_i_am_your_father.jpg", planet_name="Bespin")
pi20 = PlanetImage(image_name="Endor.png", planet_name="Endor")
pi21 = PlanetImage(image_name="Endor_death_star_explosion.png", planet_name="Endor")
pi22 = PlanetImage(image_name="Endor_bunker.png", planet_name="Endor")
pi23 = PlanetImage(image_name="Endor_landing_platform.png", planet_name="Endor")
pi24 = PlanetImage(image_name="Endor_Ewok_village.jpg", planet_name="Endor")
pi25 = PlanetImage(image_name="Naboo.png", planet_name="Naboo")
pi26 = PlanetImage(image_name="Naboo_palace.jpg", planet_name="Naboo")
pi27 = PlanetImage(image_name="Naboo_theed_hangar.png", planet_name="Naboo")
pi28 = PlanetImage(image_name="Naboo_Theed_Generator_Complex.png", planet_name="Naboo")
pi29 = PlanetImage(image_name="Naboo_gungan_city.jpg", planet_name="Naboo")
pi30 = PlanetImage(image_name="Naboo_house_on_lake.png", planet_name="Naboo")
pi31 = PlanetImage(image_name="Coruscant.jpg", planet_name="Coruscant")
pi32 = PlanetImage(image_name="Coruscant_cityscape_sundown.jpg", planet_name="Coruscant")
pi33 = PlanetImage(image_name="Coruscant_Outlander_Club_bar.png", planet_name="Coruscant")
pi34 = PlanetImage(image_name="Coruscant_JediTemple.jpg", planet_name="Coruscant")
pi35 = PlanetImage(image_name="Coruscant_senate_building.jpg", planet_name="Coruscant")
pi36 = PlanetImage(image_name="Coruscant_opera_house_suite.jpg", planet_name="Coruscant")
pi37 = PlanetImage(image_name="Kamino.jpg", planet_name="Kamino")
pi38 = PlanetImage(image_name="Kamino_city.jpeg", planet_name="Kamino")
pi39 = PlanetImage(image_name="Kamino_cloning_facility.jpg", planet_name="Kamino")
pi40 = PlanetImage(image_name="Kaminoan_aiwha_rider.png", planet_name="Kamino")
pi41 = PlanetImage(image_name="Geonosis.png", planet_name="Geonosis")
pi42 = PlanetImage(image_name="Geonosis_petranaki_arena.jpg", planet_name="Geonosis")
pi43 = PlanetImage(image_name="Geonosis_trade_federation_ships.jpg", planet_name="Geonosis")
pi44 = PlanetImage(image_name="Geonosis_landscape.jpeg", planet_name="Geonosis")
pi45 = PlanetImage(image_name="Utapau.png", planet_name="Utapau")
pi46 = PlanetImage(image_name="Utapau_landscape.jpeg", planet_name="Utapau")
pi47 = PlanetImage(image_name="Utapau_hole.jpeg", planet_name="Utapau")
pi48 = PlanetImage(image_name="Utapau_varactyl.jpeg", planet_name="Utapau")
pi49 = PlanetImage(image_name="Utapau_tsmeu-6_wheel_bike.jpg", planet_name="Utapau")
pi50 = PlanetImage(image_name="Mustafar.png", planet_name="Mustafar")
pi51 = PlanetImage(image_name="Mustafar_Klegger_Corp_Mining_Facility.png", planet_name="Mustafar")
pi52 = PlanetImage(image_name="Mustafar_vaders_castle.jpg", planet_name="Mustafar")
pi53 = PlanetImage(image_name="Mustafar_landscape.jpeg", planet_name="Mustafar")
pi54 = PlanetImage(image_name="Kashyyyk.jpg", planet_name="Kashyyyk")
pi55 = PlanetImage(image_name="Kashyyyk_landscape.jpeg", planet_name="Kashyyyk")
pi56 = PlanetImage(image_name="Kashyyyk_flyover.jpg", planet_name="Kashyyyk")
pi57 = PlanetImage(image_name="Kashyyyk_battle.png", planet_name="Kashyyyk")
pi58 = PlanetImage(image_name="Polis_Massa.png", planet_name="Polis Massa")
pi59 = PlanetImage(image_name="Polis_Massa_base.jpeg", planet_name="Polis Massa")
pi60 = PlanetImage(image_name="Polis_Massa_interior.jpg", planet_name="Polis Massa")
pi61 = PlanetImage(image_name="Polis_Massa_delivery_room.jpg", planet_name="Polis Massa")
pi62 = PlanetImage(image_name="Mygeeto.jpg", planet_name="Mygeeto")
pi63 = PlanetImage(image_name="Mygeeto_bridge_battle.png", planet_name="Mygeeto")
pi64 = PlanetImage(image_name="Mygeeto_city.jpg", planet_name="Mygeeto")
pi65 = PlanetImage(image_name="Felucia.png", planet_name="Felucia")
pi66 = PlanetImage(image_name="Felucia_plant_life.png", planet_name="Felucia")
pi67 = PlanetImage(image_name="Felucia_landscape.jpeg", planet_name="Felucia")
pi68 = PlanetImage(image_name="Cato_Neimoidia.jpg", planet_name="Cato Neimoidia")
pi69 = PlanetImage(image_name="Cato_Neimoidia_arch2.jpeg", planet_name="Cato Neimoidia")
pi70 = PlanetImage(image_name="Cato_Neimoidia_city.jpeg", planet_name="Cato Neimoidia")
pi71 = PlanetImage(image_name="Cato_Neimoidia_cockpit_view.jpg", planet_name="Cato Neimoidia")
pi72 = PlanetImage(image_name="Cato_Neimoidia_green.jpg", planet_name="Cato Neimoidia")
pi73 = PlanetImage(image_name="Scarif.png", planet_name="Scarif")
pi74 = PlanetImage(image_name="Scarif_beach.jpg", planet_name="Scarif")
pi75 = PlanetImage(image_name="Scarif_water.jpg", planet_name="Scarif")

db.session.add_all([pi1, 
pi2, 
pi3, 
pi4, 
pi5, 
pi6, 
pi7, 
pi8, 
pi9, 
pi10, 
pi11, 
pi12, 
pi13, 
pi14, 
pi15, 
pi16, 
pi17, 
pi18, 
pi19, 
pi20, 
pi21, 
pi22, 
pi23,
pi24,
pi25,
pi26,
pi27,
pi28,
pi29,
pi30,
pi31,
pi32,
pi33,
pi34,
pi35,
pi36,
pi37,
pi38,
pi39,
pi40,
pi41,
pi42,
pi43,
pi44,
pi45,
pi46,
pi47,
pi48,
pi49,
pi50,
pi51,
pi52,
pi53,
pi54,
pi55,
pi56,
pi57,
pi58,
pi59,
pi60,
pi61,
pi62,
pi63,
pi64,
pi65,
pi66,
pi67,
pi68,
pi69,
pi70,
pi71,
pi72,
pi73,
pi74,
pi75])

db.session.commit()

# Adding Tours

t1 = Tour(name="Luke and Anakin Skywalker House Tour", description="Ever wanted to peer into the early lives of the most famous Force-wielders in history?  Now's your chance!  Preserved over the years, both Luke and his father's childhood houses are open to the public.  Come see what early life was like on Tatooine for them.  The Force is strong with these houses.  Who knows... maybe a little bit of the Force will rub off on you!  Book now!", start_time='07:00 AM', end_time='12:00 PM', duration=5, planet_name="Tatooine", price=50)
t2 = Tour(name="Mos Eisley City Tour", description="The Mos Eisley spaceport on Tatooine has been home to a lot of historic moments.  Come see where these moments took place!  Take a tour and a drink at Chalmun's Spaceport Cantina, where Luke Skywalker met Han Solo and Chewbacca, and where infamous bounty hunter Greedo was shot and killed by Han Solo.  Who shot first?  The galaxy may never know...  Explore the hangar where the Rebel heroes narrowly escaped a shootout with stormtroopers aboard the Millennium Falcon.  Come see all that Mos Eisley has to offer!", start_time='03:00 PM', end_time='7:00 PM', duration=4, planet_name="Tatooine", price=50)
t3 = Tour(name="Jabba's Palace Tour", description="The Hutts were a notoriously violent and sadistic gang, but luckily, their influence over the planet of Tatooine has vanished.  The last Hutt that had any real power, was famous crime lord Jabba.  He had an extravagant palace built for himself and his inner circle that is still standing today.  Located in the vast, isolated Dune Sea, the palace is an oasis.  Known for its opulent parties and lawlessness, it was a great place for criminals to rub shoulders with other criminals.  Now, it's been converted into a grand museum!  Visit Jabba's Palace today!", start_time='07:00 AM', end_time='5:00 PM', duration=10, planet_name="Tatooine", price=100)
t4 = Tour(name="Jawa Sandcrawler Tour", description="Ever wanted to go inside a sandcrawler?  Well, now's your chance!  In an exclusive agreement with Star Tours, Jawas on Tatooine have decided to rent out one of their sandcrawlers for tours!  You can tour the inside of a gigantic sandcrawler and take a ride in one too!  Don't pass on this opportunity!  It may only be here for a limited time!", start_time='05:00 PM', end_time='08:00 PM', duration=3, planet_name="Tatooine", price=40)
t5 = Tour(name="Great Temple Tour", description="The Great Temple on Yavin IV was home to one of the most successful Rebel Alliance attacks in history.  From this temple, the Rebels launched a space fleet to attack the first Death Star that was orbiting the planet of Yavin.  Some say they destroyed the Death Star with only seconds remaining before the Death Star would have destroyed their base.  It was a tremendous victory and was heard across the galaxy.  Come tour this historic temple today!", start_time='10:00 AM', end_time='01:00 PM', duration=3, planet_name="Yavin IV", price=45)
t6 = Tour(name="Rainforest Tour", description="You may have seen rainforests on Earth, but nothing compares to the rainforests on Yavin IV!  Teeming with alien wildlife and plant life, the rainforests of Yavin IV have to be seen to be believed.  Take a hiking tour with a tour guide who knows these rainforests and knows the best parts to see.  Book today!", start_time='07:00 AM', end_time='12:00 PM', duration=5, planet_name="Yavin IV", price=70)
t7 = Tour(name="Echo Base Tour", description="Tour the remnants of the famous Echo Base on Hoth, where the Empire nearly destroyed the Rebellion.  Tour the hangars, trenches, turrets, and bunkers that have survived throughout the years.  It's truly a sight to behold.  It's like stepping back in time!  Book today!", start_time='12:00 PM', end_time='02:00 PM', duration=2, planet_name="Hoth", price=85)
t8 = Tour(name="Tauntaun Tour", description="Known for their speed and invincibility to the cold, tauntauns are the preferred way to get around on the ground on Hoth.  If you can brave the cold, come take a ride on one and view the breathtaking mountains and snow dunes that surround Echo Base.  Don't worry about wampas, your tour guide is armed and always on the lookout.  Safety first!", start_time='12:00 PM', end_time='01:00 PM', duration=1, planet_name="Hoth", price=45)
t9 = Tour(name="Yoda's House Tour", description="The most powerful and famous Jedi of all time called this planet home the last few years of his long life.  Come see the modest hut Jedi Master Yoda lived in and where he trained Luke Skywalker.  Some say his Force spirit still lives on here.  Many have reported seeing his apparition and hearing his unmistakable voice.  Who knows?  Maybe you'll be the first to commune with him!", start_time='01:00 PM', end_time='03:00 PM', duration=2, planet_name="Dagobah", price=40)
t10 = Tour(name="Swamp Tour", description="The swamps of Dagobah are home to some exotic creatures and plant life.  Take a tour of them on a swamp boat with an expert guide!", start_time='03:30 PM', end_time='05:30 PM', duration=2, planet_name="Dagobah", price=30)
t11 = Tour(name="Carbon Freezing Facility Tour", description="The carbon freezing facility on Cloud City is enormous and is packed with so much history.  First, take a tour of the actual carbon freezing room where Rebel hero Han Solo was frozen in carbonite.  This same room is also where Darth Vader and Luke Skywalker had their first lightsaber battle.  As they continued through the facility, they eventually made their way out onto a catwalk.  It was there that Lord Vader cut off Skywalker's hand and proclaimed to him that he was his father.  Take a tour of this historic place and reenact this famous moment on the exact same catwalk!", start_time='01:00 PM', end_time='04:00 PM', duration=3, planet_name="Bespin", price=100)
t12 = Tour(name="Remnants of the Empire Tour", description="Even though the Empire was defeated on Endor, signs of their occupation still remain.  Tour a recreation of the shield generator bunker that the Rebels destroyed during the Battle of Endor, see the original landing pad Lord Vader once landed on and where he took his son from to meet Emperor Palpatine.  History comes alive here on Endor!", start_time='02:00 PM', end_time='05:00 PM', duration=3, planet_name="Endor", price=85)
t13 = Tour(name="Forest Speeder Tour", description="Ever wanted to hop on a speeder bike and whizz through the forests of Endor like Luke and Leia did?  Well, now's your chance!  Your tour guide will give you a few quick safety lessons, then you're off!  Zoom past the enormous trees of Endor and create a memory that will last forever!", start_time='11:00 AM', end_time='01:00 PM', duration=2, planet_name="Endor", price=85)
t14 = Tour(name="Theed Royal Palace Tour", description="The Royal Palace of Theed is a beautiful example of Naboo architecture.  Decorated with elegant paintings on its enormous ceilings, filled with grand pillars, grand arches, and grand staircases, the Royal Palace is a feast for the eyes.  The most famous royalty to rule from here was Queen Padme Amidala, wife of Anakin Skywalker (later, Lord Vader).  Sit on the same throne she once ruled from!  But wait, there's more!  Tour the rest of the complex, like the hangar where a young Anakin Skywalker and fleet of other Naboo fighters, took off and destroyed the Trade Federation ship that was occupying the planet.  Then tour the generator complex where Jedis Qui-Gon-Jinn and Obi-Wan Kenobi fought evil Sith apprentice Darth Maul.  Qui-Gon-Jinn made the ultimate sacrifice for the Republic, but his apprentice Obi-Wan avenged his death and killed Maul.  Walk in the actual steps of these Force-wielders!", start_time='12:30 PM', end_time='03:30 PM', duration=3, planet_name="Naboo", price=105)
t15 = Tour(name="Tribubble Bongo Otoh Gunga Tour", description="You've seen The Little Mermaid and sung along to 'Under The Sea', but how would you REALLY like to live under the sea?  Well, now you can!  The Gungans have loosened their restrictions on outsiders and now welcome them!  Tour their great underwater city Otoh Gunga in a Tribubble Bongo, a Gungan underwater transport vehicle!  Your Gungan tour guide knows all the best sights under the sea and after you're done, you'll have a delicious Gungan dinner in an opulent dining hall looking out into the depths of the Naboo ocean.  Book now!", start_time='04:00 PM', end_time='07:00 PM', duration=3, planet_name="Naboo", price=90)
t16 = Tour(name="Waterfall Hike Tour", description="Known for its natural beauty, no visit to Naboo would be complete without a waterfall hike in Naboo Lake Country!  Made famous as the location Anakin Skywalker and Padme Amidala got married and possibly conceived their famous children, Luke and Leia, Naboo Lake Country is absolutely stunning.  Your tour guide will take you on a hike through the beautiful grasslands, waterfalls, and lakes of Lake Country, and you'll end your day having a picnic lunch in a beautiful field surrounded by waterfalls, just like Anakin and Padme did so long ago.  Definitely a couples favorite!", start_time='09:00 AM', end_time='12:00 PM', duration=3, planet_name="Naboo", price=65)
t17 = Tour(name="Jedi Temple Tour", description="The Jedi Temple on Coruscant has survived for thousands of years.  It has been destroyed and rebuilt more than a few times and although it is not as glorious as its earlier days, it still stands.  Built atop a Force nexus, or Force strong point, the temple was home to the Jedi for thousands of years, until Emperor Palpatine's Jedi purge.  Although badly damaged during this time, it still survived.  Since then, it has undergone more damage and reconstruction than any other structure in the galaxy.  But now that there's finally peace, it has become a tourist destination.  Your tour guide will take you through the great Jedi archives, the Jedi council room, and the great halls where Anakin Skywalker turned to the dark side and became Darth Vader in his purging of Jedi younglings.  Come tour this sacred site today!", start_time='12:00 PM', end_time='03:00 PM', duration=3, planet_name="Coruscant", price=80)
t18 = Tour(name="Galactic Senate Tour", description="The center of Galactic power for thousands of years, the Galactic Senate of the Republic met in this building constantly.  It was made famous as the site where Chancellor Palpatine declared himself Emperor and declared the Republic as his Galactic Empire.  Liberty died here, as Padme Amidala famously proclaimed.  But all is back to peace now.  Palpatine's Empire is no more.  And now you get to visit this famous seat of power!  Tour the exterior first to appreciate the beautiful architecture and engineering and then go inside to view the beauty of the Senate chambers.  History comes alive here at the Galactic Senate!", start_time='04:00 PM', end_time='06:00 PM', duration=2, planet_name="Coruscant", price=50)
t19 = Tour(name="Cloning Facility Tour", description="During the days of the Republic just before the Clone Wars, a mysterious request was sent to the Kaminoans to create a massive clone army for the Republic.  History would later show that it was Emperor (then, Senator) Palpatine who secretly took over production of this army with the help of Count Dooku and bounty hunter Jango Fett.  You can tour this cloning facility where the grand Republic army was created.  It is still in operation today!  See how they do it all and after, enjoy an early dinner/late lunch in the Prime Minister's former dining hall, overlooking the raging ocean below.", start_time='03:00 PM', end_time='05:00 PM', duration=2, planet_name="Kamino", price=45)
t20 = Tour(name="Aiwha Tour", description="If you're not afraid of heights and not afraid to get wet, take a ride of a lifetime on an Aiwha!  Aiwhas are native flying creatures of Kamino that Kaminoans use to get around.  Your Kaminoan tour guide will keep you safe and guide you around the coolest spots of Tipoca City.  Book today!", start_time='12:00 PM', end_time='02:00 PM', duration=2, planet_name="Kamino", price=75)
t21 = Tour(name="Petranaki Arena Tour", description="Since the end of the Separatist control of the planet during the Clone Wars, Petranaki Arena has been left abandoned.  Recently, however, conservationists from nearby Tatooine decided to turn the arena into a tourist attraction.  They've created a grand museum inside the halls of the arena and even stage mock fights in the arena.  They have also brought in exotic animals from every corner of the galaxy and created a zoo for them here!  All kinds of things to see here at Petranaki Arena, the site of the beginning of the Clone Wars!", start_time='09:00 AM', end_time='12:00 PM', duration=3, planet_name="Geonosis", price=75)
t22 = Tour(name="Separatist Facilities Tour", description="When the Clone Wars erupted at the First Battle of Geonosis, the planet was home to a vast Separatist facility, complete with a war room, docking ports for enormous star ships, hangars, and an impressive droid army factory.  Take a tour of this facility, where infamous Jedi-turned-Sith-apprentice Count Dooku ruled.  Tour his hangar where he cut off Anakin Skywalker's arm, nearly killed Obi-Wan Kenobi, and fought Master Yoda, and still got away!  Tour the war room where the first plans for the Death Star were created!  And coolest of all, visit a docking station that still has a Trade Federation star ship inside it!  Tour the inside of the docking station and the ship!  Excitement awaits here on Geonosis!", start_time='12:30 PM', end_time='03:30 PM', duration=3, planet_name="Geonosis", price=100)
t23 = Tour(name="Speeder Tour", description="Take a tour of the land on a speeder similar to the one Count Dooku used to get away during the First Battle of Geonosis!  You can speed across the great sand dunes, plateaus, mountains, and spires.  Admire the red beauty of Geonosis today!", start_time='04:00 PM', end_time='06:00 PM', duration=2, planet_name="Geonosis", price=60)
t24 = Tour(name="Varactyl Tour", description="Tour the many levels of Pau City on the back of a varactyl!  Varactyls, even though they are big and loud, are gentle and loyal creatures.  Your native Utapauan tour guide will teach you everything you need to know about varactyls and will take you on a tour through all the levels of Pau City.  Masters of climbing, these creatures will take you anywhere you want to go.  Hold on tight and have fun!", start_time='03:00 PM', end_time='05:00 PM', duration=2, planet_name="Utapau", price=80)
t25 = Tour(name="Wheel Bike Tour", description="Prefer a mechanical vehicle over a biological one?  Then take an exhilarating ride on a TSMEU-6 Wheel Bike!  This was the preferred mode of transportation for Separatist General Grievous.  Take it for a ride through the countless levels of Pau City.  Like the varactyls, the wheel bike also is good at climbing and gripping.  Your Utapauan tour guide will teach you all the safety stuff and guide you through the city.  Book now!", start_time='12:00 PM', end_time='02:00 PM', duration=2, planet_name="Utapau", price=65)
t26 = Tour(name="Klegger Corp. Mining Facility Tour", description="Take a tour of the mining facility where Obi-Wan Kenobi and Anakin Skywalker fought for the first time since Anakin's turn to the dark side.  Their lightsaber battle only lasted for about an hour, but the outcome of it shaped the course of history.  Walk in the exact steps of Kenobi and Vader, stand on the exact same lava river bank where Kenobi de-limbed Vader, thus fueling his hatred and cementing his place in the dark side of the Force.  Stand on the same landing pad Vader unknowingly killed his wife, Padme, in a fit of Force rage.  A heartbreaking but memorable site that you just have to visit.", start_time='04:00 PM', end_time='07:00 PM', duration=3, planet_name="Mustafar", price=60)
t27 = Tour(name="Fortress Vader Tour", description="Why was it that Lord Vader chose this planet, the planet he experienced the most pain and trauma he had ever experienced before on, to build his fortress?  The galaxy may never know.  Maybe it has to do with the fact that the site was once home to a mysterious ancient Sith cave.  Whatever the reason, the days of Vader are long gone, but his fortress still stands and is open to the public for tours!  It is an enormous structure that was home to one of the most evil leaders in history.  Take a tour inside, with your Mustafarian tour guide, but please, don't be tempted by the dark side!", start_time='12:00 PM', end_time='03:00 PM', duration=3, planet_name="Mustafar", price=80)
t28 = Tour(name="Lava River Tour", description="Take a scenic lava river tour on a floating barge the Klegger miners used to use!  As with the mining facility tour, on this tour, you'll get to pass and stand on the spot where Kenobi defeated Vader.  You have the high ground on this tour!", start_time='08:00 AM', end_time='11:00 AM', duration=3, planet_name="Mustafar", price=45)
t29 = Tour(name="Wookie Flying Catamaran Tour", description="The gentle and friendly wookies will take you on quite a ride with this tour!  Take a ride with your wookie tour guide on one of their famous flying catamarans and view their capital city of Kachirho from the air!  You'll soar over the beautiful coastal city and over the surrounding lush land.  It's an exhilarating, beautiful, and unforgettable ride!", start_time='12:00 PM', end_time='01:00 PM', duration=1, planet_name="Kashyyyk", price=40)
t30 = Tour(name="Battle of Kashyyyk Tour", description="The scars of war are still present in the city of Kachirho.  Take a tour of the city and visit the sites where the Battle of Kashyyyk, during the end of the Clone Wars, left its mark.  You will see burn marks on trees, defensive walls, and pieces of droids from the Separatist army still buried in the beach's sand.  History comes alive on this tour.  Book today!", start_time='03:00 PM', end_time='06:00 PM', duration=3, planet_name="Kashyyyk", price=60)
t31 = Tour(name="Luke and Leia Birthroom Tour", description="The most famous site on Polis Massa, maybe even in the whole galaxy, is this facility right here!  Home to many advanced research and medical facilities that are still in use today, and therefore off limits to the general public, one medical facility has been granted access to the public.  That's the delivery room where Luke Skywalker and his sister Leia were born and where their mother Padme tragically passed away giving birth.  It is almost as sacred to the galaxy as the Holy Selpulchre is on Earth.  Come visit the place where the two most celebrated people in the history of the galaxy were born!", start_time='02:00 PM', end_time='04:00 PM', duration=2, planet_name="Polis Massa", price=50)
t32 = Tour(name="City Tour", description="Mygeeto has tragically been home to more battles than any planet would like to admit.  After the native species was driven out of their home planet, or reduced to slave status, the world fell into the hands of the Separatists and the Empire.  But after the fall of the Empire, the world was abandoned by former Imperial forces and the native Lurmen reclaimed their planet.  Now, they are rebuilding and welcoming visitors to their revitalized world!  With help from neighboring planets, they have reconstructed most of their cities, and are now trading again and starting up their economy from scratch.  Contribute to their economy with this tour!  Your native Lurmen tour guide will take you through the Southern Mesas region of the planet, that has been home to the most battles.  They'll take you across the bridge where Jedi Ki-Adi-Mundi was killed by his own clone troopers during the galaxy-wide execution of Order 66.  They'll take you to buildings that have not been reconstructed yet, that still bear the scars of war.  Then you'll finish the tour off having a lovely lunch in a newly reconstructed restaurant in the heart of the city.", start_time='12:00 PM', end_time='02:00 PM', duration=2, planet_name="Mygeeto", price=50)
t33 = Tour(name="Backpacking Tour", description="Felucia is home to the most diverse array of plant and animal life in the galaxy.  Your tour will start from the capital city of Kway Teow, where a native Felucian tour guide will take you on an overnight camping trip through the beautiful jungles of Felucia.  You'll return the next day and end with a lunch at the city's fanciest restaurant, overlooking the jungle.  Beauty awaits on Felucia!", start_time='04:00 PM', end_time='12:00 PM', duration=20, planet_name="Felucia", price=95)
t34 = Tour(name="Aerial City Tour", description="Take an aerial tour of Cato Neimoidia's jewel city Tarko-Se in a small aircraft and watch the sunset for a beautiful and unforgettable view.", start_time='05:00 PM', end_time='07:00 PM', duration=2, planet_name="Cato Neimoidia", price=75)
t35 = Tour(name="Backpacking Tour", description="Take a camping trip with your Neimoidian tour guide and camp out atop one of the gigantic rocks that tether the city of Tarko-Se together.  Watch the beautiful sunset and sunrise above an below the magnificent arch city.", start_time='03:00 PM', end_time='11:00 AM', duration=20, planet_name="Cato Neimoidia", price=100)
t36 = Tour(name="Imperial Remnants Tour", description="Besides the white, sandy beaches and crystal-clear blue waters, Scarif also offers history.  Although it's merely a patch of scarred land now, this spot on Scarif was once home to the Imperial Security Complex that housed the infamous Imperial Citadel Tower and Imperial Vault.  During the Galactic Civil War, a small group of Rebel forces, known as Rogue One, infiltrated the complex and successfully transmitted the Empire's Death Star schematics and gave the Rebels the upper hand.  They later used those schematics to destroy the first Death Star at the Battle of Yavin.  Rogue One heroically sacrificed themselves for the cause and the complex was soon obliterated by a blast from the Death Star.  On this tour, you can visit the exact spots where the Citadel Tower once stood, where some of the landing pads were, and where the main transport tunnel to the tower was.  You will also visit a beautiful memorial dedicated to the members of Rogue One, placed on the beautiful white-sand beach touching the water.  Truly a historic and sacred place!", start_time='05:00 PM', end_time='07:00 PM', duration=2, planet_name="Scarif", price=75)
t37 = Tour(name="Snorkeling Tour", description="What trip to a tropical paradise planet would be complete without a snorkeling tour?  Take a swim in the crystal-clear waters of Scarif and look at the amazing sea life.  Plenty of alien fish, coral, and other sea creatures await on this magical tour!", start_time='02:00 PM', end_time='04:00 PM', duration=2, planet_name="Scarif", price=45)

db.session.add_all([t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19, t20, t21, t22, t23, t24, t25, t26, t27, t28, t29, t30, t31, t32, t33, t34, t35, t36, t37])
db.session.commit()

# Adding images to tours

ti1 = TourImage(image_name="Tatooine_anakins_home.jpg", tour_id=1)
ti2 = TourImage(image_name="Tatooine_Luke.jpg", tour_id=1)
ti3 = TourImage(image_name="Tatooine_Mos_Eisley_spaceport.png", tour_id=2)
ti4 = TourImage(image_name="Tatooine_mos_eisley.png", tour_id=2)
ti5 = TourImage(image_name="Tatooine_Mos_Eisley_cantina.jpg", tour_id=2)
ti6 = TourImage(image_name="Tatooine_cantina_band.jpeg", tour_id=2)
ti7 = TourImage(image_name="Tatooine_Jabbas_palace.jpg", tour_id=3)
ti8 = TourImage(image_name="Tatooine_jawa_sandcrawler.jpeg", tour_id=4)
ti9 = TourImage(image_name="Yavin4_Great_Temple.png", tour_id=5)
ti10 = TourImage(image_name="Yavin4_forest.jpeg", tour_id=6)
ti11 = TourImage(image_name="Hoth_atats.jpg", tour_id=7)
ti12 = TourImage(image_name="Hoth_Echo_Base.png", tour_id=7)
ti13 = TourImage(image_name="Hoth_echo_base_hangar.jpg", tour_id=7)
ti14 = TourImage(image_name="Hoth_tauntaun.jpeg", tour_id=8)
ti15 = TourImage(image_name="Dagobah_yodas_hut.jpg", tour_id=9)
ti16 = TourImage(image_name="Dagobah_yodas_hut_interior.jpg", tour_id=9)
ti17 = TourImage(image_name="Dagobah_swamp.jpg", tour_id=10)
ti18 = TourImage(image_name="Bespin_carbon_freezing_chamber.jpeg", tour_id=11)
ti19 = TourImage(image_name="Bespin_luke_vs_vader.jpg", tour_id=11)
ti20 = TourImage(image_name="Bespin_i_am_your_father.jpg", tour_id=11)
ti21 = TourImage(image_name="Endor_bunker.png", tour_id=12)
ti22 = TourImage(image_name="Endor_shield_generator_explosion.jpeg", tour_id=12)
ti23 = TourImage(image_name="Endor_landing_platform.png", tour_id=12)
ti24 = TourImage(image_name="Endor_speeder_bike.jpg", tour_id=13)
ti25 = TourImage(image_name="Naboo_palace.jpg", tour_id=14)
ti26 = TourImage(image_name="Naboo_palace_interior.jpg", tour_id=14)
ti27 = TourImage(image_name="Naboo_palace_interior2.jpg", tour_id=14)
ti28 = TourImage(image_name="Naboo_theed_hangar.png", tour_id=14)
ti29 = TourImage(image_name="Naboo_Theed_hangar_interior.jpg", tour_id=14)
ti30 = TourImage(image_name="Naboo_Theed_Generator_Complex.png", tour_id=14)
ti31 = TourImage(image_name="Naboo_Laser_gates.png", tour_id=14)
ti32 = TourImage(image_name="Naboo_tribubble_bongo.jpeg", tour_id=15)
ti33 = TourImage(image_name="Naboo_gungan_city.jpg", tour_id=15)
ti34 = TourImage(image_name="Naboo_gungan_city_interior.png", tour_id=15)
ti35 = TourImage(image_name="Naboo_waterfalls.jpg", tour_id=16)
ti36 = TourImage(image_name="Naboo_house_on_lake.png", tour_id=16)
ti37 = TourImage(image_name="Coruscant_JediTemple.jpg", tour_id=17)
ti38 = TourImage(image_name="Coruscant_jedi_temple_interior.jpg", tour_id=17)
ti39 = TourImage(image_name="Coruscant_jedi_council.jpg", tour_id=17)
ti40 = TourImage(image_name="Coruscant_senate_building.jpg", tour_id=18)
ti41 = TourImage(image_name="Coruscant_senate_building_interior.jpeg", tour_id=18)
ti42 = TourImage(image_name="Kamino_cloning_facility.jpg", tour_id=19)
ti43 = TourImage(image_name="Kamino_clone_soldiers.jpg", tour_id=19)
ti44 = TourImage(image_name="Kaminoan_aiwha_rider.png", tour_id=20)
ti45 = TourImage(image_name="Kamino_buildings.png", tour_id=20)
ti46 = TourImage(image_name="Geonosis_petranaki_arena.jpg", tour_id=21)
ti47 = TourImage(image_name="Geonosis_geonosians_in_arena.jpg", tour_id=21)
ti48 = TourImage(image_name="Geonosis_arena_balcony.png", tour_id=21)
ti49 = TourImage(image_name="Geonosis_separatist_council.jpg", tour_id=22)
ti50 = TourImage(image_name="Geonosis_separatist_war_room.jpg", tour_id=22)
ti51 = TourImage(image_name="Geonosis_trade_federation_ships.jpg", tour_id=22)
ti52 = TourImage(image_name="Geonosis_dookus_hangar.jpg", tour_id=22)
ti53 = TourImage(image_name="Geonosis_dookus_speeder.png", tour_id=23)
ti54 = TourImage(image_name="Geonosis_landscape.jpeg", tour_id=23)
ti55 = TourImage(image_name="Utapau_varactyl.jpeg", tour_id=24)
ti56 = TourImage(image_name="Utapau_tsmeu-6_wheel_bike.jpg", tour_id=25)
ti57 = TourImage(image_name="Mustafar_Klegger_Corp_Mining_Facility.png", tour_id=26)
ti58 = TourImage(image_name="Mustafar_separatist_hideout.png", tour_id=26)
ti59 = TourImage(image_name="Mustafar_separatist-council-conference-room.png", tour_id=26)
ti60 = TourImage(image_name="Mustafar_vaders_castle.jpg", tour_id=27)
ti61 = TourImage(image_name="Mustafar_vaders_castle_interior.jpg", tour_id=27)
ti62 = TourImage(image_name="Mustafar_vaders_healing_chamber.jpeg", tour_id=27)
ti63 = TourImage(image_name="Mustafar_landscape.jpeg", tour_id=28)
ti64 = TourImage(image_name="Mustafar_floating_barge.jpg", tour_id=28)
ti65 = TourImage(image_name="Kashyyyk_flyover.jpg", tour_id=29)
ti66 = TourImage(image_name="Kashyyyk_wookie_rally.jpg", tour_id=30)
ti67 = TourImage(image_name="Kashyyyk_battle.png", tour_id=30)
ti68 = TourImage(image_name="Kashyyyk_droids_ocean.png", tour_id=30)
ti69 = TourImage(image_name="Polis_Massa_delivery_room.jpg", tour_id=31)
ti70 = TourImage(image_name="Mygeeto_bridge_battle.png", tour_id=32)
ti71 = TourImage(image_name="Mygeeto_city.jpg", tour_id=32)
ti72 = TourImage(image_name="Felucia_plant_life.png", tour_id=33)
ti73 = TourImage(image_name="Felucia_landscape.jpeg", tour_id=33)
ti74 = TourImage(image_name="Cato_Neimoidia_cockpit_view.jpg", tour_id=34)
ti75 = TourImage(image_name="Cato_Neimoidia_arch.jpg", tour_id=34)
ti76 = TourImage(image_name="Cato_Neimoidia_green.jpg", tour_id=35)
ti77 = TourImage(image_name="Cato_Neimoidia_arch2.jpeg", tour_id=35)
ti78 = TourImage(image_name="Scarif_imperial_vault.jpeg", tour_id=36)
ti79 = TourImage(image_name="Scarif_atat.jpg", tour_id=36)
ti80 = TourImage(image_name="Scarif_beach_charge.jpg", tour_id=36)
ti81 = TourImage(image_name="Scarif_water.jpg", tour_id=37)

db.session.add_all([ti1,
ti2,
ti3,
ti4,
ti5,
ti6,
ti7,
ti8,
ti9,
ti10,
ti11,
ti12,
ti13,
ti14,
ti15,
ti16,
ti17,
ti18,
ti19,
ti20,
ti21,
ti22,
ti23,
ti24,
ti25,
ti26,
ti27,
ti28,
ti29,
ti30,
ti31,
ti32,
ti33,
ti34,
ti35,
ti36,
ti37,
ti38,
ti39,
ti40,
ti41,
ti42,
ti43,
ti44,
ti45,
ti46,
ti47,
ti48,
ti49,
ti50,
ti51,
ti52,
ti53,
ti54,
ti55,
ti56,
ti57,
ti58,
ti59,
ti60,
ti61,
ti62,
ti63,
ti64,
ti65,
ti66,
ti67,
ti68,
ti69,
ti70,
ti71,
ti72,
ti73,
ti74,
ti75,
ti76,
ti77,
ti78,
ti79,
ti80,
ti81])

db.session.commit()

# Adding flights

# First round of flights.  Just simple go there, come back flights.  2 for each planet.

f1 = Flight(flight_num=5700, depart_planet="Earth", arrive_planet="Coruscant", depart_time="07:00 PM", arrive_time="07:00 AM", flight_time=12, price=250, depart_or_return="depart")
f2 = Flight(flight_num=5701, depart_planet="Coruscant", arrive_planet="Earth", depart_time="09:00 AM", arrive_time="09:00 PM", flight_time=12, price=250, depart_or_return="return")
f3 = Flight(flight_num=5710, depart_planet="Earth", arrive_planet="Endor", depart_time="06:00 PM", arrive_time="07:00 AM", flight_time=13, price=285, depart_or_return="depart")
f4 = Flight(flight_num=5711, depart_planet="Endor", arrive_planet="Earth", depart_time="10:30 AM", arrive_time="11:30 PM", flight_time=13, price=285, depart_or_return="return")
f5 = Flight(flight_num=5720, depart_planet="Earth", arrive_planet="Mygeeto", depart_time="07:00 PM", arrive_time="09:00 AM", flight_time=14, price=320, depart_or_return="depart")
f6 = Flight(flight_num=5721, depart_planet="Mygeeto", arrive_planet="Earth", depart_time="11:00 AM", arrive_time="01:00 AM", flight_time=14, price=320, depart_or_return="return")
f7 = Flight(flight_num=5730, depart_planet="Earth", arrive_planet="Bespin", depart_time="02:00 PM", arrive_time="06:00 AM", flight_time=16, price=390, depart_or_return="depart")
f8 = Flight(flight_num=5731, depart_planet="Bespin", arrive_planet="Earth", depart_time="11:30 AM", arrive_time="03:30 AM", flight_time=16, price=390, depart_or_return="return")
f9 = Flight(flight_num=5740, depart_planet="Earth", arrive_planet="Hoth", depart_time="03:00 PM", arrive_time="07:00 AM", flight_time=16, price=390, depart_or_return="depart")
f10 = Flight(flight_num=5741, depart_planet="Hoth", arrive_planet="Earth", depart_time="11:45 AM", arrive_time="03:45 AM", flight_time=16, price=390, depart_or_return="return")
f11 = Flight(flight_num=5750, depart_planet="Earth", arrive_planet="Polis Massa", depart_time="12:00 PM", arrive_time="05:00 AM", flight_time=17, price=425, depart_or_return="depart")
f12 = Flight(flight_num=5751, depart_planet="Polis Massa", arrive_planet="Earth", depart_time="11:00 AM", arrive_time="04:00 AM", flight_time=17, price=425, depart_or_return="return")
f13 = Flight(flight_num=5760, depart_planet="Earth", arrive_planet="Mustafar", depart_time="12:30 PM", arrive_time="06:30 AM", flight_time=18, price=460, depart_or_return="depart")
f14 = Flight(flight_num=5761, depart_planet="Mustafar", arrive_planet="Earth", depart_time="09:30 AM", arrive_time="03:30 AM", flight_time=18, price=460, depart_or_return="return")
f15 = Flight(flight_num=5770, depart_planet="Earth", arrive_planet="Dagobah", depart_time="12:00 PM", arrive_time="07:00 AM", flight_time=19, price=495, depart_or_return="depart")
f16 = Flight(flight_num=5771, depart_planet="Dagobah", arrive_planet="Earth", depart_time="07:45 AM", arrive_time="02:45 AM", flight_time=19, price=495, depart_or_return="return")
f17 = Flight(flight_num=5780, depart_planet="Earth", arrive_planet="Utapau", depart_time="11:00 AM", arrive_time="07:00 AM", flight_time=20, price=530, depart_or_return="depart")
f18 = Flight(flight_num=5781, depart_planet="Utapau", arrive_planet="Earth", depart_time="12:00 PM", arrive_time="08:00 AM", flight_time=20, price=530, depart_or_return="return")
f19 = Flight(flight_num=5790, depart_planet="Earth", arrive_planet="Kashyyyk", depart_time="01:45 PM", arrive_time="06:45 AM", flight_time=17, price=425, depart_or_return="depart")
f20 = Flight(flight_num=5791, depart_planet="Kashyyyk", arrive_planet="Earth", depart_time="07:45 AM", arrive_time="12:45 AM", flight_time=17, price=425, depart_or_return="return")
f21 = Flight(flight_num=5800, depart_planet="Earth", arrive_planet="Yavin IV", depart_time="12:00 PM", arrive_time="07:00 AM", flight_time=19, price=495, depart_or_return="depart")
f22 = Flight(flight_num=5801, depart_planet="Yavin IV", arrive_planet="Earth", depart_time="09:00 AM", arrive_time="04:00 AM", flight_time=19, price=495, depart_or_return="return")
f23 = Flight(flight_num=5810, depart_planet="Earth", arrive_planet="Naboo", depart_time="09:00 AM", arrive_time="06:00 AM", flight_time=21, price=565, depart_or_return="depart")
f24 = Flight(flight_num=5811, depart_planet="Naboo", arrive_planet="Earth", depart_time="12:00 PM", arrive_time="09:00 AM", flight_time=21, price=565, depart_or_return="return")
f25 = Flight(flight_num=5820, depart_planet="Earth", arrive_planet="Tatooine", depart_time="06:00 AM", arrive_time="06:00 AM", flight_time=24, price=670, depart_or_return="depart")
f26 = Flight(flight_num=5821, depart_planet="Tatooine", arrive_planet="Earth", depart_time="09:00 AM", arrive_time="09:00 AM", flight_time=24, price=670, depart_or_return="return")
f27 = Flight(flight_num=5830, depart_planet="Earth", arrive_planet="Geonosis", depart_time="06:45 AM", arrive_time="06:45 AM", flight_time=24, price=670, depart_or_return="depart")
f28 = Flight(flight_num=5831, depart_planet="Geonosis", arrive_planet="Earth", depart_time="12:45 PM", arrive_time="12:45 PM", flight_time=24, price=670, depart_or_return="return")
f29 = Flight(flight_num=5840, depart_planet="Earth", arrive_planet="Felucia", depart_time="06:30 AM", arrive_time="06:30 AM", flight_time=24, price=670, depart_or_return="depart")
f30 = Flight(flight_num=5841, depart_planet="Felucia", arrive_planet="Earth", depart_time="10:00 AM", arrive_time="10:00 AM", flight_time=24, price=670, depart_or_return="return")
f31 = Flight(flight_num=5850, depart_planet="Earth", arrive_planet="Cato Neimoidia", depart_time="03:50 PM", arrive_time="06:50 AM", flight_time=15, price=355, depart_or_return="depart")
f32 = Flight(flight_num=5851, depart_planet="Cato Neimoidia", arrive_planet="Earth", depart_time="11:50 AM", arrive_time="02:50 AM", flight_time=15, price=355, depart_or_return="return")
f33 = Flight(flight_num=5860, depart_planet="Earth", arrive_planet="Kamino", depart_time="05:45 AM", arrive_time="06:45 AM", flight_time=25, price=705, depart_or_return="depart")
f34 = Flight(flight_num=5861, depart_planet="Kamino", arrive_planet="Earth", depart_time="11:00 AM", arrive_time="12:00 PM", flight_time=25, price=705, depart_or_return="return")
f35 = Flight(flight_num=5870, depart_planet="Earth", arrive_planet="Scarif", depart_time="05:30 AM", arrive_time="06:30 AM", flight_time=25, price=705, depart_or_return="depart")
f36 = Flight(flight_num=5871, depart_planet="Scarif", arrive_planet="Earth", depart_time="10:30 AM", arrive_time="11:30 AM", flight_time=25, price=705, depart_or_return="return")

# Second round of flights.  Adding more options for each planet.

# Coruscant
f37 = Flight(flight_num=5702, depart_planet="Earth", arrive_planet="Coruscant", depart_time="09:00 PM", arrive_time="09:00 AM", flight_time=12, price=250, depart_or_return="depart")
f38 = Flight(flight_num=5704, depart_planet="Earth", arrive_planet="Coruscant", depart_time="11:00 PM", arrive_time="11:00 AM", flight_time=12, price=250, depart_or_return="depart")
f39 = Flight(flight_num=5706, depart_planet="Earth", arrive_planet="Coruscant", depart_time="01:00 AM", arrive_time="01:00 PM", flight_time=12, price=250, depart_or_return="depart")
f40 = Flight(flight_num=5708, depart_planet="Earth", arrive_planet="Coruscant", depart_time="03:00 AM", arrive_time="03:00 PM", flight_time=12, price=250, depart_or_return="depart")

f41 = Flight(flight_num=5703, depart_planet="Coruscant", arrive_planet="Earth", depart_time="12:00 PM", arrive_time="12:00 AM", flight_time=12, price=250, depart_or_return="return")
f42 = Flight(flight_num=5705, depart_planet="Coruscant", arrive_planet="Earth", depart_time="03:00 PM", arrive_time="03:00 AM", flight_time=12, price=250, depart_or_return="return")
f43 = Flight(flight_num=5707, depart_planet="Coruscant", arrive_planet="Earth", depart_time="06:00 PM", arrive_time="06:00 AM", flight_time=12, price=250, depart_or_return="return")
f44 = Flight(flight_num=5709, depart_planet="Coruscant", arrive_planet="Earth", depart_time="09:00 PM", arrive_time="09:00 AM", flight_time=12, price=250, depart_or_return="return")

# Endor
f45 = Flight(flight_num=5712, depart_planet="Earth", arrive_planet="Endor", depart_time="08:00 PM", arrive_time="09:00 AM", flight_time=13, price=285, depart_or_return="depart")
f46 = Flight(flight_num=5714, depart_planet="Earth", arrive_planet="Endor", depart_time="11:00 PM", arrive_time="12:00 PM", flight_time=13, price=285, depart_or_return="depart")
f47 = Flight(flight_num=5716, depart_planet="Earth", arrive_planet="Endor", depart_time="01:00 AM", arrive_time="02:00 PM", flight_time=13, price=285, depart_or_return="depart")
f48 = Flight(flight_num=5718, depart_planet="Earth", arrive_planet="Endor", depart_time="03:00 AM", arrive_time="04:00 PM", flight_time=13, price=285, depart_or_return="depart")

f49 = Flight(flight_num=5713, depart_planet="Endor", arrive_planet="Earth", depart_time="12:30 PM", arrive_time="01:30 AM", flight_time=13, price=285, depart_or_return="return")
f50 = Flight(flight_num=5715, depart_planet="Endor", arrive_planet="Earth", depart_time="02:30 PM", arrive_time="03:30 AM", flight_time=13, price=285, depart_or_return="return")
f51 = Flight(flight_num=5717, depart_planet="Endor", arrive_planet="Earth", depart_time="04:30 PM", arrive_time="05:30 AM", flight_time=13, price=285, depart_or_return="return")
f52 = Flight(flight_num=5719, depart_planet="Endor", arrive_planet="Earth", depart_time="06:30 PM", arrive_time="07:30 AM", flight_time=13, price=285, depart_or_return="return")

# Mygeeto
f53 = Flight(flight_num=5722, depart_planet="Earth", arrive_planet="Mygeeto", depart_time="10:00 PM", arrive_time="12:00 PM", flight_time=14, price=320, depart_or_return="depart")
f54 = Flight(flight_num=5724, depart_planet="Earth", arrive_planet="Mygeeto", depart_time="01:00 AM", arrive_time="03:00 PM", flight_time=14, price=320, depart_or_return="depart")

f55 = Flight(flight_num=5723, depart_planet="Mygeeto", arrive_planet="Earth", depart_time="02:00 PM", arrive_time="04:00 AM", flight_time=14, price=320, depart_or_return="return")
f56 = Flight(flight_num=5725, depart_planet="Mygeeto", arrive_planet="Earth", depart_time="05:00 PM", arrive_time="07:00 AM", flight_time=14, price=320, depart_or_return="return")

# Bespin
f57 = Flight(flight_num=5732, depart_planet="Earth", arrive_planet="Bespin", depart_time="04:00 PM", arrive_time="08:00 AM", flight_time=16, price=390, depart_or_return="depart")
f58 = Flight(flight_num=5734, depart_planet="Earth", arrive_planet="Bespin", depart_time="06:00 PM", arrive_time="10:00 AM", flight_time=16, price=390, depart_or_return="depart")
f59 = Flight(flight_num=5736, depart_planet="Earth", arrive_planet="Bespin", depart_time="08:00 PM", arrive_time="12:00 PM", flight_time=16, price=390, depart_or_return="depart")
f60 = Flight(flight_num=5738, depart_planet="Earth", arrive_planet="Bespin", depart_time="10:00 AM", arrive_time="02:00 PM", flight_time=16, price=390, depart_or_return="depart")

f61 = Flight(flight_num=5733, depart_planet="Bespin", arrive_planet="Earth", depart_time="01:30 PM", arrive_time="05:30 AM", flight_time=16, price=390, depart_or_return="return")
f62 = Flight(flight_num=5735, depart_planet="Bespin", arrive_planet="Earth", depart_time="03:30 PM", arrive_time="07:30 AM", flight_time=16, price=390, depart_or_return="return")
f63 = Flight(flight_num=5737, depart_planet="Bespin", arrive_planet="Earth", depart_time="05:30 PM", arrive_time="09:30 AM", flight_time=16, price=390, depart_or_return="return")
f64 = Flight(flight_num=5739, depart_planet="Bespin", arrive_planet="Earth", depart_time="07:30 PM", arrive_time="11:30 AM", flight_time=16, price=390, depart_or_return="return")

# Hoth
f65 = Flight(flight_num=5742, depart_planet="Earth", arrive_planet="Hoth", depart_time="05:00 PM", arrive_time="09:00 AM", flight_time=16, price=390, depart_or_return="depart")
f66 = Flight(flight_num=5744, depart_planet="Earth", arrive_planet="Hoth", depart_time="07:00 PM", arrive_time="11:00 AM", flight_time=16, price=390, depart_or_return="depart")
f67 = Flight(flight_num=5746, depart_planet="Earth", arrive_planet="Hoth", depart_time="09:00 PM", arrive_time="01:00 PM", flight_time=16, price=390, depart_or_return="depart")
f68 = Flight(flight_num=5748, depart_planet="Earth", arrive_planet="Hoth", depart_time="11:00 PM", arrive_time="03:00 PM", flight_time=16, price=390, depart_or_return="depart")

f69 = Flight(flight_num=5743, depart_planet="Hoth", arrive_planet="Earth", depart_time="01:45 PM", arrive_time="05:45 AM", flight_time=16, price=390, depart_or_return="return")
f70 = Flight(flight_num=5745, depart_planet="Hoth", arrive_planet="Earth", depart_time="03:45 PM", arrive_time="07:45 AM", flight_time=16, price=390, depart_or_return="return")
f71 = Flight(flight_num=5747, depart_planet="Hoth", arrive_planet="Earth", depart_time="05:45 PM", arrive_time="09:45 AM", flight_time=16, price=390, depart_or_return="return")
f72 = Flight(flight_num=5749, depart_planet="Hoth", arrive_planet="Earth", depart_time="07:45 PM", arrive_time="11:45 AM", flight_time=16, price=390, depart_or_return="return")

# Polis Massa
f73 = Flight(flight_num=5752, depart_planet="Earth", arrive_planet="Polis Massa", depart_time="01:00 PM", arrive_time="06:00 AM", flight_time=17, price=425, depart_or_return="depart")
f74 = Flight(flight_num=5754, depart_planet="Earth", arrive_planet="Polis Massa", depart_time="04:00 PM", arrive_time="09:00 AM", flight_time=17, price=425, depart_or_return="depart")
f75 = Flight(flight_num=5756, depart_planet="Earth", arrive_planet="Polis Massa", depart_time="07:00 PM", arrive_time="12:00 PM", flight_time=17, price=425, depart_or_return="depart")
f76 = Flight(flight_num=5758, depart_planet="Earth", arrive_planet="Polis Massa", depart_time="10:00 PM", arrive_time="03:00 PM", flight_time=17, price=425, depart_or_return="depart")

f77 = Flight(flight_num=5753, depart_planet="Polis Massa", arrive_planet="Earth", depart_time="01:00 PM", arrive_time="06:00 AM", flight_time=17, price=425, depart_or_return="return")
f78 = Flight(flight_num=5755, depart_planet="Polis Massa", arrive_planet="Earth", depart_time="04:00 PM", arrive_time="09:00 AM", flight_time=17, price=425, depart_or_return="return")
f79 = Flight(flight_num=5757, depart_planet="Polis Massa", arrive_planet="Earth", depart_time="07:00 PM", arrive_time="12:00 PM", flight_time=17, price=425, depart_or_return="return")
f80 = Flight(flight_num=5759, depart_planet="Polis Massa", arrive_planet="Earth", depart_time="10:00 PM", arrive_time="03:00 PM", flight_time=17, price=425, depart_or_return="return")

# Mustafar
f81 = Flight(flight_num=5762, depart_planet="Earth", arrive_planet="Mustafar", depart_time="02:30 PM", arrive_time="08:30 AM", flight_time=18, price=460, depart_or_return="depart")
f82 = Flight(flight_num=5764, depart_planet="Earth", arrive_planet="Mustafar", depart_time="04:30 PM", arrive_time="10:30 AM", flight_time=18, price=460, depart_or_return="depart")
f83 = Flight(flight_num=5766, depart_planet="Earth", arrive_planet="Mustafar", depart_time="06:30 PM", arrive_time="12:30 PM", flight_time=18, price=460, depart_or_return="depart")
f84 = Flight(flight_num=5768, depart_planet="Earth", arrive_planet="Mustafar", depart_time="08:30 PM", arrive_time="02:30 PM", flight_time=18, price=460, depart_or_return="depart")

f85 = Flight(flight_num=5763, depart_planet="Mustafar", arrive_planet="Earth", depart_time="11:30 AM", arrive_time="05:30 AM", flight_time=18, price=460, depart_or_return="return")
f86 = Flight(flight_num=5765, depart_planet="Mustafar", arrive_planet="Earth", depart_time="01:30 PM", arrive_time="07:30 AM", flight_time=18, price=460, depart_or_return="return")
f87 = Flight(flight_num=5767, depart_planet="Mustafar", arrive_planet="Earth", depart_time="03:30 PM", arrive_time="09:30 AM", flight_time=18, price=460, depart_or_return="return")
f88 = Flight(flight_num=5769, depart_planet="Mustafar", arrive_planet="Earth", depart_time="05:30 PM", arrive_time="11:30 AM", flight_time=18, price=460, depart_or_return="return")

# Dagobah
f89 = Flight(flight_num=5772, depart_planet="Earth", arrive_planet="Dagobah", depart_time="05:00 PM", arrive_time="12:00 PM", flight_time=19, price=495, depart_or_return="depart")
f90 = Flight(flight_num=5774, depart_planet="Earth", arrive_planet="Dagobah", depart_time="08:00 PM", arrive_time="03:00 PM", flight_time=19, price=495, depart_or_return="depart")

f91 = Flight(flight_num=5773, depart_planet="Dagobah", arrive_planet="Earth", depart_time="12:45 PM", arrive_time="07:45 AM", flight_time=19, price=495, depart_or_return="return")
f92 = Flight(flight_num=5775, depart_planet="Dagobah", arrive_planet="Earth", depart_time="05:45 PM", arrive_time="12:45 PM", flight_time=19, price=495, depart_or_return="return")

# Utapau
f93 = Flight(flight_num=5782, depart_planet="Earth", arrive_planet="Utapau", depart_time="03:00 PM", arrive_time="11:00 AM", flight_time=20, price=530, depart_or_return="depart")
f94 = Flight(flight_num=5784, depart_planet="Earth", arrive_planet="Utapau", depart_time="07:00 PM", arrive_time="03:00 PM", flight_time=20, price=530, depart_or_return="depart")

f95 = Flight(flight_num=5783, depart_planet="Utapau", arrive_planet="Earth", depart_time="05:00 PM", arrive_time="01:00 PM", flight_time=20, price=530, depart_or_return="return")
f96 = Flight(flight_num=5785, depart_planet="Utapau", arrive_planet="Earth", depart_time="10:00 PM", arrive_time="06:00 PM", flight_time=20, price=530, depart_or_return="return")

# Kashyyyk
f97 = Flight(flight_num=5792, depart_planet="Earth", arrive_planet="Kashyyyk", depart_time="03:45 PM", arrive_time="08:45 AM", flight_time=17, price=425, depart_or_return="depart")
f98 = Flight(flight_num=5794, depart_planet="Earth", arrive_planet="Kashyyyk", depart_time="06:45 PM", arrive_time="11:45 AM", flight_time=17, price=425, depart_or_return="depart")
f99 = Flight(flight_num=5796, depart_planet="Earth", arrive_planet="Kashyyyk", depart_time="08:45 PM", arrive_time="01:45 PM", flight_time=17, price=425, depart_or_return="depart")
f100 = Flight(flight_num=5798, depart_planet="Earth", arrive_planet="Kashyyyk", depart_time="10:45 PM", arrive_time="03:45 PM", flight_time=17, price=425, depart_or_return="depart")

f101 = Flight(flight_num=5793, depart_planet="Kashyyyk", arrive_planet="Earth", depart_time="10:45 AM", arrive_time="03:45 AM", flight_time=17, price=425, depart_or_return="return")
f102 = Flight(flight_num=5795, depart_planet="Kashyyyk", arrive_planet="Earth", depart_time="01:45 PM", arrive_time="06:45 AM", flight_time=17, price=425, depart_or_return="return")
f103 = Flight(flight_num=5797, depart_planet="Kashyyyk", arrive_planet="Earth", depart_time="04:45 PM", arrive_time="09:45 AM", flight_time=17, price=425, depart_or_return="return")
f104 = Flight(flight_num=5799, depart_planet="Kashyyyk", arrive_planet="Earth", depart_time="07:45 PM", arrive_time="12:45 PM", flight_time=17, price=425, depart_or_return="return")

# Yavin IV
f105 = Flight(flight_num=5802, depart_planet="Earth", arrive_planet="Yavin IV", depart_time="03:00 PM", arrive_time="10:00 AM", flight_time=19, price=495, depart_or_return="depart")
f106 = Flight(flight_num=5804, depart_planet="Earth", arrive_planet="Yavin IV", depart_time="05:00 PM", arrive_time="12:00 PM", flight_time=19, price=495, depart_or_return="depart")
f107 = Flight(flight_num=5806, depart_planet="Earth", arrive_planet="Yavin IV", depart_time="07:00 PM", arrive_time="02:00 PM", flight_time=19, price=495, depart_or_return="depart")
f108 = Flight(flight_num=5808, depart_planet="Earth", arrive_planet="Yavin IV", depart_time="09:00 PM", arrive_time="04:00 PM", flight_time=19, price=495, depart_or_return="depart")

f109 = Flight(flight_num=5803, depart_planet="Yavin IV", arrive_planet="Earth", depart_time="12:00 PM", arrive_time="07:00 AM", flight_time=19, price=495, depart_or_return="return")
f110 = Flight(flight_num=5805, depart_planet="Yavin IV", arrive_planet="Earth", depart_time="03:00 PM", arrive_time="10:00 AM", flight_time=19, price=495, depart_or_return="return")
f111 = Flight(flight_num=5807, depart_planet="Yavin IV", arrive_planet="Earth", depart_time="06:00 PM", arrive_time="01:00 PM", flight_time=19, price=495, depart_or_return="return")
f112 = Flight(flight_num=5809, depart_planet="Yavin IV", arrive_planet="Earth", depart_time="09:00 PM", arrive_time="04:00 PM", flight_time=19, price=495, depart_or_return="return")

# Naboo
f113 = Flight(flight_num=5812, depart_planet="Earth", arrive_planet="Naboo", depart_time="11:00 AM", arrive_time="08:00 AM", flight_time=21, price=565, depart_or_return="depart")
f114 = Flight(flight_num=5814, depart_planet="Earth", arrive_planet="Naboo", depart_time="01:00 PM", arrive_time="10:00 AM", flight_time=21, price=565, depart_or_return="depart")
f115 = Flight(flight_num=5816, depart_planet="Earth", arrive_planet="Naboo", depart_time="03:00 PM", arrive_time="12:00 PM", flight_time=21, price=565, depart_or_return="depart")
f116 = Flight(flight_num=5818, depart_planet="Earth", arrive_planet="Naboo", depart_time="05:00 PM", arrive_time="02:00 PM", flight_time=21, price=565, depart_or_return="depart")

f117 = Flight(flight_num=5813, depart_planet="Naboo", arrive_planet="Earth", depart_time="02:00 PM", arrive_time="11:00 AM", flight_time=21, price=565, depart_or_return="return")
f118 = Flight(flight_num=5815, depart_planet="Naboo", arrive_planet="Earth", depart_time="04:00 PM", arrive_time="01:00 PM", flight_time=21, price=565, depart_or_return="return")
f119 = Flight(flight_num=5817, depart_planet="Naboo", arrive_planet="Earth", depart_time="06:00 PM", arrive_time="03:00 PM", flight_time=21, price=565, depart_or_return="return")
f120 = Flight(flight_num=5819, depart_planet="Naboo", arrive_planet="Earth", depart_time="08:00 PM", arrive_time="05:00 PM", flight_time=21, price=565, depart_or_return="return")

# Tatooine
f121 = Flight(flight_num=5822, depart_planet="Earth", arrive_planet="Tatooine", depart_time="08:00 AM", arrive_time="08:00 AM", flight_time=24, price=670, depart_or_return="depart")
f122 = Flight(flight_num=5824, depart_planet="Earth", arrive_planet="Tatooine", depart_time="10:00 AM", arrive_time="10:00 AM", flight_time=24, price=670, depart_or_return="depart")
f123 = Flight(flight_num=5826, depart_planet="Earth", arrive_planet="Tatooine", depart_time="12:00 PM", arrive_time="12:00 PM", flight_time=24, price=670, depart_or_return="depart")
f124 = Flight(flight_num=5828, depart_planet="Earth", arrive_planet="Tatooine", depart_time="02:00 PM", arrive_time="02:00 PM", flight_time=24, price=670, depart_or_return="depart")

f125 = Flight(flight_num=5823, depart_planet="Tatooine", arrive_planet="Earth", depart_time="12:00 PM", arrive_time="12:00 PM", flight_time=24, price=670, depart_or_return="return")
f126 = Flight(flight_num=5825, depart_planet="Tatooine", arrive_planet="Earth", depart_time="03:00 PM", arrive_time="03:00 PM", flight_time=24, price=670, depart_or_return="return")
f127 = Flight(flight_num=5827, depart_planet="Tatooine", arrive_planet="Earth", depart_time="05:00 PM", arrive_time="05:00 PM", flight_time=24, price=670, depart_or_return="return")
f128 = Flight(flight_num=5829, depart_planet="Tatooine", arrive_planet="Earth", depart_time="08:00 PM", arrive_time="08:00 PM", flight_time=24, price=670, depart_or_return="return")

# Geonosis
f129 = Flight(flight_num=5832, depart_planet="Earth", arrive_planet="Geonosis", depart_time="08:45 AM", arrive_time="08:45 AM", flight_time=24, price=670, depart_or_return="depart")
f130 = Flight(flight_num=5834, depart_planet="Earth", arrive_planet="Geonosis", depart_time="10:45 AM", arrive_time="10:45 AM", flight_time=24, price=670, depart_or_return="depart")
f131 = Flight(flight_num=5836, depart_planet="Earth", arrive_planet="Geonosis", depart_time="12:45 PM", arrive_time="12:45 PM", flight_time=24, price=670, depart_or_return="depart")
f132 = Flight(flight_num=5838, depart_planet="Earth", arrive_planet="Geonosis", depart_time="02:45 PM", arrive_time="02:45 PM", flight_time=24, price=670, depart_or_return="depart")

f133 = Flight(flight_num=5833, depart_planet="Geonosis", arrive_planet="Earth", depart_time="02:45 PM", arrive_time="02:45 PM", flight_time=24, price=670, depart_or_return="return")
f134 = Flight(flight_num=5835, depart_planet="Geonosis", arrive_planet="Earth", depart_time="03:45 PM", arrive_time="03:45 PM", flight_time=24, price=670, depart_or_return="return")
f135 = Flight(flight_num=5837, depart_planet="Geonosis", arrive_planet="Earth", depart_time="05:45 PM", arrive_time="05:45 PM", flight_time=24, price=670, depart_or_return="return")
f136 = Flight(flight_num=5839, depart_planet="Geonosis", arrive_planet="Earth", depart_time="07:45 PM", arrive_time="07:45 PM", flight_time=24, price=670, depart_or_return="return")

# Felucia
f137 = Flight(flight_num=5842, depart_planet="Earth", arrive_planet="Felucia", depart_time="08:30 AM", arrive_time="08:30 AM", flight_time=24, price=670, depart_or_return="depart")
f138 = Flight(flight_num=5844, depart_planet="Earth", arrive_planet="Felucia", depart_time="10:30 AM", arrive_time="10:30 AM", flight_time=24, price=670, depart_or_return="depart")
f139 = Flight(flight_num=5846, depart_planet="Earth", arrive_planet="Felucia", depart_time="12:30 PM", arrive_time="12:30 PM", flight_time=24, price=670, depart_or_return="depart")
f140 = Flight(flight_num=5848, depart_planet="Earth", arrive_planet="Felucia", depart_time="02:30 PM", arrive_time="02:30 PM", flight_time=24, price=670, depart_or_return="depart")

f141 = Flight(flight_num=5843, depart_planet="Felucia", arrive_planet="Earth", depart_time="12:00 PM", arrive_time="12:00 PM", flight_time=24, price=670, depart_or_return="return")
f142 = Flight(flight_num=5845, depart_planet="Felucia", arrive_planet="Earth", depart_time="02:00 PM", arrive_time="02:00 PM", flight_time=24, price=670, depart_or_return="return")
f143 = Flight(flight_num=5847, depart_planet="Felucia", arrive_planet="Earth", depart_time="04:00 PM", arrive_time="04:00 PM", flight_time=24, price=670, depart_or_return="return")
f144 = Flight(flight_num=5849, depart_planet="Felucia", arrive_planet="Earth", depart_time="06:00 PM", arrive_time="06:00 PM", flight_time=24, price=670, depart_or_return="return")

# Cato Neimoidia
f145 = Flight(flight_num=5852, depart_planet="Earth", arrive_planet="Cato Neimoidia", depart_time="06:00 PM", arrive_time="09:00 AM", flight_time=15, price=355, depart_or_return="depart")
f146 = Flight(flight_num=5854, depart_planet="Earth", arrive_planet="Cato Neimoidia", depart_time="08:00 PM", arrive_time="11:00 AM", flight_time=15, price=355, depart_or_return="depart")
f147 = Flight(flight_num=5856, depart_planet="Earth", arrive_planet="Cato Neimoidia", depart_time="10:00 PM", arrive_time="01:00 PM", flight_time=15, price=355, depart_or_return="depart")
f148 = Flight(flight_num=5858, depart_planet="Earth", arrive_planet="Cato Neimoidia", depart_time="12:00 AM", arrive_time="03:00 PM", flight_time=15, price=355, depart_or_return="depart")

f149 = Flight(flight_num=5853, depart_planet="Cato Neimoidia", arrive_planet="Earth", depart_time="01:00 PM", arrive_time="04:00 AM", flight_time=15, price=355, depart_or_return="return")
f150 = Flight(flight_num=5855, depart_planet="Cato Neimoidia", arrive_planet="Earth", depart_time="03:00 PM", arrive_time="06:00 AM", flight_time=15, price=355, depart_or_return="return")
f151 = Flight(flight_num=5857, depart_planet="Cato Neimoidia", arrive_planet="Earth", depart_time="05:00 PM", arrive_time="08:00 AM", flight_time=15, price=355, depart_or_return="return")
f152 = Flight(flight_num=5859, depart_planet="Cato Neimoidia", arrive_planet="Earth", depart_time="07:00 PM", arrive_time="10:00 AM", flight_time=15, price=355, depart_or_return="return")

# Kamino
f153 = Flight(flight_num=5862, depart_planet="Earth", arrive_planet="Kamino", depart_time="06:30 AM", arrive_time="07:30 AM", flight_time=25, price=705, depart_or_return="depart")
f154 = Flight(flight_num=5864, depart_planet="Earth", arrive_planet="Kamino", depart_time="08:30 AM", arrive_time="09:30 AM", flight_time=25, price=705, depart_or_return="depart")
f155 = Flight(flight_num=5866, depart_planet="Earth", arrive_planet="Kamino", depart_time="10:30 AM", arrive_time="11:30 AM", flight_time=25, price=705, depart_or_return="depart")
f156 = Flight(flight_num=5868, depart_planet="Earth", arrive_planet="Kamino", depart_time="12:30 PM", arrive_time="01:30 PM", flight_time=25, price=705, depart_or_return="depart")

f157 = Flight(flight_num=5863, depart_planet="Kamino", arrive_planet="Earth", depart_time="01:00 PM", arrive_time="02:00 PM", flight_time=25, price=705, depart_or_return="return")
f158 = Flight(flight_num=5865, depart_planet="Kamino", arrive_planet="Earth", depart_time="03:00 PM", arrive_time="04:00 PM", flight_time=25, price=705, depart_or_return="return")
f159 = Flight(flight_num=5867, depart_planet="Kamino", arrive_planet="Earth", depart_time="05:00 PM", arrive_time="06:00 PM", flight_time=25, price=705, depart_or_return="return")
f160 = Flight(flight_num=5869, depart_planet="Kamino", arrive_planet="Earth", depart_time="07:00 PM", arrive_time="08:00 PM", flight_time=25, price=705, depart_or_return="return")

# Scarif
f161 = Flight(flight_num=5872, depart_planet="Earth", arrive_planet="Scarif", depart_time="07:30 AM", arrive_time="08:30 AM", flight_time=25, price=705, depart_or_return="depart")
f162 = Flight(flight_num=5874, depart_planet="Earth", arrive_planet="Scarif", depart_time="09:30 AM", arrive_time="10:30 AM", flight_time=25, price=705, depart_or_return="depart")
f163 = Flight(flight_num=5876, depart_planet="Earth", arrive_planet="Scarif", depart_time="11:30 AM", arrive_time="12:30 PM", flight_time=25, price=705, depart_or_return="depart")
f164 = Flight(flight_num=5878, depart_planet="Earth", arrive_planet="Scarif", depart_time="01:30 PM", arrive_time="02:30 PM", flight_time=25, price=705, depart_or_return="depart")

f165 = Flight(flight_num=5873, depart_planet="Scarif", arrive_planet="Earth", depart_time="12:30 PM", arrive_time="01:30 PM", flight_time=25, price=705, depart_or_return="return")
f166 = Flight(flight_num=5875, depart_planet="Scarif", arrive_planet="Earth", depart_time="02:30 PM", arrive_time="03:30 PM", flight_time=25, price=705, depart_or_return="return")
f167 = Flight(flight_num=5877, depart_planet="Scarif", arrive_planet="Earth", depart_time="04:30 PM", arrive_time="05:30 PM", flight_time=25, price=705, depart_or_return="return")
f168 = Flight(flight_num=5879, depart_planet="Scarif", arrive_planet="Earth", depart_time="06:30 PM", arrive_time="07:30 PM", flight_time=25, price=705, depart_or_return="return")

db.session.add_all([f1, 
f2, 
f3, 
f4, 
f5, 
f6, 
f7, 
f8, 
f9, 
f10, 
f11, 
f12, 
f13, 
f14, 
f15, 
f16, 
f17, 
f18, 
f19, 
f20, 
f21, 
f22, 
f23, 
f24, 
f25, 
f26, 
f27, 
f28, 
f29, 
f30, 
f31, 
f32, 
f33, 
f34, 
f35, 
f36, 
f37, 
f38,
f37,
f38,
f39,
f40,
f41,
f42,
f43,
f44,
f45,
f46,
f47,
f48,
f49,
f50,
f51,
f52,
f53,
f54,
f55,
f56,
f57,
f58,
f59,
f60,
f61,
f62,
f63,
f64,
f65,
f66,
f67,
f68,
f69,
f70,
f71,
f72,
f73,
f74,
f75,
f76,
f77,
f78,
f79,
f80,
f81,
f82,
f83,
f84,
f85,
f86,
f87,
f88,
f89,
f90,
f91,
f92,
f93,
f94,
f95,
f96,
f97,
f98,
f99,
f100,
f101,
f102,
f103,
f104,
f105,
f106,
f107,
f108,
f109,
f110,
f111,
f112,
f113,
f114,
f115,
f116,
f117,
f118,
f119,
f120,
f121,
f122,
f123,
f124,
f125,
f126,
f127,
f128,
f129,
f130,
f131,
f132,
f133,
f134,
f135,
f136,
f137,
f138,
f139,
f140,
f141,
f142,
f143,
f144,
f145,
f146,
f147,
f148,
f149,
f150,
f151,
f152,
f153,
f154,
f155,
f156,
f157,
f158,
f159,
f160,
f161,
f162,
f163,
f164,
f165,
f166,
f167,
f168])
db.session.commit()

# Adding a user

me = User.signup(email, username, password, first, last)

db.session.add(me)
db.session.commit()

# Adding an itinerary

itin = Itinerary(user_id=me.id)
db.session.add(itin)
db.session.commit()

d_flight_dates = FlightDate(depart_date='2020-09-30', arrive_date=set_arrive_end_date('2020-09-30', f1.depart_time, f1.flight_time), flight_num=f1.flight_num, itinerary_id=itin.id)

r_flight_dates = FlightDate(depart_date='2020-10-15', arrive_date=set_arrive_end_date('2020-10-15', f2.depart_time, f2.flight_time), flight_num=f2.flight_num, itinerary_id=itin.id)

itin.flights.append(f1)
itin.flights.append(f2)

t17_dates = TourDate(start_date='2020-10-05', end_date=set_arrive_end_date('2020-10-05', t17.start_time, t17.duration), tour_id=t17.id, itinerary_id=itin.id)

t18_dates = TourDate(start_date='2020-10-10', end_date=set_arrive_end_date('2020-10-10', t18.start_time, t18.duration), tour_id=t18.id, itinerary_id=itin.id)

itin.tours.append(t17)
itin.tours.append(t18)

db.session.add_all([d_flight_dates, r_flight_dates, t17_dates, t18_dates])
db.session.commit()

itin.planets.append(Planet.query.get("Coruscant"))

itin.start_date = d_flight_dates.depart_date
itin.end_date = r_flight_dates.arrive_date
itin.start_time = f1.depart_time
itin.end_time = f2.arrive_time
itin.total = 630

db.session.commit()