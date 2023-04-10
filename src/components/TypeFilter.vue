<template>
  <div class="select-parent">
    <v-select
      v-model="currentType"
      :aria-label="$t('amenities')"
      :options="allTypes"
      :clearable="false"
      :get-option-label="translateAmenityType"
    >
      <template #option="{ label }">
        <div class="amenity-row">
          <i
            class="fa-solid"
            :class="['fa-' + amenityIconClasses[label as AmenityType]]"
          ></i>
          <span v-t="'amenity_' + label"></span>
        </div>
      </template>
      <template #selected-option="{ label }">
        <div class="amenity-row">
          <i
            class="fa-solid"
            :class="['fa-' + amenityIconClasses[label as AmenityType]]"
          ></i>
          <span v-t="'amenity_' + label"></span>
        </div>
      </template>
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
            allTypes: Object.values(AmenityType),
            amenityIconClasses
        };
    },
    methods: {
        translateAmenityType(type: AmenityType) {
            return this.i18n.t('amenity_' + type);
        }
    }
});

const amenityIconClasses: { [type in AmenityType]: string } = {
    [AmenityType.Clinic]: 'house-medical',
    [AmenityType.Daycare]: 'child-reaching',
    [AmenityType.FoodStore]: 'carrot',
    [AmenityType.Library]: 'book',
    [AmenityType.MetroStation]: 'train-subway',
    [AmenityType.Park]: 'tree',
    [AmenityType.Pharmacy]: 'pills',
    [AmenityType.Restaurant]: 'mug-saucer',
    [AmenityType.PrimarySchool]: 'school',
    [AmenityType.SecondarySchool]: 'graduation-cap'
};

</script>

<style scoped>
.select-parent {
  pointer-events: auto;
  --vs-font-size: var(--default-font-size);
  --vs-selected-color: var(--color-text);
  --vs-border-color: var(--color-border);
  --vs-dropdown-max-height: 750%;
  flex: 1;
}
.amenity-row {
  display: flex;
  flex-direction: row;
  align-items: baseline;
  gap: var(--sz-100);
}

.amenity-row i {
  width: var(--sz-100);
  text-align: center;
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
  padding-left: var(--sz-30);
}
.v-select .vs__dropdown-menu {
    background-color: var(--color-background);
}
.v-select .vs__dropdown-option--highlight {
  background-color: var(--color-highlight);
}
</style>
