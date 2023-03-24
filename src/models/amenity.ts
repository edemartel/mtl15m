export enum AmenityType {
    FoodStore = "FOOD_STORE",
    School = "SCHOOL",
    Park = "PARK",
}

export interface Position {
    lat: number;
    lng: number;
}

export interface Amenity {
    type: AmenityType;
    position: Position;
}