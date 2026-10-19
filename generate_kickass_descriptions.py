#!/usr/bin/env python3
"""
generate_kickass_descriptions.py
Creates bespoke, kickass editorial descriptions (2-3 lines each) for all 130 images
in the WildID archive, combining the Ollama moondream vision detections with the authentic
first-person narrative of Team HackOPs at WILDHACK 2K26.

Updates:
- image_descriptions.csv
- gallery_data.json
- js/gallery_data.js
"""

import json
import csv
import os
import re

CSV_INPUT = "image_descriptions.csv"
JSON_FILE = "gallery_data.json"
JS_FILE = "js/gallery_data.js"

# Load existing moondream vision detections
vision_map = {}
if os.path.exists(CSV_INPUT):
    with open(CSV_INPUT, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if len(row) >= 2:
                vision_map[row[0]] = row[1]

# Load existing gallery records
with open(JSON_FILE, mode="r", encoding="utf-8") as f:
    data = json.load(f)

def generate_kickass_entry(item):
    filename = item["filename"]
    vision = vision_map.get(filename, "")
    
    # --- Category 1: Dawn Forest & Habitat Plates (20261017_0639xx - 0640xx) ---
    if filename.startswith("20261017_063919"):
        title = "Tadoba Dawn Canopy // Sector 4B Morning Light"
        desc = ("Early morning light breaking through the dry deciduous teak canopy of Tadoba-Andhari. "
                "Sunlight pierces through the foliage, illuminating the dense woodland corridor where Bengal tigers establish territorial trails. "
                "Captured at 06:39 AM during our field study, setting the environmental benchmark for camera-trap illumination.")
        stage = "Landscape"
        cat = "wildlife"

    elif filename.startswith("20261017_063934"):
        title = "Forest Flank Corridor // Dappled Canopy Shadow"
        desc = ("Dappled shadow patterns dancing across the forest floor as morning rays penetrate the teak canopy. "
                "This extreme contrast between direct sun and heavy shade highlights the core computational challenge: "
                "extracting invariant stripe bifurcations when ambient lighting creates false boundaries across an animal's flanks.")
        stage = "Evidence"
        cat = "wildlife"

    elif filename.startswith("20261017_063944"):
        title = "Moharli Core Trail // Horizon Depth Vector"
        desc = ("Looking outward through the dense teak corridor toward the horizon as the morning mist burns away. "
                "The rugged terrain and tangled branch structures demonstrate why automated segmentation must isolate the animal cleanly from background foliage. "
                "A foundational habitat plate for our simulated environment benchmarks.")
        stage = "Landscape"
        cat = "wildlife"

    elif filename.startswith("20261017_063954"):
        title = "Canopy Silhouette // Vertical Geometry Benchmark"
        desc = ("Twin prominent teak trunks standing tall against the luminous morning sky, casting long linear shadows. "
                "In our Blender GroveScape simulations, we used these precise vertical tree silhouettes and branch densities "
                "to parametrically model realistic occlusions for the 10,000 synthetic training scenes.")
        stage = "Landscape"
        cat = "wildlife"

    elif filename.startswith("20261017_063955"):
        title = "Teak Trunk Bifurcations // Natural Graph Topology"
        desc = ("Intertwined forest trunks and branching patterns photographed in the early hours near the Moharli gate. "
                "The fractal branching of deciduous teak trees provided inspiration for our graph-based stripe representation: "
                "treating fur bifurcations as persistent topological vertices rather than static pixel grids.")
        stage = "Evidence"
        cat = "wildlife"

    elif filename.startswith("20261017_064014"):
        title = "Deep Corridor View // Foreshortened Perspective"
        desc = ("A perspective view through the forest corridor capturing angular foreshortening and foliage layering. "
                "When a tiger turns or steps uphill, body perspective changes dramatically across camera-trap views. "
                "This plate served as our reference for tuning 3D pose-estimation keypoints under severe viewing angles.")
        stage = "Evidence"
        cat = "wildlife"

    elif filename.startswith("20261017_064022"):
        title = "The Living Forest // Epilogue Specimen Plate"
        desc = ("Warm golden light bathing the forest floor through the canopy in a moment of quiet stillness. "
                "The closing visual of our journey: a reminder that behind every biometric vector and segmentation mask lies an ancient, living ecosystem. "
                "‘The forest has a memory. We are learning to read it.’")
        stage = "Landscape"
        cat = "wildlife"

    # --- Category 2: Train Journey to WILDHACK 2K26 (IMG_20261016_052201 - 075845) ---
    elif filename == "IMG_20261016_052201.jpg":
        title = "En Route to Chandrapur // Early Morning Passenger Car"
        desc = ("05:22 AM aboard the early train heading toward Ballarpur: rows of blue seats and quiet anticipation. "
                "Team HackOPs on the move for our first-ever offline hackathon, discussing our proposed pipeline while the rest of the carriage slept. "
                "The calm before 24 hours of non-stop computer vision development.")
        stage = "Field Lab"
        cat = "chronicles"

    elif filename == "IMG_20261016_061050.jpg":
        title = "Dawn Crossing // Ballarpur Route Rail Junction"
        desc = ("06:10 AM: Passing a rural junction with trains waiting on adjacent tracks under clear morning skies. "
                "Watching the landscape transition from urban concrete into the dry deciduous plains of the Vidarbha region. "
                "The journey where our long-postponed wildlife re-identification idea finally turned into commitment.")
        stage = "Field Lab"
        cat = "chronicles"

    elif filename in ["IMG_20261016_061102.jpg", "IMG_20261016_061114.jpg", "IMG_20261016_061123.jpg", "IMG_20261016_061201.jpg"]:
        title = f"Transit Velocity // Maharashtra Rail Corridor #{filename[-6:-4]}"
        desc = ("Rushing along the central Indian railway corridor as dawn broke over roadside stations and fields. "
                "Team discussions centered on model trade-offs: whether to attempt full 3D mesh reconstruction or stick to planar fur-carpet unrolling. "
                "Every kilometer brought us closer to Ballarpur Institute of Technology.")
        stage = "Field Lab"
        cat = "chronicles"

    elif filename in ["IMG_20261016_061257.jpg", "IMG_20261016_061300.jpg", "IMG_20261016_061345.jpg", "IMG_20261016_061424.jpg"]:
        title = f"Motion Blur & Horizons // Transit Field Frame #{filename[-6:-4]}"
        desc = ("Looking out through the train window at telegraph lines and waking villages passing in a blur. "
                "Examining sample tiger photographs on a laptop screen, discussing how train motion blur parallels the shutter artifacts of nocturnal camera traps. "
                "Setting our focus on algorithmic resilience over brittle perfection.")
        stage = "Field Lab"
        cat = "chronicles"

    elif filename in ["IMG_20261016_061430.jpg", "IMG_20261016_061434.jpg", "IMG_20261016_061436.jpg", "IMG_20261016_061459.jpg", "IMG_20261016_061520.jpg", "IMG_20261016_061527.jpg"]:
        title = f"Approaching Chandrapur // Window Perspectives #{filename[-6:-4]}"
        desc = ("Sunlight cutting through the train window at an angle, illuminating our development notes. "
                "Debating how to structure the 24-hour sprint: dedicating the first six hours to local dataset rendering before assembling the vision pipeline. "
                "A shared ambition taking shape with every passing station.")
        stage = "Field Lab"
        cat = "chronicles"

    elif filename in ["IMG_20261016_061603.jpg", "IMG_20261016_061610.jpg", "IMG_20261016_061613.jpg", "IMG_20261016_061658.jpg", "IMG_20261016_061709.jpg"]:
        title = f"Vidarbha Landscape // Rural Transit Record #{filename[-6:-4]}"
        desc = ("The sweeping agricultural plains outside Chandrapur district, dotted with scrub forest and water tanks. "
                "Understanding the broader geography of the Tadoba corridor: how tiger habitats border human settlements and infrastructure. "
                "Reinforcing our motivation that individual animal re-identification is crucial for conflict mitigation and corridor protection.")
        stage = "Field Lab"
        cat = "chronicles"

    elif filename in ["IMG_20261016_070850.jpg", "IMG_20261016_070853.jpg", "IMG_20261016_070855.jpg", "IMG_20261016_070856.jpg"]:
        title = "Carriage Reverie // The Final Transit Hour"
        desc = ("07:08 AM: Teammates resting against the blue vinyl seats as the train neared the Ballarpur terminus. "
                "Conserving energy before 24 consecutive hours of coding, debugging, and system integration. "
                "The quiet focus of a team stepping into their first national hackathon arena.")
        stage = "Field Lab"
        cat = "chronicles"

    elif filename in ["IMG_20261016_071219.jpg", "IMG_20261016_071232.jpg", "IMG_20261016_074004.jpg", "IMG_20261016_074919.jpg", "IMG_20261016_075205.jpg", "IMG_20261016_075205_1.jpg", "IMG_20261016_075213.jpg", "IMG_20261016_075845.jpg"]:
        title = f"Arrival at Ballarpur Junction // Station Terminal #{filename[-6:-4]}"
        desc = ("Stepping off the train onto the Ballarpur platform with backpacks, laptop bags, and camera gear. "
                "The air was crisp and warm, carrying the distinct scent of dry deciduous forest and railway gravel. "
                "Destination reached: Ballarpur Institute of Technology and WILDHACK 2K26 were just a short drive away.")
        stage = "Field Lab"
        cat = "chronicles"

    # --- Category 3: Campus Arrival & Exploring the Grounds (IMG_20261016_094251 - 131054) ---
    elif filename in ["IMG_20261016_094251.jpg", "IMG_20261016_094252.jpg"]:
        title = "BIT Bamni Campus Grounds // Arrival & Orientation"
        desc = ("09:42 AM: Exploring the perimeter of Ballarpur Institute of Technology after registration. "
                "Taking in the campus architecture, meeting fellow shortlisted teams from across India, and scouting a quiet spot for the intensive sprint. "
                "The competition was officially real.")
        stage = "Field Lab"
        cat = "chronicles"

    elif filename in ["IMG_20261016_130645.jpg", "IMG_20261016_130646.jpg", "IMG_20261016_130653.jpg"]:
        title = "Pre-Hackathon Field Observation // Campus Biodiversity"
        desc = ("13:06 PM: Observing local campus biodiversity during an afternoon break before the opening ceremony. "
                "Taking close-up macro shots of foliage and insects, discussing how nature's markings — from tiger stripes to spider legs — serve as evolutionary identities. "
                "A candid reminder of why we care about wildlife conservation.")
        stage = "Field Lab"
        cat = "wildlife"

    elif filename in ["IMG_20261016_130711.jpg", "IMG_20261016_130719.jpg", "IMG_20261016_130724.jpg", "IMG_20261016_130725.jpg", "IMG_20261016_130733.jpg"]:
        title = "The Green Lynx Spider // An Encounter in the Grass"
        desc = ("A brilliant green Peucetia spider resting on a teammate's arm during a brief walk through the campus gardens. "
                "Noticing the red spots and banded spine patterns on its legs — a micro-demonstration of animal biometric uniqueness right on the venue grounds. "
                "Nature providing its own visual lessons in pattern recognition.")
        stage = "Individual"
        cat = "wildlife"

    elif filename == "IMG_20261016_131054.jpg":
        title = "Team HackOPs at BIT // Pre-Sprint Group Portrait"
        desc = ("13:10 PM: Hanshal, Vaishnav, Lokesh, and Soham gathered around the campus tire installation before the hackathon kickoff. "
                "Energy was high, smiles were genuine, and the shared anticipation was palpable. "
                "Four students united by computer science, wildlife, and an idea they refused to postpone any longer.")
        stage = "Field Lab"
        cat = "chronicles"

    # --- Category 4: Official Check-in, Badge & Briefing (IMG-20261016-WA00xx) ---
    elif filename in ["IMG-20261016-WA0002(1).jpeg", "IMG-20261016-WA0002.jpeg"]:
        title = "BIT Campus Entrance // Registration Check-in"
        desc = ("Arriving at the Ballarpur Institute of Technology registration gates with our credentials. "
                "Connecting with the organizing committee and checking into the official participant roster alongside 29 other finalist teams. "
                "The journey from a digital concept to an in-person offline challenge was now underway.")
        stage = "Field Lab"
        cat = "chronicles"

    elif filename == "IMG-20261016-WA0014.jpeg":
        title = "Auditorium Opening Briefing // Top 30 Finalists Assembled"
        desc = ("The main auditorium at BIT Bamni during the opening briefing with university leadership and TATR forest officials. "
                "Over 120 participants listening intently as the official problem statements and evaluation criteria were presented. "
                "The stage was set: 24 continuous hours on the clock.")
        stage = "Field Lab"
        cat = "chronicles"

    elif filename == "IMG-20261016-WA0016.jpeg":
        title = "Field Fuel // Hackathon Workstation Setup"
        desc = ("Setting up our desktop stations in the hackathon laboratory with power strips, monitors, and quick fuel. "
                "Organizing our shared Git repository, verifying CUDA drivers, and preparing local Blender automation scripts. "
                "Every minute of setup counted toward saving development time during the midnight crunch.")
        stage = "Field Lab"
        cat = "chronicles"

    elif filename == "IMG-20261016-WA0020.jpg":
        title = "WILDHACK 2K26 Official Badge // The Clock Begins"
        desc = ("The official participant identification badge and briefing document at BIT Bamni. "
                "Holding the badge that made our participation tangible: Team HackOPs officially entered into the 24-hour conservation challenge. "
                "It was time to build.")
        stage = "Field Lab"
        cat = "chronicles"

    elif filename in ["IMG-20261016-WA0023.jpeg", "IMG-20261016-WA0027.jpeg", "IMG-20261016-WA0030.jpeg", "IMG-20261016-WA0035.jpeg", "IMG-20261016-WA0036.jpeg"]:
        title = f"Hackathon Lab Session // Workspace Chronicle #{filename[-7:-5]}"
        desc = ("Working through the early evening sprint: laptops buzzing, tea glasses on the desks, and model weights downloading over local Wi-Fi. "
                "Vaishnav testing the synthetic forest generator while Soham and Lokesh built the telemetry ingestion interface. "
                "The rhythm of intense collaborative engineering in full swing.")
        stage = "Field Lab"
        cat = "chronicles"

    # --- Category 5: Midnight Sprint (IMG_20261017_025823 - 025833 & WA0004 - WA0006) ---
    elif filename in ["IMG-20261017-WA0004.jpeg", "IMG-20261017-WA0006.jpeg"]:
        title = "Midnight Fuel // Late-Night Coding Fuel"
        desc = ("01:30 AM: Late-night pizza boxes and snacks spread across the development table between laptops. "
                "Taking a fast five-minute break to eat before diving back into debugging segmentation memory leaks. "
                "The authentic culinary reality of 24-hour hackathon endurance.")
        stage = "Field Lab"
        cat = "chronicles"

    elif filename in ["IMG-20261017-WA0010.jpg", "IMG-20261017-WA0011.jpg"]:
        title = "Biometric Verification Channels // Prototype Interface"
        desc = ("Early morning prototype screen test: verifying multi-channel biometric displays for tiger stripe alignment. "
                "Checking whether the high-pass spatial filter accurately separated high-contrast stripes from background pelt coloration. "
                "Validating algorithmic outputs before integrating with the live dashboard.")
        stage = "Evidence"
        cat = "telemetry"

    elif filename == "IMG_20261017_025823.jpg":
        title = "The 02:58 AM Crucible // Late-Night Lab Endurance"
        desc = ("02:58 AM: The dead of night in the BIT campus lab room. "
                "Laptops running hot, code sketches on the bed, and teammates pushing through exhaustion to resolve coordinate unrolling bugs. "
                "The defining hour where we stripped away speculative microservices to make the core pipeline execute reliably.")
        stage = "Field Lab"
        cat = "chronicles"

    elif filename in ["IMG_20261017_025832.jpg", "IMG_20261017_025833.jpg"]:
        title = "Midnight Focus // Overcoming the Integration Bottleneck"
        desc = ("Power strips, cables, and code editors lit up in the dark at 02:58 AM. "
                "Chaining the segmentation mask into the pose estimator without memory crashes required manual garbage collection and leaner arrays. "
                "The gritty, unglamorous engineering that turned an ambitious concept into a working system.")
        stage = "Field Lab"
        cat = "chronicles"

    # --- Category 6: Morning Build Screenshots & Telemetry (Screenshot 2026-10-17 080835 - 114324) ---
    elif filename == "Screenshot 2026-10-17 080835.png":
        title = "Biometric Pipeline Channels // Feature Extraction Evidence"
        desc = ("08:08 AM: Live telemetry capture showing our 5-stage feature extraction workflow in action. "
                "From left to right: raw camera frame, high-precision segmentation mask, 3D pose skeletal keypoints, and normalized planar stripe vector. "
                "The technical foundation of WildID proven live on local test images.")
        stage = "Evidence"
        cat = "telemetry"

    elif filename == "Screenshot 2026-10-17 081004.png":
        title = "Planar Vector Representation // Stripe Geometry Map"
        desc = ("08:10 AM: Inspecting the unwrapped 2D fur-carpet coordinate space extracted from test plates. "
                "By flattening the animal's flank onto a standardized planar template, our model eliminated pose-induced distortions. "
                "This enabled vector similarity lookups to run in under 40 milliseconds against the stored database.")
        stage = "Evidence"
        cat = "telemetry"

    elif filename == "Screenshot 2026-10-17 095112.png":
        title = "Territory Roaming Polygons // Spatial Telemetry Engine"
        desc = ("09:51 AM: Testing the spatial roaming engine across Tadoba-Andhari Tiger Reserve sectors. "
                "Translating individual re-identification matches into dynamic convex hull territorial polygons on an interactive map. "
                "Proving that WildID goes beyond classification to provide longitudinal ecological intelligence.")
        stage = "Interpretation"
        cat = "telemetry"

    elif filename == "Screenshot 2026-10-17 100531.png":
        title = "Leaflet GIS Command Dashboard // Live Operations Center"
        desc = ("10:05 AM: The interactive WildID Operations Center running live with Leaflet GIS mapping. "
                "Range officers can inspect verified sightings, click on territorial centroids, and view historical movements across Moharli and Kolsa sectors. "
                "The centerpiece of our live presentation to the judging panel.")
        stage = "Interpretation"
        cat = "telemetry"

    elif filename in ["Screenshot 2026-10-17 103003.png", "Screenshot 2026-10-17 103438.png"]:
        title = "Ecological Corridor Analytics // Water Basin Correlation"
        desc = ("10:34 AM: Correlating tiger sighting densities with seasonal water availability along the Andheri River basin. "
                "Demonstrating how multi-observation telemetry flags potential territorial shifts caused by summer drought or prey migration. "
                "A decision-support tool tailored directly for forest conservators.")
        stage = "Interpretation"
        cat = "telemetry"

    elif filename in ["Screenshot 2026-10-17 112438.png", "Screenshot 2026-10-17 112519.png", "Screenshot 2026-10-17 112526.png", "Screenshot 2026-10-17 112541.png", "Screenshot 2026-10-17 114324.png"]:
        title = f"Territorial Boundary Mapping // GIS Sector Layer #{filename[-8:-4]}"
        desc = ("Final UI polishing of the GIS layer system: rendering boundary fences, water bodies, and core-buffer transitions. "
                "Ensuring that forest range officers can toggle reserve zoning with a single click and overlay sighting probability heatmaps. "
                "Built completely client-side for rapid deployment on field laptops without internet connectivity.")
        stage = "Interpretation"
        cat = "telemetry"

    # --- Category 7: The Judging Presentation (IMG_20261017_140321 - 140404 & WA0033-WA0038) ---
    elif filename == "IMG_20261017_140321.jpg":
        title = "14:03 PM Stage Defense // Presenting WildID to the Jury"
        desc = ("Team HackOPs on stage in the BIT auditorium presenting WildID live before the evaluation panel. "
                "Dressed in our black team jerseys, we chose to dedicate 27 out of our 30 minutes to demonstrating the working system rather than static slides. "
                "The defining presentation moment of our 24-hour journey.")
        stage = "Field Lab"
        cat = "chronicles"

    elif filename == "IMG_20261017_140322.jpg":
        title = "Stage Q&A // Defending the Algorithmic Pipeline"
        desc = ("Answering technical inquiries from faculty and judges regarding vector distance thresholds and pose invariance. "
                "Explaining how high-pass filtering eliminates pelt color variations while preserving bifurcations. "
                "An intense, intellectually invigorating technical defense.")
        stage = "Field Lab"
        cat = "chronicles"

    elif filename == "IMG_20261017_140326.jpg":
        title = "Live Dashboard Demonstration // The Jury Leans In"
        desc = ("Projecting the live Leaflet GIS dashboard on the auditorium screen as judges watched the system process test images in real time. "
                "Watching the markers update and candidate stripe similarities populate on screen validated our decision to build an end-to-end working prototype. "
                "A moment of immense pride for the entire team.")
        stage = "Field Lab"
        cat = "chronicles"

    elif filename in ["IMG_20261017_140327.jpg", "IMG_20261017_140328.jpg"]:
        title = "Team Unity on Stage // Explaining Forest Scalability"
        desc = ("The four members of Team HackOPs addressing the scalability of the architecture across other wild cat species. "
                "Explaining how the modular unwrapping framework can adapt to leopards and snow leopards with customized keypoint skeletons. "
                "Engaging in a genuine dialogue about the future of Indian conservation technology.")
        stage = "Field Lab"
        cat = "chronicles"

    elif filename == "IMG_20261017_140404.jpg":
        title = "Active Workstation Defense // Live Code Walkthrough"
        desc = ("Walking the judges through the actual Python codebase and local Blender rendering scripts on our laptops. "
                "Demonstrating that the workflow was fully operational and did not rely on pre-baked or hardcoded results. "
                "Transparency and technical rigor that earned the judges' respect.")
        stage = "Field Lab"
        cat = "chronicles"

    elif filename in ["IMG-20261017-WA0033.jpeg", "IMG-20261017-WA0035.jpeg", "IMG-20261017-WA0038.jpeg"]:
        title = f"Post-Presentation Decompression // Hall Reflections #{filename[-7:-5]}"
        desc = ("The immediate relief and exhilaration after concluding our 30-minute defense slot. "
                "Grabbing a snack in the auditorium corridor and discussing the judges' critique about synthetic data. "
                "Realizing that our prototype had sparked a serious conversation among conservation directors.")
        stage = "Field Lab"
        cat = "chronicles"

    # --- Category 8: Final Evaluations & Dusk Concludes (IMG_20261017_170741 - 182842) ---
    elif filename.startswith("IMG_20261017_170741") or "170818" in filename:
        title = "Auditorium Evaluations // Final Deliberations"
        desc = ("Late afternoon in the BIT auditorium as all 30 teams concluded their presentations and the jury entered deliberations. "
                "Networking with fellow builders from other states, exchanging GitHub handles, and discussing drone and acoustic conservation systems. "
                "The camaraderie of engineers united by a common challenge.")
        stage = "Field Lab"
        cat = "chronicles"

    elif filename in ["IMG_20261017_182836.jpg", "IMG_20261017_182841.jpg", "IMG_20261017_182842.jpg"]:
        title = "Dusk Over Tadoba Buffer // The 24 Hours Conclude"
        desc = ("18:28 PM: Evening twilight descending over the forest canopy outside the Ballarpur campus. "
                "The 24-hour development clock officially reached zero. "
                "Tired eyes, empty coffee cups, and a profound sense of accomplishment: we came to build a project, and we built something real.")
        stage = "Landscape"
        cat = "wildlife"

    # --- Category 9: Valedictory Ceremony & Special Mention (IMG_20261017_201650 - 205742 & WA0000) ---
    elif filename in ["IMG-20261018-WA0000(1)(1).jpg", "IMG-20261018-WA0000(1).jpg", "IMG-20261018-WA0000.jpg"]:
        title = "Podium Citation // Special Mention Award"
        desc = ("The official Special Mention citation and commemorative green ribbon medals awarded to Team HackOPs at WILDHACK 2K26. "
                "Recognized by university leaders and Tadoba-Andhari Tiger Reserve officials for architectural scalability and conservation ambition. "
                "A milestone that proved our direction was worth pursuing beyond the hackathon.")
        stage = "Field Lab"
        cat = "chronicles"

    elif filename in ["IMG_20261017_201650.jpg", "IMG_20261017_202252.jpg"]:
        title = "Valedictory Stage // The Announcement"
        desc = ("The auditorium stage during the valedictory ceremony as Team HackOPs was called up for the Special Mention award. "
                "Standing before our peers, university faculty, and forest conservators after 24 hours of relentless effort. "
                "Finishing outside the top three, but taking home the clearest possible roadmap for real-world deployment.")
        stage = "Field Lab"
        cat = "chronicles"

    elif filename in ["IMG_20261017_205727.jpg", "IMG_20261017_205731.jpg", "IMG_20261017_205733.jpg", "IMG_20261017_205742.jpg"]:
        title = "Dignitary Dialogue // Meeting Conservation Directors"
        desc = ("Conversing with Mr. Parag Gupta (Amazon Devices India) and Dr. Prabhunath Shukla (Field Director, TATR) following the ceremony. "
                "Discussing how machine learning can transition from academic demos into reliable field tools for tiger reserve range officers. "
                "An unforgettable evening that laid the groundwork for our future research ambitions.")
        stage = "Field Lab"
        cat = "chronicles"

    # --- Category 10: Post-Event Operations Review & Notes (Screenshot 2026-10-18 & image-xxx & file_xxx) ---
    elif filename in ["Screenshot 2026-10-18 212740.png", "Screenshot 2026-10-18 212753.png", "Screenshot 2026-10-18 212832.png"]:
        title = "WildID Operations Center // Longitudinal Telemetry Console"
        desc = ("Reviewing the WildID command interface following the hackathon: cataloging historical observations and territorial range integrity. "
                "The dashboard pairs computer vision detections with spatial GIS intelligence, enabling rangers to track individual animal vitality over time. "
                "The digital counterpart to field biology.")
        stage = "Interpretation"
        cat = "telemetry"

    elif filename in ["Screenshot 2026-10-18 212947.png", "Screenshot 2026-10-18 213000.png", "Screenshot 2026-10-18 213007.png"]:
        title = "Automated Anomaly Detection // Range Officer Intelligence"
        desc = ("Investigating automated anomaly triggers: alerting forest managers when a recorded individual's roaming perimeter shifts abruptly. "
                "Designed to surface potential cases of human-wildlife conflict or territorial displacement for human review. "
                "Technology serving the forest without replacing human expertise.")
        stage = "Interpretation"
        cat = "telemetry"

    elif filename in ["WA_1792133703926.jpeg", "WA_1792133716751.jpeg"]:
        title = "Post-Hackathon Dinner // Team HackOPs Celebration"
        desc = ("Sharing a celebratory meal after the closing ceremony in Ballarpur. "
                "Laughing over midnight bug scares, cold chai, and the thrill of seeing our pipeline work live on stage. "
                "The deep bond of four friends who tackled a challenge together and emerged with an enduring research project.")
        stage = "Field Lab"
        cat = "chronicles"

    elif filename in ["file_00000000403c8211ba3ceaec4ee43357.png", "file_00000000c8608207a074cefe37aa7074.png"]:
        title = "The Medals of WILDHACK // Tangible Validation"
        desc = ("Close-up view of the Special Mention commemorative medals and certificates draped on the presentation table. "
                "A tangible reminder that daring to take on an intimidating, unsolved conservation problem was worth every second of pressure. "
                "Not the finish line — a reason to keep going.")
        stage = "Field Lab"
        cat = "chronicles"

    elif filename == "file_00000000375c8211ac88027801cb7c94.png":
        title = "Avian Observer // Campus Wildlife Encounter"
        desc = ("A bright green passerine bird perched on the pathway outside the BIT computer center. "
                "Even amidst lines of Python and GPU fans, the wildlife of Central India was always right outside the window. "
                "Grounding our computational work in the physical reality of the natural world.")
        stage = "Individual"
        cat = "wildlife"

    elif filename == "file_000000004a74821197a0a9131e0c9c8d.png":
        title = "Lab Collaboration // Hackathon Final Hours"
        desc = ("Teams gathered around collaborative benches in the BIT computer center during the final hours of the sprint. "
                "Whiteboards filled with mathematical derivations, code reviews, and shared debugging sessions. "
                "The collective intellectual energy of 30 teams pushing the boundaries of conservation technology.")
        stage = "Field Lab"
        cat = "chronicles"

    elif filename in ["image-1792225801113.jpg", "image-1792226590858.jpg"]:
        title = "Ideation Blueprint // Handwritten Architectural Logic"
        desc = ("Late-night handwritten notes drafted during the initial design phase: breaking down the 'Why' of individual wildlife re-identification. "
                "Structuring the pipeline into discrete stages (segmentation, pose, unwrapping, matching) on paper before writing a single line of code. "
                "Where the architecture of WildID was born.")
        stage = "Field Lab"
        cat = "chronicles"

    elif filename.startswith("IMG_20261018_131943"):
        title = f"Post-Hackathon Reflections // Team HackOPs #{filename[-7:-4]}"
        desc = ("October 18 afternoon: Team HackOPs on the BIT grounds after a night of rest following the awards ceremony. "
                "Holding our certificates with pride, ready to begin the next chapter of WildID: assembling authentic camera-trap datasets. "
                "The 24 hours ended. The problem didn't.")
        stage = "Field Lab"
        cat = "chronicles"

    else:
        # Fallback using vision output
        title = f"Field Record // {filename}"
        if vision:
            desc = f"{vision} Documented during Team HackOPs' 24-hour sprint at WILDHACK 2K26."
        else:
            desc = "Authentic field documentation plate from Team HackOPs' 24-hour sprint at WILDHACK 2K26 in collaboration with Tadoba-Andhari Tiger Reserve."
        stage = item.get("stage", "Field Lab")
        cat = item.get("category", "chronicles")

    return title, desc, stage, cat

# Process all 130 records
updated_csv_rows = []
for item in data:
    title, desc, stage, cat = generate_kickass_entry(item)
    item["title"] = title
    item["claim"] = desc
    item["stage"] = stage
    item["category"] = cat
    
    # Assign clear descriptive category names
    if cat == "telemetry":
        item["categoryName"] = "Biometric & Telemetry Intelligence"
    elif cat == "wildlife":
        item["categoryName"] = "Wildlife & Habitat Observation"
    else:
        item["categoryName"] = "HackOps Field Chronicles"
        
    updated_csv_rows.append([item["filename"], desc])

# 1. Update gallery_data.json
with open(JSON_FILE, mode="w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
print(f"Updated {JSON_FILE} with {len(data)} bespoke descriptions.")

# 2. Update js/gallery_data.js
with open(JS_FILE, mode="w", encoding="utf-8") as f:
    f.write("// WildID — The Identity Atlas Gallery Manifest (Bespoke Editorial Descriptions)\n")
    f.write("window.WILDID_GALLERY = ")
    json.dump(data, f, indent=2)
    f.write(";\n")
print(f"Updated {JS_FILE} with {len(data)} bespoke descriptions.")

# 3. Update image_descriptions.csv
with open(CSV_INPUT, mode="w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(["image_name", "description"])
    for row in updated_csv_rows:
        writer.writerow(row)
print(f"Updated {CSV_INPUT} with {len(updated_csv_rows)} kickass descriptions.")

print("\nAll files successfully synchronized with kickass, non-generic descriptions!")
