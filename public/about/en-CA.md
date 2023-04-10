**mtl15m** is an interactive map Web application that displays the availability of various amenities within walking distance in the various municipalities of the island of Montreal.

Its authors are [Andy Emond](https://twitter.com/Drahakar), [Jesse Emond](https://twitter.com/JesseEmond) and [Etienne de Martel](https://twitter.com/edemartel).

The source code is available on [GitHub](https://github.com/edemartel/mtl15m/).

# Methodology

Montreal was subdivided in areas following the limits of Statistics Canada's dissemination areas, additionally delineated by terrestrial boundaries to cut portions that were over water. Areas with a population of zero in the 2021 census are then eliminated.

For each area, we only consider amenities within a radius of 2.5 km as the crow flies of its centre. The distance of 2.5 km was chosen because it is 30 minutes at a typical walking speed of 5 km/h. For the remaining amenities, we then compute the walking distance using a local execution of [OpenRouteService](https://openrouteservice.org/). The shortest path for a specific category of amenities is then chosen as the distance between that area and that category.

The colour shown on the map is simply calculated based on the ratio between that distance and the maximum chosen distance of 2.5 km. The data is then displayed over a map with tiles provided by [the OpenStreetMap project](https://www.openstreetmap.org/).

# Sources

- [2021 Census – Boundary files](https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/index2021-eng.cfm?Year=21)
- [Population and dwelling counts - 2021](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=9810001501&pickMembers%5B0%5D=1.14402)
- [Limites terrestres de l'île de Montréal](https://donnees.montreal.ca/ville-de-montreal/limites-terrestres)
- [Locaux commerciaux  et statuts d'occupation](https://donnees.montreal.ca/ville-de-montreal/locaux-commerciaux)
- [Lieux culturels municipaux de Montréal](https://donnees.montreal.ca/ville-de-montreal/lieux-culturels)
- [Grands parcs, parcs d'arrondissements et espaces publics](https://donnees.montreal.ca/ville-de-montreal/grands-parcs-parcs-d-arrondissements-et-espaces-publics)
- [Localisation des établissements d'enseignement du réseau scolaire au Québec](https://www.donneesquebec.ca/recherche/dataset/localisation-des-etablissements-d-enseignement-du-reseau-scolaire-au-quebec)
- [Tracés des lignes de bus et de métro](https://donnees.montreal.ca/societe-de-transport-de-montreal/stm-traces-des-lignes-de-bus-et-de-metro)