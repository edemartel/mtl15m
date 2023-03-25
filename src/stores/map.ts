import { defineStore } from 'pinia';
import { FeatureCollection } from 'geojson';
import axios from 'axios';

export const useMapStore = defineStore('map', {
    state: () => ({
        features: {
            type: 'FeatureCollection',
            features: []
        } as FeatureCollection
    }),
    actions: {
        async loadMap() {
            const response = await axios.get<FeatureCollection>('data/map.json');
            this.features = response.data;
        }
    }
});