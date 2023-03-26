<template>
  <div 
    ref="mapOwner"
    class="map-owner"
  >
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
        ref="mapLayer"
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
import { defineComponent, PropType, ref, watch } from 'vue';
import { LMap, LTileLayer, LGeoJson, LControlAttribution } from '@vue-leaflet/vue-leaflet';
import L from 'leaflet';
import { useMapStore } from '../stores/map';
import { Feature } from 'geojson';
import { AreaProperties, SCORE_INCREMENT } from '../models/area_properties';
import { AmenityType } from '../models/amenity_type';


export default defineComponent({
    components: {
        LMap,
        LTileLayer,
        LGeoJson,
        LControlAttribution
    },
    props: {
        selectedType: {
            type: String as PropType<AmenityType>,
            default: AmenityType.FoodStore
        }
    },
    setup(props) {
        const knownColours = ['Blue', 'Green', 'Yellow', 'Orange', 'Red', 'Black'];
        
        function updateAreaColours(layer: L.GeoJSON, amenityType: AmenityType) {
            if (layer.feature) {
                const feature = layer.feature as Feature;
                const properties = feature.properties as AreaProperties;
                const foodDistance = properties.distances[amenityType];
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
            }else {
                layer.resetStyle();
            }
        }
        
        const mapLayer = ref<InstanceType<typeof LGeoJson> | null>(null);

        const geoJsonOptions: L.GeoJSONOptions = {
            onEachFeature(feature: Feature, layer: L.GeoJSON) {
                if (feature.id) {
                    layer.bindTooltip(feature.id as string);
                }
                updateAreaColours(layer, props.selectedType);
            }
        };

        watch(() => props.selectedType, (type, oldType) => {
            if (type !== oldType && mapLayer.value?.leafletObject) {
                mapLayer.value.leafletObject.eachLayer(layer => {
                    updateAreaColours(layer as L.GeoJSON, type);
                });
            }
        });

        const map = ref<InstanceType<typeof LMap> | null>();

        const resizeObserver = new ResizeObserver(entries => {
            const rect = entries[0].contentRect;
            if (map.value?.leafletObject && rect.width > 0 && rect.height > 0) {
                map.value.leafletObject.invalidateSize({
                    pan: true,
                });
            }
        });

        return {
            mapStore: useMapStore(),
            geoJsonOptions,
            map,
            mapLayer,
            mapOwner: ref<HTMLDivElement | null>(null),
            resizeObserver
        };
    },
    mounted() {
        if(this.mapOwner) {
            this.resizeObserver.observe(this.mapOwner);
        }
    },
    unmounted() {
        if(this.mapOwner) {
            this.resizeObserver.unobserve(this.mapOwner);
        }
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