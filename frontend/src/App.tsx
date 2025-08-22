import { useState } from "react";
import { fetchWeather } from "./api";
import type { Weather } from "./types";
import WeatherForm from "./components/WeatherForm";
import WeatherCard from "./components/WeatherCard";
import "./App.css";

export default function App() {
  const [city, setCity] = useState("");
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<Weather | null>(null);
  const [error, setError] = useState<string>("");

  const load = async () => {
    setError("");
    setData(null);
    setLoading(true);

    try {
      const res = await fetchWeather(city.trim());
      setData(res);
    } catch (e: unknown) {
      if (e instanceof Error) {
        setError(e.message);
      } else {
        setError("Failed to retrieve weather data.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Weather Viewer</h1>

      <WeatherForm
        city={city}
        setCity={setCity}
        loading={loading}
        onSubmit={load}
      />

      {error && (
        <div role="alert" className="error">
          {error}
        </div>
      )}

      {data && <WeatherCard data={data} />}
    </div>
  );
}
