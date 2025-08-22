import type { Weather, ApiError } from "./types";

// ✅ Use Vite's import.meta.env instead of process.env
const BASE = import.meta.env.VITE_API_BASE_URL || "http://backend:8000";

export async function fetchWeather(city: string): Promise<Weather> {
    const url = `${BASE}/weather?city=${encodeURIComponent(city)}`;

    try {
        const res = await fetch(url, { headers: { Accept: "application/json" } });

        if (!res.ok) {
            let message = "Failed to retrieve weather data.";
            try {
                const err = (await res.json()) as ApiError;
                if (err?.detail) message = err.detail;
            } catch {
                // Ignore JSON parse errors, fallback to default message
            }
            throw new Error(message);
        }

        return (await res.json()) as Weather;
    } catch (error) {
        // ✅ Handle network errors or backend unavailability
        throw new Error("Unable to connect to the weather service. Please try again later.");
    }
}
