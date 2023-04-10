<template>
  <header>
    <h1
      class="logo"
      :aria-label="$t('logo')"
    >
      <i class="fa-solid fa-person-walking"></i>
      mtl15m
    </h1>
    <div class="type-filter-parent">
      <TypeFilter
        class="type-filter"
        :selected-type="selectedType"
        @selected-type-changed="onSelectedTypeChanged"
      ></TypeFilter>
    </div>
    <div>
      <AboutWindow></AboutWindow>
    </div>
    <LanguageSelector></LanguageSelector>
  </header>
  <main>
    <MapView
      :selected-type="selectedType"
    ></MapView>
  </main>
  <div
    v-if="!loadingCompleted"
    class="loading-overlay"
  >
    <LoadingSpinner role="status"></LoadingSpinner>
    <p
      v-t="'loading'"
      class="loading-message"
    ></p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import MapView from './components/MapView.vue';
import LoadingSpinner from './components/LoadingSpinner.vue';
import { useMapStore } from './stores/map';
import { AmenityType, defaultAmenityType } from './models/amenity_type';
import TypeFilter from './components/TypeFilter.vue';
import LanguageSelector from './components/LanguageSelector.vue';
import AboutWindow from './components/AboutWindow.vue';

export default defineComponent({
    components: { MapView, LoadingSpinner, TypeFilter, LanguageSelector, AboutWindow },
    setup() {
        const loadingCompleted = ref<boolean>(false);

        const mapStore = useMapStore();

        const storeLoads = Promise.allSettled([
            mapStore.loadMap()
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
            selectedType: ref(defaultAmenityType),
            loadingCompleted
        };
    },
    methods: {
        onSelectedTypeChanged(type: AmenityType) {
            this.selectedType = type;
        }
    }
});

</script>

<style scoped>
main {
    width: 100%;
    height: 100%;
    flex: 1;
}
header {
    display: flex;
    padding: var(--sz-10);
    padding-left: var(--sz-200);
    padding-right: var(--sz-200);
    align-items: center;
    gap: var(--sz-200);
}
.logo {
    display: inline;
    font-size: 24px;
    margin: 0;
    white-space: nowrap;
}
.type-filter-parent {
  flex: 1;
}
.type-filter {
  max-width: 200px;
  margin-right: var(--sz-30);
}

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

@media only screen and (min-width: 600px) {
  .type-filter {
    max-width: 250px;
  }
}

@media only screen and (min-width: 900px) {
  .type-filter {
    max-width: 300px;
  }
}

@media only screen and (min-width: 1200px) {
  .type-filter {
    max-width: 400px;
  }
}

</style>
