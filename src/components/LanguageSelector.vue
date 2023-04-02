<template>
  <a
    href="#"
    :title="otherLocale.name"
    :aria-label="otherLocale.name"
    @click="$event => { locale = otherLocale.id; $event.preventDefault();}"
  >
    {{ otherLocale.id.substring(0, 2).toLocaleUpperCase() }}
  </a>
</template>
  
<script lang="ts">
  
import { computed, defineComponent } from 'vue';
import { useI18n } from 'vue-i18n';
  
export default defineComponent({
    setup() {       
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

        return { locale };
    },
    computed: {
        otherLocale() {
            if (this.locale === 'fr-CA') {
                return {
                    id:'en-CA',
                    name: 'English'
                };
            } return {
                id:'fr-CA',
                name: 'Français'
            };
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
a {
  font-size: 0.8em;
  line-height: 0.8em;
}
</style>

