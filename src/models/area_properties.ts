import { Point } from 'geojson';
import { AmenityType } from './amenity_type';

export const MAX_DISTANCE = 2500;
export const WALKING_SPEED = 83.333; // in metres per minute
export const MAX_TIME = 30;

export type ServiceDistances = {
    [type in AmenityType]: { pt: Point, dist: number } | undefined;
};

export interface AreaProperties {
    center: Point;
    area: number;
    population: number;
    distances: ServiceDistances;
}