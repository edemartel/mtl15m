<template>
  <div class="filter-root">
    <span v-t="'filter_by'"></span>
    <div class="select-parent">
      <v-select
        v-model="currentType"
        :aria-label="$t('amenities')"
        :options="allTypes"
        :clearable="false"
        :get-option-label="translateAmenityType"
      >
      </v-select>
    </div>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, PropType } from 'vue';
import { AmenityType, defaultAmenityType } from '../models/amenity_type';
import vSelect from 'vue-select';
import { useI18n } from 'vue-i18n';

export default defineComponent({
    components: { vSelect },
    props: {
        selectedType: {
            type: String as PropType<AmenityType>,
            default: defaultAmenityType
        }
    },
    emits: ['selectedTypeChanged'],
    setup(props, { emit }) {
        const currentType = computed({
            get: () => props.selectedType,
            set: (value) => emit('selectedTypeChanged', value)
        });
        const i18n = useI18n();
        return { 
            currentType,
            i18n,
            allTypes: Object.values(AmenityType)
        };
    },
    methods: {
        translateAmenityType(type: AmenityType) {
            return this.i18n.t('amenity_' + type);
        }
    }
});
</script>

<style scoped>
.filter-root {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 1ch;
}

.select-parent {
  pointer-events: auto;
  --vs-font-size: var(--default-font-size);
  --vs-selected-color: var(--color-text);
  --vs-border-color: var(--color-border);
  --vs-dropdown-max-height: 750%;
  flex: 1;
}
</style>
<style>  /* global */
.v-select .vs__selected-options {
  flex-wrap: nowrap;
  overflow: hidden;
  white-space: nowrap;
}
.v-select .vs__dropdown-toggle {
  height: 100%;
}
.v-select .vs__dropdown-menu {
    background-color: var(--color-background);
}
</style>
