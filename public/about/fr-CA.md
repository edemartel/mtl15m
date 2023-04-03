**mtl15m** est une application Web de carte intéractive qui affiche la disponibilité de différents services à distance de marche dans les différentes municipalitées de l'île de Montréal.

Ses auteurs sont [Andy Emond](https://twitter.com/Drahakar), [Jesse Emond](https://twitter.com/JesseEmond) et [Etienne de Martel](https://twitter.com/edemartel).

# Méthodologie

Montréal a été subdivisée en secteurs en suivant les frontières des aires de diffusion de Statistiques Canada, additionnellement délimitées par les frontières terrestres pour couper les portions au dessus de l'eau. Les aires avec une population de zéro au recensement de 2021 ont été éliminées.

Pour chaque secteur, on ne considère que les services dans un rayon de 2,5 km de son centre, à vol d'oiseau. La distance de 2,5 km a été choisie car elle constitue 30 minutes à une vitesse de marche typique de 5 km/h. Pour les services restants, on calcule alors la distance de marche en utilisant une exécution locale de [OpenRouteService](https://openrouteservice.org/). Le chemin le plus court pour une catégorie de service est retenu comme la distance entre ce secteur et cette catégorie de service.

La couleur affichée sur la carte est calculée simplement en fonction du ratio entre cette distance et la distance maximale choisie de 2,5 km.

# Sources

- [Limites des aires de diffusion - 2021](https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/index2021-fra.cfm?year=21)
- [Chiffres de population et des logements - 2021](https://www150.statcan.gc.ca/t1/tbl1/fr/tv.action?pid=9810001501&pickMembers%5B0%5D=1.14402)
- [Limites terrestres de l'île de Montréal](https://donnees.montreal.ca/ville-de-montreal/limites-terrestres)
- [Établissements alimentaires](https://donnees.montreal.ca/ville-de-montreal/etablissements-alimentaires)
- [Locaux commerciaux  et statuts d'occupation](https://donnees.montreal.ca/ville-de-montreal/locaux-commerciaux)
- [Lieux culturels municipaux de Montréal](https://donnees.montreal.ca/ville-de-montreal/lieux-culturels)
- [Grands parcs, parcs d'arrondissements et espaces publics](https://donnees.montreal.ca/ville-de-montreal/grands-parcs-parcs-d-arrondissements-et-espaces-publics)
- [Localisation des établissements d'enseignement du réseau scolaire au Québec](https://www.donneesquebec.ca/recherche/dataset/localisation-des-etablissements-d-enseignement-du-reseau-scolaire-au-quebec)
- [Tracés des lignes de bus et de métro](https://donnees.montreal.ca/societe-de-transport-de-montreal/stm-traces-des-lignes-de-bus-et-de-metro)