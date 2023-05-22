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
      <l-control position="bottomleft">
        <div class="legendbox">
          <div v-t="'legend'"></div>
          <div
            v-for="(item, index) in travelTimeToColour"
            :key="index"
            class="legend"
          >
            <span 
              :style="{'background-color': item}" 
              class="legendcolor"
            >
                &nbsp;
            </span>
            <span class="traveltime">&gt;{{ index }} minutes</span>
          </div>
        </div>
      </l-control>
    </l-map>
  </div>
</template>


<script lang="ts">
import 'leaflet/dist/leaflet.css';
import { defineComponent, PropType, ref, watch } from 'vue';
import { LMap, LTileLayer, LGeoJson, LLayerGroup, LControlAttribution, LControl } from '@vue-leaflet/vue-leaflet';
import L from 'leaflet';
import { useMapStore } from '../stores/map';
import { Feature } from 'geojson';
import { AreaProperties } from '../models/area_properties';
import { AmenityType, amenityIconClasses } from '../models/amenity_type';
import { useI18n } from 'vue-i18n';

const areaStyle: L.PathOptions = {
    weight: 1,
    fillOpacity: 0.6,
    color: 'var(--color-map-area-border)',
    opacity: 1
};

const travelTimeToColour = {
    30: '#999999', //Grey
    25: '#b8432e', //Red
    20: '#dd643c', //Orange
    15: '#fda668', //Peach
    10: '#abedab', //Light green
    5: '#5aabac', //Teal
    0: '#0868ac', //Blue
};

export default defineComponent({
    components: {
        LMap,
        LTileLayer,
        LGeoJson,
        LLayerGroup,
        LControlAttribution,
        LControl
    },
    props: {
        selectedType: {
            type: String as PropType<AmenityType>,
            default: AmenityType.FoodStore
        }
    },
    setup(props) {        
        function distanceToHexColour(distance: number|undefined) : string {
            if (distance === undefined || distance > 2500) {
                return travelTimeToColour[30]; 
            } else if (distance > 2100) {
                return travelTimeToColour[25]; 
            } else if (distance > 1700) { 
                return travelTimeToColour[20]; 
            } else if (distance > 1250) {
                return travelTimeToColour[15];
            } else if (distance > 800) {
                return travelTimeToColour[10];
            } else if (distance > 400) {  
                return travelTimeToColour[5];
            } else {
                return travelTimeToColour[0];
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
        const i18n = useI18n();

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
                        const pos: L.LatLngLiteral = {
                            lng: distances.pt.coordinates[0],
                            lat: distances.pt.coordinates[1]
                        };
                        const options: L.MarkerOptions = {
                            icon: L.divIcon({
                                html: `<i class="fa-solid fa-${amenityIconClasses[type]} mapicon"></i>`,
                                iconSize: [36, 36],
                            })
                        };
                        const marker = L.marker(pos, options);
                        marker.bindPopup(`<a href="https://docs.google.com/forms/d/e/1FAIpQLSdAW14AmmplUH8iNPzhTJZ4UY-DW9OY9TR78C6_OIPYy2L7_g/viewform?usp=pp_url&entry.919457431=${distances.pt.coordinates[1]},${distances.pt.coordinates[0]}">${i18n.t('correction')}</a>`);
                        markers.value.leafletObject.addLayer(marker);
                    }
                }
            }
        }

        const geoJsonOptions: L.GeoJSONOptions = {
            onEachFeature(feature: Feature, layer: L.GeoJSON) {
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
    data() {
        return {
            travelTimeToColour: travelTimeToColour
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
.legendbox {
    background-color: white;
    padding: 5px;
}

.legendbox .legendcolor {
    margin-right: 5px;
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

.leaflet-marker-icon {
    background-color: rgba(0, 0, 0, 0.4);
    border: none;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 18px;
}

.mapicon {
    color: white;
    display: block;
    font-size: 20px;
}

</style>