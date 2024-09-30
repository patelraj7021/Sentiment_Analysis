import React, { Component, useState } from "react";
import Summary from "./Summary";
import SearchBar from "./SearchBar";
import Grid from "@mui/material/Grid2";
import Typography from "@mui/material/Typography";
import { Button, TextField } from "@mui/material";

export default function App() {
  const [ticker, setTicker] = useState("NVDA");
  const [overall_rating, setOverallRating] = useState(50);

  const handleTickerChange = (e) => {
    setTicker(e.target.value);
  };

  const handleAnalyzePress = () => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ticker: ticker,
      }),
    };
    fetch("/sentiment-app/analyze-request", requestOptions)
      .then((response) => response.json())
      .then((data) => setOverallRating(data.overall_rating));
  };

  return (
    <Grid container spacing={2} display="flex" margin="auto" direction="column">
      <SearchBar
        ticker={ticker}
        onChange={handleTickerChange}
        onClick={handleAnalyzePress}
      />
      <Grid container spacing={2}>
        <Summary overall_rating={overall_rating} />
        <Grid item margin="auto">
          <Button color="primary" variant="contained">
            Search
          </Button>
        </Grid>
      </Grid>
    </Grid>
  );
}
