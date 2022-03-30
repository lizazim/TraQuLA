#!/usr/bin/env python3
# -*- coding: utf-8 -*-

path = pathlib.Path(__file__).parent.absolute() 
exec(open(str(path) + "/src/Properties_Verbalisations.py").read())

properties_dict = {}

with open(str(path) + "/src/Properties.txt", "r") as f:
  lines = f.readlines()
  for l in lines:
    l = l.strip()
    matches = re.search('(.*?) = (.*?) "(.*?)" ;$', l)
    if matches == None:
      pass
    else:
      prop = matches.group(3)
      prop_function = matches.group(1)
      if prop_function.startswith("--"):
        pass
      else:
        prop_words = prop.split()
        first_word_of_prop = prop_words[0].lower()
        if first_word_of_prop in properties_dict:
          if prop in properties_dict[first_word_of_prop]:
            if prop_function in properties_dict[first_word_of_prop][prop]:
              pass
            else:
              properties_dict[first_word_of_prop][prop] = properties_dict[first_word_of_prop][prop] + [prop_function]
          else:
            properties_dict[first_word_of_prop][prop] = [prop_function]
        else:
          properties_dict[first_word_of_prop] = {prop: [prop_function]}

properties_dict["country"]["country"] = ['country_O', 'country_P', 'locationCountry_P']
properties_dict["location"]["location country"] = ['country_O', 'country_P', 'locationCountry_P']
properties_dict["starring"]["starring"] = ['starring_O', 'starring_P']
properties_dict["alma"]["alma mater"] = ['almaMater_O', 'almaMater_P']
properties_dict["birth"]["birth place"] = ['birthPlace_O', 'birthPlace_P']
properties_dict["prizes"] = {"prizes" : ['prizes_P']}
properties_dict["married"]["married"] = ['spouse_O', 'spouse_P', 'married_P']
properties_dict["married"]["married to"] = ['spouse_O', 'spouse_P', 'married_P', 'partner_O', 'partner_P']
properties_dict["marrying"] = {"marrying" : ['spouse_O', 'spouse_P', 'married_P']}
properties_dict["marry"] = {"marry" : ['spouse_O', 'spouse_P', 'married_P']}
properties_dict["marries"] = {"marries" : ['spouse_O', 'spouse_P', 'married_P']}
properties_dict["spouse"] = {"spouse" : ['spouse_O', 'spouse_P', 'married_P']}
properties_dict["placed"] = {'placed' : ["locationCity_O", "locationCity_P", "location_O", "location_P", 'locations_P', "city_O", "city_P", "county_O", "county_P", "state_O", "state_P", "province_O", "province_P", "region_O", "region_P", "district_O", "district_P", "territory_O", "territory_P", "based_P", "basedOn_O", "basedOn_P", "basedAt_P"], 'placed at' : ["locationCity_O", "locationCity_P", "location_O", "location_P", 'locations_P', "city_O", "city_P", "county_O", "county_P", "state_O", "state_P", "province_O", "province_P", "region_O", "region_P", "district_O", "district_P", "territory_O", "territory_P", "based_P", "basedOn_O", "basedOn_P", "basedAt_P"], 'placed in' : ["locationCity_O", "locationCity_P", "location_O", "location_P", 'locations_P', "city_O", "city_P", "county_O", "county_P", "state_O", "state_P", "province_O", "province_P", "region_O", "region_P", "district_O", "district_P", "territory_O", "territory_P", "based_P", "basedOn_O", "basedOn_P", "basedAt_P"]}
properties_dict["based"] = {'based' : ["locationCity_O", "locationCity_P", "location_O", "location_P", 'locations_P', "city_O", "city_P", "county_O", "county_P", "state_O", "state_P", "province_O", "province_P", "region_O", "region_P", "district_O", "district_P", "territory_O", "territory_P", "based_P", "basedOn_O", "basedOn_P", "basedAt_P"], 'based on' : ["locationCity_O", "locationCity_P", "location_O", "location_P", 'locations_P', "city_O", "city_P", "county_O", "county_P", "state_O", "state_P", "province_O", "province_P", "region_O", "region_P", "district_O", "district_P", "territory_O", "territory_P", "based_P", "basedOn_O", "basedOn_P", "basedAt_P"], 'based at' : ["locationCity_O", "locationCity_P", "location_O", "location_P", 'locations_P', "city_O", "city_P", "county_O", "county_P", "state_O", "state_P", "province_O", "province_P", "region_O", "region_P", "district_O", "district_P", "territory_O", "territory_P", "based_P", "basedOn_O", "basedOn_P", "basedAt_P"], 'based in' : ["locationCity_O", "locationCity_P", "location_O", "location_P", 'locations_P', "city_O", "city_P", "county_O", "county_P", "state_O", "state_P", "province_O", "province_P", "region_O", "region_P", "district_O", "district_P", "territory_O", "territory_P", "based_P", "basedOn_O", "basedOn_P", "basedAt_P"]}
properties_dict["founded"] = {'founded title': ['foundedTitle_P'], 'founded on': ['foundedOn_P', 'foundation_O', 'foundation_P', 'founded_P'], 'founded': ['founder_O', 'founder_P', 'foundedBy_O', 'foundedBy_P', 'founded_P', 'discoverer_O', 'discoverer_P', 'foundedIn_P', 'foundationPlace_O', 'foundationPlace_P', 'foundation_O', 'foundation_P', 'foundedPlace_P', 'foundedDate_P'], 'founded by': ['founder_O', 'founder_P', 'foundedBy_O', 'foundedBy_P', 'founded_P', 'discoverer_O', 'discoverer_P'], 'founded date': ['foundedDate_P'], 'founded in': ['foundedIn_P', 'founder_O', 'founder_P', 'foundedBy_O', 'foundedBy_P', 'founded_P', 'discoverer_O', 'discoverer_P', 'foundationPlace_O', 'foundationPlace_P', 'foundation_O', 'foundation_P', 'foundedPlace_P', 'foundedDate_P'], 'founded place': ['foundedPlace_P', 'foundationPlace_O', 'foundationPlace_P', 'foundation_O', 'foundation_P']}
properties_dict["found"] = {"found" : ['founder_P', 'founder_O', 'foundedBy_O', 'founded_P', 'discoverer_O', 'discoverer_P', 'foundationPlace_O', 'foundationPlace_P', 'foundation_O', 'foundation_P', 'foundedOn_P', 'foundedIn_P', 'foundedPlace_P', 'foundedDate_P']}
properties_dict["founds"] = {"founds" : ['founder_P', 'founder_O', 'foundedBy_O', 'founded_P', 'discoverer_O', 'discoverer_P', 'foundationPlace_O', 'foundationPlace_P', 'foundation_O', 'foundation_P', 'foundedOn_P', 'foundedIn_P', 'foundedPlace_P', 'foundedDate_P']}
properties_dict["founding"] = {"founding" : ['founder_P', 'founder_O', 'foundedBy_O', 'founded_P', 'discoverer_O', 'discoverer_P', 'foundationPlace_O', 'foundationPlace_P', 'foundation_O', 'foundation_P', 'foundedOn_P', 'foundedIn_P', 'foundedPlace_P', 'foundedDate_P']}
del properties_dict["many"] 
del properties_dict["person"] 
del properties_dict["mother"]["mother name"]

verbs = {}
ivps = {}
for key in prop_functions.keys():
  prop_words = key.split("_")[:-1]
  ending = key.split("_")[-1]
  if ending in ["V", "V2"]:
    verbs[key] = prop_functions[key]
  elif ending in ["IVPS", "IVP", "PP"]:
    ivps[key] = prop_functions[key]
  else:
    prop_str = " ".join(prop_words)
    first_word_of_prop = prop_words[0].lower()

    functions = []
    for p in prop_functions[key]:
      link = p[0].replace("SLASH", "/")
      if link.startswith("http://dbpedia.org/ontology/"):
        functions.append(link[28:] + "_O")
      elif link.startswith("http://dbpedia.org/property/"):
        functions.append(link[28:] + "_P")
    if first_word_of_prop in properties_dict:
      if prop_str in properties_dict[first_word_of_prop]:
        for p in functions:
          if p in properties_dict[first_word_of_prop][prop_str]:
            pass
          else:
            properties_dict[first_word_of_prop][prop_str] = properties_dict[first_word_of_prop][prop_str] + [p]
          new_functions = []
          for p in properties_dict[first_word_of_prop][prop_str]:
            if p.endswith("Prop"):
              pass
            else:
              new_functions.append(p)
          properties_dict[first_word_of_prop][prop_str] = new_functions
      else:
        properties_dict[first_word_of_prop][prop_str] = functions
    else:
      properties_dict[first_word_of_prop] = {prop_str: functions}

