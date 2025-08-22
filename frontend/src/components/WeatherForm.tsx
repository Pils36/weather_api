import type { FormEvent } from "react";

type Props = {
  city: string;
  setCity: (v: string) => void;
  loading: boolean;
  onSubmit: () => void;
};

export default function WeatherForm({
  city,
  setCity,
  loading,
  onSubmit,
}: Props) {
  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    onSubmit();
  };

  return (
    <form onSubmit={handleSubmit} className="form">
      <input
        aria-label="City"
        placeholder="Enter a city e.g. Lagos"
        value={city}
        onChange={(e) => setCity(e.target.value)}
        className="input"
      />
      <button
        className="button"
        type="submit"
        disabled={loading || !city.trim()}
      >
        {loading ? "Loading..." : "Get Weather"}
      </button>
    </form>
  );
}
