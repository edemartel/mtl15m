<template>
  <a
    href="#"
    :title="$t('go_to_position')"
    @click="requestPosition"
  >
    <i class="fa-solid fa-location-crosshairs"></i>
  </a>
</template>

<script lang="ts">

import { LatLng } from 'leaflet';
import { defineComponent } from 'vue';

export default defineComponent({
    emits: ['locationProvided'],
    methods: {
        requestPosition(event: Event) {
            navigator.geolocation.getCurrentPosition(position => {
                const pos = new LatLng(position.coords.latitude, position.coords.longitude);
                this.$emit('locationProvided', pos);
            });
            event.preventDefault();
        }
    }
});
</script>

<style scoped>
</style>