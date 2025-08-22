export type Weather = {
    city: string;
    temperature: number;
    humidity: number;
    wind_speed: number;
    condition: string;
};

export type ApiError = { detail: string };