verbs_dict = {}
verbs_dict["begin"] = {"begin" : ['source_O', 'source_P', 'origin_O', 'origin_P']}
verbs_dict["begins"] = {"begins" : ['source_O', 'source_P', 'origin_O', 'origin_P']}
verbs_dict["began"] = {"began" : ['source_O', 'source_P', 'origin_O', 'origin_P']}
verbs_dict["begun"] = {"begun" : ['source_O', 'source_P', 'origin_O', 'origin_P']}
verbs_dict["beginning"] = {"beginning" : ['source_O', 'source_P', 'origin_O', 'origin_P']}
verbs_dict["broadcast"] = {"broadcast" : ['network_O', 'network_P', 'channel_O', 'channel_P']}
verbs_dict["broadcasts"] = {"broadcasts" : ['network_O', 'network_P', 'channel_O', 'channel_P']}
verbs_dict["broadcasted"] = {"broadcasted" : ['network_O', 'network_P', 'channel_O', 'channel_P']}
verbs_dict["broadcasting"] = {"broadcasting" : ['network_O', 'network_P', 'channel_O', 'channel_P']}
verbs_dict["associate"] = {"associate" : ['associate_O', 'associatedMusicalArtist_O', 'associatedBand_O', 'associatedActs_P']}
verbs_dict["associates"] = {"associates" : ['associate_O', 'associatedMusicalArtist_O', 'associatedBand_O', 'associatedActs_P']}
verbs_dict["associated"] = {"associated" : ['associate_O', 'associatedMusicalArtist_O', 'associatedBand_O', 'associatedActs_P']}
verbs_dict["associating"] = {"associating" : ['associate_O', 'associatedMusicalArtist_O', 'associatedBand_O', 'associatedActs_P']}
verbs_dict["authore"] = {"authore" : ['writer_O', 'writer_P', 'author_O', 'author_P', 'composer_O', 'composer_P', 'creator_P', 'creator_O', 'musicBy_O', 'musicBy_P']}
verbs_dict["authores"] = {"authores" : ['writer_O', 'writer_P', 'author_O', 'author_P', 'composer_O', 'composer_P', 'creator_P', 'creator_O', 'musicBy_O', 'musicBy_P']}
verbs_dict["authored"] = {"authored" : ['writer_O', 'writer_P', 'author_O', 'author_P', 'composer_O', 'composer_P', 'creator_P', 'creator_O', 'musicBy_O', 'musicBy_P']}
verbs_dict["authoring"] = {"authoring" : ['writer_O', 'writer_P', 'author_O', 'author_P', 'composer_O', 'composer_P', 'creator_P', 'creator_O', 'musicBy_O', 'musicBy_P']}
verbs_dict["marry"] = {"marry" : ['spouse_P', 'spouse_O', 'partner_O', 'partner_P']}
verbs_dict["marries"] = {"marries" : ['spouse_P', 'spouse_O', 'partner_O', 'partner_P']}
verbs_dict["married"] = {"married" : ['spouse_P', 'spouse_O', 'partner_O', 'partner_P']}
verbs_dict["marrying"] = {"marrying" : ['spouse_P', 'spouse_O', 'partner_O', 'partner_P']}
verbs_dict["produce"] = {"produce" : ['producer_O', 'producer_P', 'product_O', 'developer_O', 'developer_P', 'creator_O', 'creator_P', 'manufacturer_O', 'manufacturer_P', 'designer_O', 'designer_P']}
verbs_dict["produces"] = {"produces" : ['producer_O', 'producer_P', 'product_O', 'developer_O', 'developer_P', 'creator_O', 'creator_P', 'manufacturer_O', 'manufacturer_P', 'designer_O', 'designer_P']}
verbs_dict["produced"] = {"produced" : ['producer_O', 'producer_P', 'product_O', 'developer_O', 'developer_P', 'creator_O', 'creator_P', 'manufacturer_O', 'manufacturer_P', 'designer_O', 'designer_P'], "produced by" : ['producer_O', 'producer_P', 'product_O', 'developer_O', 'developer_P', 'creator_O', 'creator_P', 'manufacturer_O', 'manufacturer_P', 'designer_O', 'designer_P']}
verbs_dict["producing"] = {"producing" : ['producer_O', 'producer_P', 'product_O', 'developer_O', 'developer_P', 'creator_O', 'creator_P', 'manufacturer_O', 'manufacturer_P', 'designer_O', 'designer_P']}
verbs_dict["present"] = {"present" : ['presenter_O', 'presenter_P']}
verbs_dict["presents"] = {"presents" : ['presenter_O', 'presenter_P']}
verbs_dict["presented"] = {"presented" : ['presenter_O', 'presenter_P'], "presented by" : ['presenter_O', 'presenter_P']}
verbs_dict["presenting"] = {"presenting" : ['presenter_O', 'presenter_P']}
verbs_dict["build"] = {"build" : ['builder_O', 'manufacturer_O', 'manufacturer_P', 'builder_P']}
verbs_dict["builds"] = {"builds" : ['builder_O', 'manufacturer_O', 'manufacturer_P', 'builder_P']}
verbs_dict["built"] = {"built" : ['builder_O', 'manufacturer_O', 'manufacturer_P', 'builder_P', 'built_P'], "built by" : ['builder_O', 'manufacturer_O', 'manufacturer_P', 'builder_P']}
verbs_dict["building"] = {"building" : ['builder_O', 'manufacturer_O', 'manufacturer_P', 'builder_P']}
verbs_dict["influence"] = {"influence" : ['influenced_P', 'influenced_O', 'influencedBy_P', 'influencedBy_O', 'influences_P', 'basedOn_O', 'basedOn_P', 'stylisticOrigin_O', 'stylisticOrigin_P']}
verbs_dict["influences"] = {"influences" : ['influenced_P', 'influenced_O', 'influencedBy_P', 'influencedBy_O', 'influences_P', 'basedOn_O', 'basedOn_P', 'stylisticOrigin_O', 'stylisticOrigin_P']}
verbs_dict["influenced"] = {"influenced" : ['influenced_P', 'influenced_O', 'influencedBy_P', 'influencedBy_O', 'influences_P', 'basedOn_O', 'basedOn_P', 'stylisticOrigin_O', 'stylisticOrigin_P'], "influenced by" : ['influenced_P', 'influenced_O', 'influencedBy_P', 'influencedBy_O', 'influences_P', 'basedOn_O', 'basedOn_P', 'stylisticOrigin_O', 'stylisticOrigin_P']}
verbs_dict["influencing"] = {"influencing" : ['influenced_P', 'influenced_O', 'influencedBy_P', 'influencedBy_O', 'influences_P', 'basedOn_O', 'basedOn_P', 'stylisticOrigin_O', 'stylisticOrigin_P']}
verbs_dict["maintain"] = {"maintain" : ['maintainedBy_O', 'owner_O', 'owningOrganisation_O', 'occupation_O', 'authority_O', 'field_P', 'parent_P', 'owners_P', 'owningCompany_O', 'system_P', 'arena_P', 'owned_P', 'parentOrganisation_O', 'parentCompany_O', 'ground_P', 'stadium_P', 'company_P', 'network_O', 'foundedBy_O', 'foundedBy_P']}
verbs_dict["maintains"] = {"maintains" : ['maintainedBy_O', 'owner_O', 'owningOrganisation_O', 'occupation_O', 'authority_O', 'field_P', 'parent_P', 'owners_P', 'owningCompany_O', 'system_P', 'arena_P', 'owned_P', 'parentOrganisation_O', 'parentCompany_O', 'ground_P', 'stadium_P', 'company_P', 'network_O', 'foundedBy_O', 'foundedBy_P']}
verbs_dict["maintained"] = {"maintained" : ['maintainedBy_O', 'owner_O', 'owningOrganisation_O', 'occupation_O', 'authority_O', 'field_P', 'parent_P', 'owners_P', 'owningCompany_O', 'system_P', 'arena_P', 'owned_P', 'parentOrganisation_O', 'parentCompany_O', 'ground_P', 'stadium_P', 'company_P', 'network_O', 'foundedBy_O', 'foundedBy_P']}
verbs_dict["maintaining"] = {"maintaining" : ['maintainedBy_O', 'owner_O', 'owningOrganisation_O', 'occupation_O', 'authority_O', 'field_P', 'parent_P', 'owners_P', 'owningCompany_O', 'system_P', 'arena_P', 'owned_P', 'parentOrganisation_O', 'parentCompany_O', 'ground_P', 'stadium_P', 'company_P', 'network_O', 'foundedBy_O', 'foundedBy_P']}
verbs_dict["voice"] = {"voice" : ['voice_O']}
verbs_dict["voices"] = {"voices" : ['voice_O']}
verbs_dict["voiced"] = {"voiced" : ['voice_O'], "voiced by" : ['voice_O']}
verbs_dict["voicing"] = {"voicing" : ['voice_O']}
verbs_dict["record"] = {"record" : ['recordedIn_O']}
verbs_dict["records"] = {"records" : ['recordedIn_O']}
verbs_dict["recorded"] = {"recorded" : ['recordedIn_O']}
verbs_dict["recording"] = {"recording" : ['recordedIn_O']}
verbs_dict["star"] = {"star" : ['starring_P', 'starring_O'], "star in" : ['starring_P', 'starring_O']}
verbs_dict["stars"] = {"stars" : ['starring_P', 'starring_O'], "stars in" : ['starring_P', 'starring_O']}
verbs_dict["starred"] = {"starred" : ['starring_P', 'starring_O'], "starred in" : ['starring_P', 'starring_O']}
verbs_dict["starring"] = {"starring" : ['starring_P', 'starring_O'], "starring in" : ['starring_P', 'starring_O']}
verbs_dict["paint"] = {"paint" : ['creator_O', 'artist_O', 'author_O', 'illustrator_O', 'creator_P', 'artist_P', 'author_P', 'property_O', 'painter_P']}
verbs_dict["paints"] = {"paints" : ['creator_O', 'artist_O', 'author_O', 'illustrator_O', 'creator_P', 'artist_P', 'author_P', 'property_O', 'painter_P']}
verbs_dict["painted"] = {"painted" : ['creator_O', 'artist_O', 'author_O', 'illustrator_O', 'creator_P', 'artist_P', 'author_P', 'property_O', 'painter_P'], "painted by" : ['creator_O', 'artist_O', 'author_O', 'illustrator_O', 'creator_P', 'artist_P', 'author_P', 'property_O', 'painter_P']}
verbs_dict["painting"] = {"painting" : ['creator_O', 'artist_O', 'author_O', 'illustrator_O', 'creator_P', 'artist_P', 'author_P', 'property_O', 'painter_P']}
verbs_dict["perform"] = {"perform" : ['artist_O', 'artist_P', 'voice_O', 'voice_P']}
verbs_dict["performs"] = {"performs" : ['artist_O', 'artist_P', 'voice_O', 'voice_P']}
verbs_dict["performed"] = {"performed" : ['artist_O', 'artist_P', 'voice_O', 'voice_P']}
verbs_dict["performing"] = {"performing" : ['artist_O', 'artist_P', 'voice_O', 'voice_P']}
verbs_dict["serve"] = {"serve" : ['cityServed_P', 'destination_O', 'destination_P', 'destinations_P', 'regionServed_O', 'regionServed_P', 'order_O', 'order_P']}
verbs_dict["serves"] = {"serves" : ['cityServed_P', 'destination_O', 'destination_P', 'destinations_P', 'regionServed_O', 'regionServed_P', 'order_O', 'order_P']}
verbs_dict["served"] = {"served" : ['cityServed_P', 'destination_O', 'destination_P', 'destinations_P', 'regionServed_O', 'regionServed_P', 'order_O', 'order_P'], "served by" : ['cityServed_P', 'destination_O', 'destination_P', 'destinations_P', 'regionServed_O', 'regionServed_P', 'order_O', 'order_P']}
verbs_dict["serving"] = {"serving" : ['cityServed_P', 'destination_O', 'destination_P', 'destinations_P', 'regionServed_O', 'regionServed_P', 'order_O', 'order_P']}
verbs_dict["edit"] = {"edit" : ['editor_O', 'editor_P', 'editing_P', 'editing_O']}
verbs_dict["edits"] = {"edit" : ['editor_O', 'editor_P', 'editing_P', 'editing_O']}
verbs_dict["edited"] = {"edited" : ['editor_O', 'editor_P', 'editing_P', 'editing_O'], "edited by" : ['editor_O', 'editor_P', 'editing_P', 'editing_O']}
verbs_dict["editing"] = {"editing" : ['editor_O', 'editor_P', 'editing_P', 'editing_O']}
verbs_dict["develop"] = {"develop" : ['developer_O', 'developer_P', 'producer_O', 'producer_P', 'designer_O', 'designer_P', 'product_O', 'creator_O', 'creator_P', 'manufacturer_O', 'manufacturer_P']}
verbs_dict["develops"] = {"develops" : ['developer_O', 'developer_P', 'producer_O', 'producer_P', 'designer_O', 'designer_P', 'product_O', 'creator_O', 'creator_P', 'manufacturer_O', 'manufacturer_P']}
verbs_dict["developed"] = {"developed" : ['developer_O', 'developer_P', 'producer_O', 'producer_P', 'designer_O', 'designer_P', 'product_O', 'creator_O', 'creator_P', 'manufacturer_O', 'manufacturer_P'], "developed by" : ['developer_O', 'developer_P', 'producer_O', 'producer_P', 'designer_O', 'designer_P', 'product_O', 'creator_O', 'creator_P', 'manufacturer_O', 'manufacturer_P']}
verbs_dict["developing"] = {"developing" : ['developer_O', 'developer_P', 'producer_O', 'producer_P', 'designer_O', 'designer_P', 'product_O', 'creator_O', 'creator_P', 'manufacturer_O', 'manufacturer_P']}
verbs_dict["fight"] = {"fight" : ['battles_P', 'battle_O', 'battle_P', 'combatant_P', 'territory_O', 'territory_P']}
verbs_dict["fights"] = {"fights" : ['battles_P', 'battle_O', 'battle_P', 'combatant_P', 'territory_O', 'territory_P']}
verbs_dict["fought"] = {"fought" : ['battles_P', 'battle_O', 'battle_P', 'combatant_P', 'territory_O', 'territory_P'], "fought by" : ['battles_P', 'battle_O', 'battle_P', 'combatant_P', 'territory_O', 'territory_P']}
verbs_dict["fighting"] = {"fighting" : ['battles_P', 'battle_O', 'battle_P', 'combatant_P', 'territory_O', 'territory_P']}
verbs_dict["study"] = {"study" : ['mainInterests_P']}
verbs_dict["studies"] = {"studies" : ['mainInterests_P']}
verbs_dict["studied"] = {"studied" : ['mainInterests_P'], "studied by" : ['mainInterests_P']}
verbs_dict["studying"] = {"studying" : ['mainInterests_P']}
verbs_dict["illustrate"] = {"illustrate" : ['illustrator_O', 'illustrator_P']}
verbs_dict["illustrates"] = {"illustrates" : ['illustrator_O', 'illustrator_P']}
verbs_dict["illustrated"] = {"illustrated" : ['illustrator_O', 'illustrator_P'], "illustrated by" : ['illustrator_O', 'illustrator_P']}
verbs_dict["illustrating"] = {"illustrating" : ['illustrator_O', 'illustrator_P']}
verbs_dict["discover"] = {"discover" : ['discoverer_O', 'discoverer_P', 'discoveredBy_P']}
verbs_dict["discovers"] = {"discovers" : ['discoverer_O', 'discoverer_P', 'discoveredBy_P']}
verbs_dict["discovered"] = {"discovered" : ['discoverer_O', 'discoverer_P', 'discoveredBy_P'], "discovered by" : ['discoverer_O', 'discoverer_P']}
verbs_dict["discovering"] = {"discovering" : ['discoverer_O', 'discoverer_P', 'discoveredBy_P']}
verbs_dict["coach"] = {"coach" : ['coach_O', 'coach_P', 'trainer_O', 'trainer_P']}
verbs_dict["coaches"] = {"coaches" : ['coach_O', 'coach_P', 'trainer_O', 'trainer_P']}
verbs_dict["coached"] = {"coached" : ['coach_O', 'coach_P', 'trainer_O', 'trainer_P'], "coached by" : ['coach_O', 'coach_P', 'trainer_O', 'trainer_P']}
verbs_dict["coaching"] = {"coaching" : ['coach_O', 'coach_P', 'trainer_O', 'trainer_P']}
verbs_dict["run"] = {"run" : ['governingBody_O', 'governingBody_P', 'governingbody_P'], "run on" : ['operatingSystem_O', 'operatingSystem_P', 'governingBody_O', 'governingBody_P', 'governingbody_P'], "run by" : ['governingBody_O', 'governingBody_P', 'governingbody_P']}
verbs_dict["runs"] = {"runs" : ['governingBody_O', 'governingBody_P', 'governingbody_P'], "runs on" : ['operatingSystem_O', 'operatingSystem_P', 'governingBody_O', 'governingBody_P', 'governingbody_P']}
verbs_dict["ran"] = {"ran" : ['governingBody_O', 'governingBody_P', 'governingbody_P'], "ran on" : ['operatingSystem_O', 'operatingSystem_P', 'governingBody_O', 'governingBody_P', 'governingbody_P']}
verbs_dict["running"] = {"running" : ['governingBody_O', 'governingBody_P', 'governingbody_P'], "running on" : ['operatingSystem_O', 'operatingSystem_P', 'governingBody_O', 'governingBody_P', 'governingbody_P']}
verbs_dict["employ"] = {"employ" : ['occupation_O', 'occupation_P', 'profession_O', 'profession_P', 'employer_O', 'employer_P'], "employ the service" : ['service_O', 'services_P', 'service_P']}
verbs_dict["employs"] = {"employs" : ['occupation_O', 'occupation_P', 'profession_O', 'profession_P', 'employer_O', 'employer_P'], "employs the service" : ['service_O', 'services_P', 'service_P']}
verbs_dict["employed"] = {"employed" : ['occupation_O', 'occupation_P', 'profession_O', 'profession_P', 'employer_O', 'employer_P'], "employed by" : ['occupation_O', 'occupation_P', 'profession_O', 'profession_P', 'employer_O', 'employer_P'], "employed the service" : ['service_O', 'services_P', 'service_P']}
verbs_dict["employing"] = {"employing" : ['occupation_O', 'occupation_P', 'profession_O', 'profession_P', 'employer_O', 'employer_P'], "employing the service" : ['service_O', 'services_P', 'service_P']}
verbs_dict["inspire"] = {"inspire" : ['influences_P', 'basedOn_O', 'basedOn_P', 'stylisticOrigin_O', 'stylisticOrigin_P']}
verbs_dict["inspires"] = {"inspires" : ['influences_P', 'basedOn_O', 'basedOn_P', 'stylisticOrigin_O', 'stylisticOrigin_P']}
verbs_dict["inspired"] = {"inspired" : ['influences_P', 'basedOn_O', 'basedOn_P', 'stylisticOrigin_O', 'stylisticOrigin_P'], "inspired by" : ['influences_P', 'basedOn_O', 'basedOn_P', 'stylisticOrigin_O', 'stylisticOrigin_P']}
verbs_dict["inspiring"] = {"inspiring" : ['influences_P', 'basedOn_O', 'basedOn_P', 'stylisticOrigin_O', 'stylisticOrigin_P']}
verbs_dict["narrate"] = {"narrate" : ['narrated_P']}
verbs_dict["narrates"] = {"narrates" : ['narrated_P']}
verbs_dict["narrated"] = {"narrated" : ['narrated_P'], "narrated by" : ['narrated_P']}
verbs_dict["narrating"] = {"narrating" : ['narrated_P']}
verbs_dict["command"] = {"command" : ['commander_P']}
verbs_dict["commands"] = {"commands" : ['commander_P']}
verbs_dict["commanded"] = {"commanded" : ['commander_P']}
verbs_dict["commanding"] = {"commanding" : ['commander_P']}
verbs_dict["beatify"] = {"beatify" : ['beatifiedBy_P']}
verbs_dict["beatifies"] = {"beatifies" : ['beatifiedBy_P']}
verbs_dict["beatified"] = {"beatified" : ['beatifiedBy_P']}
verbs_dict["beatifying"] = {"beatifying" : ['beatifiedBy_P']}
verbs_dict["write"] = {"write" : ['writer_O', 'writer_P', 'author_O', 'author_P', 'composer_O', 'composer_P', 'musicBy_O', 'musicBy_P']}
verbs_dict["writes"] = {"writes" : ['writer_O', 'writer_P', 'author_O', 'author_P', 'composer_O', 'composer_P', 'musicBy_O', 'musicBy_P']}
verbs_dict["wrote"] = {"wrote" : ['writer_O', 'writer_P', 'author_O', 'author_P', 'composer_O', 'composer_P', 'musicBy_O', 'musicBy_P']}
verbs_dict["written"] = {"written" : ['writer_O', 'writer_P', 'author_O', 'author_P', 'composer_O', 'composer_P', 'musicBy_O', 'musicBy_P'], "written by" : ['writer_O', 'writer_P', 'author_O', 'author_P', 'composer_O', 'composer_P', 'musicBy_O', 'musicBy_P']}
verbs_dict["writing"] = {"writing" : ['writer_O', 'writer_P', 'author_O', 'author_P', 'composer_O', 'composer_P', 'musicBy_O', 'musicBy_P']}
verbs_dict["distribute"] = {"distribute" : ['distributor_O', 'distributor_P', 'publisher_O', 'publisher_P']}
verbs_dict["distributes"] = {"distributes" : ['distributor_O', 'distributor_P', 'publisher_O', 'publisher_P']}
verbs_dict["distributed"] = {"distributed" : ['distributor_O', 'distributor_P', 'publisher_O', 'publisher_P'], "distributed by" : ['distributor_O', 'distributor_P', 'publisher_O', 'publisher_P']}
verbs_dict["distributing"] = {"distributing" : ['distributor_O', 'distributor_P', 'publisher_O', 'publisher_P']}
verbs_dict["participate"] = {"participate" : ['battles_P', 'battle_O', 'battle_P']}
verbs_dict["participates"] = {"participates" : ['battles_P', 'battle_O', 'battle_P']}
verbs_dict["participated"] = {"participated" : ['battles_P', 'battle_O', 'battle_P']}
verbs_dict["participating"] = {"participating" : ['battles_P', 'battle_O', 'battle_P']}
verbs_dict["sing"] = {"sing" : ['musicalArtist_O', 'musicalArtist_P', 'musicalBand_O', 'musicalBand_P']}
verbs_dict["sings"] = {"sings" : ['musicalArtist_O', 'musicalArtist_P', 'musicalBand_O', 'musicalBand_P']}
verbs_dict["sang"] = {"sang" : ['musicalArtist_O', 'musicalArtist_P', 'musicalBand_O', 'musicalBand_P']}
verbs_dict["sung"] = {"sung" : ['musicalArtist_O', 'musicalArtist_P', 'musicalBand_O', 'musicalBand_P'], "sung by" : ['musicalArtist_O', 'musicalArtist_P', 'musicalBand_O', 'musicalBand_P']}
verbs_dict["singing"] = {"singing" : ['musicalArtist_O', 'musicalArtist_P', 'musicalBand_O', 'musicalBand_P']}
verbs_dict["cost"] = {"cost" : ['budget_O', 'budget_P']}
verbs_dict["costs"] = {"costs" : ['budget_O', 'budget_P']}
verbs_dict["costing"] = {"costing" : ['budget_O', 'budget_P']}
verbs_dict["appoint"] = {"appoint" : ['appointer_P']}
verbs_dict["appoints"] = {"appoints" : ['appointer_P']}
verbs_dict["appointed"] = {"appointed" : ['appointer_P'], "appointed by" : ['appointer_P']}
verbs_dict["appointing"] = {"appointing" : ['appointer_P']}
verbs_dict["manage"] = {"manage" : ['manager_O', 'manager_P', 'managerclubs_P', 'managerClub_O', 'president_O', 'president_P', 'presidents_P', 'leaderName_O', 'leaderName_P', 'operator_O', 'director_O', 'director_P', 'directedby_P', 'operator_P', 'governingBody_O', 'chancellor_O', 'chancellor_P', 'governingBody_P', 'head_O', 'head_P', 'principal_O', 'principal_P', 'chairman_O', 'chairman_P', 'deputy_O', 'deputy_P', 'servingRailwayLine_O', 'servingRailwayLine_P', 'operatedBy_O', 'operatedBy_P', 'cinematography_O', 'cinematography_P']}
verbs_dict["manages"] = {"manages" : ['manager_O', 'manager_P', 'managerclubs_P', 'managerClub_O', 'president_O', 'president_P', 'presidents_P', 'leaderName_O', 'leaderName_P', 'operator_O', 'director_O', 'director_P', 'directedby_P', 'operator_P', 'governingBody_O', 'chancellor_O', 'chancellor_P', 'governingBody_P', 'head_O', 'head_P', 'principal_O', 'principal_P', 'chairman_O', 'chairman_P', 'deputy_O', 'deputy_P', 'servingRailwayLine_O', 'servingRailwayLine_P', 'operatedBy_O', 'operatedBy_P', 'cinematography_O', 'cinematography_P']}
verbs_dict["managed"] = {"managed" : ['manager_O', 'manager_P', 'managerclubs_P', 'managerClub_O', 'president_O', 'president_P', 'presidents_P', 'leaderName_O', 'leaderName_P', 'operator_O', 'director_O', 'director_P', 'directedby_P', 'operator_P', 'governingBody_O', 'chancellor_O', 'chancellor_P', 'governingBody_P', 'head_O', 'head_P', 'principal_O', 'principal_P', 'chairman_O', 'chairman_P', 'deputy_O', 'deputy_P', 'servingRailwayLine_O', 'servingRailwayLine_P', 'operatedBy_O', 'operatedBy_P', 'cinematography_O', 'cinematography_P'], "managed by" : ['manager_O', 'manager_P', 'managerclubs_P', 'managerClub_O', 'president_O', 'president_P', 'leaderName_O', 'leaderName_P', 'operator_O', 'director_O', 'director_P', 'directedby_P', 'operator_P', 'governingBody_O', 'chancellor_O', 'chancellor_P', 'governingBody_P', 'head_O', 'head_P', 'principal_O', 'principal_P', 'chairman_O', 'chairman_P', 'deputy_O', 'deputy_P', 'servingRailwayLine_O', 'servingRailwayLine_P', 'operatedBy_O', 'operatedBy_P', 'cinematography_O', 'cinematography_P']}
verbs_dict["managing"] = {"managing" : ['manager_O', 'manager_P', 'managerclubs_P', 'managerClub_O', 'president_O', 'president_P', 'presidents_P', 'leaderName_O', 'leaderName_P', 'operator_O', 'director_O', 'director_P', 'directedby_P', 'operator_P', 'governingBody_O', 'chancellor_O', 'chancellor_P', 'governingBody_P', 'head_O', 'head_P', 'principal_O', 'principal_P', 'chairman_O', 'chairman_P', 'deputy_O', 'deputy_P', 'servingRailwayLine_O', 'servingRailwayLine_P', 'operatedBy_O', 'operatedBy_P', 'cinematography_O', 'cinematography_P']}
verbs_dict["win"] = {"win" : ['award_O', 'awards_P', 'award_P', 'title_P', 'champion_O', 'champion_P']}
verbs_dict["wins"] = {"wins" : ['award_O', 'awards_P', 'award_P', 'title_P', 'champion_O', 'champion_P']}
verbs_dict["won"] = {"won" : ['award_O', 'awards_P', 'award_P', 'title_P', 'champion_O', 'champion_P'], "won by" : ['award_O', 'awards_P', 'award_P', 'title_P', 'champion_O', 'champion_P']}
verbs_dict["winning"] = {"winning" : ['award_O', 'awards_P', 'award_P', 'title_P', 'champion_O', 'champion_P']}
verbs_dict["host"] = {"host" : ['presenter_O', 'presenter_P', 'host_O', 'host_P', 'hostCity_O', 'hostCity_P']}
verbs_dict["hosts"] = {"hosts" : ['presenter_O', 'presenter_P', 'host_O', 'host_P', 'hostCity_O', 'hostCity_P']}
verbs_dict["hosted"] = {"hosted" : ['presenter_O', 'presenter_P', 'host_O', 'host_P', 'hostCity_O', 'hostCity_P'], "hosted by" : ['presenter_O', 'presenter_P', 'host_O', 'host_P', 'hostCity_O', 'hostCity_P']}
verbs_dict["hosting"] = {"hosting" : ['presenter_O', 'presenter_P', 'host_O', 'host_P', 'hostCity_O', 'hostCity_P']}
verbs_dict["precede"] = {"precede" : ['predecessor_O']}
verbs_dict["precedes"] = {"precedes" : ['predecessor_O']}
verbs_dict["preceded"] = {"preceded" : ['predecessor_O'], "preceded by" : ['predecessor_O']}
verbs_dict["preceding"] = {"preceding" : ['predecessor_O']}
verbs_dict["make"] = {"make" : ['notableWork_O', 'notableWork_P', 'manufacturer_O', 'manufacturer_P', 'artist_O', 'artist_P', 'creator_O', 'creator_P', 'musicalBand_O', 'musicalBand_P']}
verbs_dict["makes"] = {"makes" : ['notableWork_O', 'notableWork_P', 'manufacturer_O', 'manufacturer_P', 'artist_O', 'artist_P', 'creator_O', 'creator_P', 'musicalBand_O', 'musicalBand_P']}
verbs_dict["made"] = {"made" : ['notableWork_O', 'notableWork_P', 'manufacturer_O', 'manufacturer_P', 'artist_O', 'artist_P', 'creator_O', 'creator_P', 'musicalBand_O', 'musicalBand_P'], "made by" : ['notableWork_O', 'notableWork_P', 'manufacturer_O', 'manufacturer_P', 'artist_O', 'artist_P', 'creator_O', 'creator_P', 'musicalBand_O', 'musicalBand_P']}
verbs_dict["making"] = {"making" : ['notableWork_O', 'notableWork_P', 'manufacturer_O', 'manufacturer_P', 'artist_O', 'artist_P', 'creator_O', 'creator_P', 'musicalBand_O', 'musicalBand_P']}
verbs_dict["manufacture"] = {"manufacture" : ['manufacturer_O', 'product_O', 'product_P', 'products_P']}
verbs_dict["manufactures"] = {"manufactures" : ['manufacturer_O', 'product_O', 'product_P', 'products_P']}
verbs_dict["manufactured"] = {"manufactured" : ['manufacturer_O', 'product_O', 'product_P', 'products_P'], "manufactured by" : ['manufacturer_O', 'product_O', 'product_P', 'products_P']}
verbs_dict["manufacturing"] = {"manufacturing" : ['manufacturer_O', 'product_O', 'product_P', 'products_P']}
verbs_dict["cross"] = {"cross" : ['crosses_O', 'crosses_P']}
verbs_dict["crosses"] = {"crosses" : ['crosses_O', 'crosses_P']}
verbs_dict["crossed"] = {"crossed" : ['crosses_O', 'crosses_P'], "crossed by" : ['crosses_O', 'crosses_P']}
verbs_dict["crossing"] = {"crossing" : ['crosses_O', 'crosses_P']}
verbs_dict["own"] = {"own" : ['owner_O', 'owningOrganisation_O', 'occupation_O', 'authority_O', 'field_P', 'parent_P', 'owners_P', 'owningCompany_O', 'system_P', 'arena_P', 'owned_P', 'parentOrganisation_O', 'parentCompany_O', 'ground_P', 'stadium_P', 'company_P', 'network_O', 'foundedBy_O', 'foundedBy_P', 'network_O', 'network_P']}
verbs_dict["owns"] = {"owns" : ['owner_O', 'owningOrganisation_O', 'occupation_O', 'authority_O', 'field_P', 'parent_P', 'owners_P', 'owningCompany_O', 'system_P', 'arena_P', 'owned_P', 'parentOrganisation_O', 'parentCompany_O', 'ground_P', 'stadium_P', 'company_P', 'network_O', 'foundedBy_O', 'foundedBy_P', 'network_O', 'network_P']}
verbs_dict["owned"] = {"owned" : ['owner_O', 'owningOrganisation_O', 'occupation_O', 'authority_O', 'field_P', 'parent_P', 'owners_P', 'owningCompany_O', 'system_P', 'arena_P', 'owned_P', 'parentOrganisation_O', 'parentCompany_O', 'ground_P', 'stadium_P', 'company_P', 'network_O', 'foundedBy_O', 'foundedBy_P', 'network_O', 'network_P'], "owned by" : ['owner_O', 'owningOrganisation_O', 'occupation_O', 'authority_O', 'field_P', 'parent_P', 'owners_P', 'owningCompany_O', 'system_P', 'arena_P', 'owned_P', 'parentOrganisation_O', 'parentCompany_O', 'ground_P', 'stadium_P', 'company_P', 'network_O', 'foundedBy_O', 'foundedBy_P', 'network_O', 'network_P']}
verbs_dict["owning"] = {"owning" : ['owner_O', 'owningOrganisation_O', 'occupation_O', 'authority_O', 'field_P', 'parent_P', 'owners_P', 'owningCompany_O', 'system_P', 'arena_P', 'owned_P', 'parentOrganisation_O', 'parentCompany_O', 'ground_P', 'stadium_P', 'company_P', 'network_O', 'foundedBy_O', 'foundedBy_P', 'network_O', 'network_P']}
verbs_dict["publish"] = {"publish" : ['publisher_O', 'publisher_P', 'distributor_O', 'distributor_P']}
verbs_dict["publishes"] = {"publishes" : ['publisher_O', 'publisher_P', 'distributor_O', 'distributor_P']}
verbs_dict["published"] = {"published" : ['publisher_O', 'publisher_P', 'distributor_O', 'distributor_P']}
verbs_dict["publishing"] = {"publishing" : ['publisher_O', 'publisher_P', 'distributor_O', 'distributor_P']}
verbs_dict["get"] = {"get" : ['award_O', 'awards_P', 'award_P']}
verbs_dict["gets"] = {"gets" : ['award_O', 'awards_P', 'award_P']}
verbs_dict["got"] = {"got" : ['award_O', 'awards_P', 'award_P'], "got by" : ['award_O', 'awards_P', 'award_P']}
verbs_dict["getting"] = {"getting" : ['award_O', 'awards_P', 'award_P']}
verbs_dict["receive"] = {"receive" : ['award_O', 'awards_P', 'award_P', 'title_P']}
verbs_dict["receives"] = {"receives" : ['award_O', 'awards_P', 'award_P', 'title_P']}
verbs_dict["received"] = {"received" : ['award_O', 'awards_P', 'award_P', 'title_P'], "received by" : ['award_O', 'awards_P', 'award_P', 'title_P']}
verbs_dict["receiving"] = {"receiving" : ['award_O', 'awards_P', 'award_P', 'title_P']}
verbs_dict["canonize"] = {"canonize" : ['canonizedBy_P', 'canonizedBy_O']}
verbs_dict["canonizes"] = {"canonizes" : ['canonizedBy_P', 'canonizedBy_O']}
verbs_dict["canonized"] = {"canonized" : ['canonizedBy_P', 'canonizedBy_O']}
verbs_dict["canonizing"] = {"canonizing" : ['canonizedBy_P', 'canonizedBy_O']}
verbs_dict["canonise"] = {"canonise" : ['canonizedBy_P', 'canonizedBy_O']}
verbs_dict["canonises"] = {"canonises" : ['canonizedBy_P', 'canonizedBy_O']}
verbs_dict["canonised"] = {"canonised" : ['canonizedBy_P', 'canonizedBy_O']}
verbs_dict["canonising"] = {"canonising" : ['canonizedBy_P', 'canonizedBy_O']}
verbs_dict["pen"] = {"pen" : ['writer_O', 'writer_P', 'author_O', 'author_P', 'creator_P', 'creator_O']}
verbs_dict["pens"] = {"pens" : ['writer_O', 'writer_P', 'author_O', 'author_P', 'creator_P', 'creator_O']}
verbs_dict["penned"] = {"penned" : ['writer_O', 'writer_P', 'author_O', 'author_P', 'creator_P', 'creator_O']}
verbs_dict["penning"] = {"penning" : ['writer_O', 'writer_P', 'author_O', 'author_P', 'creator_P', 'creator_O']}
verbs_dict["head"] = {"head" : ['leader_O', 'leader_P', 'keyPeople_P', 'keyPerson_O', 'chairman_O', 'chairman_P']}
verbs_dict["heads"] = {"heads" : ['leader_O', 'leader_P', 'keyPeople_P', 'keyPerson_O', 'chairman_O', 'chairman_P']}
verbs_dict["headed"] = {"headed" : ['leader_O', 'leader_P', 'keyPeople_P', 'keyPerson_O', 'chairman_O', 'chairman_P']}
verbs_dict["heading"] = {"heading" : ['leader_O', 'leader_P', 'keyPeople_P', 'keyPerson_O', 'chairman_O', 'chairman_P']}
verbs_dict["start"] = {"start" : ['routeStart_O', 'routeStart_P', 'sourceMountain_O', 'sourceMountain_P', 'sourceRegion_O', 'sourceRegion_P', 'foundationPlace_O', 'foundationPlace_P'], "start in" : ['routeStart_O', 'routeStart_P', 'sourceMountain_O', 'sourceMountain_P', 'sourceRegion_O', 'sourceRegion_P', 'foundationPlace_O', 'foundationPlace_P'], "start at the pole position" : ['poleDriver_O', 'poleDriver_P'], "start his career" : ['debutTeam_P', 'debutTeam_O', 'debutteam_P'], "start her career" : ['debutTeam_P', 'debutTeam_O', 'debutteam_P'], "start their career" : ['debutTeam_P', 'debutTeam_O', 'debutteam_P']}
verbs_dict["starts"] = {"starts" : ['routeStart_O', 'routeStart_P', 'sourceMountain_O', 'sourceMountain_P', 'sourceRegion_O', 'sourceRegion_P', 'foundationPlace_O', 'foundationPlace_P'], "starts in" : ['routeStart_O', 'routeStart_P', 'sourceMountain_O', 'sourceMountain_P', 'sourceRegion_O', 'sourceRegion_P', 'foundationPlace_O', 'foundationPlace_P'], "starts at the pole position" : ['poleDriver_O', 'poleDriver_P'], "starts his career" : ['debutTeam_P', 'debutTeam_O', 'debutteam_P'], "starts her career" : ['debutTeam_P', 'debutTeam_O', 'debutteam_P'], "starts their career" : ['debutTeam_P', 'debutTeam_O', 'debutteam_P']}
verbs_dict["started"] = {"started" : ['routeStart_O', 'routeStart_P', 'sourceMountain_O', 'sourceMountain_P', 'sourceRegion_O', 'sourceRegion_P', 'foundationPlace_O', 'foundationPlace_P'], "started in" : ['routeStart_O', 'routeStart_P', 'sourceMountain_O', 'sourceMountain_P', 'sourceRegion_O', 'sourceRegion_P', 'foundationPlace_O', 'foundationPlace_P'], "started at the pole position" : ['poleDriver_O', 'poleDriver_P'], "started his career" : ['debutTeam_P', 'debutTeam_O', 'debutteam_P'], "started her career" : ['debutTeam_P', 'debutTeam_O', 'debutteam_P'], "started their career" : ['debutTeam_P', 'debutTeam_O', 'debutteam_P']}
verbs_dict["starting"] = {"starting" : ['routeStart_O', 'routeStart_P', 'sourceMountain_O', 'sourceMountain_P', 'sourceRegion_O', 'sourceRegion_P', 'foundationPlace_O', 'foundationPlace_P'], "starting in" : ['routeStart_O', 'routeStart_P', 'sourceMountain_O', 'sourceMountain_P', 'sourceRegion_O', 'sourceRegion_P', 'foundationPlace_O', 'foundationPlace_P'], "starting at the pole position" : ['poleDriver_O', 'poleDriver_P'], "starting his career" : ['debutTeam_P', 'debutTeam_O', 'debutteam_P'], "starting her career" : ['debutTeam_P', 'debutTeam_O', 'debutteam_P'], "starting their career" : ['debutTeam_P', 'debutTeam_O', 'debutteam_P']}
verbs_dict["commence"] = {"commence" : ['date_O', 'date_P']}
verbs_dict["commences"] = {"commences" : ['date_O', 'date_P']}
verbs_dict["commenced"] = {"commenced" : ['date_O', 'date_P']}
verbs_dict["commencing"] = {"commencing" : ['date_O', 'date_P']}
verbs_dict["telecast"] = {"telecast" : ['network_O', 'network_P', 'channel_O', 'channel_P']}
verbs_dict["telecasts"] = {"telecasts" : ['network_O', 'network_P', 'channel_O', 'channel_P']}
verbs_dict["telecasted"] = {"telecasted" : ['network_O', 'network_P', 'channel_O', 'channel_P']}
verbs_dict["telecasting"] = {"telecasting" : ['network_O', 'network_P', 'channel_O', 'channel_P']}
verbs_dict["end"] = {"end" : ['routeEnd_O', 'riverMouth_O', 'riverMouth_P']}
verbs_dict["ends"] = {"ends" : ['routeEnd_O', 'riverMouth_O', 'riverMouth_P']}
verbs_dict["ended"] = {"ended" : ['routeEnd_O', 'riverMouth_O', 'riverMouth_P']}
verbs_dict["ending"] = {"ending" : ['routeEnd_O', 'riverMouth_O', 'riverMouth_P']}
verbs_dict["portray"] = {"portray" : ['portrayer_O', 'portrayer_P', 'creator_O', 'creator_P', 'creator_O', 'author_O', 'author_P']}
verbs_dict["portrays"] = {"portrays" : ['portrayer_O', 'portrayer_P', 'creator_O', 'creator_P', 'creator_O', 'author_O', 'author_P']}
verbs_dict["portrayed"] = {"portrayed" : ['portrayer_O', 'portrayer_P', 'creator_O', 'creator_P', 'creator_O', 'author_O', 'author_P']}
verbs_dict["portraying"] = {"portraying" : ['portrayer_O', 'portrayer_P', 'creator_O', 'creator_P', 'creator_O', 'author_O', 'author_P']}
verbs_dict["create"] = {"create" : ['creator_P', 'creator_O', 'author_O', 'writer_O', 'writer_P', 'author_P', 'composer_O', 'composer_P', 'developer_O', 'producer_O', 'musicBy_O', 'musicBy_P', 'foundedBy_O', 'foundedBy_P', 'designer_O', 'designer_P', 'product_O', 'notableWork_O', 'notableWork_P']}
verbs_dict["creates"] = {"creates" : ['creator_P', 'creator_O', 'author_O', 'writer_O', 'writer_P', 'author_P', 'composer_O', 'composer_P', 'developer_O', 'producer_O', 'musicBy_O', 'musicBy_P', 'foundedBy_O', 'foundedBy_P', 'designer_O', 'designer_P', 'product_O', 'notableWork_O', 'notableWork_P']}
verbs_dict["created"] = {"created" : ['creator_P', 'creator_O', 'author_O', 'writer_O', 'writer_P', 'author_P', 'composer_O', 'composer_P', 'developer_O', 'producer_O', 'musicBy_O', 'musicBy_P', 'foundedBy_O', 'foundedBy_P', 'designer_O', 'designer_P', 'product_O', 'notableWork_O', 'notableWork_P'], "created by" : ['creator_P', 'creator_O', 'author_O', 'writer_O', 'writer_P', 'author_P', 'composer_O', 'composer_P', 'developer_O', 'producer_O', 'musicBy_O', 'musicBy_P', 'foundedBy_O', 'foundedBy_P', 'designer_O', 'designer_P', 'product_O', 'notableWork_O', 'notableWork_P']}
verbs_dict["creating"] = {"creating" : ['creator_P', 'creator_O', 'author_O', 'writer_O', 'writer_P', 'author_P', 'composer_O', 'composer_P', 'developer_O', 'producer_O', 'musicBy_O', 'musicBy_P', 'foundedBy_O', 'foundedBy_P', 'designer_O', 'designer_P', 'product_O', 'notableWork_O', 'notableWork_P']}
verbs_dict["release"] = {'release': ['release_P', 'releases_P', 'released_P', 'product_O', 'product_P',  'Stream/discharge_O', 'Stream/discharge_P', 'discharge_O', 'discharge_P'], 'release date': ['releaseDate_O', 'releaseDate_P'], 'release place': ['releasePlace_P']}
verbs_dict["releases"] = {'releases': ['release_P', 'releases_P', 'released_P', 'product_O', 'product_P',  'Stream/discharge_O', 'Stream/discharge_P', 'discharge_O', 'discharge_P']}
verbs_dict["released"] = {'released': ['release_P', 'releases_P', 'released_P', 'product_O', 'product_P',  'Stream/discharge_O', 'Stream/discharge_P', 'discharge_O', 'discharge_P'], 'released by': ['release_P', 'releases_P', 'released_P', 'product_O', 'product_P',  'Stream/discharge_O', 'Stream/discharge_P', 'discharge_O', 'discharge_P']}
verbs_dict["releasing"] = {'releasing': ['release_P', 'releases_P', 'released_P', 'product_O', 'product_P',  'Stream/discharge_O', 'Stream/discharge_P', 'discharge_O', 'discharge_P']}
verbs_dict["operate"] = {"operate" : ['operatedBy_O', 'operator_O', 'regionServed_O', 'regionServed_P']}
verbs_dict["operates"] = {"operates" : ['operatedBy_O', 'operator_O', 'regionServed_O', 'regionServed_P']}
verbs_dict["operated"] = {"operated" : ['operatedBy_O', 'operator_O', 'regionServed_O', 'regionServed_P'], "operated by" : ['operatedBy_O', 'operator_O', 'regionServed_O', 'regionServed_P']}
verbs_dict["operating"] = {"operating" : ['operatedBy_O', 'operator_O', 'operating_P', 'regionServed_O', 'regionServed_P']}
verbs_dict["have"] = {"have" : ['company_O', 'company_P']}
verbs_dict["has"] = {"has" : ['company_O', 'company_P']}
verbs_dict["had"] = {"had" : ['company_O', 'company_P']}
verbs_dict["having"] = {"having" : ['company_O', 'company_P']}
verbs_dict["affiliate"] = {"affiliate" : ['affiliation_O', 'affiliation_P', 'affiliate_P', 'affiliates_P', 'affiliations_P']}
verbs_dict["affiliates"] = {"affiliates" : ['affiliation_O', 'affiliation_P', 'affiliate_P', 'affiliates_P', 'affiliations_P']}
verbs_dict["affiliated"] = {"affiliated" : ['affiliation_O', 'affiliation_P', 'affiliate_P', 'affiliates_P', 'affiliations_P'], "affiliated by" : ['affiliation_O', 'affiliation_P', 'affiliate_P', 'affiliates_P', 'affiliations_P']}
verbs_dict["affiliating"] = {"affiliating" : ['affiliation_O', 'affiliation_P', 'affiliate_P', 'affiliates_P', 'affiliations_P']}
verbs_dict["succeed"] = {"succeed" : ['successor_P', 'successor_O']}
verbs_dict["succeeds"] = {"succeeds" : ['successor_P', 'successor_O']}
verbs_dict["succeeded"] = {"succeeded" : ['successor_P', 'successor_O'], "succeeded by" : ['successor_P', 'successor_O']}
verbs_dict["succeeding"] = {"succeeding" : ['successor_P', 'successor_O']}
verbs_dict["compose"] = {"compose" : ['composer_O', 'composer_P', 'musicComposer_O', 'musicComposer_P', 'musicBy_O', 'musicBy_P', 'music_P', 'writer_O', 'writer_P', 'author_O', 'author_P']}
verbs_dict["composes"] = {"composes" : ['composer_O', 'composer_P', 'musicComposer_O', 'musicComposer_P', 'musicBy_O', 'musicBy_P', 'music_P', 'writer_O', 'writer_P', 'author_O', 'author_P']}
verbs_dict["composed"] = {"composed" : ['composer_O', 'composer_P', 'musicComposer_O', 'musicComposer_P', 'musicBy_O', 'musicBy_P', 'music_P', 'writer_O', 'writer_P', 'author_O', 'author_P'], "composed by" : ['composer_O', 'composer_P', 'musicComposer_O', 'musicComposer_P', 'musicBy_O', 'musicBy_P', 'music_P', 'writer_O', 'writer_P', 'author_O', 'author_P']}
verbs_dict["composing"] = {"composing" : ['composer_O', 'composer_P', 'musicComposer_O', 'musicComposer_P', 'musicBy_O', 'musicBy_P', 'music_P', 'writer_O', 'writer_P', 'author_O', 'author_P']}
verbs_dict["play"] = {"play" : ['play_P', 'sport_O', 'sport_P', 'plays_O', 'plays_P', 'instrument_O', 'instrument_P', 'notableInstruments_P', 'pastteams_P', 'team_O', 'team_P', 'playedFor_P', 'formerTeam_O', 'formerTeam_P', 'debutTeam_O', 'debutTeam_P', 'prospectTeam_P', 'athletics_P', 'athletics_O'], "play for" : ['play_P', 'sport_O', 'sport_P', 'plays_O', 'plays_P', 'pastteams_P', 'team_O', 'team_P', 'playedFor_P', 'formerTeam_O', 'formerTeam_P', 'debutTeam_O', 'debutTeam_P', 'prospectTeam_P', 'athletics_P', 'athletics_O'], "play in" : ['play_P', 'sport_O', 'sport_P', 'plays_O', 'plays_P', 'pastteams_P', 'team_O', 'team_P', 'playedFor_P', 'formerTeam_O', 'formerTeam_P', 'debutTeam_O', 'debutTeam_P', 'prospectTeam_P', 'athletics_P', 'athletics_O'], "play at" : ['play_P', 'sport_O', 'sport_P', 'plays_O', 'plays_P', 'pastteams_P', 'team_O', 'team_P', 'playedFor_P', 'formerTeam_O', 'formerTeam_P', 'debutTeam_O', 'debutTeam_P', 'prospectTeam_P', 'athletics_P', 'athletics_O']}
verbs_dict["plays"] = {"plays" : ['play_P', 'sport_O', 'sport_P', 'plays_O', 'plays_P', 'instrument_O', 'instrument_P', 'notableInstruments_P', 'pastteams_P', 'team_O', 'team_P', 'playedFor_P', 'formerTeam_O', 'formerTeam_P', 'debutTeam_O', 'debutTeam_P', 'prospectTeam_P', 'athletics_P', 'athletics_O'], "plays for" : ['play_P', 'sport_O', 'sport_P', 'plays_O', 'plays_P', 'pastteams_P', 'team_O', 'team_P', 'playedFor_P', 'formerTeam_O', 'formerTeam_P', 'debutTeam_O', 'debutTeam_P', 'prospectTeam_P', 'athletics_P', 'athletics_O'], "plays in" : ['play_P', 'sport_O', 'sport_P', 'plays_O', 'plays_P', 'pastteams_P', 'team_O', 'team_P', 'playedFor_P', 'formerTeam_O', 'formerTeam_P', 'debutTeam_O', 'debutTeam_P', 'prospectTeam_P', 'athletics_P', 'athletics_O'], "plays at" : ['play_P', 'sport_O', 'sport_P', 'plays_O', 'plays_P', 'pastteams_P', 'team_O', 'team_P', 'playedFor_P', 'formerTeam_O', 'formerTeam_P', 'debutTeam_O', 'debutTeam_P', 'prospectTeam_P', 'athletics_P', 'athletics_O']}
verbs_dict["played"] = {"played" : ['play_P', 'sport_O', 'sport_P', 'plays_O', 'plays_P', 'instrument_O', 'instrument_P', 'notableInstruments_P', 'pastteams_P', 'team_O', 'team_P', 'playedFor_P', 'formerTeam_O', 'formerTeam_P', 'debutTeam_O', 'debutTeam_P', 'prospectTeam_P', 'athletics_P', 'athletics_O'], "played by" : ['play_P', 'sport_O', 'sport_P', 'plays_O', 'plays_P', 'instrument_O', 'instrument_P', 'notableInstruments_P', 'pastteams_P', 'team_O', 'team_P', 'playedFor_P', 'formerTeam_O', 'formerTeam_P', 'debutTeam_O', 'debutTeam_P', 'prospectTeam_P', 'athletics_P', 'athletics_O'], "played for" : ['play_P', 'sport_O', 'sport_P', 'plays_O', 'plays_P', 'pastteams_P', 'team_O', 'team_P', 'playedFor_P', 'formerTeam_O', 'formerTeam_P', 'debutTeam_O', 'debutTeam_P', 'prospectTeam_P', 'athletics_P', 'athletics_O'], "played in" : ['play_P', 'sport_O', 'sport_P', 'plays_O', 'plays_P', 'pastteams_P', 'team_O', 'team_P', 'playedFor_P', 'formerTeam_O', 'formerTeam_P', 'debutTeam_O', 'debutTeam_P', 'prospectTeam_P', 'athletics_P', 'athletics_O'], "played at" : ['play_P', 'sport_O', 'sport_P', 'plays_O', 'plays_P', 'pastteams_P', 'team_O', 'team_P', 'playedFor_P', 'formerTeam_O', 'formerTeam_P', 'debutTeam_O', 'debutTeam_P', 'prospectTeam_P', 'athletics_P', 'athletics_O']}
verbs_dict["playing"] = {"playing" : ['play_P', 'sport_O', 'sport_P', 'plays_O', 'plays_P', 'instrument_O', 'instrument_P', 'notableInstruments_P', 'pastteams_P', 'team_O', 'team_P', 'playedFor_P', 'formerTeam_O', 'formerTeam_P', 'debutTeam_O', 'debutTeam_P', 'prospectTeam_P', 'athletics_P', 'athletics_O'], "playing for" : ['play_P', 'sport_O', 'sport_P', 'plays_O', 'plays_P', 'pastteams_P', 'team_O', 'team_P', 'playedFor_P', 'formerTeam_O', 'formerTeam_P', 'debutTeam_O', 'debutTeam_P', 'prospectTeam_P', 'athletics_P', 'athletics_O'], "playing in" : ['play_P', 'sport_O', 'sport_P', 'plays_O', 'plays_P', 'pastteams_P', 'team_O', 'team_P', 'playedFor_P', 'formerTeam_O', 'formerTeam_P', 'debutTeam_O', 'debutTeam_P', 'prospectTeam_P', 'athletics_P', 'athletics_O'], "playing at" : ['play_P', 'sport_O', 'sport_P', 'plays_O', 'plays_P', 'pastteams_P', 'team_O', 'team_P', 'playedFor_P', 'formerTeam_O', 'formerTeam_P', 'debutTeam_O', 'debutTeam_P', 'prospectTeam_P', 'athletics_P', 'athletics_O']}
verbs_dict["currently"] = {"currently play": ['currentteam_P', 'currentclub_P'], "currently play for" : ['currentteam_P', 'currentclub_P'], "currently play in" : ['currentteam_P', 'currentclub_P'], "currently play at" : ['currentteam_P', 'currentclub_P'], "currently plays": ['currentteam_P', 'currentclub_P'], "currently plays for" : ['currentteam_P', 'currentclub_P'], "currently plays in" : ['currentteam_P', 'currentclub_P'], "currently plays at" : ['currentteam_P', 'currentclub_P'], "currently playing": ['currentteam_P', 'currentclub_P'], "currently playing for" : ['currentteam_P', 'currentclub_P'], "currently playing in" : ['currentteam_P', 'currentclub_P'], "currently playing at" : ['currentteam_P', 'currentclub_P'], 'currently used for': ['currentlyUsedFor_O'], 'currently resides': ['currentlyResides_P']}
verbs_dict["train"] = {"train" : ['trainer_O', 'trainer_P', 'training_O', 'training_P']}
verbs_dict["trains"] = {"trains" : ['trainer_O', 'trainer_P', 'training_O', 'training_P']}
verbs_dict["trained"] = {"trained" : ['trainer_O', 'trainer_P', 'training_O', 'training_P'], "trained by" : ['trainer_O', 'trainer_P', 'training_O', 'training_P']}
verbs_dict["training"] = {"training" : ['trainer_O', 'trainer_P', 'training_O', 'training_P']}
verbs_dict["design"] = {"design" : ['designer_P', 'designer_O', 'designCompany_O', 'design_P', 'architect_O', 'architect_P']}
verbs_dict["designs"] = {"designs" : ['designer_P', 'designer_O', 'designCompany_O', 'design_P', 'architect_O', 'architect_P']}
verbs_dict["designed"] = {"designed" : ['designer_P', 'designer_O', 'designCompany_O', 'design_P', 'architect_O', 'architect_P'], "designed by" : ['designer_P', 'designer_O', 'designCompany_O', 'design_P', 'architect_O', 'architect_P']}
verbs_dict["designing"] = {"designing" : ['designer_P', 'designer_O', 'designCompany_O', 'design_P', 'architect_O', 'architect_P']}
verbs_dict["direct"] = {"direct" : ['director_O', 'director_P', 'directedby_P', 'creator_O', 'creator_P']}
verbs_dict["directs"] = {"directs" : ['director_O', 'director_P', 'directedby_P', 'creator_O', 'creator_P']}
verbs_dict["directed"] = {"directed" : ['director_O', 'director_P', 'directedby_P', 'creator_O', 'creator_P'], "directed by" : ['director_O', 'director_P', 'directedby_P', 'creator_O', 'creator_P']}
verbs_dict["directing"] = {"directing" : ['director_O', 'director_P', 'directedby_P', 'creator_O', 'creator_P']}

