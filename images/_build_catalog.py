#!/usr/bin/env python3
"""Build _catalog.json and _rename_plan.json for Entertainment Pros images."""
import json, os, re
from datetime import datetime, timezone

with open('/tmp/ep_originals.txt') as f:
    originals = [l.strip() for l in f if l.strip()]
with open('/tmp/ep_refs.json') as f:
    rd = json.load(f)
refs = rd['refs']
alts = rd['alts']
with open('/tmp/ep_dims.json') as f:
    dims = json.load(f)

skip = {'blog', 'button-widget-start-icon.svg', 'clicktocall-widget-icon.svg',
        'dm-common-icons.svg', 'dm-font.svg', 'dm-social-font.svg',
        'email-widget-icon.svg', 'map-widget-icon.svg', 'default-skin.svg',
        'menu-image1.jpg', 'preloader.gif', 'galleryLoader.gif',
        'spritesheet-2x.png', 'layers-2x.png', 'layers.png',
        'marker-icon-2x.png', 'marker-icon.png', 'marker-shadow.png',
        'tag-arrow-left.png', 'tag-arrow.png', 'default-skin.png',
        'icons@2x.png', 'imgPlaceholder1.png', 'imgPlaceholder2.png',
        'imgPlaceholder3.png', 'arrowBlackRight.png', 'aidsBg.png',
        'bg_37.png', 'pink_pattern.png', 'click2Call.jpg',
        'cyberMondayBg.jpg', 'halloween_call.jpg', 'holidaySnow.png',
        'smbSaturdayBg.jpg', 'thanksgivingBg.jpg', 'Trick-or-Treat.jpg',
        'sunset-hair.jpg', 'multi_137.jpg', 'site_background_education-2087x1173.jpg',
        'sectionImg5.jpg', 'download.png', 'download (12).png',
        'download (13).png', 'download (14).png', 'download (15).png',
        'download (16).png', 'download--2817-29.png', 'installation.png',
        'yelpLogo.png'}

brand_logos = {
    'epson.gif': 'Epson', 'lutron.gif': 'Lutron', 'monitor_audio.gif': 'Monitor Audio',
    'niles.gif': 'Niles Audio', 'peerless.gif': 'Peerless', 'samsung.gif': 'Samsung',
    'sonos.gif': 'Sonos', 'sony.gif': 'Sony', 'stealth_acoustics.gif': 'Stealth Acoustics',
    'urc.gif': 'Universal Remote Control', 'yamaha.gif': 'Yamaha',
    'lg.svg': 'LG', 'nice_elan.png': 'Elan / Nice', 'speakercraft.svg': 'SpeakerCraft',
    'svs.png': 'SVS', 'draper.png': 'Draper', 'draper.webp': 'Draper',
    'furman.svg': 'Furman', 'panamax.svg': 'Panamax', 'surgex.svg': 'SurgeX',
    'fxluminaire.jpg': 'FX Luminaire', 'fx -l logo.jpg': 'FX Luminaire',
    'Marine Corps Logo.jpg': 'United States Marine Corps',
    'Transparent Logo.png': 'Entertainment Pros',
    'EPLogo1200SmallStroke+copy.jpg': 'Entertainment Pros',
    'Entertainment Pros logo copy.png': 'Entertainment Pros',
    'Entertainment Pros logo.png': 'Entertainment Pros',
    'Landscape Lighting.gif': 'Landscape Lighting (animated banner)',
}

