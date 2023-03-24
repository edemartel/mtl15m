<template>
  <div class="map-owner">
    <l-map
      ref="map"
      :zoom="17"
      :center="[45.54127302051837, -73.6513139615433]"
      :options="mapOptions"
    >
      <l-tile-layer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        layer-type="base"
        attribution="&copy; <a href=&quot;https://www.openstreetmap.org/copyright&quot;>OpenStreetMap</a>"
      ></l-tile-layer>
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
import { LMap, LTileLayer, LControlAttribution } from '@vue-leaflet/vue-leaflet';
import L from 'leaflet';

export default defineComponent({
    components: {
        LMap,
        LTileLayer,
        LControlAttribution
    },
    data() {
        const mapOptions: L.MapOptions = {
            attributionControl: false
        };
        return {
            mapOptions
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
</style>