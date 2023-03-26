import { Point } from 'geojson';
import { AmenityType } from './amenity_type';

export const MAX_SCORE = 2500;
export const SCORE_INCREMENT = 500;

export type ServiceDistances = {
    [type in AmenityType]: number | undefined;
};

export interface AreaProperties {
    center: Point;
    area: number;
    population: number;
    distances: ServiceDistances;
}