for v in verbs_dict.keys():
  if v in properties_dict:
    for v_version in verbs_dict[v]:
      if v_version in properties_dict[v]:
        for p in verbs_dict[v][v_version]:
          if p in properties_dict[v][v_version]:
            pass
          else:
            properties_dict[v][v_version] = properties_dict[v][v_version] + [p]
      else:
        properties_dict[v][v_version] = verbs_dict[v][v_version]
  else:
    properties_dict[v] = verbs_dict[v]

properties_dict["rule"] = {'rule' : ['leaderName_O', 'leaderName_P'], 'rule over' : ['leaderName_O', 'leaderName_P']}
properties_dict["rules"] = {'rules' : ['leaderName_O', 'leaderName_P'], 'rules over' : ['leaderName_O', 'leaderName_P']}
properties_dict["ruled"] = {'ruled' : ['leaderName_O', 'leaderName_P'], 'ruled over' : ['leaderName_O', 'leaderName_P']}
properties_dict["ruling"] = {'ruling' : ['leaderName_O', 'leaderName_P'], 'ruling over' : ['leaderName_O', 'leaderName_P']}
properties_dict["exist"] = {'exist' : ['locationCity_O', 'locationCity_P', 'location_O', 'location_P', 'locations_P', 'city_O', 'city_P', 'county_O', 'county_P', 'region_O', 'region_P', 'state_O', 'state_P', 'province_O', 'province_P', 'district_O', 'district_P', 'territory_O', 'territory_P'], 'exist in' : ['locationCity_O', 'locationCity_P', 'location_O', 'location_P', 'city_O', 'city_P', 'county_O', 'county_P', 'region_O', 'region_P', 'state_O', 'state_P', 'province_O', 'province_P', 'district_O', 'district_P', 'territory_O', 'territory_P']}
properties_dict["exists"] = {'exists' : ['locationCity_O', 'locationCity_P', 'location_O', 'location_P', 'locations_P', 'city_O', 'city_P', 'county_O', 'county_P', 'region_O', 'region_P', 'state_O', 'state_P', 'province_O', 'province_P', 'district_O', 'district_P', 'territory_O', 'territory_P'], 'exists in' : ['locationCity_O', 'locationCity_P', 'location_O', 'location_P', 'city_O', 'city_P', 'county_O', 'county_P', 'region_O', 'region_P', 'state_O', 'state_P', 'province_O', 'province_P', 'district_O', 'district_P', 'territory_O', 'territory_P']}
properties_dict["existed"] = {'existed' : ['locationCity_O', 'locationCity_P', 'location_O', 'location_P', 'locations_P', 'city_O', 'city_P', 'county_O', 'county_P', 'region_O', 'region_P', 'state_O', 'state_P', 'province_O', 'province_P', 'district_O', 'district_P', 'territory_O', 'territory_P'], 'existed in' : ['locationCity_O', 'locationCity_P', 'location_O', 'location_P', 'city_O', 'city_P', 'county_O', 'county_P', 'region_O', 'region_P', 'state_O', 'state_P', 'province_O', 'province_P', 'district_O', 'district_P', 'territory_O', 'territory_P']}
properties_dict["existing"] = {'existing' : ['locationCity_O', 'locationCity_P', 'location_O', 'location_P', 'locations_P', 'city_O', 'city_P', 'county_O', 'county_P', 'region_O', 'region_P', 'state_O', 'state_P', 'province_O', 'province_P', 'district_O', 'district_P', 'territory_O', 'territory_P'], 'existing in' : ['locationCity_O', 'locationCity_P', 'location_O', 'location_P', 'city_O', 'city_P', 'county_O', 'county_P', 'region_O', 'region_P', 'state_O', 'state_P', 'province_O', 'province_P', 'district_O', 'district_P', 'territory_O', 'territory_P']}
properties_dict["cover"] = {'cover artist': ['coverArtist_O', 'coverArtist_P'], 'cover': ['coverArtist_O', 'coverArtist_P', 'cover_P', 'address_O', 'address_P', 'crosses_O', 'crosses_P'], 'cover size': ['coverSize_P']}
properties_dict["pole"] = {'pole position': ['poleDriver_O', 'poleDriver_P'], 'pole driver': ['poleDriver_O', 'poleDriver_P'], 'pole team': ['poleTeam_P'], 'pole': ['pole_P', 'poles_O', 'poles_P'], 'pole ecliptic lon': ['poleEclipticLon_P'], 'pole': ['poles_O', 'poles_P'], 'pole driver country': ['poleDriverCountry_P'], 'pole ecliptic lat': ['poleEclipticLat_P'], 'pole speed': ['poleSpeed_P'], 'pole time': ['poleTime_P']}
properties_dict["owner"] = {"owner" : ['owner_O', 'owningOrganisation_O', 'occupation_O', 'authority_O', 'field_P', 'parent_P', 'owners_P', 'owningCompany_O', 'system_P', 'arena_P', 'owned_P', 'parentOrganisation_O', 'parentCompany_O', 'ground_P', 'stadium_P', 'company_P', 'network_O', 'foundedBy_O', 'foundedBy_P']}
properties_dict["owners"] = {"owners" : ['owner_O', 'owningOrganisation_O', 'occupation_O', 'authority_O', 'field_P', 'parent_P', 'owners_P', 'owningCompany_O', 'system_P', 'arena_P', 'owned_P', 'parentOrganisation_O', 'parentCompany_O', 'ground_P', 'stadium_P', 'company_P', 'network_O', 'foundedBy_O', 'foundedBy_P']}
properties_dict["manage"]["manage a club"] = ['manager_O', 'manager_P', 'managerclubs_P', 'managerClub_O']
properties_dict["manage"]["manage the club"] = ['manager_O', 'manager_P', 'managerclubs_P', 'managerClub_O']
properties_dict["manage"]["manage club"] = ['manager_O', 'manager_P', 'managerclubs_P', 'managerClub_O']
properties_dict["manages"]["manages a club"] = ['manager_O', 'manager_P', 'managerclubs_P', 'managerClub_O']
properties_dict["manages"]["manages the club"] = ['manager_O', 'manager_P', 'managerclubs_P', 'managerClub_O']
properties_dict["manages"]["manages club"] = ['manager_O', 'manager_P', 'managerclubs_P', 'managerClub_O']
properties_dict["managed"]["managed a club"] = ['manager_O', 'manager_P', 'managerclubs_P', 'managerClub_O']
properties_dict["managed"]["managed the club"] = ['manager_O', 'manager_P', 'managerclubs_P', 'managerClub_O']
properties_dict["managed"]["managed club"] = ['manager_O', 'manager_P', 'managerclubs_P', 'managerClub_O']
properties_dict["managing"]["managing a club"] = ['manager_O', 'manager_P', 'managerclubs_P', 'managerClub_O']
properties_dict["managing"]["managing the club"] = ['manager_O', 'manager_P', 'managerclubs_P', 'managerClub_O']
properties_dict["managing"]["managing club"] = ['manager_O', 'manager_P', 'managerclubs_P', 'managerClub_O']
properties_dict["development"]["development"] = ['developer_O', 'developer_P', 'development_P']
properties_dict["flow"] = {'flow' : ['inflow_O', 'inflow_P', 'rightTributary_O', 'rightTributary_P', 'leftTributary_O', 'leftTributary_P', 'flow_P', 'outflow_O', 'outflow_P'], 'flow into' : ['inflow_O', 'inflow_P', 'rightTributary_O', 'rightTributary_P', 'leftTributary_O', 'leftTributary_P', 'flow_P'], 'flow out' : ['outflow_O', 'outflow_P'], 'flow through' : ['city_O', 'city_P', 'cities_P']}
properties_dict["flows"] = {'flows' : ['inflow_O', 'inflow_P', 'rightTributary_O', 'rightTributary_P', 'leftTributary_O', 'leftTributary_P', 'flow_P', 'outflow_O', 'outflow_P'], 'flows into' : ['inflow_O', 'inflow_P', 'rightTributary_O', 'rightTributary_P', 'leftTributary_O', 'leftTributary_P', 'flow_P'], 'flows out' : ['outflow_O', 'outflow_P'], 'flows through' : ['city_O', 'city_P', 'cities_P']}
properties_dict["flowed"] = {'flowed' : ['inflow_O', 'inflow_P', 'rightTributary_O', 'rightTributary_P', 'leftTributary_O', 'leftTributary_P', 'flow_P', 'outflow_O', 'outflow_P'], 'flowed into' : ['inflow_O', 'inflow_P', 'rightTributary_O', 'rightTributary_P', 'leftTributary_O', 'leftTributary_P', 'flow_P'], 'flowed out' : ['outflow_O', 'outflow_P'], 'flowed through' : ['city_O', 'city_P', 'cities_P']}
properties_dict["flowing"] = {'flowing' : ['inflow_O', 'inflow_P', 'rightTributary_O', 'rightTributary_P', 'leftTributary_O', 'leftTributary_P', 'flow_P', 'outflow_O', 'outflow_P'], 'flowing into' : ['inflow_O', 'inflow_P', 'rightTributary_O', 'rightTributary_P', 'leftTributary_O', 'leftTributary_P', 'flow_P'], 'flowing out' : ['outflow_O', 'outflow_P'], 'flowing through' : ['city_O', 'city_P', 'cities_P']}
properties_dict["power"]["power"] = ['power_P', 'office_O', 'office_P', 'constituency_P']
properties_dict["come"] = {'come to': ['related_O', 'related_P'], 'come up to': ['address_O', 'address_P'], 'come through': ['wins_O', 'wins_P'], 'come before': ['predecessor_O', 'predecessor_P'], 'come from': ['birthPlace_O', 'birthPlace_P', 'placeOfBirth_P', 'homeland_P', 'hometown_O', 'homeTown_P']}
properties_dict["comes"] = {'comes to': ['related_O', 'related_P'], 'comes up to': ['address_O', 'address_P'], 'comes through': ['wins_O', 'wins_P'], 'comes before': ['predecessor_O', 'predecessor_P'], 'comes from': ['birthPlace_O', 'birthPlace_P', 'placeOfBirth_P', 'homeland_P', 'hometown_O', 'homeTown_P']}
properties_dict["came"] = {'came to': ['related_O', 'related_P'], 'came up to': ['address_O', 'address_P'], 'came through': ['wins_O', 'wins_P'], 'came before': ['predecessor_O', 'predecessor_P'], 'came from': ['birthPlace_O', 'birthPlace_P', 'placeOfBirth_P', 'homeland_P', 'hometown_O', 'homeTown_P']}
properties_dict["coming"] = {'coming to': ['related_O', 'related_P'], 'coming up to': ['address_O', 'address_P'], 'coming through': ['wins_O', 'wins_P'], 'coming before': ['predecessor_O', 'predecessor_P'], 'coming from': ['birthPlace_O', 'birthPlace_P', 'placeOfBirth_P', 'homeland_P', 'hometown_O', 'homeTown_P']}
properties_dict["award"]["award"] = ['award_O', 'award_P', 'honours_O', 'honours_P', 'awards_P']
properties_dict["awards"]["awards"] = ['award_O', 'award_P', 'honours_O', 'honours_P', 'awards_P']
properties_dict["awarded"]["awarded"] = ['award_O', 'award_P', 'honours_O', 'honours_P', 'awards_P']
properties_dict["awarded"]["awarded by"] = ['award_O', 'award_P', 'honours_O', 'honours_P', 'awards_P', 'awardedBy_P']
properties_dict["awarded"]["awarded to"] = ['award_O', 'award_P', 'honours_O', 'honours_P', 'awards_P', 'awardedBy_P']
properties_dict["famous"]["famous for"] = ['knownFor_O', 'knownFor_P', 'famousFor_P', 'notableWork_O', 'notableworks_P', 'works_P', 'notablework_P', 'notableWorks_P', 'notableWork_P', 'importantWorks_P', 'field_O', 'field_P']
properties_dict["famous"]["famous"] = ['knownFor_O', 'knownFor_P', 'famousFor_P', 'notableWork_O', 'notableworks_P', 'works_P', 'notablework_P', 'notableWorks_P', 'notableWork_P', 'importantWorks_P', 'field_O', 'field_P']
del properties_dict["famous"]["Famous for"]
properties_dict["judge"] = {'judge': ['judge_O', 'judge_P', 'judges_P'], 'judge president': ['judgepresident_P'], 'judge rapporteur': ['judgerapporteur_P']}
properties_dict["judges"] = {'judges': ['judge_O', 'judge_P', 'judges_P']}
properties_dict["judged"] = {'judged': ['judge_O', 'judge_P', 'judges_P'], 'judged by': ['judge_O', 'judge_P', 'judges_P']}
properties_dict["judging"] = {'judging': ['judge_O', 'judge_P', 'judges_P']}
properties_dict["known"]["known for"] = ['knownFor_O', 'knownFor_P', 'famousFor_P', 'notableWork_O', 'notableworks_P', 'works_P', 'notablework_P', 'notableWorks_P', 'notableWork_P', 'importantWorks_P', 'field_O', 'field_P']
properties_dict["compose"]["compose music"] = ['writer_O', 'writer_P', 'author_O', 'author_P', 'composer_O', 'composer_P', 'musicBy_O', 'musicBy_P', 'music_P']
properties_dict["composes"]["composes music"] = ['writer_O', 'writer_P', 'author_O', 'author_P', 'composer_O', 'composer_P', 'musicBy_O', 'musicBy_P', 'music_P']
properties_dict["composed"]["composed music"] = ['writer_O', 'writer_P', 'author_O', 'author_P', 'composer_O', 'composer_P', 'musicBy_O', 'musicBy_P', 'music_P']
properties_dict["composing"]["composing music"] = ['writer_O', 'writer_P', 'author_O', 'author_P', 'composer_O', 'composer_P', 'musicBy_O', 'musicBy_P']
properties_dict["breed"] = {"breed" : ['breed_P', 'breeder_O', 'breeder_P']}
properties_dict["breeds"] = {"breeds" : ['breed_P', 'breeder_O', 'breeder_P']}
properties_dict["bred"] = {"bred" : ['breeder_O', 'breeder_P'], "bred by" : ['breeder_O', 'breeder_P']}
properties_dict["breeding"] = {"breeding" : ['breeder_O', 'breeder_P', 'breed_P']}
properties_dict["sire"] = {"sire" : ['sire_O', 'sire_P']}
properties_dict["sires"] = {"sires" : ['sire_O', 'sire_P']}
properties_dict["sired"] = {"sired" : ['sire_O', 'sire_P'], "sired by" : ['breeder_O', 'breeder_P']}
properties_dict["siring"] = {"siring" : ['sire_O', 'sire_P']}
properties_dict["hold"] = {'hold in': ['locationCity_O', 'locationCity_P', 'location_O', 'location_P', 'locations_P', 'city_O', 'city_P', 'district_O', 'district_P', 'territory_O', 'territory_P', 'address_O', 'address_P'], 'hold at': ['locationCity_O', 'locationCity_P', 'location_O', 'location_P', 'city_O', 'city_P', 'district_O', 'district_P', 'territory_O', 'territory_P', 'address_O', 'address_P']}
properties_dict["holds"] = {'holds in': ['locationCity_O', 'locationCity_P', 'location_O', 'location_P', 'locations_P', 'city_O', 'city_P', 'district_O', 'district_P', 'territory_O', 'territory_P', 'address_O', 'address_P'], 'holds at': ['locationCity_O', 'locationCity_P', 'location_O', 'location_P', 'city_O', 'city_P', 'district_O', 'district_P', 'territory_O', 'territory_P', 'address_O', 'address_P']}
properties_dict["held"] = {'held in': ['locationCity_O', 'locationCity_P', 'location_O', 'location_P', 'locations_P', 'city_O', 'city_P', 'district_O', 'district_P', 'territory_O', 'territory_P', 'address_O', 'address_P'], 'held at': ['locationCity_O', 'locationCity_P', 'location_O', 'location_P', 'city_O', 'city_P', 'district_O', 'district_P', 'territory_O', 'territory_P', 'address_O', 'address_P']}
properties_dict["holding"] = {'holding in': ['locationCity_O', 'locationCity_P', 'location_O', 'location_P', 'locations_P', 'city_O', 'city_P', 'district_O', 'district_P', 'territory_O', 'territory_P', 'address_O', 'address_P'], 'holding at': ['locationCity_O', 'locationCity_P', 'location_O', 'location_P', 'city_O', 'city_P', 'district_O', 'district_P', 'territory_O', 'territory_P', 'address_O', 'address_P']}
properties_dict["lead"] = {'lead': ['lead_P', 'keyPerson_O', 'leaderName_O', 'leaderName_P', 'result_O', 'result_P', 'principal_O', 'principal_P', 'head_O', 'head_P', 'subsequentWork_O', 'subsequentWork_P'], 'lead to': ['lead_P', 'result_O', 'result_P', 'principal_O', 'principal_P', 'head_O', 'head_P', 'subsequentWork_O', 'subsequentWork_P']}
properties_dict["leads"] = {'leads': ['lead_P', 'keyPerson_O', 'leaderName_O', 'leaderName_P', 'result_O', 'result_P', 'principal_O', 'principal_P', 'head_O', 'head_P', 'subsequentWork_O', 'subsequentWork_P'], 'leads to': ['lead_P', 'result_O', 'result_P', 'principal_O', 'principal_P', 'head_O', 'head_P', 'subsequentWork_O', 'subsequentWork_P']}
properties_dict["led"] = {'led': ['lead_P', 'keyPerson_O', 'leaderName_O', 'leaderName_P', 'result_O', 'result_P', 'principal_O', 'principal_P', 'head_O', 'head_P', 'subsequentWork_O', 'subsequentWork_P'], 'led by': ['lead_P', 'keyPerson_O', 'leaderName_O', 'leaderName_P', 'principal_O', 'principal_P', 'head_O', 'head_P'], 'led to': ['lead_P', 'result_O', 'result_P', 'principal_O', 'principal_P', 'head_O', 'head_P', 'subsequentWork_O', 'subsequentWork_P']}
properties_dict["leading"] = {'leading': ['lead_P', 'keyPerson_O', 'leaderName_O', 'leaderName_P', 'result_O', 'result_P', 'principal_O', 'principal_P', 'head_O', 'head_P', 'subsequentWork_O', 'subsequentWork_P'], 'leading to': ['lead_P', 'result_O', 'result_P', 'principal_O', 'principal_P', 'head_O', 'head_P', 'subsequentWork_O', 'subsequentWork_P']}
properties_dict["do"] = {'do phd': ['doctoralAdvisor_P', 'doctoralAdvisor_O', 'phdStudents_P', 'phdAlmaMater_P']}
properties_dict["does"] = {'does phd': ['doctoralAdvisor_P', 'doctoralAdvisor_O', 'phdStudents_P', 'phdAlmaMater_P']}
properties_dict["did"] = {'did phd': ['doctoralAdvisor_P', 'doctoralAdvisor_O', 'phdStudents_P', 'phdAlmaMater_P']}
properties_dict["doing"] = {'doing phd': ['doctoralAdvisor_P', 'doctoralAdvisor_O', 'phdStudents_P', 'phdAlmaMater_P']}
properties_dict["act"] = {'act as': ['plays_O', 'plays_P'], 'act upon': ['influenced_O', 'influenced_P'], 'act': ['act_P', 'plays_O', 'plays_P', 'starring_P', 'starring_O'], 'act in': ['starring_P', 'starring_O', 'act_P', 'plays_O', 'plays_P']}
properties_dict["acts"] = {'acts as': ['plays_O', 'plays_P'], 'acts upon': ['influenced_O', 'influenced_P'], 'acts': ['act_P', 'plays_O', 'plays_P', 'starring_P', 'starring_O'], 'acts in': ['starring_P', 'starring_O', 'act_P', 'plays_O', 'plays_P']}
properties_dict["acted"] = {'acted as': ['plays_O', 'plays_P'], 'acted upon': ['influenced_O', 'influenced_P'], 'acted': ['act_P', 'plays_O', 'plays_P', 'starring_P', 'starring_O'], 'acted in': ['starring_P', 'starring_O', 'act_P', 'plays_O', 'plays_P']}
properties_dict["acting"] = {'acting as': ['plays_O', 'plays_P'], 'acting upon': ['influenced_O', 'influenced_P'], 'acting': ['act_P', 'plays_O', 'plays_P', 'starring_P', 'starring_O'], 'acting in': ['starring_P', 'starring_O', 'act_P', 'plays_O', 'plays_P']}
properties_dict["collaborate"] = {'collaborate': ['related_O', 'related_P', 'relative_O', 'relative_P', 'relation_O', 'relation_P', 'associatedBand_O', 'associatedBand_P', 'associatedMusicalArtist_O', 'associatedMusicalArtist_P'], 'collaborate with': ['related_O', 'related_P', 'relative_O', 'relative_P', 'relation_O', 'relation_P', 'associatedBand_O', 'associatedBand_P', 'associatedMusicalArtist_O', 'associatedMusicalArtist_P']}
properties_dict["collaborates"] = {'collaborates': ['related_O', 'related_P', 'relative_O', 'relative_P', 'relation_O', 'relation_P', 'associatedBand_O', 'associatedBand_P', 'associatedMusicalArtist_O', 'associatedMusicalArtist_P'], 'collaborates with': ['related_O', 'related_P', 'relative_O', 'relative_P', 'relation_O', 'relation_P', 'associatedBand_O', 'associatedBand_P', 'associatedMusicalArtist_O', 'associatedMusicalArtist_P']}
properties_dict["collaborated"] = {'collaborated': ['related_O', 'related_P', 'relative_O', 'relative_P', 'relation_O', 'relation_P', 'associatedBand_O', 'associatedBand_P', 'associatedMusicalArtist_O', 'associatedMusicalArtist_P'], 'collaborated with': ['related_O', 'related_P', 'relative_O', 'relative_P', 'relation_O', 'relation_P', 'associatedBand_O', 'associatedBand_P', 'associatedMusicalArtist_O', 'associatedMusicalArtist_P']}
properties_dict["collaborating"] = {'collaborating': ['related_O', 'related_P', 'relative_O', 'relative_P', 'relation_O', 'relation_P', 'associatedMusicalArtist_O', 'associatedMusicalArtist_P', 'associatedBand_O', 'associatedBand_P'], 'collaborating with': ['related_O', 'related_P', 'relative_O', 'relative_P', 'relation_O', 'relation_P', 'associatedMusicalArtist_O', 'associatedMusicalArtist_P', 'associatedBand_O', 'associatedBand_P']}
properties_dict["connect"] = {'connect': ['associatedMusicalArtist_O', 'associatedBand_O', 'associatedActs_P', 'associate_O', 'associate_P', 'related_O', 'related_P'], 'connect to': ['associatedMusicalArtist_O', 'associatedBand_O', 'associatedActs_P', 'associate_O', 'associate_P', 'related_O', 'related_P']}
properties_dict["connects"] = {'connects': ['associatedMusicalArtist_O', 'associatedBand_O', 'associatedActs_P', 'associate_O', 'associate_P', 'related_O', 'related_P'], 'connects to': ['associatedMusicalArtist_O', 'associatedBand_O', 'associatedActs_P', 'associate_O', 'associate_P', 'related_O', 'related_P']}
properties_dict["connected"] = {'connected': ['associatedMusicalArtist_O', 'associatedBand_O', 'associatedActs_P', 'associate_O', 'associate_P', 'related_O', 'related_P'], 'connected to': ['associatedMusicalArtist_O', 'associatedBand_O', 'associatedActs_P', 'associate_O', 'associate_P', 'related_O', 'related_P']}
properties_dict["connecting"] = {'connecting': ['associatedMusicalArtist_O', 'associatedBand_O', 'associatedActs_P', 'associate_O', 'associate_P', 'related_O', 'related_P'], 'connecting to': ['associatedMusicalArtist_O', 'associatedBand_O', 'associatedActs_P', 'associate_O', 'associate_P', 'related_O', 'related_P']}
properties_dict["bury"] = {'bury': ['restingPlace_O', 'restingPlace_P', 'restingplace_P', 'placeOfBurial_P', 'buriedPlace_P', 'buriedAt_P', 'buried_P', 'burialLocation_P', 'burial_P'], 'bury at': ['restingPlace_O', 'restingPlace_P', 'restingplace_P', 'placeOfBurial_P', 'buriedPlace_P', 'buriedAt_P', 'buried_P', 'burialLocation_P', 'burial_P'], 'bury in': ['restingPlace_O', 'restingPlace_P', 'restingplace_P', 'placeOfBurial_P', 'buriedPlace_P', 'buriedAt_P', 'buried_P', 'burialLocation_P', 'burial_P']}
properties_dict["buries"] = {'buries': ['restingPlace_O', 'restingPlace_P', 'restingplace_P', 'placeOfBurial_P', 'buriedPlace_P', 'buriedAt_P', 'buried_P', 'burialLocation_P', 'burial_P'], 'buries at': ['restingPlace_O', 'restingPlace_P', 'restingplace_P', 'placeOfBurial_P', 'buriedPlace_P', 'buriedAt_P', 'buried_P', 'burialLocation_P', 'burial_P'], 'buries in': ['restingPlace_O', 'restingPlace_P', 'restingplace_P', 'placeOfBurial_P', 'buriedPlace_P', 'buriedAt_P', 'buried_P', 'burialLocation_P', 'burial_P']}
properties_dict["buried"] = {'buried': ['restingPlace_O', 'restingPlace_P', 'restingplace_P', 'placeOfBurial_P', 'buriedPlace_P', 'buriedAt_P', 'buried_P', 'burialLocation_P', 'burial_P'], 'buried at': ['restingPlace_O', 'restingPlace_P', 'restingplace_P', 'placeOfBurial_P', 'buriedPlace_P', 'buriedAt_P', 'buried_P', 'burialLocation_P', 'burial_P'], 'buried in': ['restingPlace_O', 'restingPlace_P', 'restingplace_P', 'placeOfBurial_P', 'buriedPlace_P', 'buriedAt_P', 'buried_P', 'burialLocation_P', 'burial_P'], 'buried place': ['buriedPlace_P']}
properties_dict["burying"] = {'burying': ['restingPlace_O', 'restingPlace_P', 'restingplace_P', 'placeOfBurial_P', 'buriedPlace_P', 'buriedAt_P', 'buried_P', 'burialLocation_P', 'burial_P'], 'burying at': ['restingPlace_O', 'restingPlace_P', 'restingplace_P', 'placeOfBurial_P', 'buriedPlace_P', 'buriedAt_P', 'buried_P', 'burialLocation_P', 'burial_P'], 'burying in': ['restingPlace_O', 'restingPlace_P', 'restingplace_P', 'placeOfBurial_P', 'buriedPlace_P', 'buriedAt_P', 'buried_P', 'burialLocation_P', 'burial_P']}
properties_dict["die"] = {'die': ['deathPlace_O', 'deathPlace_P', 'placeOfDeath_P', 'deathCause_O', 'deathCause_P', 'causeOfDeath_P'], 'die in': ['deathPlace_O', 'deathPlace_P', 'placeOfDeath_P'], 'die at': ['deathPlace_O', 'deathPlace_P', 'placeOfDeath_P', 'deathCause_O', 'deathCause_P', 'causeOfDeath_P'], 'die from': ['deathCause_O', 'deathCause_P', 'causeOfDeath_P'], 'die due to': ['deathCause_O', 'deathCause_P', 'causeOfDeath_P'], 'die of': ['deathCause_O', 'deathCause_P', 'causeOfDeath_P']}
properties_dict["dies"] = {'dies': ['deathPlace_O', 'deathPlace_P', 'placeOfDeath_P', 'deathCause_O', 'deathCause_P', 'causeOfDeath_P'], 'dies in': ['deathPlace_O', 'deathPlace_P', 'placeOfDeath_P'], 'dies at': ['deathPlace_O', 'deathPlace_P', 'placeOfDeath_P', 'deathCause_O', 'deathCause_P', 'causeOfDeath_P'], 'dies from': ['deathCause_O', 'deathCause_P', 'causeOfDeath_P'], 'dies due to': ['deathCause_O', 'deathCause_P', 'causeOfDeath_P'], 'dies of': ['deathCause_O', 'deathCause_P', 'causeOfDeath_P']}
properties_dict["died"] = {'died': ['deathPlace_O', 'deathPlace_P', 'placeOfDeath_P', 'deathCause_O', 'deathCause_P', 'causeOfDeath_P'], 'died in': ['deathPlace_O', 'deathPlace_P', 'placeOfDeath_P'], 'died at': ['deathPlace_O', 'deathPlace_P', 'placeOfDeath_P', 'deathCause_O', 'deathCause_P', 'causeOfDeath_P'], 'died from': ['deathCause_O', 'deathCause_P', 'causeOfDeath_P'], 'died due to': ['deathCause_O', 'deathCause_P', 'causeOfDeath_P'], 'died of': ['deathCause_O', 'deathCause_P', 'causeOfDeath_P']}
properties_dict["dead"] = {'dead': ['deathPlace_O', 'deathPlace_P', 'placeOfDeath_P', 'deathCause_O', 'deathCause_P', 'causeOfDeath_P'], 'dead in': ['deathPlace_O', 'deathPlace_P', 'placeOfDeath_P'], 'dead at': ['deathPlace_O', 'deathPlace_P', 'placeOfDeath_P', 'deathCause_O', 'deathCause_P', 'causeOfDeath_P'], 'dead from': ['deathCause_O', 'deathCause_P', 'causeOfDeath_P'], 'dead due to': ['deathCause_O', 'deathCause_P', 'causeOfDeath_P']}
properties_dict["dying"] = {'dying': ['deathPlace_O', 'deathPlace_P', 'placeOfDeath_P', 'deathCause_O', 'deathCause_P', 'causeOfDeath_P'], 'dying in': ['deathPlace_O', 'deathPlace_P', 'placeOfDeath_P'], 'dying at': ['deathPlace_O', 'deathPlace_P', 'placeOfDeath_P'], 'dying from': ['deathCause_O', 'deathCause_P', 'causeOfDeath_P'], 'dying due to': ['deathCause_O', 'deathCause_P', 'causeOfDeath_P'], 'dying of': ['deathCause_O', 'deathCause_P', 'causeOfDeath_P']}
properties_dict["live"] = {'live': ['residence_O', 'residence_P', 'live_P'], 'live in': ['residence_O', 'residence_P', 'liveIn_P'], 'live albums': ['liveAlbums_P']}
properties_dict["lives"] = {'lives': ['residence_O', 'residence_P', 'live_P'], 'lives in': ['residence_O', 'residence_P', 'liveIn_P']}
properties_dict["lived"] = {'lived': ['residence_O', 'residence_P', 'live_P'], 'lived in': ['residence_O', 'residence_P', 'liveIn_P']}
properties_dict["living"] = {'living': ['residence_O', 'residence_P', 'live_P'], 'living in': ['residence_O', 'residence_P', 'liveIn_P']}
properties_dict["reside"] = {'reside': ['residence_O', 'residence_P', 'live_P'], 'reside in': ['residence_O', 'residence_P', 'liveIn_P']}
properties_dict["resides"] = {'resides': ['residence_O', 'residence_P', 'live_P'], 'resides in': ['residence_O', 'residence_P', 'liveIn_P']}
properties_dict["resided"] = {'resided': ['residence_O', 'residence_P', 'live_P'], 'resided in': ['residence_O', 'residence_P', 'liveIn_P']}
properties_dict["residing"] = {'living': ['residence_O', 'residence_P', 'live_P'], 'residing in': ['residence_O', 'residence_P', 'liveIn_P']}
properties_dict["sell"] = {'sell': ['soldBy_P', 'manufacturer_O', 'manufacturer_P', 'region_O', 'region_P']}
properties_dict["sells"] = {'sells': ['soldBy_P', 'manufacturer_O', 'manufacturer_P', 'region_O', 'region_P']}
properties_dict["sold"] = {'sold': ['soldBy_P', 'manufacturer_O', 'manufacturer_P', 'region_O', 'region_P']}
properties_dict["selling"] = {'selling': ['soldBy_P', 'manufacturer_O', 'manufacturer_P', 'region_O', 'region_P']}
properties_dict["study"] = {'study_where': ['college_O', 'college_P', 'university_O', 'university_P', 'almaMater_O', 'almaMater_P', 'institution_O', 'institution_P', 'education_O', 'education_P', 'training_O', 'training_P', 'school_O', 'school_P'], 'study at': ['college_O', 'college_P', 'university_O', 'university_P', 'almaMater_O', 'almaMater_P', 'institution_O', 'institution_P', 'education_O', 'education_P', 'training_O', 'training_P', 'school_O', 'school_P'], 'study in': ['college_O', 'college_P', 'university_O', 'university_P', 'almaMater_O', 'almaMater_P', 'institution_O', 'institution_P', 'education_O', 'education_P', 'training_O', 'training_P', 'school_O', 'school_P'], 'study_what': ['field_O', 'field_P', 'discipline_O', 'discipline_P', 'mainInterests_P'], 'study': ['college_O', 'college_P', 'university_O', 'university_P', 'almaMater_O', 'almaMater_P', 'institution_O', 'institution_P', 'education_O', 'education_P', 'training_O', 'training_P', 'school_O', 'school_P', 'field_O', 'field_P', 'discipline_O', 'discipline_P', 'mainInterests_P']}
properties_dict["studies"] = {'studies_where': ['college_O', 'college_P', 'university_O', 'university_P', 'almaMater_O', 'almaMater_P', 'institution_O', 'institution_P', 'education_O', 'education_P', 'training_O', 'training_P', 'school_O', 'school_P'], 'studies at': ['college_O', 'college_P', 'university_O', 'university_P', 'almaMater_O', 'almaMater_P', 'institution_O', 'institution_P', 'education_O', 'education_P', 'training_O', 'training_P', 'school_O', 'school_P'], 'studies in': ['college_O', 'college_P', 'university_O', 'university_P', 'almaMater_O', 'almaMater_P', 'institution_O', 'institution_P', 'education_O', 'education_P', 'training_O', 'training_P', 'school_O', 'school_P'], 'studies_what': ['field_O', 'field_P', 'discipline_O', 'discipline_P', 'mainInterests_P'], 'studies': ['college_O', 'college_P', 'university_O', 'university_P', 'almaMater_O', 'almaMater_P', 'institution_O', 'institution_P', 'education_O', 'education_P', 'training_O', 'training_P', 'field_O', 'field_P', 'discipline_O', 'discipline_P', 'mainInterests_P', 'school_O', 'school_P']}
properties_dict["studied"] = {'studied_where': ['college_O', 'college_P', 'university_O', 'university_P', 'almaMater_O', 'almaMater_P', 'institution_O', 'institution_P', 'education_O', 'education_P', 'training_O', 'training_P', 'school_O', 'school_P'], 'studied at': ['college_O', 'college_P', 'university_O', 'university_P', 'almaMater_O', 'almaMater_P', 'institution_O', 'institution_P', 'education_O', 'education_P', 'training_O', 'training_P', 'school_O', 'school_P'], 'studied in': ['college_O', 'college_P', 'university_O', 'university_P', 'almaMater_O', 'almaMater_P', 'institution_O', 'institution_P', 'education_O', 'education_P', 'training_O', 'training_P', 'school_O', 'school_P'], 'studied_what': ['field_O', 'field_P', 'discipline_O', 'discipline_P', 'mainInterests_P'], 'studied': ['college_O', 'college_P', 'university_O', 'university_P', 'almaMater_O', 'almaMater_P', 'institution_O', 'institution_P', 'education_O', 'education_P', 'training_O', 'training_P', 'field_O', 'field_P', 'discipline_O', 'discipline_P', 'mainInterests_P', 'school_O', 'school_P']}
properties_dict["studying"] = {'studying_where': ['college_O', 'college_P', 'university_O', 'university_P', 'almaMater_O', 'almaMater_P', 'institution_O', 'institution_P', 'education_O', 'education_P', 'training_O', 'training_P', 'school_O', 'school_P'], 'studying at': ['college_O', 'college_P', 'university_O', 'university_P', 'almaMater_O', 'almaMater_P', 'institution_O', 'institution_P', 'education_O', 'education_P', 'training_O', 'training_P', 'school_O', 'school_P'], 'studying in': ['college_O', 'college_P', 'university_O', 'university_P', 'almaMater_O', 'almaMater_P', 'institution_O', 'institution_P', 'education_O', 'education_P', 'training_O', 'training_P', 'school_O', 'school_P'], 'studying_what': ['field_O', 'field_P', 'discipline_O', 'discipline_P', 'mainInterests_P'], 'studying_': ['college_O', 'college_P', 'university_O', 'university_P', 'almaMater_O', 'almaMater_P', 'institution_O', 'institution_P', 'education_O', 'education_P', 'training_O', 'training_P', 'field_O', 'field_P', 'discipline_O', 'discipline_P', 'mainInterests_P', 'school_O', 'school_P']}
del properties_dict["career"]["career"]
properties_dict["graduate"] = {'graduate': ['education_O', 'education_P', 'university_O', 'university_P', 'almaMater_O', 'almaMater_P', 'college_O', 'college_P', 'institution_O', 'institution_P''training_O', 'training_P', 'school_O', 'school_P'], 'graduate from': ['education_O', 'education_P', 'university_O', 'university_P', 'almaMater_O', 'almaMater_P', 'college_O', 'college_P', 'institution_O', 'institution_P''training_O', 'training_P', 'school_O', 'school_P']}
properties_dict["graduates"] = {'graduates': ['education_O', 'education_P', 'university_O', 'university_P', 'almaMater_O', 'almaMater_P', 'college_O', 'college_P', 'institution_O', 'institution_P''training_O', 'training_P', 'school_O', 'school_P'], 'graduates from': ['education_O', 'education_P', 'university_O', 'university_P', 'almaMater_O', 'almaMater_P', 'college_O', 'college_P', 'institution_O', 'institution_P''training_O', 'training_P', 'school_O', 'school_P']}
properties_dict["graduated"] = {'graduated': ['education_O', 'education_P', 'university_O', 'university_P', 'almaMater_O', 'almaMater_P', 'college_O', 'college_P', 'institution_O', 'institution_P''training_O', 'training_P', 'school_O', 'school_P'], 'graduated from': ['education_O', 'education_P', 'university_O', 'university_P', 'almaMater_O', 'almaMater_P', 'college_O', 'college_P', 'institution_O', 'institution_P''training_O', 'training_P', 'school_O', 'school_P']}
properties_dict["graduating"] = {'graduating': ['education_O', 'education_P', 'university_O', 'university_P', 'almaMater_O', 'almaMater_P', 'college_O', 'college_P', 'institution_O', 'institution_P''training_O', 'training_P', 'school_O', 'school_P'], 'graduating from': ['education_O', 'education_P', 'university_O', 'university_P', 'almaMater_O', 'almaMater_P', 'college_O', 'college_P', 'institution_O', 'institution_P''training_O', 'training_P', 'school_O', 'school_P']}
properties_dict["educate"] = {'educate': ['education_O', 'education_P', 'university_O', 'university_P', 'almaMater_O', 'almaMater_P', 'college_O', 'college_P', 'institution_O', 'institution_P''training_O', 'training_P', 'school_O', 'school_P'], 'educate at': ['education_O', 'education_P', 'university_O', 'university_P', 'almaMater_O', 'almaMater_P', 'college_O', 'college_P', 'institution_O', 'institution_P''training_O', 'training_P', 'school_O', 'school_P'], 'educate in': ['education_O', 'education_P', 'university_O', 'university_P', 'almaMater_O', 'almaMater_P', 'college_O', 'college_P', 'institution_O', 'institution_P''training_O', 'training_P', 'school_O', 'school_P']}
properties_dict["educates"] = {'educates': ['education_O', 'education_P', 'university_O', 'university_P', 'almaMater_O', 'almaMater_P', 'college_O', 'college_P', 'institution_O', 'institution_P''training_O', 'training_P', 'school_O', 'school_P'], 'educates at': ['education_O', 'education_P', 'university_O', 'university_P', 'almaMater_O', 'almaMater_P', 'college_O', 'college_P', 'institution_O', 'institution_P''training_O', 'training_P', 'school_O', 'school_P'], 'educates in': ['education_O', 'education_P', 'university_O', 'university_P', 'almaMater_O', 'almaMater_P', 'college_O', 'college_P', 'institution_O', 'institution_P''training_O', 'training_P', 'school_O', 'school_P']}
properties_dict["educated"] = {'educated': ['education_O', 'education_P', 'university_O', 'university_P', 'almaMater_O', 'almaMater_P', 'college_O', 'college_P', 'institution_O', 'institution_P''training_O', 'training_P', 'school_O', 'school_P'], 'educated at': ['education_O', 'education_P', 'university_O', 'university_P', 'almaMater_O', 'almaMater_P', 'college_O', 'college_P', 'institution_O', 'institution_P''training_O', 'training_P', 'school_O', 'school_P'], 'educated in': ['education_O', 'education_P', 'university_O', 'university_P', 'almaMater_O', 'almaMater_P', 'college_O', 'college_P', 'institution_O', 'institution_P''training_O', 'training_P', 'school_O', 'school_P']}
properties_dict["educating"] = {'educating': ['education_O', 'education_P', 'university_O', 'university_P', 'almaMater_O', 'almaMater_P', 'college_O', 'college_P', 'institution_O', 'institution_P''training_O', 'training_P', 'school_O', 'school_P'], 'educating at': ['education_O', 'education_P', 'university_O', 'university_P', 'almaMater_O', 'almaMater_P', 'college_O', 'college_P', 'institution_O', 'institution_P''training_O', 'training_P', 'school_O', 'school_P'], 'educating in': ['education_O', 'education_P', 'university_O', 'university_P', 'almaMater_O', 'almaMater_P', 'college_O', 'college_P', 'institution_O', 'institution_P''training_O', 'training_P', 'school_O', 'school_P']}
properties_dict["locate"] = {'locate': ['locationCity_O', 'locationCity_P', 'location_O', 'location_P', 'locations_P', 'city_O', 'city_P', 'county_O', 'county_P', 'state_O', 'state_P', 'province_O', 'province_P', 'region_O', 'region_P', 'district_O', 'district_P', 'territory_O', 'territory_P', 'campus_O', 'campus_P']}
properties_dict["locates"] = {'locates': ['locationCity_O', 'locationCity_P', 'location_O', 'location_P', 'locations_P', 'city_O', 'city_P', 'county_O', 'county_P', 'state_O', 'state_P', 'province_O', 'province_P', 'region_O', 'region_P', 'district_O', 'district_P', 'territory_O', 'territory_P', 'campus_O', 'campus_P']}
properties_dict["located"] = {'located': ['locationCity_O', 'locationCity_P', 'location_O', 'location_P', 'locations_P', 'city_O', 'city_P', 'county_O', 'county_P', 'state_O', 'state_P', 'province_O', 'province_P', 'region_O', 'region_P', 'district_O', 'district_P', 'territory_O', 'territory_P', "based_P", "basedOn_O", "basedOn_P", "basedAt_P", 'birthPlace_O', 'birthPlace_P', 'placeOfBirth_P', 'campus_O', 'campus_P'], 'located at': ['locationCity_O', 'locationCity_P', 'location_O', 'location_P', 'city_O', 'city_P', 'county_O', 'county_P', 'state_O', 'state_P', 'province_O', 'province_P', 'region_O', 'region_P', 'district_O', 'district_P', 'territory_O', 'territory_P', 'birthPlace_O', 'birthPlace_P', 'placeOfBirth_P', 'campus_O', 'campus_P'], 'located in': ['locationCity_O', 'locationCity_P', 'location_O', 'location_P', 'city_O', 'city_P', 'county_O', 'county_P', 'state_O', 'state_P', 'province_O', 'province_P', 'region_O', 'region_P', 'district_O', 'district_P', 'territory_O', 'territory_P', 'birthPlace_O', 'birthPlace_P', 'placeOfBirth_P', 'campus_O', 'campus_P'], 'located in area': ['locatedInArea_O']}
properties_dict["locating"] = {'locating': ['locationCity_O', 'locationCity_P', 'location_O', 'location_P', 'locations_P', 'city_O', 'city_P', 'county_O', 'county_P', 'state_O', 'state_P', 'province_O', 'province_P', 'region_O', 'region_P', 'district_O', 'district_P', 'territory_O', 'territory_P', 'campus_O', 'campus_P']}
properties_dict["born"] = {'born' : ['birthPlace_O', 'birthPlace_P', 'placeOfBirth_P', 'homeland_O', 'homeland_P', 'hometown_O','homeTown_P', 'bornPlace_P', 'stateOfOrigin_O', 'stateOfOrigin_P'], 'born in' : ['birthPlace_O', 'birthPlace_P', 'placeOfBirth_P', 'homeland_O', 'homeland_P', 'hometown_O','homeTown_P', 'bornPlace_P', 'stateOfOrigin_O', 'stateOfOrigin_P'], 'born at' : ['birthPlace_O', 'birthPlace_P', 'placeOfBirth_P', 'homeland_O', 'homeland_P', 'hometown_O','homeTown_P', 'bornPlace_P', 'stateOfOrigin_O', 'stateOfOrigin_P'], 'Born as': ['bornAs_P'], 'born date': ['bornDate_P'], 'Born Place': ['bornPlace_P']}
properties_dict["go"] = {'go': ['destination_O', 'destination_P', 'targetAirport_O', 'targetAirport_P'], 'go to' : ['destination_O', 'destination_P', 'targetAirport_O', 'targetAirport_P']}
properties_dict["goes"] = {'goes': ['destination_O', 'destination_P', 'targetAirport_O', 'targetAirport_P'], 'goes to' : ['destination_O', 'destination_P', 'targetAirport_O', 'targetAirport_P']}
properties_dict["went"] = {'went': ['destination_O', 'destination_P', 'targetAirport_O', 'targetAirport_P'], 'went to' : ['destination_O', 'destination_P', 'targetAirport_O', 'targetAirport_P']}
properties_dict["gone"] = {'gone': ['destination_O', 'destination_P', 'targetAirport_O', 'targetAirport_P'], 'gone to' : ['destination_O', 'destination_P', 'targetAirport_O', 'targetAirport_P']}
properties_dict["going"] = {'going': ['destination_O', 'destination_P', 'targetAirport_O', 'targetAirport_P'], 'going to' : ['destination_O', 'destination_P', 'targetAirport_O', 'targetAirport_P']}
properties_dict["belong"] = {'belong': ['owner_O', 'owningOrganisation_O', 'occupation_O', 'profession_O', 'profession_P', 'authority_O', 'field_P', 'parent_P', 'owners_P', 'owningCompany_O', 'system_P', 'arena_P', 'owned_P', 'parentOrganisation_O', 'parentCompany_O', 'ground_P', 'stadium_P', 'company_P', 'network_O', 'foundedBy_O', 'foundedBy_P'], 'belong to' : ['owner_O', 'owningOrganisation_O', 'occupation_O', 'profession_O', 'profession_P', 'authority_O', 'field_P', 'parent_P', 'owners_P', 'owningCompany_O', 'system_P', 'arena_P', 'owned_P', 'parentOrganisation_O', 'parentCompany_O', 'ground_P', 'stadium_P', 'company_P', 'network_O', 'foundedBy_O', 'foundedBy_P']}
properties_dict["belongs"] = {'belongs': ['owner_O', 'owningOrganisation_O', 'occupation_O', 'profession_O', 'profession_P', 'authority_O', 'field_P', 'parent_P', 'owners_P', 'owningCompany_O', 'system_P', 'arena_P', 'owned_P', 'parentOrganisation_O', 'parentCompany_O', 'ground_P', 'stadium_P', 'company_P', 'network_O', 'foundedBy_O', 'foundedBy_P'], 'belongs to' : ['owner_O', 'owningOrganisation_O', 'occupation_O', 'profession_O', 'profession_P', 'authority_O', 'field_P', 'parent_P', 'owners_P', 'owningCompany_O', 'system_P', 'arena_P', 'owned_P', 'parentOrganisation_O', 'parentCompany_O', 'ground_P', 'stadium_P', 'company_P', 'network_O', 'foundedBy_O', 'foundedBy_P']}
properties_dict["belonged"] = {'belonged': ['owner_O', 'owningOrganisation_O', 'occupation_O', 'profession_O', 'profession_P', 'authority_O', 'field_P', 'parent_P', 'owners_P', 'owningCompany_O', 'system_P', 'arena_P', 'owned_P', 'parentOrganisation_O', 'parentCompany_O', 'ground_P', 'stadium_P', 'company_P', 'network_O', 'foundedBy_O', 'foundedBy_P'], 'belonged to' : ['owner_O', 'owningOrganisation_O', 'occupation_O', 'profession_O', 'profession_P', 'authority_O', 'field_P', 'parent_P', 'owners_P', 'owningCompany_O', 'system_P', 'arena_P', 'owned_P', 'parentOrganisation_O', 'parentCompany_O', 'ground_P', 'stadium_P', 'company_P', 'network_O', 'foundedBy_O', 'foundedBy_P']}
properties_dict["belonging"] = {'belonging': ['owner_O', 'owningOrganisation_O', 'occupation_O', 'profession_O', 'profession_P', 'authority_O', 'field_P', 'parent_P', 'owners_P', 'owningCompany_O', 'system_P', 'arena_P', 'owned_P', 'parentOrganisation_O', 'parentCompany_O', 'ground_P', 'stadium_P', 'company_P', 'network_O', 'foundedBy_O', 'foundedBy_P'], 'belonging to' : ['owner_O', 'owningOrganisation_O', 'occupation_O', 'profession_O', 'profession_P', 'authority_O', 'field_P', 'parent_P', 'owners_P', 'owningCompany_O', 'system_P', 'arena_P', 'owned_P', 'parentOrganisation_O', 'parentCompany_O', 'ground_P', 'stadium_P', 'company_P', 'network_O', 'foundedBy_O', 'foundedBy_P']}
properties_dict["associate"] = {'Associate 7 start': ['associate7Start_P'], 'Associate 8 start': ['associate8Start_P'], 'Associate 3 start': ['associate3Start_P'], 'Associate 4 start': ['associate4Start_P'], 'Associate 2 start': ['associate2Start_P'], 'associate': ['associate_O', 'associate_P', 'related_O', 'related_P', 'associatedMusicalArtist_O', 'associatedBand_O', 'associatedActs_P'], 'associate with': ['associate_O', 'associate_P', 'related_O', 'related_P', 'associatedMusicalArtist_O', 'associatedBand_O', 'associatedActs_P'], 'Associate 6 start': ['associate6Start_P'], 'Associate 8 end': ['associate8End_P'], 'Associate 7 end': ['associate7End_P'], 'Associate 6 end': ['associate6End_P'], 'Associate 3 end': ['associate3End_P'], 'Associate 4 end': ['associate4End_P'], 'Associate 2 end': ['associate2End_P'], 'Associate start': ['associateStart_P'], 'Associate end': ['associateEnd_P'], 'associate degree': ['associate_O', 'associate_P'], 'Associate 5 start': ['associate5Start_P'], 'Associate 5 end': ['associate5End_P']}
properties_dict["associates"] = {'associates': ['associate_O', 'associate_P', 'related_O', 'related_P', 'associatedMusicalArtist_O', 'associatedBand_O', 'associatedActs_P'], 'associates with': ['associate_O', 'associate_P', 'related_O', 'related_P', 'associatedMusicalArtist_O', 'associatedBand_O', 'associatedActs_P']}
properties_dict["associated"] = {'associated': ['associate_O', 'associate_P', 'related_O', 'related_P', 'associatedMusicalArtist_O', 'associatedBand_O', 'associatedActs_P'], 'associated with': ['associate_O', 'associate_P', 'related_O', 'related_P', 'associatedMusicalArtist_O', 'associatedBand_O', 'associatedActs_P']}
properties_dict["associating"] = {'associating': ['associate_O', 'associate_P', 'related_O', 'related_P', 'associatedMusicalArtist_O', 'associatedBand_O', 'associatedActs_P'], 'associating with': ['associate_O', 'associate_P', 'related_O', 'related_P', 'associatedMusicalArtist_O', 'associatedBand_O', 'associatedActs_P']}
properties_dict["originate"] = {'originate': ['hometown_O', 'origin_O', 'stylisticOrigins_P', 'stylisticOrigin_O', 'stylisticOrigin_P', 'sourceRegion_P', 'foundationPlace_O', 'source_O', 'sourceLocation_P', 'sourcePlace_P', 'sourceMountain_O'], 'originate in': ['hometown_O', 'origin_O', 'stylisticOrigins_P', 'stylisticOrigin_O', 'stylisticOrigin_P', 'sourceRegion_P', 'foundationPlace_O', 'source_O', 'sourceLocation_P', 'sourcePlace_P', 'sourceMountain_O']}
properties_dict["originates"] = {'originates': ['hometown_O', 'origin_O', 'stylisticOrigins_P', 'stylisticOrigin_O', 'stylisticOrigin_P', 'sourceRegion_P', 'foundationPlace_O', 'source_O', 'sourceLocation_P', 'sourcePlace_P', 'sourceMountain_O'], 'originates in': ['hometown_O', 'origin_O', 'stylisticOrigins_P', 'stylisticOrigin_O', 'stylisticOrigin_P', 'sourceRegion_P', 'foundationPlace_O', 'source_O', 'sourceLocation_P', 'sourcePlace_P', 'sourceMountain_O']}
properties_dict["originated"] = {'originated': ['hometown_O', 'origin_O', 'stylisticOrigins_P', 'stylisticOrigin_O', 'stylisticOrigin_P', 'sourceRegion_P', 'foundationPlace_O', 'source_O', 'sourceLocation_P', 'sourcePlace_P', 'sourceMountain_O'], 'originated in': ['hometown_O', 'origin_O', 'stylisticOrigins_P', 'stylisticOrigin_O', 'stylisticOrigin_P', 'sourceRegion_P', 'foundationPlace_O', 'source_O', 'sourceLocation_P', 'sourcePlace_P', 'sourceMountain_O']}
properties_dict["originating"] = {'originating': ['hometown_O', 'origin_O', 'stylisticOrigins_P', 'stylisticOrigin_O', 'stylisticOrigin_P', 'sourceRegion_P', 'foundationPlace_O', 'source_O', 'sourceLocation_P', 'sourcePlace_P', 'sourceMountain_O'], 'originating in': ['hometown_O', 'origin_O', 'stylisticOrigins_P', 'stylisticOrigin_O', 'stylisticOrigin_P', 'sourceRegion_P', 'foundationPlace_O', 'source_O', 'sourceLocation_P', 'sourcePlace_P', 'sourceMountain_O']}
properties_dict["sign"] = {'sign': ['sign_P', 'recordLabel_O', 'recordLabel_P'], 'sign up': ['recordLabel_O', 'recordLabel_P'], 'sign up with': ['recordLabel_O', 'recordLabel_P']}
properties_dict["signs"] = {'signs': ['sign_P', 'recordLabel_O', 'recordLabel_P'], 'signs up': ['recordLabel_O', 'recordLabel_P'], 'signs up with': ['recordLabel_O', 'recordLabel_P']}
properties_dict["signed"] = {'signed': ['sign_P', 'recordLabel_O', 'recordLabel_P'], 'signed up': ['recordLabel_O', 'recordLabel_P'], 'signed up with': ['recordLabel_O', 'recordLabel_P']}
properties_dict["signing"] = {'signing': ['sign_P', 'recordLabel_O', 'recordLabel_P'], 'signing up': ['recordLabel_O', 'recordLabel_P'], 'signing up with': ['recordLabel_O', 'recordLabel_P']}
properties_dict["mouth"]['mouth'] = ['mouth_P', 'riverMouth_O']
properties_dict["mouth"]['mouth located'] = ['mouth_P', 'riverMouth_O']
properties_dict["relate"] = {'relate': ['associate_O', 'associate_P', 'related_O', 'related_P', 'relative_O', 'relative_P', 'relation_O', 'relation_P', 'associatedMusicalArtist_O', 'associatedMusicalArtist_P', 'associatedBand_O', 'associatedBand_P', 'relatedTo_P'], 'relate to': ['associate_O', 'associate_P', 'related_O', 'related_P', 'relative_O', 'relative_P', 'relation_O', 'relation_P', 'associatedMusicalArtist_O', 'associatedMusicalArtist_P', 'associatedBand_O', 'associatedBand_P', 'relatedTo_P']}
properties_dict["relates"] = {'relates': ['associate_O', 'associate_P', 'related_O', 'related_P', 'relative_O', 'relative_P', 'relation_O', 'relation_P', 'associatedMusicalArtist_O', 'associatedMusicalArtist_P', 'associatedBand_O', 'associatedBand_P', 'relatedTo_P'], 'relates to': ['associate_O', 'associate_P', 'related_O', 'related_P', 'relative_O', 'relative_P', 'relation_O', 'relation_P', 'associatedMusicalArtist_O', 'associatedMusicalArtist_P', 'associatedBand_O', 'associatedBand_P', 'relatedTo_P']}
properties_dict["related"] = {'related': ['associate_O', 'associate_P', 'related_O', 'related_P', 'relative_O', 'relative_P', 'relation_O', 'relation_P', 'associatedMusicalArtist_O', 'associatedMusicalArtist_P', 'associatedBand_O', 'associatedBand_P', 'relatedTo_P'], 'related to': ['associate_O', 'associate_P', 'related_O', 'related_P', 'relative_O', 'relative_P', 'relation_O', 'relation_P', 'associatedMusicalArtist_O', 'associatedMusicalArtist_P', 'associatedBand_O', 'associatedBand_P', 'relatedTo_P'], 'Related artists': ['relatedArtists_P'], 'related mean of transportation': ['relatedMeanOfTransportation_O'], 'related names': ['relatedNames_P'], 'related occupation': ['relatedOccupation_P'], 'Related acts': ['relatedActs_P']}
properties_dict["relating"] = {'relating': ['associate_O', 'associate_P', 'related_O', 'related_P', 'relative_O', 'relative_P', 'relation_O', 'relation_P', 'associatedMusicalArtist_O', 'associatedMusicalArtist_P', 'associatedBand_O', 'associatedBand_P', 'relatedTo_P'], 'relating to': ['associate_O', 'associate_P', 'related_O', 'related_P', 'relative_O', 'relative_P', 'relation_O', 'relation_P', 'associatedMusicalArtist_O', 'associatedMusicalArtist_P', 'associatedBand_O', 'associatedBand_P', 'relatedTo_P']}
del properties_dict["lost"]["lost"]
properties_dict["system"]["system"] = ['system_P', "settlementType_P"]
properties_dict["phd"]["phd"] = ['doctoralAdvisor_P', 'doctoralAdvisor_O']
properties_dict["take"]["take place"] = ['place_O', 'place_P', 'locationCity_O', 'locationCity_P', 'location_O', 'location_P', 'locations_P', 'city_O', 'city_P', 'county_O', 'county_P', 'state_O', 'state_P', 'province_O', 'province_P', 'region_O', 'region_P', 'district_O', 'district_P', 'territory_O', 'territory_P']
properties_dict["takes"] = {"takes place" : ['place_O', 'place_P', 'locationCity_O', 'locationCity_P', 'location_O', 'location_P', 'locations_P', 'city_O', 'city_P', 'county_O', 'county_P', 'state_O', 'state_P', 'province_O', 'province_P', 'region_O', 'region_P', 'district_O', 'district_P', 'territory_O', 'territory_P']}
properties_dict["took"] = {"took place" : ['place_O', 'place_P', 'locationCity_O', 'locationCity_P', 'location_O', 'location_P', 'locations_P', 'city_O', 'city_P', 'county_O', 'county_P', 'state_O', 'state_P', 'province_O', 'province_P', 'region_O', 'region_P', 'district_O', 'district_P', 'territory_O', 'territory_P']}
properties_dict["taken"] = {"taken place" : ['place_O', 'place_P', 'locationCity_O', 'locationCity_P', 'location_O', 'location_P', 'locations_P', 'city_O', 'city_P', 'county_O', 'county_P', 'state_O', 'state_P', 'province_O', 'province_P', 'region_O', 'region_P', 'district_O', 'district_P', 'territory_O', 'territory_P']}
properties_dict["taking"] = {"taking place" : ['place_O', 'place_P', 'locationCity_O', 'locationCity_P', 'location_O', 'location_P', 'locations_P', 'city_O', 'city_P', 'county_O', 'county_P', 'state_O', 'state_P', 'province_O', 'province_P', 'region_O', 'region_P', 'district_O', 'district_P', 'territory_O', 'territory_P']}
properties_dict["fly"] = {'fly' : ['hubAirport_O', 'hubAirport_P', 'destination_O', 'destination_P', 'targetAirport_O', 'targetAirport_P'], 'fly from' : ['hubAirport_O', 'hubAirport_P'], 'fly to' : ['destination_O', 'destination_P', 'targetAirport_O', 'targetAirport_P']}
properties_dict["flies"] = {'flies' : ['hubAirport_O', 'hubAirport_P', 'destination_O', 'destination_P', 'targetAirport_O', 'targetAirport_P'], 'flies from' : ['hubAirport_O', 'hubAirport_P'], 'flies to' : ['destination_O', 'destination_P', 'targetAirport_O', 'targetAirport_P']}
properties_dict["flied"] = {'flied' : ['hubAirport_O', 'hubAirport_P', 'destination_O', 'destination_P', 'targetAirport_O', 'targetAirport_P'], 'flied from' : ['hubAirport_O', 'hubAirport_P'], 'flied to' : ['destination_O', 'destination_P', 'targetAirport_O', 'targetAirport_P']}
properties_dict["flying"] = {'flying' : ['hubAirport_O', 'hubAirport_P', 'destination_O', 'destination_P', 'targetAirport_O', 'targetAirport_P'], 'flying from' : ['hubAirport_O', 'hubAirport_P'], 'flying to' : ['destination_O', 'destination_P', 'targetAirport_O', 'targetAirport_P'], 'flying field': ['field_O', 'field_P']}
properties_dict["headquartered"] = {'headquartered' : ['headquarters_P', 'headquarter_O'], 'headquartered at' : ['headquarters_P', 'headquarter_O'], 'headquartered in' : ['headquarters_P', 'headquarter_O']}
properties_dict["work"]["work"] = ['work_P', 'notableWork_O', 'notableworks_P', 'works_P', 'notablework_P', 'notableWorks_P', 'notableWork_P', 'importantWorks_P', 'majorWorks_P', 'plays_O', 'plays_P', 'influenced_O', 'influenced_P', 'label_P', 'occupation_O', 'occupation_P', 'profession_O', 'profession_P', 'institution_O', 'institution_P', "employer_O", "employer_P"]
properties_dict["work"]["work for"] = ['label_P', 'occupation_O', 'occupation_P', 'profession_O', 'profession_P', 'institution_O', 'institution_P', 'company_O', 'company_P', "employer_O", "employer_P"]
properties_dict["works"] = {"works" : ['work_P', 'notableWork_O', 'notableworks_P', 'works_P', 'notablework_P', 'notableWorks_P', 'notableWork_P', 'importantWorks_P', 'majorWorks_P', 'plays_O', 'plays_P', 'influenced_O', 'influenced_P', 'label_P', 'occupation_O', 'occupation_P', 'profession_O', 'profession_P', 'institution_O', 'institution_P', "employer_O", "employer_P"], "works for" : ['label_P', 'occupation_O', 'occupation_P', 'profession_O', 'profession_P', 'institution_O', 'institution_P', 'company_O', 'company_P', "employer_O", "employer_P"], 'works under': ['worksUnder_P', "employer_O", "employer_P"]}
properties_dict["worked"] = {"worked" : ['work_P', 'notableWork_O', 'notableworks_P', 'works_P', 'notablework_P', 'notableWorks_P', 'notableWork_P', 'importantWorks_P', 'majorWorks_P', 'plays_O', 'plays_P', 'influenced_O', 'influenced_P', 'label_P', 'occupation_O', 'occupation_P', 'profession_O', 'profession_P', 'institution_O', 'institution_P', "employer_O", "employer_P"], "worked for" : ['label_P', 'occupation_O', 'occupation_P', 'profession_O', 'profession_P', 'institution_O', 'institution_P', 'company_O', 'company_P', "employer_O", "employer_P"], 'worked by until': ['workedByUntil_P'], 'Worked on': ['workedOn_P', "employer_O", "employer_P"]}
properties_dict["working"] = {"working" : ['work_P', 'notableWork_O', 'notableworks_P', 'works_P', 'notablework_P', 'notableWorks_P', 'notableWork_P', 'importantWorks_P', 'majorWorks_P', 'plays_O', 'plays_P', 'influenced_O', 'influenced_P', 'label_P', 'occupation_O', 'occupation_P', 'profession_O', 'profession_P', 'institution_O', 'institution_P', "employer_O", "employer_P"], "working for" : ['label_P', 'occupation_O', 'occupation_P', 'profession_O', 'profession_P', 'institution_O', 'institution_P', 'company_O', 'company_P', "employer_O", "employer_P"]}
del properties_dict["label"]["Label"]
properties_dict["compete"] = {"compete" : ['races_O', 'races_P', 'race_O', 'race_P', 'compete_P'], "compete in" : ['races_O', 'races_P', 'race_O', 'race_P', 'compete_P']}
properties_dict["competes"] = {"competes" : ['races_O', 'races_P', 'race_O', 'race_P', 'compete_P'], "competes in" : ['races_O', 'races_P', 'race_O', 'race_P', 'compete_P']}
properties_dict["competed"] = {"competed" : ['races_O', 'races_P', 'race_O', 'race_P', 'compete_P'], "competed in" : ['races_O', 'races_P', 'race_O', 'race_P', 'compete_P']}
properties_dict["competing"] = {"competing" : ['races_O', 'races_P', 'race_O', 'race_P', 'compete_P'], "competing in" : ['races_O', 'races_P', 'race_O', 'race_P', 'compete_P']}
properties_dict["demise"] = {'demise': ['deathPlace_O', 'deathPlace_P', 'placeOfDeath_P', 'deathCause_O', 'deathCause_P', 'causeOfDeath_P']}
properties_dict["cast"]["cast in"] = ['cast_P', 'starring_P', 'starring_O']
properties_dict["casts"] = {'casts' : ['cast_P', 'starring_P', 'starring_O'], 'casts in' : ['cast_P', 'starring_P', 'starring_O']}
properties_dict["casted"] = {'casted' : ['cast_P', 'starring_P', 'starring_O'], 'casted in' : ['cast_P', 'starring_P', 'starring_O']}
properties_dict["casting"] = {'casting' : ['cast_P', 'starring_P', 'starring_O'], 'casting in' : ['cast_P', 'starring_P', 'starring_O']}
properties_dict["follow"] = {'follow' : ['subsequentWork_O', 'following_P', 'followedBy_P', 'followed_P']}
properties_dict["follows"] = {'follows' : ['subsequentWork_O', 'following_P', 'followedBy_P', 'followed_P']}
properties_dict["followed"] = {'followed' : ['subsequentWork_O', 'following_P', 'followedBy_P', 'followed_P'], 'followed by' : ['subsequentWork_O', 'following_P', 'followedBy_P', 'followed_P']}
properties_dict["following"] = {'following' : ['subsequentWork_O', 'following_P', 'followedBy_P', 'followed_P']}
properties_dict["hub"] = {'hub airport': ['hubAirport_O'], 'hub': ['hub_P', 'hubs_P', 'hubAirport_O'], 'hub for': ['hubFor_P']}
properties_dict["leader"] = {"leader" : ['leader_O', 'leader_P', 'leaders_P', 'leaderName_O', 'leaderName_P'], 'leader term': ['leaderTerm_P'], 'leader title1     Town Manager': ['leaderTitle1TownManager_P'], 'leader name': ['leaderName_O', 'leaderName_P'], 'leader date': ['leaderDate_P'], 'leader year': ['leaderYear_P'], 'leader party': ['leaderParty_O', 'leaderParty_P'], 'leader title': ['leaderTitle_O', 'leaderTitle_P'], 'leader function': ['leaderFunction_O'], 'leader title     Vice Mayor': ['leaderTitleViceMayor_P'], 'leader type': ['leaderType_P'], 'leader know': ['leaderKnow_P'], 'leader wise name': ['leaderWiseName_P'], 'leader years': ['leaderYears_P'], 'leader since': ['leaderSince_P'], 'leader from': ['leaderFrom_P']} 
properties_dict["leaders"] = {"leaders" : ['leader_O', 'leader_P', 'leaders_P', 'leaderName_O', 'leaderName_P']}
properties_dict["member"] = {'member': ['member_P', 'team_O', 'team_P', 'league_O', 'league_P', 'pastMember_P', 'pastMembers_P', 'pastmember_P', 'currentMembers_P', 'nationalTeam_O', 'nationalTeam_P', 'nationalteam_P', 'bandMember_O', 'bandMember_P'], 'Member of Parliament': ['memberOfParliament_P'], 'Member Of Lokshaba': ['memberOfLokshaba_P']}
properties_dict["sports"] = {'sports stadium': ['stadium_O', 'stadium_P'], 'sports illustrated': ['sportsillustrated_P'], 'sports': ['sport_O', 'sport_P', 'sports_P', 'athletics_O', 'athletics_P', 'plays_O', 'plays_P']}
properties_dict["used"] = {'used banknotes': ['usedBanknotes_P'], 'used in war': ['usedInWar_O'], 'used': ['used_P', 'usedBy_P', 'usedInWar_O'], 'used by': ['usedBy_P', 'used_P', 'usedInWar_O']}
properties_dict["destination"] = {'destination': ['destination_O', 'destination_P', 'destinations_P', 'targetAirport_O', 'targetAirport_P', 'address_O', 'address_P']}
properties_dict["destinations"] = {'destinations': ['destination_O', 'destination_P', 'destinations_P', 'targetAirport_O', 'targetAirport_P', 'address_O', 'address_P']}
properties_dict["team"]["team"] = ['team_O', 'team_P', 'pastteams_P', 'playedFor_P', 'formerTeam_O', 'formerTeam_P', 'debutTeam_O', 'debutTeam_P', 'prospectTeam_P', 'league_O', 'league_P', 'pastMember_P', 'pastmember_P', 'currentMembers_P', 'nationalTeam_O', 'nationalTeam_P', 'nationalteam_P']
properties_dict["lieutenants"] = {'lieutenants': ['lieutenant_O', 'lieutenant_P', 'lieutenants_P']}
del properties_dict["current"]["current"]
properties_dict["serving"]["serving line"] = ['servingRailwayLine_O']
properties_dict["alumni"] = {'alumni': ['alumni_P', 'almaMater_O', 'almaMater_P', 'college_O', 'college_P', 'university_O', 'university_P', 'institution_O', 'institution_P', 'education_O', 'education_P', 'training_O', 'training_P', 'school_O', 'school_P']}
properties_dict["religions"]["religions"] = ['religion_O', 'religions_P', 'religions_P']
properties_dict["pupil"] = {'pupil': ['pupil_P', 'coach_O', 'coach_P', 'trainer_O', 'trainer_P']}
properties_dict["company"]["company"] = ['company_O', 'company_P', 'leader_O', 'leader_P', 'keyPeople_P', 'keyPerson_O', 'chairman_O', 'chairman_P', 'party_O', 'party_P']
properties_dict["manufacturers"] = {'manufacturers': ['manufacturers_P', 'producer_O', 'producer_P', 'product_O', 'developer_O', 'developer_P', 'creator_O', 'creator_P', 'manufacturer_O', 'manufacturer_P', 'designer_O', 'designer_P']}
properties_dict["agency"]["agency name"] = ['agencyName_P', 'agency_O', 'agency_P', 'office_O', 'office_P']
properties_dict["distribution"]["distribution region"] = ['distribution_P', "locationCity_O", "locationCity_P", "location_O", "location_P", 'locations_P', "city_O", "city_P", \
                                         "county_O", "county_P", "state_O", "state_P", "province_O", "province_P", "region_O", \
                                         "region_P", "district_O", "district_P", "territory_O", "territory_P", "based_P", \
                                         "basedOn_O", "basedOn_P", "basedAt_P"]
