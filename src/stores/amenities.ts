import { defineStore } from 'pinia';
import { List } from 'immutable';
import { Amenity } from '../models/amenity';
import axios from 'axios';

export const useAmenityStore = defineStore('amenities', {
    state: () => ({
        amenities: List<Amenity>()
    }),
    actions: {
        async loadAmenities() {
            const response = await axios.get<Amenity[]>('data/amenities.json');
            this.amenities = List(response.data);
        }
    }
});