manual = {
    '1-177ec18b.jpg': dict(category='outdoor-av', tags=['outdoor','pool','luxury','waterfront','landscape','dock','patio'], subject='Waterfront luxury home with pool patio overlooking marina', alt_text='Waterfront luxury home with poolside patio and marina view', best_for=['outdoor av landing','about us','project showcase'], has_tv=False, indoor=False, outdoor=True, people=False, rename='waterfront-luxury-home-pool-patio-marina.jpg'),
    '1-3c00d43a.jpg': dict(category='brand-logo', tags=['logo','review','yelp'], subject='Yelp 5-star review badge', alt_text='Yelp 5-star review badge', best_for=['social proof','reviews section'], has_tv=False, indoor=False, outdoor=False, people=False, rename='yelp-5-star-review-badge.jpg'),
    '2-168358e2.jpg': dict(category='brand-logo', tags=['logo','google','review'], subject='Google My Business logo', alt_text='Google My Business logo', best_for=['social proof','reviews section'], has_tv=False, indoor=False, outdoor=False, people=False, rename='google-my-business-logo.jpg'),
    '3-78515fc2.jpg': dict(category='brand-logo', tags=['logo','facebook','review'], subject='Facebook 5-star review badge', alt_text='Facebook 5-star review badge', best_for=['social proof','reviews section'], has_tv=False, indoor=False, outdoor=False, people=False, rename='facebook-5-star-review-badge.jpg'),
    '20180315_102131 2.jpg': dict(category='surround-sound', tags=['tv','living-room','traditional','tower-speakers','subwoofer','entertainment-center','beach'], subject='Beach-themed living room with TV, tower speakers, and subwoofer', alt_text='Living room surround sound system with tower speakers and TV', best_for=['surround sound page','traditional living room example'], has_tv=True, indoor=True, outdoor=False, people=False, rename='beach-themed-living-room-surround-sound-tower-speakers.jpg'),
    '20191024_202332.jpg': dict(category='landscape-lighting', tags=['outdoor','night','holiday','colored-lights','palm-trees','luxury'], subject='Luxury home exterior with red and green LED palm tree lighting for the holidays', alt_text='Holiday red and green landscape lighting on luxury home', best_for=['holiday lighting','exterior illumination page','seasonal post'], has_tv=False, indoor=False, outdoor=True, people=False, rename='holiday-red-green-led-palm-tree-lighting-luxury-home.jpg'),
    '20200821_142850.jpg': dict(category='outdoor-av', tags=['outdoor','patio','pool','tv','outdoor-kitchen','pergola'], subject='Outdoor pool deck with multiple TVs over an outdoor bar/kitchen under a pergola', alt_text='Outdoor pool deck bar with multiple wall-mounted TVs', best_for=['outdoor av page','condo amenity case study'], has_tv=True, indoor=False, outdoor=True, people=False, rename='outdoor-pool-deck-bar-multiple-tvs-pergola.jpg'),
    '20201202_180550- 3.jpg': dict(category='tv-install', tags=['condo','luxury','glass','chandelier','dining-room','sunset','high-rise'], subject='High-rise luxury condo dining area with crystal chandelier overlooking sunset city view', alt_text='Luxury condo dining room with chandelier and panoramic sunset windows', best_for=['luxury condo page','automated shades page','about us hero'], has_tv=False, indoor=True, outdoor=False, people=False, rename='luxury-high-rise-condo-dining-chandelier-sunset.jpg'),
    '20210512_164435.jpg': dict(category='home-theater', tags=['theater-room','projector','colored-lights','star-ceiling','luxury'], subject='Dedicated home theater with star-field ceiling, magenta LED accents and projector', alt_text='Luxury home theater with starfield ceiling and magenta LED lighting', best_for=['home theater page','theater hero','LED tape lighting article'], has_tv=False, indoor=True, outdoor=False, people=False, rename='luxury-home-theater-starfield-ceiling-magenta-led.jpg'),
    '20210713_115656.jpg': dict(category='tools-process', tags=['tools','dropcloth','dewalt','clean','process'], subject='DeWalt power tools laid out on a quilted dropcloth before installation', alt_text='Professional installer tools laid out on protective dropcloth', best_for=['proven process page','about us','clean install blog'], has_tv=False, indoor=True, outdoor=False, people=False, rename='installer-tools-dewalt-dropcloth-clean-install.jpg'),
    '20210713_123352.jpg': dict(category='wiring-cleanup', tags=['wiring','clean','process','speaker-wall-plate','installer'], subject='Installer leveling a speaker wall plate during clean cable termination', alt_text='Installer leveling speaker wall plate during clean cable install', best_for=['wiring cleanup page','process detail'], has_tv=False, indoor=True, outdoor=False, people=True, rename='installer-leveling-speaker-wall-plate.jpg'),
    '20210713_142834-2e657fd1-f563d90b.jpg': dict(category='tv-install', tags=['tv','living-room','floating-shelves','clean','modern'], subject='Wall-mounted TV displaying cityscape between floating accent shelves over a wood console', alt_text='Wall-mounted TV with floating shelves above a wood entertainment console', best_for=['tv mounting page','condo TV page','clean install gallery'], has_tv=True, indoor=True, outdoor=False, people=False, rename='wall-mounted-tv-floating-shelves-wood-console.jpg'),
    '20210923_134158.jpg': dict(category='home-theater', tags=['theater-room','colored-lights','red-leds','recliners','large-screen','luxury'], subject='Dedicated home theater with red LED ceiling backlight, theater recliners and a giant front projection screen', alt_text='Dedicated home theater with red LED accents and projection screen', best_for=['home theater hero','luxury theater showcase'], has_tv=True, indoor=True, outdoor=False, people=False, rename='luxury-home-theater-red-led-ceiling-recliners-projection.jpg'),
    '20211111_211342.jpg': dict(category='landscape-lighting', tags=['outdoor','night','palm-trees','warm-white','curb-appeal'], subject='Single-story home with warm-white landscape lighting on palm trees and shrubs at night', alt_text='Warm-white landscape lighting on palm trees in front of home', best_for=['landscape lighting page','exterior illumination'], has_tv=False, indoor=False, outdoor=True, people=False, rename='warm-white-landscape-lighting-palm-trees-home.jpg'),
    '20220422_140110.jpg': dict(category='tv-install', tags=['tv','stone-wall','linear-fireplace','floating-shelves','pool-view','modern'], subject='Modern living room with stone-veneer feature wall, linear fireplace and TV, sliders to pool deck', alt_text='Modern living room TV mounted on stone wall with linear fireplace and pool view', best_for=['custom feature wall','luxury living page','tv install gallery'], has_tv=True, indoor=True, outdoor=False, people=False, rename='modern-living-room-stone-wall-tv-linear-fireplace-pool-view.jpg'),
    '20230327_205029-b8afab97.jpg': dict(category='home-theater', tags=['theater-room','wood-entertainment-center','recliners','colored-lights','traditional'], subject='Traditional home theater with built-in wood entertainment cabinetry, theater recliners and warm LED accents', alt_text='Traditional home theater room with wood built-ins and theater recliners', best_for=['home theater alternative','traditional theater design'], has_tv=True, indoor=True, outdoor=False, people=False, rename='traditional-home-theater-wood-built-ins-recliners.jpg'),
    '209447837_4873968955963165_3131736088981353353_n.jpg': dict(category='tv-install', tags=['motorized-mount','tv-lift','equipment','process'], subject='Rear view of TV on a motorized lift mechanism mid-install in a bedroom', alt_text='Motorized TV lift mechanism mid-installation', best_for=['motorized mount page','process detail'], has_tv=True, indoor=True, outdoor=False, people=False, rename='motorized-tv-lift-mechanism-mid-install-bedroom.jpg'),
    '3-4eaff711.jpg': dict(category='home-theater', tags=['media-room','projector','tufted-couch','tower-speakers','game-room','tricky-layout'], subject='Multipurpose media room with projector, tufted leather couch, tower speakers and ping-pong/pool game area', alt_text='Multipurpose media room with projector and game area', best_for=['tricky media room project','flex room','game room AV'], has_tv=False, indoor=True, outdoor=False, people=False, rename='multipurpose-media-room-projector-tufted-couch-game-area.jpg'),
    '6-30f94ff6.jpg': dict(category='tv-install', tags=['frame-tv','bedroom','condo','minimal','high-rise'], subject='Frame-style TV displaying art over a contemporary dresser in a high-rise condo bedroom', alt_text='Frame-style TV mounted in a contemporary condo bedroom', best_for=['frame tv','bedroom tv','condo bedroom'], has_tv=True, indoor=True, outdoor=False, people=False, rename='frame-tv-contemporary-condo-bedroom-dresser.jpg'),
    '6-6b0ad540.jpg': dict(category='tv-install', tags=['frame-tv','bedroom','condo','duplicate'], subject='Frame TV in condo bedroom (duplicate of 6-30f94ff6.jpg)', alt_text='Frame-style TV mounted in a contemporary condo bedroom', best_for=['frame tv','bedroom tv'], has_tv=True, indoor=True, outdoor=False, people=False, rename='frame-tv-contemporary-condo-bedroom-dresser-2.jpg'),
    '6-88d884f4-753aa3e7.jpg': dict(category='outdoor-av', tags=['outdoor','tv','marble','pergola','outdoor-kitchen','condo-amenity'], subject='Outdoor amenity area with TV mounted on porcelain feature wall over an outdoor kitchen with marble counters', alt_text='Outdoor patio TV on porcelain wall above outdoor kitchen', best_for=['outdoor av','commercial amenity'], has_tv=True, indoor=False, outdoor=True, people=False, rename='outdoor-amenity-tv-porcelain-wall-outdoor-kitchen.jpg'),
    '6-88d884f4-753aa3e7.png': dict(category='outdoor-av', tags=['outdoor','tv','marble','pergola','outdoor-kitchen','condo-amenity','duplicate'], subject='Same as 6-88d884f4-753aa3e7.jpg (PNG duplicate)', alt_text='Outdoor patio TV on porcelain wall above outdoor kitchen', best_for=['outdoor av'], has_tv=True, indoor=False, outdoor=True, people=False, rename='outdoor-amenity-tv-porcelain-wall-outdoor-kitchen.png'),
    '7-2afc1f2e.jpg': dict(category='tv-install', tags=['tv','stone-wall','large-format','in-ceiling-speakers','luxury'], subject='Large wall-mounted TV on dark stone-veneer feature wall with in-ceiling speakers', alt_text='Large TV on stone feature wall with in-ceiling speakers', best_for=['feature wall','tv install'], has_tv=True, indoor=True, outdoor=False, people=False, rename='large-tv-dark-stone-feature-wall-in-ceiling-speakers.jpg'),
    '7-e8dfeb48.jpg': dict(category='tv-install', tags=['tv','stone-wall','large-format','in-ceiling-speakers','duplicate'], subject='Same as 7-2afc1f2e.jpg', alt_text='Large TV on stone feature wall with in-ceiling speakers', best_for=['feature wall'], has_tv=True, indoor=True, outdoor=False, people=False, rename='large-tv-dark-stone-feature-wall-in-ceiling-speakers-2.jpg'),
    '8-273caddb.jpg': dict(category='tv-install', tags=['tv','wood-wall','custom-cabinetry','stone-wall','chandelier','luxury','entertainment-center'], subject='Luxury living room with custom wood entertainment center, mounted TV with LED backlight and stacked stone accent wall', alt_text='Luxury custom wood entertainment center with mounted TV', best_for=['luxury home page','custom cabinetry','hero image'], has_tv=True, indoor=True, outdoor=False, people=False, rename='luxury-custom-wood-entertainment-center-tv-led-backlight.jpg'),
    '8-def9127b.jpg': dict(category='tv-install', tags=['tv','wood-wall','custom-cabinetry','luxury','duplicate'], subject='Same as 8-273caddb.jpg', alt_text='Luxury custom wood entertainment center with mounted TV', best_for=['luxury home'], has_tv=True, indoor=True, outdoor=False, people=False, rename='luxury-custom-wood-entertainment-center-tv-led-backlight-2.jpg'),
    '9-398dd4c4.jpg': dict(category='tv-install', tags=['tv','bar','wine-cellar','wood-wall','luxury','entertainment'], subject='Home bar with mounted TV, glass wine cellar and floating shelves of premium liquor', alt_text='Luxury home bar with mounted TV and wine cellar', best_for=['bar AV','luxury home','entertaining space'], has_tv=True, indoor=True, outdoor=False, people=False, rename='luxury-home-bar-tv-wine-cellar-floating-shelves.jpg'),
    '9-c1b598ff-056b96a4.jpg': dict(category='decorative', tags=['blog-illustration','smashing-equipment','outdoor','jeep'], subject='Person using a chainsaw to destroy a damaged subwoofer in a driveway', alt_text='Demonstrating subwoofer destruction with a chainsaw outdoors', best_for=['field destroying equipment blog','humor blog'], has_tv=False, indoor=False, outdoor=True, people=True, rename='destroying-subwoofer-chainsaw-driveway-blog.jpg'),
    '9-79701556.png': dict(category='unknown', tags=['unknown'], subject='Unknown', alt_text='', best_for=[], has_tv=False, indoor=False, outdoor=False, people=False),
    '423036321_3535199346721358_7469586442484551707_n.jpg': dict(category='wiring-cleanup', tags=['new-construction','prewire','process','behind-the-scenes','luxury','waterfront'], subject='Studs-out new-construction interior during AV pre-wire phase of a custom waterfront home', alt_text='Custom waterfront home during AV pre-wire phase', best_for=['behind the scenes','prewire page','process'], has_tv=False, indoor=True, outdoor=False, people=False, rename='custom-waterfront-home-av-prewire-new-construction.jpg'),
    'AV Equipment and Installation for Unique Spaces (2).jpg': dict(category='commercial', tags=['unique-space','model-train','custom','dropcloth','project'], subject='Large model-train layout in a converted residential room (unique space project)', alt_text='Custom model train room AV install in a unique space', best_for=['unique spaces blog','specialty project'], has_tv=False, indoor=True, outdoor=False, people=False, rename='custom-model-train-room-av-install-unique-space.jpg'),
    'AV Sales and Installation Entertainment Pros (1)-18f43083.jpg': dict(category='home-theater', tags=['theater-room','blue-leds','recliners','colored-lights','luxury','large-screen'], subject='Dedicated home theater with deep blue LED ceiling accents and theater recliners', alt_text='Home theater with blue LED ceiling and theater recliners', best_for=['home theater page','luxury theater'], has_tv=True, indoor=True, outdoor=False, people=False, rename='home-theater-blue-led-ceiling-recliners.jpg'),
    'Condo TV (1)-275a1a5f.jpg': dict(category='tv-install', tags=['condo','bedroom','motorized-mount','tv-lift','automated','luxury'], subject='Luxury condo bedroom with motorized TV lift rising from foot of bed', alt_text='Motorized TV lift in a luxury condo bedroom', best_for=['motorized mount','condo bedroom','automation'], has_tv=True, indoor=True, outdoor=False, people=False, rename='motorized-tv-lift-luxury-condo-bedroom.jpg'),
    'Condo TV-b3d99dc7.jpg': dict(category='tv-install', tags=['frame-tv','condo','art-mode','wood-slat-wall','samsung'], subject='Samsung Frame TV in art-mode (Monet water lilies) on slatted wood wall in a condo', alt_text='Samsung Frame TV in art mode on slatted wood wall', best_for=['frame tv','condo tv','samsung'], has_tv=True, indoor=True, outdoor=False, people=False, rename='samsung-frame-tv-art-mode-wood-slat-wall-condo.jpg'),
    'DIY LED Tape Lighting vs. Professional Design.jpg': dict(category='landscape-lighting', tags=['indoor','led-tape','colored-lights','blog'], subject='LED tape lighting demonstration / blog hero', alt_text='DIY vs professional LED tape lighting comparison', best_for=['LED tape blog','lighting design'], has_tv=False, indoor=True, outdoor=False, people=False, rename='diy-vs-professional-led-tape-lighting.jpg'),
    'Gemini_Generated_Image_sx0wlcsx0wlcsx0w.png': dict(category='tv-install', tags=['frame-tv','bedroom','automated-shades','wallpaper','luxury','generated'], subject='Bedroom with frame TV showing Starry Night, automated shades half-down, statement wallpaper (AI-generated)', alt_text='Bedroom with frame TV and automated shades', best_for=['automated shades','bedroom tv','frame tv'], has_tv=True, indoor=True, outdoor=False, people=False, rename='ai-bedroom-frame-tv-starry-night-automated-shades.png'),
    'MC (2).jpg': dict(category='surround-sound', tags=['living-room','tv','entertainment-center','tower-speakers','subwoofer','plantation-shutters','traditional'], subject='Traditional living room with white built-in entertainment center, large TV, tower speakers and dual subwoofers', alt_text='Traditional living room with built-in entertainment center and full surround system', best_for=['surround page','traditional install','condo'], has_tv=True, indoor=True, outdoor=False, people=False, rename='traditional-living-room-white-entertainment-center-surround.jpg'),
    'Macleod (2)-fe55375d.jpg': dict(category='home-theater', tags=['theater-room','star-ceiling','colored-lights','purple-leds','front-projection','luxury','sconces'], subject='MacLeod luxury theater: purple LED ceiling, star ceiling, theater seating and front-projection screen', alt_text='MacLeod home theater with purple star ceiling and projection screen', best_for=['home theater hero','luxury theater'], has_tv=False, indoor=True, outdoor=False, people=False, rename='macleod-home-theater-purple-star-ceiling-projection.jpg'),
    'Magazine Sept.jpg': dict(category='tv-install', tags=['luxury','condo','high-rise','open-floor-plan','colored-lights','kitchen','tv','magazine-feature'], subject='Open-plan luxury condo with TV, kitchen island and lavender LED cove ceiling lighting (magazine featured)', alt_text='Magazine-featured luxury condo with TV and LED cove ceiling', best_for=['luxury condo','magazine feature'], has_tv=True, indoor=True, outdoor=False, people=False, rename='luxury-condo-open-plan-tv-led-cove-ceiling-magazine.jpg'),
    'Make Staying home Fun (Presentation (169)).jpg': dict(category='service-graphic', tags=['marketing','collage','blueprints','project'], subject='Marketing collage of waterfront home with equipment / blueprints', alt_text='Make Staying Home Fun campaign collage', best_for=['blog hero','marketing'], has_tv=False, indoor=False, outdoor=False, people=False, rename='make-staying-home-fun-marketing-collage.jpg'),
    'Screen Shot 2021-06-25 at 11.24.44 AM.png': dict(category='unknown', tags=['screenshot'], subject='Screenshot (likely social/marketing)', alt_text='', best_for=[], has_tv=False, indoor=False, outdoor=False, people=False),
    'TdZKdel5TzuaP9Erxsl3_Framed TVs.v2.0000000.jpg': dict(category='service-graphic', tags=['frame-tv','blog-hero','samsung'], subject='Stylized blog hero illustration about framed TVs', alt_text='Frame TVs blog hero illustration', best_for=['frame tv blog'], has_tv=True, indoor=True, outdoor=False, people=False, rename='framed-tvs-blog-hero-illustration.jpg'),
    'Untitled design (7)-6c31d3a0.jpg': dict(category='tv-install', tags=['frame-tv','bedroom','automated-shades','wallpaper','luxury'], subject='Luxury bedroom with frame TV, dramatic wallpaper accent wall, modern chandelier and automated shades', alt_text='Luxury bedroom with frame TV and automated shades', best_for=['automated shades','bedroom','luxury'], has_tv=True, indoor=True, outdoor=False, people=False, rename='luxury-bedroom-frame-tv-wallpaper-automated-shades.jpg'),
    'Untitled design (7)-843d99a6.jpg': dict(category='tv-install', tags=['frame-tv','bedroom','automated-shades','duplicate'], subject='Same as Untitled design (7)-6c31d3a0.jpg', alt_text='Luxury bedroom with frame TV and automated shades', best_for=['bedroom'], has_tv=True, indoor=True, outdoor=False, people=False, rename='luxury-bedroom-frame-tv-wallpaper-automated-shades-2.jpg'),
    'WhatsApp Image 2024-07-26 at 10.35.35 AM.jpeg': dict(category='tv-install', tags=['tv','wood-wall','custom-cabinetry','luxury','entertainment-center'], subject='Luxury living room with custom dark wood entertainment center, LED backlit, mounted TV', alt_text='Luxury wood entertainment center with mounted TV', best_for=['luxury home page','custom cabinetry'], has_tv=True, indoor=True, outdoor=False, people=False, rename='luxury-wood-entertainment-center-led-backlit-tv.jpeg'),
    'WhatsApp Image 2025-04-25 at 09.47.48.jpeg': dict(category='tv-install', tags=['frame-tv','condo','luxury','marble','wood-wall','foyer','high-rise'], subject='Luxury condo foyer/lounge with two recessed frame-style TVs displaying abstract art on wood feature walls', alt_text='Luxury condo foyer with twin frame TVs in wood feature walls', best_for=['luxury condo hero','frame tv','high-end'], has_tv=True, indoor=True, outdoor=False, people=False, rename='luxury-condo-foyer-twin-frame-tvs-wood-feature-walls.jpeg'),
    'WhatsApp Image 2025-09-26 at 09.53.14-9f0f9351.jpeg': dict(category='tv-install', tags=['luxury','condo','high-rise','kitchen','dining','ocean-view','chandelier','frame-tv'], subject='High-rise luxury condo with kitchen, dining and dramatic glass-bulb chandelier overlooking ocean view', alt_text='Luxury high-rise condo kitchen dining with ocean view', best_for=['luxury hero','condo','about us'], has_tv=True, indoor=True, outdoor=False, people=False, rename='luxury-high-rise-condo-kitchen-ocean-view-chandelier.jpeg'),
    'WhatsApp Image 2025-10-03 at 11.30.02.jpeg': dict(category='landscape-lighting', tags=['outdoor','night','colored-lights','red','blue','curb-appeal','holiday'], subject='Front of home illuminated with red and blue color-changing landscape lights at night', alt_text='Color-changing landscape lighting on home front at night', best_for=['exterior lighting','holiday lighting','color changing leds'], has_tv=False, indoor=False, outdoor=True, people=False, rename='red-blue-color-changing-landscape-lighting-home.jpeg'),
    'WhatsApp Image 2025-10-03 at 11.30.10.jpeg': dict(category='tv-install', tags=['frame-tv','condo','luxury','duplicate'], subject='Same scene as WhatsApp Image 2025-04-25 at 09.47.48 (luxury condo lounge with frame TVs)', alt_text='Luxury condo with frame TVs', best_for=['luxury condo'], has_tv=True, indoor=True, outdoor=False, people=False, rename='luxury-condo-foyer-twin-frame-tvs-2.jpeg'),
    'cO7Jpl1zQuuI0Qjakx7A_It’s more than hanging a TV (1).v2.0000000.jpg': dict(category='service-graphic', tags=['blog-hero','tv-mounting'], subject='Blog hero illustration "It\'s More Than Hanging a TV"', alt_text='Its more than hanging a TV blog hero', best_for=['tv mounting blog'], has_tv=True, indoor=True, outdoor=False, people=False, rename='its-more-than-hanging-a-tv-blog-hero.jpg'),
    'fx -l logo.jpg': dict(category='brand-logo', tags=['logo','fx-luminaire','landscape-lighting'], subject='FX Luminaire logo (variant)', alt_text='FX Luminaire logo', best_for=['brands'], has_tv=False, indoor=False, outdoor=False, people=False, rename='fx-luminaire-logo-variant.jpg'),
    'WhatsApp-Image-2025-09-26-at-10.02.01-833620c9.png': dict(category='tv-install', tags=['luxury','condo','tv','recent'], subject='Recent luxury condo project photo (Sept 26 2025 batch)', alt_text='Recent luxury condo project photo', best_for=['recent project','condo'], has_tv=True, indoor=True, outdoor=False, people=False, rename='luxury-condo-project-2025-09-26.png'),
    # Additional known images
    'Custom TV.jpg': dict(category='tv-install', tags=['luxury','condo','tv','wood-feature-wall','marble','indoor','living-room'], subject='Luxury condo TV mounted on a custom wood and marble feature wall', alt_text='Luxury condo TV on custom wood and marble entertainment wall', best_for=['home page hero','condo TV page','portfolio gallery'], has_tv=True, indoor=True, outdoor=False, people=False, rename='luxury-condo-tv-wood-marble-wall.jpg'),
    'Surround Systems (1).jpg': dict(category='surround-sound', tags=['tv','living-room','surround-speakers','tower-speakers','subwoofer'], subject='Living room with TV and full surround sound speaker setup', alt_text='Living room with TV and surround sound system', best_for=['surround sound page','living room example'], has_tv=True, indoor=True, outdoor=False, people=False, rename='living-room-tv-full-surround-sound.jpg'),
    'Surround Systems (2).jpg': dict(category='surround-sound', tags=['tv','living-room','surround-speakers'], subject='Living room surround sound install', alt_text='Living room surround sound', best_for=['surround sound page'], has_tv=True, indoor=True, outdoor=False, people=False, rename='living-room-surround-sound-2.jpg'),
    'Surround Systems (3).jpg': dict(category='surround-sound', tags=['tv','living-room','surround-speakers'], subject='Entertainment system design with surround sound', alt_text='Entertainment system design with surround sound', best_for=['surround sound','design page'], has_tv=True, indoor=True, outdoor=False, people=False, rename='entertainment-system-surround-sound-design.jpg'),
    'Surround Systems (4).jpg': dict(category='surround-sound', tags=['living-room','receiver','surround-speakers','subwoofer'], subject='Complete living room surround sound setup with receiver and speakers', alt_text='Complete living room surround sound setup with receiver and speakers', best_for=['surround sound page','equipment showcase'], has_tv=True, indoor=True, outdoor=False, people=False, rename='complete-living-room-surround-sound-receiver-speakers.jpg'),
    'Surround Systems.jpg': dict(category='surround-sound', tags=['surround-speakers','living-room','professional','luxury'], subject='Professional surround sound system installation in a Pinellas County home', alt_text='Professional surround sound system installation in a Pinellas County home', best_for=['surround sound','about'], has_tv=True, indoor=True, outdoor=False, people=False, rename='professional-surround-sound-pinellas-county.jpg'),
    'Corp Audio Video (1).jpg': dict(category='commercial', tags=['office','reception','tv','professional'], subject='Commercial reception area with professionally mounted wall TV', alt_text='Commercial reception area with professionally mounted wall TV', best_for=['commercial page','corporate AV'], has_tv=True, indoor=True, outdoor=False, people=False, rename='commercial-reception-area-mounted-wall-tv.jpg'),
    'Corp Audio Video (2).jpg': dict(category='commercial', tags=['office','training-room','multiple-monitors'], subject='Commercial training room with multiple screens for corporate presentations', alt_text='Commercial training room with multiple screens', best_for=['commercial page','training room'], has_tv=True, indoor=True, outdoor=False, people=False, rename='commercial-training-room-multiple-screens.jpg'),
    'Corp Audio Video (3).jpg': dict(category='commercial', tags=['office','conference-room','video-call'], subject='Conference room video calling and AV system installation', alt_text='Conference room video calling AV system', best_for=['commercial page','boardroom'], has_tv=True, indoor=True, outdoor=False, people=False, rename='conference-room-video-call-av-system.jpg'),
    'Corp Audio Video (4).jpg': dict(category='commercial', tags=['office','reception','tv'], subject='Professional reception area TV installation', alt_text='Professional reception area TV installation', best_for=['commercial page','reception'], has_tv=True, indoor=True, outdoor=False, people=False, rename='professional-reception-area-tv-install.jpg'),
    'Corp Automated shades.jpg': dict(category='commercial', tags=['boardroom','automated-shades','luxury','executive','lighting-control'], subject='Executive boardroom with automated motorized shades and lighting', alt_text='Automated motorized shades installation', best_for=['automated shades page','commercial page'], has_tv=False, indoor=True, outdoor=False, people=False, rename='executive-boardroom-automated-motorized-shades.jpg'),
    'Corp Custom.jpg': dict(category='commercial', tags=['lobby','school','academy','tv'], subject='Custom commercial AV install at Academy of Holy Names lobby', alt_text='Custom commercial AV install at Academy of Holy Names lobby', best_for=['commercial page','schools'], has_tv=True, indoor=True, outdoor=False, people=False, rename='academy-holy-names-lobby-tv-install.jpg'),
    'Corp Video Wall.JPG': dict(category='commercial', tags=['video-wall','office','large-format'], subject='Commercial video wall installation', alt_text='Commercial video wall installation', best_for=['commercial page','video wall'], has_tv=True, indoor=True, outdoor=False, people=False, rename='commercial-video-wall-install.jpg'),
    'Corp audio.jpg': dict(category='commercial', tags=['hangar','aviation','large-space'], subject='Aircraft hangar AV install for private aviation client', alt_text='Aircraft hangar AV installation', best_for=['commercial page','unique spaces'], has_tv=False, indoor=True, outdoor=False, people=False, rename='aircraft-hangar-av-install-private-aviation.jpg'),
    'MacLeod.jpg': dict(category='home-theater', tags=['theater-room','star-ceiling','purple-leds','recliners','luxury','front-projection'], subject='MacLeod dedicated home theater with purple LED ceiling and theater seating', alt_text='Transform Your Home Theater Experience with Entertainment Pros', best_for=['home theater hero','MacLeod project'], has_tv=False, indoor=True, outdoor=False, people=False, rename='macleod-home-theater-purple-led-ceiling.jpg'),
    'Invisible speakers.JPG': dict(category='surround-sound', tags=['invisible-speakers','living-room','luxury','stealth-acoustics'], subject='Living room with invisible speakers hidden behind walls', alt_text='Invisible speaker installation in a modern living room', best_for=['invisible speakers','stealth audio'], has_tv=True, indoor=True, outdoor=False, people=False, rename='invisible-speakers-modern-living-room.jpg'),
    'Outdoor Spaces (1).jpg': dict(category='outdoor-av', tags=['outdoor','pool','lanai','firepit','luxury'], subject='Outdoor pool/lanai with fire pit setup', alt_text='Boom For The Outdoor Room', best_for=['outdoor av','firepit space'], has_tv=False, indoor=False, outdoor=True, people=False, rename='outdoor-pool-lanai-firepit.jpg'),
    'gallery-1.jpeg': dict(category='tv-install', tags=['living-room','chandelier','luxury'], subject='Luxury living room with chandelier', alt_text='Residential AV installation', best_for=['gallery','luxury living'], has_tv=False, indoor=True, outdoor=False, people=False),
    'gallery-2.jpeg': dict(category='tv-install', tags=['marble','recessed-tv','luxury','wall-feature'], subject='Recessed TV installation in marble wall', alt_text='Recessed TV installation in marble wall', best_for=['gallery','luxury','feature wall'], has_tv=True, indoor=True, outdoor=False, people=False),
    'gallery-3.jpeg': dict(category='outdoor-av', tags=['outdoor','patio','tv'], subject='Outdoor patio TV installation', alt_text='Outdoor patio TV installation by Entertainment Pros', best_for=['outdoor av','gallery'], has_tv=True, indoor=False, outdoor=True, people=False),
    'gallery-4.jpeg': dict(category='outdoor-av', tags=['outdoor','patio','tv','duplicate'], subject='Duplicate of gallery-3.jpeg', alt_text='Outdoor patio TV installation', best_for=['outdoor av'], has_tv=True, indoor=False, outdoor=True, people=False),
    'gallery-5.jpeg': dict(category='tv-install', tags=['two-story','luxury','living-room','large-format'], subject='Two-story luxury living room with large wall-mounted TV', alt_text='Two-story luxury living room with large wall-mounted TV', best_for=['luxury living','hero','gallery'], has_tv=True, indoor=True, outdoor=False, people=False),
    'gallery-6.jpeg': dict(category='decorative', tags=['bathroom','luxury'], subject='Luxury bathroom (no TV)', alt_text='Luxury bathroom', best_for=['gallery'], has_tv=False, indoor=True, outdoor=False, people=False),
    'service-av.jpeg': dict(category='service-graphic', tags=['service-hero','av','planning'], subject='Audio-video planning and installation service hero', alt_text='Audio-video planning and installation', best_for=['service page','av service hero'], has_tv=True, indoor=True, outdoor=False, people=False),
    'service-theater.jpeg': dict(category='service-graphic', tags=['service-hero','entertainment-center','wood-wall','tv'], subject='Custom wood entertainment center with mounted TV and speakers', alt_text='Custom wood entertainment center with mounted TV and speakers', best_for=['service page','theater service'], has_tv=True, indoor=True, outdoor=False, people=False),
    'service-luxury.jpeg': dict(category='service-graphic', tags=['service-hero','luxury','art-deco','theater'], subject='Luxury art deco home theater conversion with premium AV equipment', alt_text='Luxury art deco home theater conversion', best_for=['luxury service','theater conversion'], has_tv=True, indoor=True, outdoor=False, people=False),
    'service-automation.jpeg': dict(category='service-graphic', tags=['service-hero','automation','smart-home','touchpanel'], subject='Smart home automation system with touch control panel', alt_text='Smart home automation system with touch control panel', best_for=['automation service'], has_tv=False, indoor=True, outdoor=False, people=False),
    'service-exterior.jpg': dict(category='service-graphic', tags=['service-hero','landscape-lighting','exterior'], subject='Landscape and exterior lighting service hero', alt_text='Landscape and exterior lighting', best_for=['exterior lighting service'], has_tv=False, indoor=False, outdoor=True, people=False),
    'service-lighting.jpg': dict(category='service-graphic', tags=['service-hero','lighting'], subject='Lighting service hero', alt_text='Lighting service', best_for=['lighting service'], has_tv=False, indoor=False, outdoor=False, people=False),
    'hero-luxury-av-hires.png': dict(category='tv-install', tags=['hero','luxury','condo','custom-wall','tv'], subject='Luxury condo AV installation with custom entertainment wall (high-res hero)', alt_text='Luxury condo AV installation with custom entertainment wall by Entertainment Pros', best_for=['home hero','luxury hero'], has_tv=True, indoor=True, outdoor=False, people=False),
    'hero-luxury-av.jpg': dict(category='tv-install', tags=['hero','luxury','condo','tv'], subject='Luxury condo AV hero photo', alt_text='Luxury condo AV', best_for=['home hero'], has_tv=True, indoor=True, outdoor=False, people=False),
    'hero-condo-av.jpeg': dict(category='tv-install', tags=['hero','condo','av','tv'], subject='Condo AV hero photo', alt_text='Condo AV hero', best_for=['condo page hero'], has_tv=True, indoor=True, outdoor=False, people=False),
    'hero-living-room.jpeg': dict(category='tv-install', tags=['hero','living-room','tv'], subject='Living room AV hero photo', alt_text='Living room AV', best_for=['home hero'], has_tv=True, indoor=True, outdoor=False, people=False),
    '708x606_about_us_firepit.jpg': dict(category='outdoor-av', tags=['firepit','pool','outdoor','luxury'], subject='Outdoor firepit and pool', alt_text='Entertainment Pros outdoor firepit AV installation', best_for=['about us','outdoor av'], has_tv=False, indoor=False, outdoor=True, people=False, rename='outdoor-firepit-pool-about-us.jpg'),
    '572x438_laprade.jpg': dict(category='tv-install', tags=['featured-project','tv','speakers','clean','white'], subject='Clean white speaker setup with wall-mounted TV', alt_text='Clean white speaker setup with wall-mounted TV by Entertainment Pros', best_for=['featured project','portfolio'], has_tv=True, indoor=True, outdoor=False, people=False, rename='laprade-clean-white-speakers-wall-mounted-tv.jpg'),
    '572x438_pearson.jpg': dict(category='tv-install', tags=['featured-project','entertainment-center','speakers','tv'], subject='Entertainment wall with integrated speakers and mounted display', alt_text='Entertainment wall with integrated speakers and mounted display', best_for=['featured project','portfolio'], has_tv=True, indoor=True, outdoor=False, people=False, rename='pearson-entertainment-wall-integrated-speakers.jpg'),
    '572x438_permuy.jpg': dict(category='tv-install', tags=['featured-project','contemporary','luxury'], subject='Sleek contemporary residential AV installation', alt_text='Sleek contemporary residential AV installation', best_for=['featured project','portfolio'], has_tv=True, indoor=True, outdoor=False, people=False, rename='permuy-contemporary-residential-av.jpg'),
    '572x438_macleod_closed.jpg': dict(category='surround-sound', tags=['featured-project','invisible-speakers','stealth'], subject='Stealth surround sound installation with hidden speakers', alt_text='Stealth surround sound installation with hidden speakers', best_for=['featured project','invisible speakers'], has_tv=True, indoor=True, outdoor=False, people=False, rename='macleod-stealth-surround-hidden-speakers.jpg'),
    '20240319_200635.jpg': dict(category='landscape-lighting', tags=['outdoor','night','colored-lights','tree','exterior'], subject='Colorful LED exterior tree lighting at night', alt_text='Colorful LED exterior tree lighting at night', best_for=['exterior lighting','color changing'], has_tv=False, indoor=False, outdoor=True, people=False, rename='colorful-led-exterior-tree-lighting-night.jpg'),
    '20240320_205836.jpg': dict(category='landscape-lighting', tags=['outdoor','night','colored-lights','palm-trees','teal','pink'], subject='Stunning teal and pink LED-lit palm trees at night', alt_text='Stunning teal and pink LED-lit palm trees at night', best_for=['color changing','exterior lighting'], has_tv=False, indoor=False, outdoor=True, people=False, rename='teal-pink-led-palm-trees-night.jpg'),
    '20240320_210308.jpg': dict(category='landscape-lighting', tags=['outdoor','night','colored-lights','palm-trees'], subject='Multicolor LED-lit palm trees viewed through window', alt_text='Multicolor LED-lit palm trees viewed through window', best_for=['exterior lighting'], has_tv=False, indoor=False, outdoor=True, people=False, rename='multicolor-led-palm-trees-through-window.jpg'),
    '20211111_211222 (1).jpg': dict(category='landscape-lighting', tags=['outdoor','night','palm-trees','warm-white','professional'], subject='Palm trees lit up with professional landscape lighting at night', alt_text='Palm trees lit up with professional landscape lighting at night', best_for=['landscape lighting','exterior'], has_tv=False, indoor=False, outdoor=True, people=False, rename='palm-trees-professional-landscape-lighting-night.jpg'),
    '20220421_110408.jpg': dict(category='tools-process', tags=['installer','ladder','tv-install','process'], subject='Entertainment Pros installer on ladder during professional TV wall mounting', alt_text='Entertainment Pros installer on ladder during professional TV wall mounting', best_for=['process','about us','team at work'], has_tv=True, indoor=True, outdoor=False, people=True, rename='installer-on-ladder-tv-wall-mount.jpg'),
    'Marine Corps Logo.jpg': dict(category='brand-logo', tags=['logo','usmc','military'], subject='United States Marine Corps emblem', alt_text='United States Marine Corps emblem', best_for=['veterans','about us'], has_tv=False, indoor=False, outdoor=False, people=False),
    'Van+Website+Picture.JPG': dict(category='team-van', tags=['van','team','branded-vehicle'], subject='Entertainment Pros service van', alt_text='Entertainment Pros service van', best_for=['about us','contact'], has_tv=False, indoor=False, outdoor=True, people=False, rename='entertainment-pros-service-van.jpg'),
    'van.jpg': dict(category='team-van', tags=['van','team','branded-vehicle'], subject='Entertainment Pros service van parked at customer', alt_text='Entertainment Pros service van parked at a customer', best_for=['about us','contact'], has_tv=False, indoor=False, outdoor=True, people=False),
    'For Sliding pictures         Home Automation             Control at the touch of a finger.-a42acc3e.jpg': dict(category='service-graphic', tags=['automation','touch-control','slider'], subject='Home automation slider image', alt_text='Home automation control at the touch of a finger', best_for=['automation page','slider'], has_tv=False, indoor=True, outdoor=False, people=False, rename='home-automation-touch-control-slider.jpg'),
    'For Sliding pictures    Lighting & Shades Control     save energy, add convenience, create ambiance..jpg': dict(category='service-graphic', tags=['lighting','shades','automation','slider'], subject='Lighting and shades control system slider image', alt_text='Lighting and shades control system for energy savings and ambiance', best_for=['automation','lighting service','slider'], has_tv=False, indoor=True, outdoor=False, people=False, rename='lighting-shades-control-slider.jpg'),
    'For sliding pictures          High Performance         Audio             Our most popular and luxurious product category.-335f5b94.jpg': dict(category='service-graphic', tags=['audio','high-performance','slider'], subject='High-performance audio slider image', alt_text='High-performance audio slider', best_for=['audio service','slider'], has_tv=False, indoor=True, outdoor=False, people=False, rename='high-performance-audio-slider.jpg'),
    'For sliding pictures          High Performance         Audio             Our most popular and luxurious product category..jpg': dict(category='service-graphic', tags=['audio','high-performance','slider','duplicate'], subject='Duplicate of For sliding pictures... High Performance Audio', alt_text='High-performance audio slider', best_for=['audio service','slider'], has_tv=False, indoor=True, outdoor=False, people=False, rename='high-performance-audio-slider-2.jpg'),
    'It-s more than hanging a TV.jpg': dict(category='tv-install', tags=['tv','clean-cabling','process'], subject='Professional TV installation with clean cable management', alt_text='Professional TV installation showcasing clean cable management and finished result', best_for=['tv mounting','process'], has_tv=True, indoor=True, outdoor=False, people=False, rename='professional-tv-install-clean-cable-management.jpg'),
    'Hanging-on-a-TV-mount-fde45019.png': dict(category='tv-install', tags=['blog-hero','articulating','tv-mount'], subject='Articulating TV wall mount reinstallation blog hero', alt_text='Articulating TV Wall Mount Reinstallation: Fixing a DIY Disaster', best_for=['articulating mount blog'], has_tv=True, indoor=True, outdoor=False, people=False, rename='articulating-tv-wall-mount-reinstallation-blog-hero.png'),
    'project-living-room-surround.jpeg': dict(category='surround-sound', tags=['project','living-room','surround','tv'], subject='Living room surround sound and TV project', alt_text='Living Room Surround Sound and TV Options', best_for=['portfolio','surround sound page'], has_tv=True, indoor=True, outdoor=False, people=False),
    'project-outdoor-sound.jpg': dict(category='outdoor-av', tags=['project','outdoor','speakers','backyard'], subject='Backyard outdoor sound system project', alt_text='1 Backyard, 3 Installs - Killer Outdoor Sound', best_for=['outdoor av','portfolio'], has_tv=False, indoor=False, outdoor=True, people=False),
    'project-ricky-ts.jpg': dict(category='surround-sound', tags=['project','ricky-t'], subject='Ricky T project', alt_text='Ricky T project photo', best_for=['portfolio'], has_tv=False, indoor=True, outdoor=False, people=False),
    'project-stealth-speakers.jpg': dict(category='surround-sound', tags=['project','invisible-speakers','stealth-acoustics'], subject='Invisible speakers with Stealth Acoustics', alt_text='Invisible Speakers with Stealth Acoustics', best_for=['invisible speakers','portfolio'], has_tv=False, indoor=True, outdoor=False, people=False),
    'project-tricky-media-room.jpg': dict(category='home-theater', tags=['project','media-room','flex-room'], subject='Tricky layout multi-purpose media room', alt_text='From Tricky Layout to Multi-Purpose Media Room', best_for=['portfolio','media room'], has_tv=False, indoor=True, outdoor=False, people=False),
    'project-when-work-goes-wrong.jpg': dict(category='wiring-cleanup', tags=['project','before','rescue'], subject='When work goes wrong - AV professionals matter', alt_text='When Work Goes Wrong - Why AV Pros Matter', best_for=['portfolio','av pros matter'], has_tv=False, indoor=True, outdoor=False, people=False),
    'WhatsApp-Image-2025-05-23-at-10.13.33.jpeg': dict(category='tv-install', tags=['recent','project'], subject='Recent project photo (May 23 2025)', alt_text='Recent project photo', best_for=['recent projects'], has_tv=False, indoor=True, outdoor=False, people=False, rename='project-photo-2025-05-23.jpeg'),
    'WhatsApp-Image-2024-07-26-at-10.58.03-AM.jpeg': dict(category='tv-install', tags=['recent','project'], subject='Recent project photo (July 26 2024)', alt_text='Recent project photo', best_for=['recent projects'], has_tv=False, indoor=True, outdoor=False, people=False, rename='project-photo-2024-07-26-1058.jpeg'),
    'WhatsApp-Image-2024-07-26-at-10.33.30-AM--281-29.jpeg': dict(category='tv-install', tags=['recent','project'], subject='Recent project photo (July 26 2024)', alt_text='Recent project photo', best_for=['recent projects'], has_tv=False, indoor=True, outdoor=False, people=False, rename='project-photo-2024-07-26-1033.jpeg'),
    'contemparary bollard light.jpg': dict(category='landscape-lighting', tags=['outdoor','bollard','garden','contemporary'], subject='Contemporary bollard path light in a garden setting', alt_text='Contemporary bollard path light in a garden setting', best_for=['landscape lighting','exterior'], has_tv=False, indoor=False, outdoor=True, people=False, rename='contemporary-bollard-path-light-garden.jpg'),
    'AV Equipment and Installation for Unique Spaces (3).jpg': dict(category='commercial', tags=['unique-space','model-train','project'], subject='Model train room install variant', alt_text='AV Equipment installation for unique spaces', best_for=['unique spaces blog'], has_tv=False, indoor=True, outdoor=False, people=False, rename='model-train-room-av-install-2.jpg'),
    'AV Installation Home Theaters Indoor and Outdoor Lighting Home Automation.png': dict(category='service-graphic', tags=['marketing','services','overview'], subject='Service overview marketing graphic', alt_text='AV installation, home theaters, indoor and outdoor lighting, home automation', best_for=['services overview'], has_tv=False, indoor=False, outdoor=False, people=False, rename='services-overview-marketing-graphic.png'),
    'Lighting Control.png': dict(category='service-graphic', tags=['icon','service','lighting'], subject='Lighting control service icon', alt_text='Professional lighting control system installation by Entertainment Pros', best_for=['service icons'], has_tv=False, indoor=False, outdoor=False, people=False),
    'Exterior Illumination.png': dict(category='service-graphic', tags=['icon','service','exterior'], subject='Exterior illumination service icon', alt_text='Thank You To Our Friends In Innisbrook For Inviting Us To Upgrade Their Exterior Lighting!', best_for=['service icons'], has_tv=False, indoor=False, outdoor=False, people=False),
    'Audio Visual.png': dict(category='service-graphic', tags=['icon','service','av'], subject='Audio visual service icon', alt_text='Audio visual service', best_for=['service icons'], has_tv=False, indoor=False, outdoor=False, people=False),
    'Commercial.png': dict(category='service-graphic', tags=['icon','service','commercial'], subject='Commercial service icon', alt_text='Commercial AV service', best_for=['service icons'], has_tv=False, indoor=False, outdoor=False, people=False),
    'Sales.png': dict(category='service-graphic', tags=['icon','service','sales'], subject='Sales service icon', alt_text='AV sales service', best_for=['service icons'], has_tv=False, indoor=False, outdoor=False, people=False),
    'Who Makes the Best Surround Sound System.jpg': dict(category='surround-sound', tags=['blog-hero','surround','installer'], subject='Surround sound and the art of setup blog hero', alt_text='Surround Sound and the Art of Setup: Where Tech Meets Configuration', best_for=['surround sound blog'], has_tv=True, indoor=True, outdoor=False, people=False, rename='surround-sound-art-of-setup-blog-hero.jpg'),
}

