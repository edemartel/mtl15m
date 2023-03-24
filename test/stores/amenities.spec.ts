import { createPinia, setActivePinia } from 'pinia';
import { beforeEach, describe, expect, it, Mock, vi } from 'vitest'
import { List } from 'immutable';
import { useAmenityStore } from '../../src/stores/amenities';
import { Amenity, AmenityType } from '../../src/models/amenity';
import axios from 'axios';

vi.mock('axios');
describe('Amenity Store', () => {
    beforeEach(() => {
        setActivePinia(createPinia());
    });

    it('should return all amenities', async () => {
        const amenities: Amenity[] = [
            {
                type: AmenityType.FoodStore,
                position: {
                    lat: 45.530045,
                    lng: -73.55924
                }
            }
        ];

        (axios.get as Mock).mockResolvedValue({
            data: amenities,
        });

        const store = useAmenityStore();
        await store.loadAmenities();

        expect(axios.get).toHaveBeenCalledWith('data/amenities.json');
        expect(store.amenities).toStrictEqual(List(amenities));
    });
});