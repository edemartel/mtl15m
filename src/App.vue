<template>
  <Map></Map>
  <div v-if="!loadingCompleted" class="loading-overlay">
    <LoadingSpinner role="status"></LoadingSpinner>
    <p class="loading-message">Chargement des données...</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import Map from './components/Map.vue'
import { useAmenityStore } from './stores/amenities';
import LoadingSpinner from "./components/LoadingSpinner.vue";

export default defineComponent({
  components: { Map, LoadingSpinner },
  setup() {
    const loadingCompleted = ref<boolean>(false);

    const store = useAmenityStore();

    const storeLoads = Promise.allSettled([
      store.loadAmenities()
    ]);
    storeLoads.then(promises => {
      loadingCompleted.value = true;
      for (const promise of promises) {
        if (promise.status === 'rejected') {
          // TODO: log to Sentry
        }
      }
    });

    return {
      loadingCompleted
    }
  }
});
</script>

<style scoped>
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  z-index: 1000;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>