def slug(s):
    s2 = s.lower()
    s2 = re.sub(r'\.[a-z0-9]+$', '', s2)
    s2 = re.sub(r'[^a-z0-9]+', '-', s2)
    return s2.strip('-')

def categorize_by_filename(fn):
    low = fn.lower()
    base, ext = os.path.splitext(low)
    if fn in skip:
        return None
    if fn in brand_logos:
        return 'brand-logo'
    if ext == '.svg':
        return 'brand-logo' if ('logo' in low or fn in brand_logos) else 'decorative'
    if ext == '.gif':
        if base in ('preloader','galleryloader'):
            return None
        if 'landscape lighting' in low:
            return 'service-graphic'
        return 'brand-logo'
    if low.startswith('pexels-'):
        return 'decorative'
    if 'logo' in low:
        return 'brand-logo'
    blog_keywords = [
        ('tv-mounting-tips', 'tv-install'),
        ('tv-installation-and-mounting', 'tv-install'),
        ('articulating-tv-wall-mount', 'tv-install'),
        ('motorized-tv-mount', 'tv-install'),
        ('tv-articulating-full-motion', 'tv-install'),
        ('clean-home-av', 'wiring-cleanup'),
        ('easy-wiring-clean', 'wiring-cleanup'),
        ('structured-wiring', 'wiring-cleanup'),
        ('does-this-wiring-mess', 'wiring-cleanup'),
        ('cables-are-the-unsung', 'wiring-cleanup'),
        ('discrete-surround-sound', 'surround-sound'),
        ('comparing-a-sonos', 'surround-sound'),
        ('from-clutter-to-clarity', 'surround-sound'),
        ('entertainment-system-design', 'surround-sound'),
        ('sonos-samsung-oled', 'tv-install'),
        ('home-theater-upgrade', 'home-theater'),
        ('home-theaters-in-any-room', 'home-theater'),
        ('outdoor-living-elevated', 'outdoor-av'),
        ('superior-summer-entertainment', 'outdoor-av'),
        ('make-your-yard-rumble', 'outdoor-av'),
        ('pool-cage-lighting', 'landscape-lighting'),
        ('fx-luminaire', 'landscape-lighting'),
        ('diy-led-tape-lighting', 'landscape-lighting'),
        ('holiday-home-transformation', 'landscape-lighting'),
        ('remote-controlsclean', 'tv-install'),
        ('thank-you-', 'commercial'),
        ('tech-takedown', 'tools-process'),
        ('job-site-cleanliness', 'tools-process'),
        ('entertainment-pros-is-hiring', 'team-van'),
        ('entertainment-pros-named-samsung', 'brand-logo'),
        ('field-destroying-equipment', 'decorative'),
        ('signs-critters', 'wiring-cleanup'),
        ('reusing-your-old-av', 'wiring-cleanup'),
        ('issues-and-troubleshooting', 'wiring-cleanup'),
        ('trouble-shooting-an-audio', 'wiring-cleanup'),
        ('behind-the-scenes', 'wiring-cleanup'),
        ('upgrading-speakers-and-tvs', 'tv-install'),
    ]
    for kw, cat in blog_keywords:
        if kw in low:
            return cat
    if low.startswith('whatsapp'):
        return 'tv-install'
    if low.startswith('20'):
        return 'unknown'
    return None

