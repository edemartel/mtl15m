<template>
  <main>
    <TypeFilter
      id="filter"
      @selected-type-changed="onSelectedTypeChanged"
    ></TypeFilter>
    <MapView
      id="map"
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
import { computed, defineComponent, ref } from 'vue';
import MapView from './components/MapView.vue';
import LoadingSpinner from './components/LoadingSpinner.vue';
import { useI18n } from 'vue-i18n';
import { useMapStore } from './stores/map';
import { AmenityType } from './models/amenity_type';
import TypeFilter from './components/TypeFilter.vue';

export default defineComponent({
    components: { MapView, LoadingSpinner, TypeFilter },
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

        const i18n = useI18n();

        const locale = computed<string>({
            get() {
                return i18n.locale.value;
            },
            set(value) {
                localStorage.setItem('locale', value);
                i18n.locale.value = value;
            }
        });

        const desiredLocale = getDesiredLocale();
        if (desiredLocale) {
            i18n.locale.value = desiredLocale;
        }

        return {
            selectedType: ref(AmenityType.FoodStore),
            locale,
            loadingCompleted
        };
    },
    methods: {
        onSelectedTypeChanged(type: AmenityType) {
            this.selectedType = type;
        }
    }
});

function getDesiredLocale() {
    let locale = localStorage.getItem('locale');
    if (!locale) {
        for (const language of navigator.languages) {
            const index = language.indexOf('-');
            const lang = (index === -1 ? language : language.substring(0, index)).toLowerCase();
            if (lang === 'fr' || lang === 'en') {
                locale = `${lang}-CA`;
                localStorage.setItem('locale', locale);
                break;
            }
        }
    }
    return locale;
}
</script>

<style scoped>
main {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: row;
    gap: 1em;
}
#map {
    flex: 1;
}
#filter {
    padding: 0.5em;
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
</style>
