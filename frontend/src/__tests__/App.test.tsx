import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import App from "../App";
import { fetchWeather } from "../api";
import type { Weather } from "../types";

import { vi, describe, it, expect } from "vitest";

vi.mock("../api", () => ({
  fetchWeather: vi.fn(),
}));

const mockFetchWeather = fetchWeather as unknown as ReturnType<typeof vi.fn>;

describe("Weather App", () => {
  it("renders weather data on success", async () => {
    const payload: Weather = {
      city: "Lagos",
      temperature: 29.3,
      humidity: 78,
      wind_speed: 12.5,
      condition: "Partly cloudy",
    };

    mockFetchWeather.mockResolvedValueOnce(payload);

    render(<App />);

    await userEvent.type(screen.getByLabelText(/city/i), "Lagos");
    await userEvent.click(screen.getByRole("button", { name: /get weather/i }));

    expect(
      await screen.findByRole("region", { name: /weather result/i })
    ).toBeInTheDocument();
    expect(screen.getByText(/Lagos/)).toBeInTheDocument();
    expect(screen.getByText(/29.3 °C/)).toBeInTheDocument();
    expect(screen.getByText(/78%/)).toBeInTheDocument();
    expect(screen.getByText(/12.5 kph/)).toBeInTheDocument();
    expect(screen.getByText(/Partly cloudy/)).toBeInTheDocument();
  });

  it("shows an error message when backend fails", async () => {
    mockFetchWeather.mockRejectedValueOnce(new Error("City not found"));

    render(<App />);

    await userEvent.type(screen.getByLabelText(/city/i), "NowhereCity");
    await userEvent.click(screen.getByRole("button", { name: /get weather/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent(
      "City not found"
    );
  });
});
