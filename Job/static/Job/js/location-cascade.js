(function () {
    var LOCATION_DATA = {
        "India": {
            "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Gandhinagar"],
            "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Thane"],
            "Karnataka": ["Bengaluru", "Mysuru", "Mangaluru", "Hubli", "Belagavi"],
            "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem"],
            "Delhi": ["New Delhi", "Dwarka", "Rohini", "Saket", "Karol Bagh"],
            "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Kota", "Ajmer"],
            "Uttar Pradesh": ["Lucknow", "Kanpur", "Noida", "Varanasi", "Agra"],
            "West Bengal": ["Kolkata", "Howrah", "Durgapur", "Siliguri", "Asansol"],
            "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Karimnagar", "Khammam"],
            "Kerala": ["Kochi", "Thiruvananthapuram", "Kozhikode", "Thrissur", "Kollam"]
        },
        "United States": {
            "California": ["Los Angeles", "San Francisco", "San Diego", "San Jose", "Sacramento"],
            "Texas": ["Houston", "Dallas", "Austin", "San Antonio", "Fort Worth"],
            "New York": ["New York City", "Buffalo", "Rochester", "Albany", "Syracuse"],
            "Florida": ["Miami", "Orlando", "Tampa", "Jacksonville", "Tallahassee"],
            "Illinois": ["Chicago", "Aurora", "Naperville", "Springfield", "Peoria"],
            "Washington": ["Seattle", "Spokane", "Tacoma", "Bellevue", "Olympia"],
            "Massachusetts": ["Boston", "Cambridge", "Worcester", "Springfield", "Lowell"],
            "Georgia": ["Atlanta", "Savannah", "Augusta", "Athens", "Macon"],
            "Colorado": ["Denver", "Boulder", "Colorado Springs", "Aurora", "Fort Collins"],
            "Arizona": ["Phoenix", "Tucson", "Mesa", "Scottsdale", "Tempe"]
        },
        "United Kingdom": {
            "England": ["London", "Manchester", "Birmingham", "Liverpool", "Leeds"],
            "Scotland": ["Edinburgh", "Glasgow", "Aberdeen", "Dundee", "Inverness"],
            "Wales": ["Cardiff", "Swansea", "Newport", "Wrexham", "Bangor"],
            "Northern Ireland": ["Belfast", "Derry", "Lisburn", "Newry", "Armagh"],
            "Greater London": ["Westminster", "Camden", "Greenwich", "Croydon", "Harrow"],
            "West Midlands": ["Birmingham", "Coventry", "Wolverhampton", "Dudley", "Solihull"],
            "North West": ["Manchester", "Liverpool", "Chester", "Preston", "Blackpool"],
            "Yorkshire": ["Leeds", "Sheffield", "York", "Bradford", "Hull"],
            "South East": ["Brighton", "Reading", "Oxford", "Southampton", "Canterbury"],
            "South West": ["Bristol", "Bath", "Plymouth", "Exeter", "Bournemouth"]
        },
        "Canada": {
            "Ontario": ["Toronto", "Ottawa", "Mississauga", "Hamilton", "London"],
            "Quebec": ["Montreal", "Quebec City", "Laval", "Gatineau", "Longueuil"],
            "British Columbia": ["Vancouver", "Victoria", "Surrey", "Burnaby", "Richmond"],
            "Alberta": ["Calgary", "Edmonton", "Red Deer", "Lethbridge", "Banff"],
            "Manitoba": ["Winnipeg", "Brandon", "Steinbach", "Thompson", "Portage la Prairie"],
            "Saskatchewan": ["Saskatoon", "Regina", "Prince Albert", "Moose Jaw", "Swift Current"],
            "Nova Scotia": ["Halifax", "Sydney", "Dartmouth", "Truro", "Yarmouth"],
            "New Brunswick": ["Saint John", "Moncton", "Fredericton", "Dieppe", "Miramichi"],
            "Newfoundland and Labrador": ["St. John's", "Corner Brook", "Gander", "Mount Pearl", "Happy Valley"],
            "Prince Edward Island": ["Charlottetown", "Summerside", "Stratford", "Cornwall", "Montague"]
        },
        "Australia": {
            "New South Wales": ["Sydney", "Newcastle", "Wollongong", "Parramatta", "Canberra"],
            "Victoria": ["Melbourne", "Geelong", "Ballarat", "Bendigo", "Frankston"],
            "Queensland": ["Brisbane", "Gold Coast", "Cairns", "Townsville", "Toowoomba"],
            "Western Australia": ["Perth", "Fremantle", "Bunbury", "Geraldton", "Albany"],
            "South Australia": ["Adelaide", "Mount Gambier", "Whyalla", "Murray Bridge", "Port Lincoln"],
            "Tasmania": ["Hobart", "Launceston", "Devonport", "Burnie", "Kingston"],
            "Australian Capital Territory": ["Canberra", "Belconnen", "Gungahlin", "Tuggeranong", "Woden"],
            "Northern Territory": ["Darwin", "Alice Springs", "Palmerston", "Katherine", "Nhulunbuy"],
            "Sunshine Coast": ["Maroochydore", "Caloundra", "Noosa", "Nambour", "Mooloolaba"],
            "Hunter Region": ["Newcastle", "Maitland", "Cessnock", "Singleton", "Muswellbrook"]
        },
        "Germany": {
            "Bavaria": ["Munich", "Nuremberg", "Augsburg", "Regensburg", "Ingolstadt"],
            "Berlin": ["Mitte", "Charlottenburg", "Kreuzberg", "Spandau", "Pankow"],
            "Hamburg": ["Altona", "Eimsbüttel", "Harburg", "Wandsbek", "Bergedorf"],
            "Hesse": ["Frankfurt", "Wiesbaden", "Darmstadt", "Kassel", "Offenbach"],
            "North Rhine-Westphalia": ["Cologne", "Düsseldorf", "Dortmund", "Essen", "Bonn"],
            "Baden-Württemberg": ["Stuttgart", "Mannheim", "Karlsruhe", "Freiburg", "Heidelberg"],
            "Saxony": ["Dresden", "Leipzig", "Chemnitz", "Zwickau", "Meissen"],
            "Lower Saxony": ["Hanover", "Braunschweig", "Oldenburg", "Osnabrück", "Göttingen"],
            "Rhineland-Palatinate": ["Mainz", "Ludwigshafen", "Koblenz", "Trier", "Kaiserslautern"],
            "Schleswig-Holstein": ["Kiel", "Lübeck", "Flensburg", "Neumünster", "Norderstedt"]
        },
        "Singapore": {
            "Central Region": ["Downtown Core", "Orchard", "Marina Bay", "Rochor", "Newton"],
            "East Region": ["Bedok", "Tampines", "Pasir Ris", "Changi", "Marine Parade"],
            "North Region": ["Woodlands", "Yishun", "Sembawang", "Mandai", "Admiralty"],
            "North-East Region": ["Hougang", "Sengkang", "Punggol", "Serangoon", "Ang Mo Kio"],
            "West Region": ["Jurong East", "Jurong West", "Clementi", "Bukit Batok", "Choa Chu Kang"],
            "South Region": ["HarbourFront", "Sentosa", "Telok Blangah", "Bukit Merah", "Queenstown"],
            "Downtown": ["Raffles Place", "Tanjong Pagar", "Chinatown", "Bugis", "City Hall"],
            "Jurong": ["Jurong Island", "Boon Lay", "Pioneer", "Tuas", "Gul Circle"],
            "Changi": ["Changi Airport", "Changi Business Park", "Changi Village", "Loyang", "Expo"],
            "Woodlands Zone": ["Woodlands Central", "Marsiling", "Woodlands North", "Woodlands South", "Woodlands East"]
        },
        "United Arab Emirates": {
            "Dubai": ["Downtown Dubai", "Marina", "Jumeirah", "Deira", "Business Bay"],
            "Abu Dhabi": ["Al Reem Island", "Corniche", "Yas Island", "Khalifa City", "Al Ain"],
            "Sharjah": ["Al Majaz", "Al Nahda", "Muwaileh", "University City", "Al Qasimia"],
            "Ajman": ["Ajman Corniche", "Al Nuaimiya", "Al Rashidiya", "Al Jurf", "Al Mowaihat"],
            "Ras Al Khaimah": ["Al Hamra", "Al Nakheel", "Al Qusaidat", "Al Dhait", "Mina Al Arab"],
            "Fujairah": ["Fujairah City", "Dibba", "Mirbah", "Sakamkam", "Al Faseel"],
            "Umm Al Quwain": ["UAQ City", "Al Raas", "Falaj Al Mualla", "Al Salamah", "Al Ramlah"],
            "Al Ain Region": ["Al Jimi", "Al Mutaredh", "Zakher", "Hili", "Al Foah"],
            "Northern Emirates": ["Dhaid", "Kalba", "Khor Fakkan", "Masafi", "Hatta"],
            "Western Region": ["Madinat Zayed", "Ruwais", "Liwa", "Ghayathi", "Mirfa"]
        },
        "Japan": {
            "Tokyo": ["Shibuya", "Shinjuku", "Minato", "Chiyoda", "Setagaya"],
            "Osaka": ["Osaka City", "Sakai", "Higashiosaka", "Toyonaka", "Suita"],
            "Kanagawa": ["Yokohama", "Kawasaki", "Sagamihara", "Yokosuka", "Kamakura"],
            "Aichi": ["Nagoya", "Toyota", "Okazaki", "Ichinomiya", "Toyohashi"],
            "Hokkaido": ["Sapporo", "Asahikawa", "Hakodate", "Obihiro", "Kushiro"],
            "Fukuoka": ["Fukuoka City", "Kitakyushu", "Kurume", "Omuta", "Iizuka"],
            "Kyoto": ["Kyoto City", "Uji", "Kameoka", "Maizuru", "Fukuchiyama"],
            "Hyogo": ["Kobe", "Himeji", "Nishinomiya", "Amagasaki", "Akashi"],
            "Saitama": ["Saitama City", "Kawaguchi", "Kawagoe", "Tokorozawa", "Koshigaya"],
            "Chiba": ["Chiba City", "Funabashi", "Matsudo", "Ichikawa", "Kashiwa"]
        },
        "France": {
            "Île-de-France": ["Paris", "Versailles", "Boulogne-Billancourt", "Saint-Denis", "Nanterre"],
            "Provence-Alpes-Côte d'Azur": ["Marseille", "Nice", "Toulon", "Aix-en-Provence", "Cannes"],
            "Auvergne-Rhône-Alpes": ["Lyon", "Grenoble", "Saint-Étienne", "Annecy", "Chambéry"],
            "Nouvelle-Aquitaine": ["Bordeaux", "Limoges", "Poitiers", "La Rochelle", "Pau"],
            "Occitanie": ["Toulouse", "Montpellier", "Nîmes", "Perpignan", "Carcassonne"],
            "Hauts-de-France": ["Lille", "Amiens", "Roubaix", "Tourcoing", "Calais"],
            "Grand Est": ["Strasbourg", "Reims", "Metz", "Nancy", "Mulhouse"],
            "Pays de la Loire": ["Nantes", "Angers", "Le Mans", "Saint-Nazaire", "Laval"],
            "Brittany": ["Rennes", "Brest", "Quimper", "Vannes", "Saint-Malo"],
            "Normandy": ["Rouen", "Caen", "Le Havre", "Cherbourg", "Évreux"]
        }
    };

    function fillSelect(select, placeholder, values, enable) {
        select.innerHTML = '';
        var first = document.createElement('option');
        first.value = '';
        first.textContent = placeholder;
        select.appendChild(first);
        (values || []).forEach(function (name) {
            var opt = document.createElement('option');
            opt.value = name;
            opt.textContent = name;
            select.appendChild(opt);
        });
        select.disabled = !enable;
        select.value = '';
    }

    function initLocationCascade() {
        var country = document.getElementById('locCountry');
        var state = document.getElementById('locState');
        var city = document.getElementById('locCity');
        if (!country || !state || !city || country.dataset.cascadeBound === '1') return;
        country.dataset.cascadeBound = '1';

        fillSelect(state, 'Select your state', [], false);
        fillSelect(city, 'Select your city', [], false);

        country.addEventListener('change', function () {
            var states = LOCATION_DATA[country.value]
                ? Object.keys(LOCATION_DATA[country.value])
                : [];
            fillSelect(state, 'Select your state', states, !!country.value);
            fillSelect(city, 'Select your city', [], false);
        });

        state.addEventListener('change', function () {
            var cities = (LOCATION_DATA[country.value] && LOCATION_DATA[country.value][state.value]) || [];
            fillSelect(city, 'Select your city', cities, !!state.value);
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initLocationCascade);
    } else {
        initLocationCascade();
    }
})();
