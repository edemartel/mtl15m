<template>
  <div class="map-owner">
    <l-map
      ref="map"
      :zoom="11"
      :center="[45.54127302051837, -73.6513139615433]"
      :options="{ attributionControl: false }"
    >
      <l-tile-layer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        layer-type="base"
        attribution="&copy; <a href=&quot;https://www.openstreetmap.org/copyright&quot;>OpenStreetMap</a>"
      ></l-tile-layer>
      <l-geo-json
        :geojson="mapStore.features"
        :options="geoJsonOptions"
      ></l-geo-json>
      <l-control-attribution
        prefix=""
        position="bottomright"
      ></l-control-attribution>
    </l-map>
  </div>
</template>


<script lang="ts">
import 'leaflet/dist/leaflet.css';
import { defineComponent } from 'vue';
import { LMap, LTileLayer, LGeoJson, LControlAttribution } from '@vue-leaflet/vue-leaflet';
import L from 'leaflet';
import { useMapStore } from '../stores/map';
import { Feature } from 'geojson';
import { AreaProperties, SCORE_INCREMENT } from '../models/area_properties';


export default defineComponent({
    components: {
        LMap,
        LTileLayer,
        LGeoJson,
        LControlAttribution
    },
    setup() {
        const knownColours = ['Blue', 'Green', 'Yellow', 'Orange', 'Red', 'Black'];
        
        const mapStore = useMapStore();
        const geoJsonOptions: L.GeoJSONOptions = {
            onEachFeature(feature: Feature, layer: L.GeoJSON) {
                if (feature.id) {
                    layer.bindTooltip(feature.id as string);
                }
                if (feature.properties) {
                    const properties = feature.properties as AreaProperties;
                    const foodDistance = properties.distances.food_store;
                    let colour = knownColours[knownColours.length - 1];
                    if(foodDistance !== undefined) {
                        const score = Math.min(Math.floor(foodDistance / SCORE_INCREMENT), knownColours.length - 1);
                        colour = knownColours[score];
                    }
                    layer.setStyle({
                        weight: 1,
                        fillOpacity: 0.7,
                        fillColor: colour,
                        stroke: false
                    });
                }
            }
        };
        return {
            mapStore,
            geoJsonOptions
        };
    }
});

</script>

<style scoped>
.map-owner {
  height: 100%;
}
</style>
<style>
.leaflet-control-container {
  width: 100%;
  height: 100%;
}
path.leaflet-interactive:focus {
    outline: none;
}
</style>