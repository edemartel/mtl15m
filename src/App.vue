<template>
  <MapView></MapView>
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

export default defineComponent({
    components: { MapView, LoadingSpinner },
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
            locale,
            loadingCompleted
        };
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
