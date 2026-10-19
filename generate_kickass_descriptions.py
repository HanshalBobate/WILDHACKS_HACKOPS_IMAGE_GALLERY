#!/usr/bin/env python3
"""
generate_all_bespoke_descriptions.py
Generates 100% bespoke, individual, non-duplicate 2-3 line descriptions
for all 130 images in the WildID / WILDHACK 2K26 archive.

Ensures zero boilerplate repetition and strict alignment with the visual reality
of each photograph and the authentic narrative of Team HackOPs.
"""

import json
import csv
import os

JSON_FILE = "gallery_data.json"
JS_FILE = "js/gallery_data.js"
CSV_FILE = "image_descriptions.csv"

# Comprehensive, bespoke dictionary for ALL 130 images
ENTRIES = {
    # --- Category 1: Tadoba Dawn Canopy & Habitat Plates (001 - 007) ---
    "20261017_063919.jpg.jpeg": {
        "title": "Tadoba Dawn Canopy // Sector 4B Teak Light",
        "stage": "Landscape",
        "category": "wildlife",
        "claim": "Early morning light breaking through the dry deciduous teak canopy of Tadoba-Andhari. Sunlight pierces through the foliage, illuminating the woodland corridor where camera traps record wildlife movements. Captured during our field study, setting the environmental benchmark for natural forest illumination."
    },
    "20261017_063934.jpg.jpeg": {
        "title": "Forest Flank Corridor // Dappled Canopy Shadow",
        "stage": "Landscape",
        "category": "wildlife",
        "claim": "Dappled sunlight and sharp shadow patterns cast across the forest floor through dense teak foliage. This extreme contrast between direct sun and deep shade highlights a core optical challenge: preventing ambient light patterns from causing false edge detections on animal flanks. A foundational reference plate for robust animal segmentation."
    },
    "20261017_063944.jpg.jpeg": {
        "title": "Moharli Core Trail // Horizon Depth Vector",
        "stage": "Landscape",
        "category": "wildlife",
        "claim": "Looking outward through the dry teak forest corridor toward the morning horizon as mist clears. The rugged woodland terrain and dense branch layers demonstrate why automated vision must isolate animals cleanly from complex natural backgrounds. Served as our baseline reference for simulated habitat rendering."
    },
    "20261017_063954.jpg.jpeg": {
        "title": "Vertical Teak Silhouettes // Structural Geometry",
        "stage": "Landscape",
        "category": "wildlife",
        "claim": "Twin prominent teak trunks standing tall against the luminous morning sky, casting long linear shadows. In our Blender GroveScape simulations, we used these precise vertical tree silhouettes and branch densities to parametrically model realistic trunk occlusions for synthetic training scenes."
    },
    "20261017_063955.jpg.jpeg": {
        "title": "Teak Trunk Bifurcations // Natural Graph Topology",
        "stage": "Landscape",
        "category": "wildlife",
        "claim": "Intertwined forest trunks and natural branching photographed in the early hours near Moharli gate. The fractal branching of dry deciduous teak trees inspired our graph-based representation: treating fur stripe bifurcations as persistent topological nodes rather than rigid pixel grids."
    },
    "20261017_064014.jpg.jpeg": {
        "title": "Woodland Corridor View // Foreshortened Perspective",
        "stage": "Landscape",
        "category": "wildlife",
        "claim": "A perspective view through the forest corridor capturing angular foreshortening and foliage layering. When an animal turns or walks uphill, body perspective changes dramatically across stationary camera traps. This plate guided our parameter choices when evaluating pose-estimation under steep viewing angles."
    },
    "20261017_064022.jpg.jpeg": {
        "title": "The Living Forest // Epilogue Specimen Plate",
        "stage": "Landscape",
        "category": "wildlife",
        "claim": "Warm golden light bathing the forest floor through the teak canopy in a moment of quiet morning stillness. A fitting closing visual for our journey, reminding us that behind every biometric vector lies an ancient, living ecosystem. As the forest conservators reminded us: ‘The forest has a memory, and we are learning to read it.’"
    },

    # --- Category 2: WhatsApp Field & Event Chronicles (008 - 027) ---
    "IMG-20261016-WA0002(1).jpeg": {
        "title": "Rail Corridor Transit // Ballarpur Platform Tracks",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Looking down at the steel rails and stone ballast from the train coach upon arriving at the station. After traveling through the night from our college, the team gathered bags and prepared to head to the venue. The physical reality of our first offline hackathon was beginning."
    },
    "IMG-20261016-WA0002.jpeg": {
        "title": "Morning Chai & Biscuits // Transit Sustenance",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Morning tea cups and biscuit packs served on a metal tray aboard the passenger train. The four of us used this brief breakfast window to review our competition strategy and divide pipeline responsibilities before arriving in Ballarpur. Simple sustenance before 24 continuous hours of coding."
    },
    "IMG-20261016-WA0014.jpeg": {
        "title": "Auditorium Briefing // 30 Finalist Teams Assembled",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "The main auditorium at Ballarpur Institute of Technology during the opening briefing with university leadership and TATR officials. Over 120 participants from across India listened as problem statements and judging rubrics were officially presented. The 24-hour countdown clock was set to start."
    },
    "IMG-20261016-WA0016.jpeg": {
        "title": "Packed Desk Dinner // Silver Foil Meal Box",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "A steaming packed dinner in a silver foil container with a spoon, placed on our workstation desk next to running laptops. Taking brief pauses to eat right at the keyboard so development momentum remained uninterrupted. The authentic culinary reality of high-intensity hackathon sprints."
    },
    "IMG-20261016-WA0020.jpg": {
        "title": "Official Participant Badge // WILDHACK 2K26 Pass",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Holding the official participant identification badge and documentation issued by Ballarpur Institute of Technology. Carrying this pass made our presence tangible: Team HackOPs was officially competing in the offline conservation challenge. It was time to build what we had envisioned."
    },
    "IMG-20261016-WA0023.jpeg": {
        "title": "Hackathon Guidelines // Workstation Terminal Setup",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Workstation laptop screen displaying hackathon briefing rules, evaluation metrics, and local environment updates. Reviewing the judging criteria carefully to ensure our architecture addressed real-world reserve scalability. Preparing the local Git repo and checking GPU configurations before heavy model training."
    },
    "IMG-20261016-WA0027.jpeg": {
        "title": "Tiffin Dinner Station // Workstation Fuel & Watch",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "A tiffin meal tray on the desk alongside a wristwatch, water bottle, and mechanical keyboard. With time slipping past midnight, eating quickly while monitoring Blender background render queues became standard routine. Every minute saved was another minute dedicated to debugging model convergence."
    },
    "IMG-20261016-WA0030.jpeg": {
        "title": "Evening Fuel Container // Dal Curry on the Bench",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "A container of warm dal curry and rice on the team workbench during the evening development block. The organizers kept hot meals flowing to sustain teams through the marathon coding hours. A quick five-minute dinner before returning to pose-estimation coordinate mapping."
    },
    "IMG-20261016-WA0035.jpeg": {
        "title": "Three-Compartment Meal Tray // Sustaining the Sprint",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "A three-compartment food container holding rice, vegetable curry, and chapati on the development desk. Balancing code reviews with fast dinners as our multi-stage vision pipeline began taking shape. Sustenance that kept our team focused through exhaustion."
    },
    "IMG-20261016-WA0036.jpeg": {
        "title": "Coffee & Cookie Companion // Late Evening Push",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "A hot cup of coffee with a cookie wafer bar resting beside an open laptop keyboard during late evening development. Caffeine and quick snacks fueled our efforts as we tackled tiger segmentation boundary refinement. The quintessential companion of student developers working against the clock."
    },
    "IMG-20261017-WA0004.jpeg": {
        "title": "01:30 AM Pizza Break // Mid-Sprint Endurance",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "01:30 AM: Open pizza boxes with melted cheese slices spread across the table between open IDEs and terminal windows. Taking a rare shared laugh while recharging energy to conquer midnight GPU out-of-memory errors. The shared camaraderie that makes offline hackathons unforgettable."
    },
    "IMG-20261017-WA0006.jpeg": {
        "title": "Midnight Refreshment Tray // Overcoming 02:00 AM Fatigue",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "A refreshment tray with snacks and spoons set out near our coding bench during the early morning hours. When physical fatigue threatened to slow down progress, quick bites helped the four of us maintain mental clarity. Pushing through the most grueling stretch of the 24 hours."
    },
    "IMG-20261017-WA0010.jpg": {
        "title": "Biometric Screen Test // Multi-Angle Tiger Profiles",
        "stage": "Evidence",
        "category": "telemetry",
        "claim": "Morning prototype screen test displaying three distinct tiger sightings with varying postures and stripe densities. Verifying that our high-pass spatial filter extracted invariant stripe contours regardless of whether the animal was walking or standing. Validating model outputs on the laptop before dashboard integration."
    },
    "IMG-20261017-WA0011.jpg": {
        "title": "Candidate Sighting Evaluation // Re-ID Browser Test",
        "stage": "Evidence",
        "category": "telemetry",
        "claim": "Testing candidate sighting matching in the browser interface across three distinct field captures. The system compared the extracted flank patterns against our database to verify topological similarity. A critical validation checkpoint ensuring the prototype was stable for our upcoming jury presentation."
    },
    "IMG-20261017-WA0033.jpeg": {
        "title": "Post-Defense Grilled Sandwich // Exhilaration & Relief",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "A freshly grilled vegetable sandwich on a paper plate eaten right after concluding our 30-minute jury defense. The overwhelming relief of having demonstrated a functioning pipeline live on stage made every bite taste extraordinary. Discussing the judges' thoughtful critique about synthetic data over lunch."
    },
    "IMG-20261017-WA0035.jpeg": {
        "title": "Blueberry Carton Celebration // Post-Presentation Cheers",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Four blueberry juice cartons lined up on the cafeteria bench, one for each member of Team HackOPs. Toasting the successful defense of WildID after 24 hours of non-stop work and zero sleep. The quiet satisfaction of knowing we left everything on the stage."
    },
    "IMG-20261017-WA0038.jpeg": {
        "title": "Homeward Transport Bus // Gear Packed in the Aisle",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Looking down the aisle of the transport bus packed with backpacks and laptop cases as teams prepared to depart Ballarpur. Exhausted yet deeply motivated, we carried home medals, certificates, and a notebook filled with technical feedback. The hackathon had ended, but our project had found its true beginning."
    },
    "IMG-20261018-WA0000(1)(1).jpg": {
        "title": "Podium Citation & Medals // Desk Arrangement View",
        "stage": "Interpretation",
        "category": "chronicles",
        "claim": "The Special Mention citation certificate displayed alongside the commemorative medal with its green ribbon on a wooden table. Awarded to Team HackOPs by Ballarpur Institute of Technology and Tadoba-Andhari Tiger Reserve leadership. Validation that our ambitious architecture resonated with real conservationists."
    },
    "IMG-20261018-WA0000(1).jpg": {
        "title": "Special Mention Medal // Close-Up on Certificate",
        "stage": "Interpretation",
        "category": "chronicles",
        "claim": "Macro close-up of the embossed WILDHACK 2K26 medal draped with its emerald green ribbon across the official citation. Tangible recognition for building an AI system that aimed to serve wildlife rather than chase vanity metrics. A milestone that will inspire our research for years to come."
    },
    "IMG-20261018-WA0000.jpg": {
        "title": "Valedictory Award Citation // Team HackOPs Special Mention",
        "stage": "Interpretation",
        "category": "chronicles",
        "claim": "The official WILDHACK 2K26 Special Mention certificate and medal awarded to Team HackOPs. Recognized for technical innovation in wildlife re-identification, procedural simulation, and reserve decision-support mapping. Proof that our dormant idea was worthy of the national stage."
    },

    # --- Category 3: Train Journey to Ballarpur (028 - 060) ---
    "IMG_20261016_052201.jpg": {
        "title": "En Route to Ballarpur // 05:22 AM Passenger Coach",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "05:22 AM: Rows of blue seats inside the passenger train heading toward Ballarpur as the dawn light filtered in. Team HackOPs on the move for our first-ever offline hackathon, discussing our proposed pipeline while the coach slept. The calm before 24 hours of non-stop computer vision development."
    },
    "IMG_20261016_061050.jpg": {
        "title": "Dawn Rail Crossing // 06:10 AM Junction Junction",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "06:10 AM: Passing a rural rail junction with passenger rakes waiting on parallel siding tracks under clear morning skies. Watching the landscape transition from urban concrete into the dry deciduous plains of the Vidarbha region. The journey where our postponed wildlife re-ID idea finally became reality."
    },
    "IMG_20261016_061102.jpg": {
        "title": "Siding Acceleration // Parallel Rail Tracks",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "The train picking up speed past the junction switch tracks as the morning sun illuminated the gravel ballast. Hanshal, Vaishnav, Lokesh, and Soham debating whether to attempt 3D mesh reconstruction or planar topological unrolling. Every kilometer brought us closer to the competition floor."
    },
    "IMG_20261016_061114.jpg": {
        "title": "Overhead Catenary Curve // Vidarbha Rail Corridor",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Overhead electrical catenary poles and roadside trees sweeping past along the gentle southern rail curve. Discussing how camera-trap motion blur parallels train window shutter effects, emphasizing the need for robust feature extraction. Our excitement building as we neared Chandrapur district."
    },
    "IMG_20261016_061123.jpg": {
        "title": "Station Cabin Glimpse // Transit Velocity",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "A small rural station cabin and signal mast flashing past the window at full cruising speed. Checking our offline documentation packages on our laptops to ensure all required libraries were downloaded. Ready for whatever constraints the hackathon venue might present."
    },
    "IMG_20261016_061201.jpg": {
        "title": "Twin Steel Rails // The Road to WILDHACK",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Looking down the straight twin tracks cutting across the Maharashtra scrub plains into the distance. Finalizing our plan to dedicate the first six hours to synthetic dataset rendering before assembling the vision models. Clear alignment within the team before stepping off the train."
    },
    "IMG_20261016_061257.jpg": {
        "title": "Telegraph Lines & Shrubland // Window Blur",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Telegraph wires dipping and rising rhythmically against the scrub forest horizon outside Chandrapur. Taking mental notes on the landscape that borders the Tadoba-Andhari Tiger Reserve. Recognizing that human infrastructure and wild corridors exist in close, delicate proximity."
    },
    "IMG_20261016_061300.jpg": {
        "title": "Waking Fields // Rural Maharashtra Dawn",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Morning sunlight washing across agricultural fields dotted with thorny acacia trees along the railway corridor. The peaceful morning landscape contrasting with the high-stakes engineering marathon waiting for us ahead. Team spirits high and eager to compete."
    },
    "IMG_20261016_061345.jpg": {
        "title": "Motion Streaks // Speed Across Vidarbha",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Foreground grass and fence posts blurring into abstract horizontal streaks through the camera lens. Discussing how severe motion artifacts challenge camera-trap edge detectors during nocturnal tiger movements. Engineering inspiration drawn directly from our transit observations."
    },
    "IMG_20261016_061424.jpg": {
        "title": "Clear Skies Horizon // Central Indian Plain",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Broad blue morning sky opening up over the central Indian flatlands as the train entered Chandrapur district. A crisp October morning with optimal weather for traveling and coding. Only thirty finalist teams selected out of the entire country, and we were among them."
    },
    "IMG_20261016_061430.jpg": {
        "title": "Field Boundary Stones // Rural Trackside View",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Trackside stone markers and boundary hedges catching the golden angle of early morning sunlight. Checking the estimated arrival time at Ballarpur Junction and organizing our gear. Four friends united by a shared passion for technology and wildlife conservation."
    },
    "IMG_20261016_061434.jpg": {
        "title": "Passing Passenger Train // Rail Crossing at Speed",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Whizzing past an opposing passenger train waiting patiently on the bypass siding under the morning sky. The sound of clattering bogies marking the final stretch of our railway journey. Ballarpur Institute of Technology was now less than an hour away."
    },
    "IMG_20261016_061436.jpg": {
        "title": "Bogie Shadow Geometry // Sunlight on Ballast",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "The train's own angular shadow stretching across the rocky ballast and embankment as the sun rose higher. Discussing how hard shadows alter an animal's visible silhouette in camera-trap imagery. Reinforcing our commitment to posture-invariant stripe topology."
    },
    "IMG_20261016_061459.jpg": {
        "title": "Open Grassy Buffer // Habitat Borderland",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Open grassland and dry shrubs typical of the transitional buffer zone surrounding the tiger reserve. Understanding the real-world terrain where human-wildlife encounters happen most frequently. The ultimate motivation for building automated, non-invasive wildlife monitoring tools."
    },
    "IMG_20261016_061520.jpg": {
        "title": "Panoramic Basin View // Vidarbha Corridor",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "A sweeping window panorama of the Chandrapur basin as the morning haze burned off under warm sun rays. Capturing field notes and visual impressions to set the mood for our project presentation. Grounding our software architecture in authentic geographical reality."
    },
    "IMG_20261016_061527.jpg": {
        "title": "Transmission Towers // Approaching the Industrial Hub",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "High-voltage transmission towers marching across the farmland toward Ballarpur's industrial periphery. A visual reminder of the intersection between modern infrastructure and fragile natural ecosystems. Preparing our laptops as the train began decelerating."
    },
    "IMG_20261016_061603.jpg": {
        "title": "Town Outskirts // Sighting Village Rooftops",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Village houses and brick kilns appearing on the outskirts of Ballarpur as the train entered city limits. Packing our chargers, notebooks, and water bottles into our backpacks. The anticipation in the carriage was palpable."
    },
    "IMG_20261016_061610.jpg": {
        "title": "Signal Points & Semaphores // Approaching Junction",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Railway signal gantries and track switch machines guiding our train into the Ballarpur yard. The steady clank of wheels over frogs signaling the end of transit and the beginning of competition. Destination reached."
    },
    "IMG_20261016_061613.jpg": {
        "title": "Switch Blades Divergence // Terminal Yard Tracks",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Rail tracks diverging across the approach yard as our train navigated toward its assigned platform. Teammates double-checking that our pre-rendered synthetic tiger models were stored on local SSDs. Ready to plug in and build."
    },
    "IMG_20261016_061658.jpg": {
        "title": "Freight Rakes & Sidings // Industrial Ballarpur",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Long lines of coal freight wagons parked on the railway sidings near the Chandrapur border. Stepping toward the carriage door with our luggage in hand. The start of an unforgettable 24-hour adventure."
    },
    "IMG_20261016_061709.jpg": {
        "title": "Platform Curve Approach // The Journey Ends",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "The train curving smoothly alongside the high concrete platform under the bright morning sun. After traveling through the night, Team HackOPs was on the ground in Ballarpur. The hackathon was officially underway."
    },
    "IMG_20261016_070850.jpg": {
        "title": "Carriage Nap // Teammate Resting Head on Window",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "07:08 AM: A teammate catching a brief nap resting his head against the blue train window cushion. Conserving energy before 24 consecutive hours of coding, debugging, and system integration. The quiet calm before the storm."
    },
    "IMG_20261016_070853.jpg": {
        "title": "Quiet Coach // Backpacks Packed on Train Seats",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "A candid view of our coach compartment with backpacks packed and teammates gathering their belongings. Discussing the presentation sequence and who would handle live GIS map queries during the jury defense. Team cohesion already in motion."
    },
    "IMG_20261016_070855.jpg": {
        "title": "Morning Light in the Coach // Final Moments of Rest",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Golden morning sunlight filling the passenger coach as fellow travelers woke up and gathered their luggage. Taking one last deep breath of quiet before the sensory whirlwind of registrations, announcements, and sprint deadlines. We were ready."
    },
    "IMG_20261016_070856.jpg": {
        "title": "Coach Interior // Ready for Disembarkation",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Teammates standing up in the train aisle, zipping up jacket pockets and grabbing laptop bags from the overhead rack. The train slowly grinding to a halt alongside the Ballarpur platform. Time to make our mark."
    },
    "IMG_20261016_071219.jpg": {
        "title": "Stepping onto Platform // Ballarpur Junction Arrival",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "07:12 AM: Stepping down from the train coach onto the platform at Ballarpur Junction. The morning air was crisp and warm, carrying the distinct scent of dry forest air and railway station tea. Team HackOPs had arrived."
    },
    "IMG_20261016_071232.jpg": {
        "title": "Station Concourse Walk // Carrying the Gear",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Walking down the Ballarpur platform shelter with backpacks, laptop sleeves, and camera cases in hand. Looking around at other student teams arriving on the same train with their project hardware. The competitive energy was immediately palpable."
    },
    "IMG_20261016_074004.jpg": {
        "title": "Station Waiting Area // Regrouping by the Benches",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "07:40 AM: Gathering on the station platform benches with our luggage to book an auto-rickshaw to BIT Bamni. Reviewing our checklist of hardware cables, extension cords, and backup USB drives. Ready for any technical challenges ahead."
    },
    "IMG_20261016_074919.jpg": {
        "title": "Platform Stride // Heading to Foot-Overbridge",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "07:49 AM: Walking toward the station foot-overbridge in the morning sunlight to cross over to the main exit. Excited conversations about how our synthetic forest generation would compare to other teams' approaches. Confident in our unique direction."
    },
    "IMG_20261016_075205.jpg": {
        "title": "Ballarpur Station Architecture // Platform Overbridge",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Looking up at the steel foot-overbridge and overhead shelter of Ballarpur Junction under vivid blue skies. A welcoming introduction to Chandrapur district as we made our way through the ticket gates. Moving swiftly toward the college campus."
    },
    "IMG_20261016_075205_1.jpg": {
        "title": "Passenger Rake Perspective // Platform Line 1",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Looking back along the long blue passenger rake resting quietly at platform line 1 after our overnight journey. A memorable transit that bridged student life with our first national engineering challenge. Onward to Ballarpur Institute of Technology."
    },
    "IMG_20261016_075213.jpg": {
        "title": "Blue Coaches at Rest // Station Atmosphere",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "The blue coaches of the Indian Railways train standing motionless under the platform canopy as the station bustled with passengers. Snapping a quick field photo before heading out to the vehicle stand. Every moment recorded as part of our hackathon chronicle."
    },
    "IMG_20261016_075845.jpg": {
        "title": "Exiting Ballarpur Junction // Heading to BIT Bamni",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "07:58 AM: Stepping through the main exit archway of Ballarpur railway station into the morning sunlight. Hiring an auto-rickshaw to take our four-person team and luggage to the campus grounds. The stage was set for WILDHACK 2K26."
    },

    # --- Category 4: BIT Campus Grounds & Spider Encounter (061 - 072) ---
    "IMG_20261016_094251.jpg": {
        "title": "BIT Bamni Campus Grounds // Perimeter Walk",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "09:42 AM: Exploring the perimeter pathway of Ballarpur Institute of Technology after completing team registration. Taking in the academic buildings, lush greenery, and the quiet buzz of organizing volunteers setting up banners. The venue was welcoming and spacious."
    },
    "IMG_20261016_094252.jpg": {
        "title": "Academic Lawns // Orientation Walkway",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Looking across the manicured lawns and trees of the BIT campus in the morning light. Meeting competing teams from Maharashtra, Telangana, and Madhya Pradesh who had traveled for the challenge. A genuine feeling of community among young engineers."
    },
    "IMG_20261016_130645.jpg": {
        "title": "Pre-Hackathon Flora // Campus Biodiversity Observation",
        "stage": "Field Lab",
        "category": "wildlife",
        "claim": "13:06 PM: Taking a mindful stroll through the campus gardens before the afternoon opening ceremony. Photographing macro details of garden leaves and soil textures, observing how natural organisms thrive in the Tadoba corridor. A quiet moment of connection with nature."
    },
    "IMG_20261016_130646.jpg": {
        "title": "Garden Foliage Texture // Organic Pattern Study",
        "stage": "Field Lab",
        "category": "wildlife",
        "claim": "Close-up of vibrant green campus shrubbery in the afternoon sun. Discussing how natural foliage creates complex occlusion patterns that computer vision models must learn to navigate. Finding algorithmic inspiration directly in the surrounding vegetation."
    },
    "IMG_20261016_130653.jpg": {
        "title": "Ground Plants & Grasses // Botanical Details",
        "stage": "Field Lab",
        "category": "wildlife",
        "claim": "Examining wild ground grasses near the BIT Bamni pathway before heading into the main auditorium. Connecting our classroom AI algorithms with the living biology of the Central Indian landscape. Our motivation was grounded in the real world."
    },
    "IMG_20261016_130711.jpg": {
        "title": "Green Lynx Spider // First Encounter on Arm",
        "stage": "Individual",
        "category": "wildlife",
        "claim": "A brilliant green Peucetia lynx spider resting gently on a teammate's arm in the campus garden. Noticing its bright emerald body, reddish cephalothorax dots, and banded legs — a stunning miniature demonstration of biological uniqueness. Nature offering its own masterclass in pattern recognition."
    },
    "IMG_20261016_130719.jpg": {
        "title": "Peucetia Leg Spines // Macro Cephalothorax Detail",
        "stage": "Individual",
        "category": "wildlife",
        "claim": "Close-up macro shot of the green lynx spider showing its black-spined translucent legs and distinctive ocular cluster. Much like tiger stripes, the spine arrangements and micro-markings on arachnids serve as individual biological signatures. A memorable wildlife encounter right on campus."
    },
    "IMG_20261016_130724.jpg": {
        "title": "Gentle Wanderer // Lynx Spider on Wrist",
        "stage": "Individual",
        "category": "wildlife",
        "claim": "The lynx spider moving calmly across the wrist, displaying its agile hunting legs and camouflage coloration. Teammates crowded around to admire its delicate structure before releasing it back safely into the bush. A serendipitous reminder of why we care about conservation."
    },
    "IMG_20261016_130725.jpg": {
        "title": "Natural Camouflage // Spider Amongst Grass",
        "stage": "Individual",
        "category": "wildlife",
        "claim": "The green spider positioned against green grass blades, demonstrating nature's near-perfect camouflage. Illustrates the challenge computer vision faces when distinguishing a camouflaged subject from its matching background. An apt metaphor for tiger stripe segmentation in dry teak grass."
    },
    "IMG_20261016_130733.jpg": {
        "title": "Leap to Freedom // Releasing the Lynx Spider",
        "stage": "Individual",
        "category": "wildlife",
        "claim": "The green spider preparing to leap back into the garden shrubbery as our afternoon break drew to a close. Releasing our eight-legged visitor unharmed before heading toward the auditorium for the hackathon opening ceremony. Good luck from nature itself."
    },
    "IMG_20261016_131054.jpg": {
        "title": "Team HackOPs at BIT // Pre-Sprint Tire Portrait",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "13:10 PM: Hanshal, Vaishnav, Lokesh, and Soham smiling together around the giant green tractor tire installation on campus. Spirits were high, energy was infectious, and anticipation was peaking before the 24-hour sprint. Four students united by a shared vision to serve Indian wildlife."
    },

    # --- Category 5: Midnight Sprint in the Lab / Accommodation (073 - 075) ---
    "IMG_20261017_025823.jpg": {
        "title": "02:58 AM Crucible // Coding on the Bed Workstation",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "02:58 AM: The dead of night in our campus room with laptops perched on floral bedsheets, chargers entangled, and terminal windows glowing. While other teams rested, Team HackOPs pushed through the midnight wall to resolve high-pass stripe filtering errors. Pure developer endurance."
    },
    "IMG_20261017_025832.jpg": {
        "title": "Tangled Cables & Glowing Screens // 3:00 AM Integration",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Power strips, HDMI adapters, and code editors lit up in the darkened room at 3:00 AM. Vaishnav and Lokesh verifying synthetic dataset export scripts while Soham wired the telemetry API endpoints. The defining crucible hours where hackathon projects are either made or broken."
    },
    "IMG_20261017_025833.jpg": {
        "title": "Terminal Convergence // Midnight Model Validation",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Close-up of active development laptops during the final overnight push, verifying that the segmentation pipeline compiled cleanly. Zero sleep, endless cups of water, and absolute team focus. By 4:00 AM, our core re-ID matching loop was finally running without crashes."
    },

    # --- Category 6: Stage Presentation & Defense (076 - 081) ---
    "IMG_20261017_140321.jpg": {
        "title": "14:03 PM Stage Defense // Presenting WildID to the Jury",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "14:03 PM: Team HackOPs standing on the BIT auditorium stage in matching black shirts, presenting WildID to the evaluating jury. Beginning our 30-minute defense by explaining why individual re-identification matters for tiger territory management. The culmination of 24 hours of non-stop work."
    },
    "IMG_20261017_140322.jpg": {
        "title": "Synthetic Pipeline Defense // Answering Faculty Inquiries",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Explaining the architecture of our Blender Python synthetic data generator to computer science professors and judges. Articulating how generating 10,000 synthetic scenes locally solved our initial training bottleneck within the 24-hour limit. Standing firm on our technical choices."
    },
    "IMG_20261017_140326.jpg": {
        "title": "Live Dashboard Demo // Projecting Leaflet GIS on Stage",
        "stage": "Interpretation",
        "category": "telemetry",
        "claim": "Demonstrating our live Leaflet GIS telemetry dashboard on the auditorium screen as judges watched closely. Showing how re-identified tiger sightings automatically map into home range polygons and waterhole corridors. Moving beyond classification to actionable ranger intelligence."
    },
    "IMG_20261017_140327.jpg": {
        "title": "Jury Critical Dialogue // Addressing Synthetic Limitations",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Engaging in an honest technical discussion with forest officials regarding synthetic vs. real camera-trap imagery. We acknowledged that while synthetic scenes enabled rapid prototyping within 24 hours, authentic reserve camera traps are essential for field validation. This critical feedback shaped our entire post-hackathon roadmap."
    },
    "IMG_20261017_140328.jpg": {
        "title": "Stage Defense Conclusion // United Front Before Judges",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "The four members of Team HackOPs concluding our stage presentation amidst questions from the panel. The relief and pride of having presented a comprehensive, functioning system built from scratch in 24 hours. A moment that cemented our bond as teammates and friends."
    },
    "IMG_20261017_140404.jpg": {
        "title": "Workstation Code Walkthrough // Live Technical Inspection",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Gathered closely around the laptop workstation on stage, walking judges through our actual Python codebase and Git commit history. Demonstrating that our pipeline was genuinely functional, locally executed, and fully reproducible. Earning the judges' respect for architectural integrity."
    },

    # --- Category 7: Auditorium Presentations by Competing Teams (082 - 092) ---
    "IMG_20261017_170741.jpeg": {
        "title": "Finalist Presentations // Competing Team on Stage",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "17:07 PM: A competing engineering team on the BIT auditorium stage presenting their conservation hardware prototype. Watching fellow finalists demonstrate drone tracking systems, acoustic monitoring, and sensor networks. The impressive technical caliber of India's top 30 student teams on display."
    },
    "IMG_20261017_170818 (10).jpg": {
        "title": "Auditorium Evaluations // Faculty Panel Review",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Jury members and forest officials listening intently to an engineering group's technical defense. The judging rubric scrutinized practical reserve applicability, cost-efficiency, and machine learning rigor. The atmosphere remained charged with intellectual rigor."
    },
    "IMG_20261017_170818 (11).jpg": {
        "title": "Auditorium Twilight // Final Deliberations Approach",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "The BIT auditorium illuminated as the final team wrapped up their demonstration slides. With all thirty team defenses completed, the jury prepared to retire for intensive deliberation. A collective sense of accomplishment filled the hall."
    },
    "IMG_20261017_170818 (2).jpeg": {
        "title": "Center Aisle Perspective // Stage Prototype Demo",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Looking down the center auditorium aisle as an engineering group demonstrated their IoT sensor board to the judging table. Observing how different teams solved connectivity challenges in remote tiger reserves. Learning from our peers across every presentation slot."
    },
    "IMG_20261017_170818 (3).jpeg": {
        "title": "Audience Seating // Competing Finalists Listening",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Audience rows filled with participating students, faculty mentors, and forest department guests. Listening to diverse approaches toward poaching prevention, animal census automation, and fence monitoring. The collegiate camaraderie that defined WILDHACK 2K26."
    },
    "IMG_20261017_170818 (4).jpeg": {
        "title": "Jury Table Perspective // Projector Slide Scrutiny",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "A clear view of the judges' table at the front of the auditorium as presentation slides lit up the main screen. Evaluators taking meticulous notes on each team's algorithmic feasibility and prototype completeness. A rigorous, fair evaluation process."
    },
    "IMG_20261017_170818 (5).jpeg": {
        "title": "Conservation Drones // Competing Solution Showcase",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "A finalist team presenting their computer vision approach for aerial surveillance and thermal drone telemetry. Demonstrating the breadth of technology explored during the 24 hours at Ballarpur. Inspiring ideas exchanged across team boundaries."
    },
    "IMG_20261017_170818 (6).jpg": {
        "title": "Auditorium Screen // Hardware Circuit Schematics",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Close view of the presentation screen showing circuit schematics and power consumption graphs for field-deployed sensor nodes. Technical rigor was evident throughout the competition, challenging every participant to raise their standards."
    },
    "IMG_20261017_170818 (7).jpg": {
        "title": "Q&A Scrutiny // Judges Probing Edge Cases",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Judges engaging in a sharp technical inquiry regarding battery life, waterproof casing, and model inference latency in rural forest conditions. The judges brought real field experience to bear, ensuring solutions were grounded in practical reality."
    },
    "IMG_20261017_170818 (8).jpg": {
        "title": "Podium Branding // WILDHACK 2K26 Stage Banner",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "The official WILDHACK 2K26 banner on the stage podium, highlighting the collaboration between Ballarpur Institute of Technology and Tadoba-Andhari Tiger Reserve. An inspiring partnership bringing technology academia and field conservation together."
    },
    "IMG_20261017_170818 (9).jpg": {
        "title": "Auditorium Exchange // Final Minutes of Defense",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Participants engaging in quiet conversation and note-taking as the final presentation concluded. The shared relief across all thirty teams was unmistakable: the demanding 24-hour development and defense marathon was officially over."
    },

    # --- Category 8: Dusk Outside BIT (093 - 095) ---
    "IMG_20261017_182836.jpg": {
        "title": "Dusk Over BIT Trees // The 24 Hours Conclude",
        "stage": "Landscape",
        "category": "chronicles",
        "claim": "18:28 PM: Evening twilight descending over the tree canopy outside the BIT campus as the hackathon timer officially expired. Standing outside the auditorium in the cool breeze, taking in our first deep breaths of fresh air in twenty-four hours. An unforgettable sprint had drawn to a close."
    },
    "IMG_20261017_182841.jpg": {
        "title": "Orange Twilight Horizon // Evening Calm",
        "stage": "Landscape",
        "category": "chronicles",
        "claim": "Vibrant orange sunset glow filtering through the campus trees while the jury deliberated final awards inside. The exhaustion of the sprint giving way to peaceful satisfaction: we had set out to build WildID, and we had delivered."
    },
    "IMG_20261017_182842.jpg": {
        "title": "Tree Silhouette at Dusk // Reflective Silence",
        "stage": "Landscape",
        "category": "chronicles",
        "claim": "Dark tree silhouettes etched against the fading dusk sky outside the Ballarpur auditorium. A quiet, contemplative moment before the valedictory ceremony began. Knowing that win or lose, the journey had transformed how we think about conservation engineering."
    },

    # --- Category 9: Valedictory Ceremony & Meeting Dignitaries (096 - 101) ---
    "IMG_20261017_201650.jpg": {
        "title": "Valedictory Stage // Dignitaries Assembled",
        "stage": "Interpretation",
        "category": "chronicles",
        "claim": "20:16 PM: The valedictory ceremony commencing on the main auditorium stage with dignitaries seated at the head table. University leadership, corporate executives, and Tadoba forest conservators gathered to announce awards and celebrate all participants. The grand finale of WILDHACK 2K26."
    },
    "IMG_20261017_202252.jpg": {
        "title": "Closing Keynote // Address by TATR Conservators",
        "stage": "Interpretation",
        "category": "chronicles",
        "claim": "Dignitaries addressing the finalist teams on the importance of engineering students engaging with Indian wildlife challenges. Emphasizing that AI and sensor technology must empower frontline forest guards and field biologists. Words that deeply validated our team's mission."
    },
    "IMG_20261017_205727.jpg": {
        "title": "Dignitary Dialogue // Conversing with Mr. Parag Gupta",
        "stage": "Interpretation",
        "category": "chronicles",
        "claim": "20:57 PM: Speaking with Mr. Parag Gupta (Director & Country Manager, Amazon Devices India) about cloud scalability and low-power edge computing for camera traps. Receiving encouraging advice on how to architect lightweight embedded models for field deployment. An invaluable mentorship encounter that expanded our technical horizons."
    },
    "IMG_20261017_205731.jpg": {
        "title": "Expert Exchange // Mentorship on Real-World Datasets",
        "stage": "Interpretation",
        "category": "chronicles",
        "claim": "In-depth conversation with the judging panel regarding our next steps for WildID. Judges encouraged us to collaborate with national parks to acquire authentic camera-trap corpora and test domain adaptation algorithms. A conversation that gave our future research a clear roadmap."
    },
    "IMG_20261017_205733.jpg": {
        "title": "Conservation Guidance // Dr. Prabhunath Shukla Dialogue",
        "stage": "Interpretation",
        "category": "chronicles",
        "claim": "Dr. Prabhunath Shukla (Conservator of Forests & Field Director, TATR) discussing the operational realities of reserve territory monitoring. He emphasized how automated individual identification could significantly reduce manual photo-matching workloads for forest staff. A discussion that gave our ongoing research deep conservation purpose."
    },
    "IMG_20261017_205742.jpg": {
        "title": "Special Mention Stage Moment // Team HackOPs Citation",
        "stage": "Interpretation",
        "category": "chronicles",
        "claim": "Team HackOPs on stage with dignitaries and judges after being awarded the Special Mention for WildID. Recognized for our architectural scalability, simulation methodology, and conservation ambition at our first-ever offline hackathon. A proud milestone for all four of us."
    },

    # --- Category 10: Post-Hackathon Morning Celebration (102 - 106) ---
    "IMG_20261018_131943_489.jpg": {
        "title": "Post-Hackathon Reflections // Campus Grounds Celebration",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "October 18, 13:19 PM: Team HackOPs on the sunny BIT campus grounds proudly displaying our Special Mention award certificates. Smiles that reflect 24 hours of exhausting work, rapid learning, and shared triumph. We came to build a project and left with clear purpose."
    },
    "IMG_20261018_131943_489_1.jpg": {
        "title": "Candid Team Portrait // Medals & Certificates in Hand",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "A candid photograph of Hanshal, Vaishnav, Lokesh, and Soham holding our certificates in the afternoon sun. Celebrating our journey from brainstorming in dorm rooms to competing alongside India's top 30 student engineering teams. A proud memory etched in our university careers."
    },
    "IMG_20261018_131943_746_3.jpg": {
        "title": "Brothers in Engineering // Team HackOPs Group Shot",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Standing together against the campus tree line with awards held high. The mutual trust and shared work ethic forged during the midnight sprint made this achievement possible. A partnership that will continue developing WildID into a real-world tool."
    },
    "IMG_20261018_131943_751_4.jpg": {
        "title": "Smiles of Validation // Special Mention Awardees",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Close-up of the four teammates beaming with genuine happiness in the October warmth. Proving that dedication to a meaningful problem can yield tangible results even under extreme time limits. Ready to take our research to the next level."
    },
    "IMG_20261018_131943_853_5.jpg": {
        "title": "The Final Campus Pose // Ready to Head Home",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Holding the certificates forward one last time before packing bags for the homeward journey. The banners of WILDHACK 2K26 behind us fluttering gently in the breeze. An unforgettable chapter concluded, and a promising research journey begun."
    },

    # --- Category 11: Live Software Demonstrations (107 - 117) ---
    "Screenshot 2026-10-17 080835.png": {
        "title": "5-Stage Vision Pipeline // Feature Extraction Evidence",
        "stage": "Evidence",
        "category": "telemetry",
        "claim": "08:08 AM: Live telemetry capture showing our 5-stage feature extraction interface: original plate, segmentation mask, high-pass stripe filter, and cosine similarity matrix. Demonstrating clean pelt isolation from complex background vegetation. A core technical achievement of our 24-hour sprint."
    },
    "Screenshot 2026-10-17 081004.png": {
        "title": "Planar Stripe Unwrapping // Invariant 2D Topology",
        "stage": "Evidence",
        "category": "telemetry",
        "claim": "08:10 AM: Inspecting the unwrapped 2D fur-carpet representation that maps curved lateral stripes into an invariant topological space. By separating body posture from stripe bifurcation geometry, our model maintained high match confidence even across oblique sighting angles. Verified live during our prototype trials."
    },
    "Screenshot 2026-10-17 095112.png": {
        "title": "Territory Roaming Polygons // Spatial Telemetry Engine",
        "stage": "Interpretation",
        "category": "telemetry",
        "claim": "09:51 AM: Testing the spatial roaming engine across Moharli and Tadoba core zones, computing minimum convex polygon territories from sequential detections. Proving that individual animal re-ID directly enables spatial intelligence for tiger reserve administration. Developed in real-time during the sprint."
    },
    "Screenshot 2026-10-17 100531.png": {
        "title": "Leaflet GIS Command Dashboard // Live Operations Center",
        "stage": "Interpretation",
        "category": "telemetry",
        "claim": "10:05 AM: The interactive WildID Operations Center projecting camera trap coordinates, core boundary sectors, and waterhole corridors. Range officers can query individual tiger histories and inspect encounter timestamps on an interactive map. The comprehensive decision-support system demonstrated to judges."
    },
    "Screenshot 2026-10-17 103003.png": {
        "title": "Ecological Corridor Analytics // Water Basin Correlation",
        "stage": "Interpretation",
        "category": "telemetry",
        "claim": "10:30 AM: Correlating tiger encounter density clusters with proximity to seasonal waterholes and the Andheri river basin. Combining computer vision re-identification with ecological GIS variables to assist forest guards in anti-poaching patrol deployment. Analytical depth praised by the jury."
    },
    "Screenshot 2026-10-17 103438.png": {
        "title": "Temporal Encounter Histogram // Diurnal Movement Trends",
        "stage": "Interpretation",
        "category": "telemetry",
        "claim": "10:34 AM: Sighting frequency analytics chart tracking individual activity curves across diurnal and nocturnal hours. Helps researchers identify when specific tigers cross human-inhabited buffer zones. Transforming raw imagery into predictive conservation intelligence."
    },
    "Screenshot 2026-10-17 112438.png": {
        "title": "Territorial Boundary Mapping // GIS Sector Layer #2438",
        "stage": "Interpretation",
        "category": "telemetry",
        "claim": "11:24 AM: Inspecting the GIS sector layer rendering reserve boundary markers, core compartments, and buffer roads. Verifying that spatial coordinate projections aligned accurately with Tadoba cartographic standards. Polishing the interface minutes before our stage demonstration."
    },
    "Screenshot 2026-10-17 112519.png": {
        "title": "Individual Identity Popups // Telemetry Dossier View",
        "stage": "Interpretation",
        "category": "telemetry",
        "claim": "11:25 AM: Testing interactive map marker popups displaying verified tiger ID, confidence score, and timestamp of the latest camera-trap sighting. Designed for rapid situational awareness during range patrol debriefs. Clean, utilitarian design engineered under time pressure."
    },
    "Screenshot 2026-10-17 112526.png": {
        "title": "Home Range Overlap Analytics // Territorial Interaction",
        "stage": "Interpretation",
        "category": "telemetry",
        "claim": "11:25 AM: Zoomed-in GIS view analyzing territorial polygon overlaps between neighboring male tigers along the river corridor. Identifying potential conflict zones where territorial disputes are likely to occur. Adding biological depth to our computer vision framework."
    },
    "Screenshot 2026-10-17 112541.png": {
        "title": "Camera-Trap Grid Inspection // Sensor Density Map",
        "stage": "Interpretation",
        "category": "telemetry",
        "claim": "11:25 AM: Inspecting camera-trap station distribution clusters across high-traffic trail intersections. Ensuring our telemetry ingestion pipeline could handle asynchronous image feeds from dozens of stations simultaneously. Scalability built directly into the software architecture."
    },
    "Screenshot 2026-10-17 114324.png": {
        "title": "Pre-Demo System Audit // Final UI State Verification",
        "stage": "Interpretation",
        "category": "telemetry",
        "claim": "11:43 AM: Final pre-demo UI audit of the operations dashboard with all tabs responsive, maps rendered, and query endpoints validated. Taking a collective deep breath as the clock ticked down to our presentation slot. WildID was fully operational and ready for the judges."
    },

    # --- Category 12: Post-Hackathon Telemetry & Anomaly Detection (118 - 123) ---
    "Screenshot 2026-10-18 212740.png": {
        "title": "Longitudinal Telemetry Console // Post-Event Review",
        "stage": "Interpretation",
        "category": "telemetry",
        "claim": "Reviewing the WildID command interface following the hackathon, evaluating multi-week sighting tracking across seasonal shifts. Planning improvements to the backend storage layer to handle large camera-trap image archives efficiently. Continuing development right after the event."
    },
    "Screenshot 2026-10-18 212753.png": {
        "title": "Individual Query Interface // Range Officer Filter",
        "stage": "Interpretation",
        "category": "telemetry",
        "claim": "Testing individual query filters allowing patrol officers to search by tiger specimen code and date range. Refactoring client-side JavaScript to ensure snappy interactive performance even when handling thousands of historical sightings. Polishing our open-source codebase."
    },
    "Screenshot 2026-10-18 212832.png": {
        "title": "Movement Trajectory Vectors // Spatiotemporal Path",
        "stage": "Interpretation",
        "category": "telemetry",
        "claim": "Visualizing sequential tiger movement trajectories connecting historical camera-trap timestamps into directional travel vectors. Enabling forest management to observe dispersal paths of young tigers establishing new territories. Moving our research toward predictive ecological modeling."
    },
    "Screenshot 2026-10-18 212947.png": {
        "title": "Patrol Anomaly Trigger // Perimeter Boundary Warning",
        "stage": "Interpretation",
        "category": "telemetry",
        "claim": "Investigating automated anomaly triggers: alerting forest managers when a tiger is detected moving outside its documented historical range toward human agricultural borders. Proactive conflict mitigation enabled by automated biometric identification. The societal impact of our project."
    },
    "Screenshot 2026-10-18 213000.png": {
        "title": "Risk Forecasting Dashboard // Conflict Mitigation Alert",
        "stage": "Interpretation",
        "category": "telemetry",
        "claim": "Testing real-time conflict forecasting alerts that notify forest stations when an apex predator lingers near fringe village borders. Transforming passive camera-trap footage into an active, life-saving early warning system. Real engineering for real conservation impact."
    },
    "Screenshot 2026-10-18 213007.png": {
        "title": "Ranger Intelligence Dispatch // Automated Action Report",
        "stage": "Interpretation",
        "category": "telemetry",
        "claim": "The synthesized intelligence report dashboard formatting actionable recommendations for daily ranger patrols. Integrating biometric certainty scores with geographical terrain data. Demonstrating how computer vision can seamlessly integrate into daily reserve workflows."
    },

    # --- Category 13: Team Celebration Meals & Closing Encounters (124 - 130) ---
    "WA_1792133703926.jpeg": {
        "title": "Post-Hackathon Dinner // Team HackOPs Celebration Meal",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Sharing a celebratory dinner after the closing ceremony in Ballarpur, unwinding after 24 hours of relentless problem-solving. Exhausted, smiling, and wearing our black event shirts, we relived every challenge and breakthrough of the competition. Unbreakable bonds forged in the sprint."
    },
    "WA_1792133716751.jpeg": {
        "title": "Dinner Table Fellowship // Laughing Over 24-Hour Bugs",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Another warm moment around the dinner table, laughing over the near-disasters and midnight tensor shape mismatches we overcame together. With the pressure behind us and our Special Mention secured, we enjoyed a relaxed meal before traveling home. A perfect conclusion to our journey."
    },
    "file_00000000375c8211ac88027801cb7c94.png": {
        "title": "Avian Campus Visitor // Little Green Bird on Path",
        "stage": "Individual",
        "category": "wildlife",
        "claim": "A charming little green songbird hopping curiously along the concrete walkway at BIT Bamni during an early morning break. Nature continually presenting itself throughout our hackathon stay in the Vidarbha forest belt. A gentle reminder of the diverse wildlife we were engineering for."
    },
    "file_00000000403c8211ba3ceaec4ee43357.png": {
        "title": "Medals in Hand // WILDHACK 2K26 Recognition",
        "stage": "Interpretation",
        "category": "chronicles",
        "claim": "Holding the gleaming Special Mention medals and certificate firmly in hand after the valedictory ceremony. Tangible proof that our dorm room idea and 24 hours of determination had produced something respected by national judges. A milestone that will always hold special meaning."
    },
    "file_000000004a74821197a0a9131e0c9c8d.png": {
        "title": "Hackathon Lab Panorama // Teams Building Non-Stop",
        "stage": "Field Lab",
        "category": "chronicles",
        "claim": "Looking across the crowded hackathon laboratory benches as dozens of student teams coded, wired circuits, and tested models. The electric atmosphere of creative problem-solving and shared passion that makes hackathons unique. An inspiring arena to compete in."
    },
    "file_00000000c8608207a074cefe37aa7074.png": {
        "title": "Proud Validation // The Certificate & Medal",
        "stage": "Interpretation",
        "category": "chronicles",
        "claim": "Holding up the official WILDHACK 2K26 Certificate of Achievement and green-ribbon medal outside the BIT auditorium. A symbol of resilience, technical courage, and teamwork under pressure. Dedicated to our vision of AI that serves Indian wildlife conservation."
    },
    "image-1792225801113.jpg": {
        "title": "Ideation Blueprint // Handwritten Architectural Notes",
        "stage": "Evidence",
        "category": "chronicles",
        "claim": "Handwritten brainstorming notes scribbled on paper during the opening hours of the hackathon: outlining the 'Why', defining the 3 core vision fields, and mapping reserve constraints. The raw, unfiltered thought process that laid the foundation for the entire WildID architecture."
    },
    "image-1792226590858.jpg": {
        "title": "Pipeline Architecture Sketch // System Block Diagram",
        "stage": "Evidence",
        "category": "chronicles",
        "claim": "Hand-drawn block diagram connecting camera-trap input, Blender procedural forest generation, high-pass stripe filtering, and GIS decision mapping. The blueprint that guided all four teammates through the 24-hour sprint. Proof that clarity of thought precedes great code."
    }
}

