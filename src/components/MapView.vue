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
          <h3 v-t="'legend'"></h3>
          <table class="legend">
            <tr
              v-for="time of breakpoints"
              :key="time"
            >
              <td 
                :style="{'background-color': `var(--color-distance-l${time}`}" 
                class="colour"
              >
              </td>
              <td>
                <i class="fa-solid fa-less-than"></i>
              </td>
              <td class="time">
                {{ time }}
              </td>
              <td>
                minutes
              </td>
            </tr>
            <tr>
              <td 
                style="background-color: var(--color-distance-inf)" 
                class="colour"
              >
              </td>
              <td>
                <i class="fa-solid fa-greater-than"></i>
              </td>
              <td class="time">
                30
              </td>
              <td>
                minutes
              </td>
            </tr>
          </table>
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
import { AmenityType } from '../models/amenity_type';
import { useI18n } from 'vue-i18n';
import { List } from 'immutable';
import { WALKING_SPEED, MAX_TIME } from '../models/area_properties';

const areaStyle: L.PathOptions = {
    weight: 1,
    fillOpacity: 0.6,
    color: 'var(--color-map-area-border)',
    opacity: 1
};

const timeIncrement = 5;
const breakpoints = List([...Array(6).keys()].map(x => (x + 1) * timeIncrement));

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
        function distanceToHexColour(distance: number | undefined) : string {
            let index = Number.POSITIVE_INFINITY;
            if(distance !== undefined) {
                const time = distance / WALKING_SPEED;
                index = Math.ceil(time / timeIncrement) * timeIncrement;
            }
            if (index > MAX_TIME) {
                return 'var(--color-distance-inf)';
            }
            return `var(--color-distance-l${index})`;
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
                        const marker = L.marker({
                            lng: distances.pt.coordinates[0],
                            lat: distances.pt.coordinates[1]
                        }).bindPopup('<a href="https://docs.google.com/forms/d/e/1FAIpQLSdAW14AmmplUH8iNPzhTJZ4UY-DW9OY9TR78C6_OIPYy2L7_g/viewform?usp=pp_url&entry.919457431=' + distances.pt.coordinates[1] + ','  + distances.pt.coordinates[0] + '">' + i18n.t('correction') + '</a>');
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
            breakpoints
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
    background-color: rgba(255, 255, 255, 0.9);
    border-radius: 10%;
    padding: 10px;
    padding-top: 5px;
}

.legend {
    font-size: 1.1em;
}

.legend td {
    vertical-align: middle;
    height: 22px;
    padding-left: 2px;
    padding-right: 2px;
}

.legend .colour {
    display: inline-block;
    width: 16px;
    height: 16px;
}

.legend .time {
    font-weight: bold;
    font-size: 1.1em;
    text-align: right;
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