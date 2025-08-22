import type { Weather } from "../types";

type Props = { data: Weather };

export default function WeatherCard({ data }: Props) {
  return (
    <div className="card" role="region" aria-label="Weather Result">
      <h2 className="city">{data.city}</h2>
      <div className="grid">
        <div>
          <strong>Temperature:</strong> {data.temperature} °C
        </div>
        <div>
          <strong>Humidity:</strong> {data.humidity}%
        </div>
        <div>
          <strong>Wind:</strong> {data.wind_speed} kph
        </div>
        <div>
          <strong>Condition:</strong> {data.condition}
        </div>
      </div>
    </div>
  );
}