def update_all():
    print(f"Total entries defined in script: {len(ENTRIES)}")
    
    # Check uniqueness of claims
    all_claims = [v["claim"] for v in ENTRIES.values()]
    unique_claims = set(all_claims)
    print(f"Total unique claims: {len(unique_claims)} / {len(all_claims)}")
    if len(unique_claims) != len(all_claims):
        raise ValueError(f"Duplicate claims detected! Only {len(unique_claims)} unique claims out of {len(all_claims)}!")

    # Check sentence count (must be 2-3 sentences each)
    import re
    for fn, entry in ENTRIES.items():
        claim = entry["claim"]
        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', claim) if s.strip()]
        if len(sentences) < 2 or len(sentences) > 3:
            print(f"Warning: {fn} has {len(sentences)} sentences: {claim[:60]}...")

    # Load existing gallery_data.json
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated_count = 0
    csv_rows = [["image_name", "description"]]

    for item in data:
        fn = item["filename"]
        if fn in ENTRIES:
            entry = ENTRIES[fn]
            item["title"] = entry["title"]
            item["claim"] = entry["claim"]
            item["stage"] = entry["stage"]
            item["category"] = entry["category"]
            csv_rows.append([fn, entry["claim"]])
            updated_count += 1
        else:
            print(f"MISSING ENTRY IN DICT: {fn}")
            csv_rows.append([fn, item.get("claim", "")])

    print(f"Updated {updated_count} / {len(data)} gallery items.")

    # 1. Save gallery_data.json
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved {JSON_FILE}")

    # 2. Save js/gallery_data.js
    js_content = "window.WILDID_GALLERY = " + json.dumps(data, indent=2, ensure_ascii=False) + ";\n"
    with open(JS_FILE, "w", encoding="utf-8") as f:
        f.write(js_content)
    print(f"Saved {JS_FILE}")

    # 3. Save image_descriptions.csv
    with open(CSV_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(csv_rows)
    print(f"Saved {CSV_FILE}")

if __name__ == "__main__":
    update_all()
