<template>
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
.select-parent {
  pointer-events: auto;
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
</style>
