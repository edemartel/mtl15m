<template>
  <div
    class="language-list"
    :aria-label="$t('language_selection')"
  >
    <div
      v-for="loc of locales"
      :key="loc.id"
    >
      <input
        :id="'loc_' + loc.id"
        type="radio"
        name="locale"
        :value="loc"
        :checked="locale === loc.id"
        @change="locale = loc.id"
      >
      <label
        :for="'loc_' + loc.id"
        :title="loc.name"
        :aria-label="loc.name"
      >      
        {{ loc.id.substring(0, 2).toLocaleUpperCase() }}
      </label>
    </div>
  </div>
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

        const locales = [{
            id:'fr-CA',
            name: 'Français'
        },
        {
            id:'en-CA',
            name: 'English'
        } ];
        return { locale, locales };
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
.language-list {
    display: flex;
    flex-direction: row;
    gap: 1ch;
}
input {
    opacity: 0;
    position: absolute;
    cursor: pointer;
}

label {
    cursor: pointer;
}

label:hover, input:hover+label {
    color: var(--color-accent);
}

input:checked+label {
    font-weight: bold;
}
</style>

