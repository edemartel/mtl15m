export enum AmenityType {
    Clinic = 'clinic',
    Daycare = 'daycare',
    FoodStore = 'food_store',
    Library = 'library',
    MetroStation = 'metro_station',
    Park = 'park',
    Pharmacy = 'pharmacy',
    Restaurant = 'restaurant',
    PrimarySchool = 'primary_school',
    SecondarySchool= 'secondary_school'
}

export const amenityIconClasses: { [type in AmenityType]: string } = {
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

export const defaultAmenityType = AmenityType.FoodStore;