properties_dict["profession"] = {'profession': ['profession_O', 'profession_P', 'occupation_O', 'occupation_P', 'employer_O', 'employer_P']}
properties_dict["proprietor"] = {'proprietor': ['owner_O', 'owner_P', 'foundedBy_O', 'foundedBy_P', 'owningOrganisation_O', 'occupation_O', 'authority_O', 'field_P', 'parent_P', 'owners_P', 'owningCompany_O', 'system_P', 'arena_P', 'owned_P', 'parentOrganisation_O', 'parentCompany_O', 'ground_P', 'stadium_P', 'company_P', 'network_O']}
properties_dict["pod"] = {'pod': ['deathPlace_O', 'deathPlace_P', 'placeOfDeath_P']}
properties_dict["division"]["division"] = ['division_O', 'division_P', 'divisions_P', 'part_O', 'part_P', 'classes_O', 'classes_P', 'class_O', 'class_P', 'owner_O', 'owningOrganisation_O', 'authority_O', 'parent_P', 'owners_P', 'owningCompany_O', 'system_P', 'owned_P', 'parentOrganisation_O', 'parentCompany_O', 'company_P', 'network_O', 'foundedBy_O', 'foundedBy_P']
properties_dict["divisions"]["divisions"] = ['division_O', 'division_P', 'divisions_P', 'part_O', 'part_P', 'classes_O', 'classes_P', 'class_O', 'class_P', 'owner_O', 'owningOrganisation_O', 'authority_O', 'parent_P', 'owners_P', 'owningCompany_O', 'system_P', 'owned_P', 'parentOrganisation_O', 'parentCompany_O', 'company_P', 'network_O', 'foundedBy_O', 'foundedBy_P']
properties_dict["presidents"]["presidents"] = ['presidents_P', 'president_O', 'president_P', 'manager_O', 'manager_P', 'managerclubs_P', 'managerClub_O', 'leaderName_O', 'leaderName_P', 'operator_O', 'director_O', 'director_P', 'directedby_P', 'operator_P', 'governingBody_O', 'chancellor_O', 'chancellor_P', 'governingBody_P', 'head_O', 'head_P', 'principal_O', 'principal_P', 'chairman_O', 'chairman_P', 'deputy_O', 'deputy_P']
properties_dict["president"]["president"] = ['president_O', 'president_P', 'presidents_P', 'manager_O', 'manager_P', 'managerclubs_P', 'managerClub_O', 'leaderName_O', 'leaderName_P', 'operator_O', 'director_O', 'director_P', 'directedby_P', 'operator_P', 'governingBody_O', 'chancellor_O', 'chancellor_P', 'governingBody_P', 'head_O', 'head_P', 'principal_O', 'principal_P', 'chairman_O', 'chairman_P', 'deputy_O', 'deputy_P']
properties_dict["domain"]["domain"] = ['domain_P', 'domains_P', 'area_O', 'area_P', 'field_O', 'field_P', 'discipline_O', 'discipline_P', 'mainInterests_P']
properties_dict["domains"]["domains"] = ['domain_P', 'domains_P', 'area_O', 'area_P', 'field_O', 'field_P', 'discipline_O', 'discipline_P', 'mainInterests_P']
properties_dict["debut"]["debut"] = ['debut_O', 'debut_P', 'debutTeam_P', 'debutTeam_O', 'debutteam_P', 'debutWork_P', 'debutWorks_P', 'debutDate_P', 'debutBook_P']
properties_dict["debut"]["debut team"] = ['debutTeam_P', 'debutTeam_O', 'debutteam_P']
properties_dict["debuts"] = {"debuts" : ['debut_O', 'debut_P', 'debutTeam_P', 'debutTeam_O', 'debutteam_P', 'debutWork_P', 'debutWorks_P', 'debutDate_P', 'debutBook_P']}
properties_dict["debuted"] = {"debuted" : ['debut_O', 'debut_P', 'debutTeam_P', 'debutTeam_O', 'debutteam_P', 'debutWork_P', 'debutWorks_P', 'debutDate_P', 'debutBook_P']}
properties_dict["debuting"] = {"debuting" : ['debut_O', 'debut_P', 'debutTeam_P', 'debutTeam_O', 'debutteam_P', 'debutWork_P', 'debutWorks_P', 'debutDate_P', 'debutBook_P']}
properties_dict["movie"]["movie director"] = ['director_O', 'director_P', 'directedby_P']
properties_dict["built"] = {"built" : ['builder_O', 'manufacturer_O', 'manufacturer_P', 'builder_P', 'built_P'], "built by" : ['builder_O', 'manufacturer_O', 'manufacturer_P', 'builder_P']}
properties_dict["compose"]["compose the music"] = ['composer_O', 'composer_P', 'musicBy_O', 'musicBy_P', 'music_P', 'writer_O', 'writer_P', 'author_O', 'author_P']
properties_dict["composes"]["composes the music"] = ['composer_O', 'composer_P', 'musicBy_O', 'musicBy_P', 'music_P', 'writer_O', 'writer_P', 'author_O', 'author_P']
properties_dict["composed"]["composed the music"] = ['composer_O', 'composer_P', 'musicBy_O', 'musicBy_P', 'music_P', 'writer_O', 'writer_P', 'author_O', 'author_P']
properties_dict["composing"]["composing the music"] = ['composer_O', 'composer_P', 'musicBy_O', 'musicBy_P', 'music_P', 'writer_O', 'writer_P', 'author_O', 'author_P']
properties_dict["burial"] = {'burial': ['restingPlace_O', 'restingPlace_P', 'restingplace_P', 'placeOfBurial_P', 'buriedPlace_P', 'buriedAt_P', 'buried_P', 'burialLocation_P', 'burial_P'], 'burial place': ['restingPlace_O', 'restingPlace_P', 'restingplace_P', 'placeOfBurial_P', 'buriedPlace_P', 'buriedAt_P', 'buried_P', 'burialLocation_P', 'burial_P'], 'burial date': ['burialDate_P'], 'burial location': ['burialLocation_P']}
properties_dict["matter"]["matter"] = ['subject_P', 'field_O', 'field_P', 'discipline_O', 'discipline_P']
properties_dict["matters"] = {"matter" : ['subject_P', 'field_O', 'field_P', 'discipline_O', 'discipline_P']}
properties_dict["sovereign"] = {'sovereign state': ['sovereignState_P', "county_O", "county_P", "state_O", "state_P", "location_O", "location_P", 'locations_P', "province_O", "province_P", "region_O", "region_P", "district_O", "district_P", "territory_O", "territory_P", "based_P", "basedOn_O", "basedOn_P", "basedAt_P"], 'sovereign': ['monarch_O', 'monarch_P']}
properties_dict["sculpt"] = {"sculpt" : ['sculptor_P', 'creator_P', 'creator_O', 'author_O', 'author_P', 'writer_O', 'writer_P']}
properties_dict["sculpts"] = {"sculpts" : ['sculptor_P', 'creator_P', 'creator_O', 'author_O', 'author_P', 'writer_O', 'writer_P']}
properties_dict["sculpted"] = {"sculpted" : ['sculptor_P', 'creator_P', 'creator_O', 'author_O', 'author_P', 'writer_O', 'writer_P'], "sculpted by" : ['sculptor_P', 'creator_P', 'creator_O', 'author_O', 'author_P', 'writer_O', 'writer_P']}
properties_dict["sculpting"] = {"sculpting" : ['sculptor_P', 'creator_P', 'creator_O', 'author_O', 'author_P', 'writer_O', 'writer_P']}
properties_dict["administrative"] = {"administrative center" : ['administrativeCenter_P', 'capital_O', 'capital_P']}
properties_dict["administrative"] = {"administrative centre" : ['administrativeCenter_P', 'capital_O', 'capital_P']}
properties_dict["govern"] = {"govern" : ['government_O', 'government_P', 'governingBody_O', 'governingBody_P', 'governingBoard_P', 'manager_O', 'manager_P', 'managerclubs_P', 'managerClub_O', 'president_O', 'president_P', 'presidents_P', 'leaderName_O', 'leaderName_P', 'operator_O', 'director_O', 'director_P', 'directedby_P', 'operator_P', 'chancellor_O', 'chancellor_P', 'head_O', 'head_P', 'principal_O', 'principal_P', 'chairman_O', 'chairman_P', 'deputy_O', 'deputy_P', 'operatedBy_O', 'operatedBy_P', 'order_O', 'order_P']}
properties_dict["governs"] = {"governs" : ['government_O', 'government_P', 'governingBody_O', 'governingBody_P', 'governingBoard_P', 'manager_O', 'manager_P', 'managerclubs_P', 'managerClub_O', 'president_O', 'president_P', 'presidents_P', 'leaderName_O', 'leaderName_P', 'operator_O', 'director_O', 'director_P', 'directedby_P', 'operator_P', 'chancellor_O', 'chancellor_P', 'head_O', 'head_P', 'principal_O', 'principal_P', 'chairman_O', 'chairman_P', 'deputy_O', 'deputy_P', 'operatedBy_O', 'operatedBy_P', 'order_O', 'order_P']}
properties_dict["governed"] = {"governed" : ['government_O', 'government_P', 'governingBody_O', 'governingBody_P', 'governingBoard_P', 'manager_O', 'manager_P', 'managerclubs_P', 'managerClub_O', 'president_O', 'president_P', 'presidents_P', 'leaderName_O', 'leaderName_P', 'operator_O', 'director_O', 'director_P', 'directedby_P', 'operator_P', 'chancellor_O', 'chancellor_P', 'head_O', 'head_P', 'principal_O', 'principal_P', 'chairman_O', 'chairman_P', 'deputy_O', 'deputy_P', 'operatedBy_O', 'operatedBy_P', 'order_O', 'order_P'], "governed by" : ['government_O', 'government_P', 'governingBody_O', 'governingBody_P', 'governingBoard_P', 'manager_O', 'manager_P', 'managerclubs_P', 'managerClub_O', 'president_O', 'president_P', 'presidents_P', 'leaderName_O', 'leaderName_P', 'operator_O', 'director_O', 'director_P', 'directedby_P', 'operator_P', 'chancellor_O', 'chancellor_P', 'head_O', 'head_P', 'principal_O', 'principal_P', 'chairman_O', 'chairman_P', 'deputy_O', 'deputy_P', 'operatedBy_O', 'operatedBy_P']}
properties_dict["governing"] = {'governing board': ['governingBoard_P'], 'governing body': ['governingBody_O', 'governingBody_P'], 'governing': ['government_O', 'government_P', 'governingBody_O', 'governingBody_P', 'governingBoard_P', 'manager_O', 'manager_P', 'managerclubs_P', 'managerClub_O', 'president_O', 'president_P', 'presidents_P', 'leaderName_O', 'leaderName_P', 'operator_O', 'director_O', 'director_P', 'directedby_P', 'operator_P', 'chancellor_O', 'chancellor_P', 'head_O', 'head_P', 'principal_O', 'principal_P', 'chairman_O', 'chairman_P', 'deputy_O', 'deputy_P', 'operatedBy_O', 'operatedBy_P', 'order_O', 'order_P']}
properties_dict["licensed"] = {'licensed': ['license_O', 'license_P', 'licence_P', 'licence_O', 'contentLicense_P']}
properties_dict["licenced"] = {'licenced': ['license_O', 'license_P', 'licence_P', 'licence_O', 'contentLicense_P']}
properties_dict["first"]["first ascented"] = ['firstAscentPerson_O', 'firstAscentPerson_P']
