<template>
  <div>
    <div 
      v-for="amenityType of allTypes"
      :key="amenityType"
    >
      <input
        :id="amenityType + '_radio'"
        class="amenity-type"
        type="radio"
        name="amenity_type"
        :value="amenityType"
        :checked="amenityType === currentType"
        @change="onSelected(amenityType)"
      >
      <label
        v-t="'amenity_' + amenityType"
        :for="amenityType + '_radio'"
      >
      </label>
    </div>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, PropType } from 'vue';
import { AmenityType } from '../models/amenity_type';
export default defineComponent({
    props: {
        selectedType: {
            type: String as PropType<AmenityType>,
            default: AmenityType.FoodStore
        }
    },
    emits: ['selectedTypeChanged'],
    setup(props, { emit }) {
        const currentType = computed({
            get: () => props.selectedType,
            set: (value) => emit('selectedTypeChanged', value)
        });
        return { 
            currentType,
            allTypes: Object.values(AmenityType)
        };
    },
    methods: {
        onSelected(type: AmenityType) {
            this.currentType = type;
        }
    }
});
</script>

<style scoped>
</style>