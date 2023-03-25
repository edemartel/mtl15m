import { createPinia, setActivePinia } from 'pinia';
import { beforeEach, describe, expect, it, Mock, vi } from 'vitest';
import { useMapStore } from '../../src/stores/map';
import { Feature, FeatureCollection } from 'geojson';
import axios from 'axios';

vi.mock('axios');
describe('Amenity Store', () => {
    beforeEach(() => {
        setActivePinia(createPinia());
    });

    it('should return all amenities', async () => {
        const feature: Feature = {
            type: 'Feature',
            geometry: {
                type: 'Point',
                coordinates: [1, 2]
            },
            properties: {}
        };
        const features: FeatureCollection = {
            type: 'FeatureCollection',
            features: [feature]
        };

        (axios.get as Mock).mockResolvedValue({
            data: features,
        });

        const store = useMapStore();
        await store.loadMap();

        expect(axios.get).toHaveBeenCalledWith('data/map.json');
        expect(store.features).toStrictEqual(features);
    });
});