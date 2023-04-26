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
      <l-layer-group ref="markers"></l-layer-group>
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
import { LMap, LTileLayer, LGeoJson, LLayerGroup, LControlAttribution } from '@vue-leaflet/vue-leaflet';
import L from 'leaflet';
import { useMapStore } from '../stores/map';
import { Feature } from 'geojson';
import { AreaProperties } from '../models/area_properties';
import { AmenityType } from '../models/amenity_type';

const areaStyle: L.PathOptions = {
    weight: 1,
    fillOpacity: 0.6,
    color: 'var(--color-map-area-border)',
    opacity: 1
};

export default defineComponent({
    components: {
        LMap,
        LTileLayer,
        LGeoJson,
        LLayerGroup,
        LControlAttribution
    },
    props: {
        selectedType: {
            type: String as PropType<AmenityType>,
            default: AmenityType.FoodStore
        }
    },
    setup(props) {        
        function distanceToHexColour(distance: number|undefined) : string {
            if (distance === undefined || distance > 2500) { // >30m
                return '#999999'; // Gray
            } else if (distance > 2100) { //>25m
                return '#b8432e'; // Red
            } else if (distance > 1700) { //>20m
                return '#dd643c'; //Orange
            } else if (distance > 1250) { //>15m
                return '#fda668'; // peach
            } else if (distance > 800) { //>10m
                return '#abedab'; //light green
            } else if (distance > 400) { //>5m 
                return '#5aabac'; //teal
            } else { //<5m
                return '#0868ac'; // blue
            }
        }

        function updateAreaColours(layer: L.GeoJSON, amenityType: AmenityType) {
            if (layer.feature) {
                const feature = layer.feature as Feature;
                const properties = feature.properties as AreaProperties;
                const distance = properties.distances[amenityType];
                
                const hexColour = distanceToHexColour(distance?.dist);

                layer.setStyle({
                    ...areaStyle,
                    fillColor: hexColour,
                });
            }else {
                layer.resetStyle();
            }
        }
        
        const mapLayer = ref<InstanceType<typeof LGeoJson> | null>(null);
        const markers = ref<InstanceType<typeof LLayerGroup> | null>(null);

        const selectedArea = ref<Feature | null>(null);

        watch(selectedArea, current => {
            updateBestAmenity(current, props.selectedType);
        });

        function updateBestAmenity(feature: Feature | null, type: AmenityType) {
            if(markers.value?.leafletObject) {
                markers.value.leafletObject.clearLayers();
                if(feature) {
                    const properties = feature.properties as AreaProperties;
                    const distances = properties.distances[type];
                    if(distances) {
                        const marker = L.marker({
                            lng: distances.pt.coordinates[0],
                            lat: distances.pt.coordinates[1]
                        });
                        markers.value.leafletObject.addLayer(marker);
                    }
                }
            }
        }

        const geoJsonOptions: L.GeoJSONOptions = {
            onEachFeature(feature: Feature, layer: L.GeoJSON) {
                if (feature.id) {
                    layer.bindTooltip(feature.id as string);
                }
                updateAreaColours(layer, props.selectedType);
                layer.addEventListener('click', () => {
                    selectedArea.value = feature;
                });
            }
        };

        watch(() => props.selectedType, (type, oldType) => {
            if (type !== oldType) {
                if (mapLayer.value?.leafletObject) {
                    mapLayer.value.leafletObject.eachLayer(layer => {
                        updateAreaColours(layer as L.GeoJSON, type);
                    });
                }
                updateBestAmenity(selectedArea.value, type);
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
            resizeObserver,
            selectedArea,
            markers
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
    },
    methods: {
        panTo(pos: L.LatLngExpression) {
            if(this.map?.leafletObject) {
                this.map.leafletObject.flyTo(pos, 14, {
                    animate: true,
                    duration: 0.5
                });
            }
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
.leaflet-container {
    background-color: var(--color-background);
}
.leaflet-control-container {
  width: 100%;
  height: 100%;
}
path.leaflet-interactive:focus {
    outline: none;
}
.leaflet-container .leaflet-control-attribution {
    color: var(--color-text);
    background-color: var(--color-background);
}
.leaflet-control a {
    color: var(--color-text);
    background-color: var(--color-background);
}
.leaflet-control a:hover {
    color: var(--color-accent);
    background-color: var(--color-background);
    text-decoration: none;
}

</style>