images = []
renames = []
for fn in originals:
    if fn in skip:
        continue
    entry = {
        'filename': fn,
        'slug': slug(fn),
        'category': 'unknown',
        'tags': [],
        'subject': '',
        'alt_text': '',
        'dimensions': dims.get(fn),
        'best_for': [],
        'has_tv': False,
        'indoor': False,
        'outdoor': False,
        'people': False,
        'referenced_in': refs.get(fn, []),
    }
    rename_target = None
    if alts.get(fn):
        entry['alt_text'] = alts[fn][0]
        entry['subject'] = alts[fn][0]
    if fn in manual:
        m = dict(manual[fn])
        rename_target = m.pop('rename', None)
        for k, v in m.items():
            if k == 'tags':
                entry['tags'] = sorted(set(entry.get('tags', []) + v))
            else:
                entry[k] = v
    elif fn in brand_logos:
        entry['category'] = 'brand-logo'
        entry['tags'] = sorted(set(entry.get('tags', []) + ['logo','brand']))
        entry['subject'] = entry['subject'] or f"{brand_logos[fn]} brand logo"
        entry['alt_text'] = entry['alt_text'] or f"{brand_logos[fn]} logo"
        entry['best_for'] = ['brands page']
    else:
        cat = categorize_by_filename(fn)
        if cat:
            entry['category'] = cat
        low = fn.lower()
        tagmap = [
            ('outdoor','outdoor'),('pool','pool'),('patio','patio'),('lanai','lanai'),
            ('palm','palm-trees'),('night','night'),('holiday','holiday'),
            ('condo','condo'),('bedroom','bedroom'),('living','living-room'),
            ('theater','theater-room'),('boardroom','boardroom'),
            ('office','office'),('restaurant','restaurant'),
            ('hangar','hangar'),('lobby','lobby'),
            ('luxury','luxury'),('marble','marble'),
            ('chandelier','chandelier'),('shades','automated-shades'),
            ('motorized','motorized-mount'),('lift','tv-lift'),
            ('frame','frame-tv'),('invisible','invisible-speakers'),
            ('subwoofer','subwoofer'),('projector','projector'),('screen','screen'),
            ('rack','equipment-rack'),('remote','remote'),
            ('clean','clean'),('messy','messy'),('before','before'),('after','after'),
            ('led','colored-lights'),
        ]
        for kw, t in tagmap:
            if kw in low:
                entry['tags'].append(t)
        if ' tv' in low or '-tv' in low or 'tv-' in low or low.startswith('tv'):
            entry['has_tv'] = True
        entry['tags'] = sorted(set(entry['tags']))
    if not entry['best_for'] and entry['referenced_in']:
        entry['best_for'] = [r.replace('.html','').replace('-',' ') for r in entry['referenced_in'][:3]]
    images.append(entry)
    # Rename plan
    needs_rename = False
    # Add rename if filename is unfriendly
    bad = (re.match(r'^\d+-[0-9a-f]+', fn) or  # hash names
           fn.startswith(('1-','2-','3-','4-','5-','6-','7-','8-','9-')) or
           fn.startswith('20') or # date prefix
           fn.lower().startswith('whatsapp') or
           fn.startswith(('209447','423036','423568','423619','423735')) or
           fn.startswith('Untitled') or fn.startswith('Gemini_') or
           fn.startswith('Screen Shot') or fn.startswith('TdZ') or
           fn.startswith('cO7Jpl') or fn.startswith('For Sliding') or
           fn.startswith('For sliding') or
           fn.startswith('AV Sales') or fn.startswith('Magazine') or
           fn.startswith('Make Staying') or
           fn.startswith('MC ') or fn.startswith('Macleod (') or
           ' (' in fn or '+' in fn)
    if rename_target:
        renames.append({'old': fn, 'new': rename_target, 'referenced_in': refs.get(fn, [])})
    elif bad:
        # auto-suggest from slug
        new = slug(fn)
        ext = os.path.splitext(fn)[1].lower()
        if ext == '.jpeg': ext = '.jpg'
        renames.append({'old': fn, 'new': new + ext, 'referenced_in': refs.get(fn, [])})

cat_count = {}
for i in images:
    cat_count[i['category']] = cat_count.get(i['category'], 0) + 1

catalog = {
    'version': 1,
    'generated_at': datetime.now(timezone.utc).isoformat(),
    'image_count': len(images),
    'images': images,
}
out_path = '/Users/justinbabcock/Desktop/Websites/Entertainment Pros/modernized/images/_catalog.json'
with open(out_path, 'w') as f:
    json.dump(catalog, f, indent=2)
print('Wrote', out_path)
print('Image count:', len(images))
print('Categories:')
for k, v in sorted(cat_count.items(), key=lambda x: -x[1]):
    print(f'  {k}: {v}')

rp_path = '/Users/justinbabcock/Desktop/Websites/Entertainment Pros/modernized/images/_rename_plan.json'
with open(rp_path, 'w') as f:
    json.dump({'renames': renames, 'count': len(renames)}, f, indent=2)
print('Wrote rename plan with', len(renames), 'entries to', rp_path)
