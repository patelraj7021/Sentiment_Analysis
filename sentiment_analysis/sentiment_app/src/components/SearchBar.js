import React, { Component } from "react";
import Grid from "@mui/material/Grid2";
import { Button, TextField } from "@mui/material";

export default function SearchBar(props) {
  // const handleTickerChange = (e) => {
  //   props.setTicker(e.target.value);
  // };

  const handleAnalyzePress = () => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ticker: props.ticker,
      }),
    };
    fetch("/sentiment-app/analyze-request", requestOptions);
  };

  return (
    <Grid container spacing={2}>
      <Grid item margin="auto">
        <TextField
          id="search-input"
          label="Enter Stock Ticker"
          variant="outlined"
          onChange={props.onChange}
          defaultValue={props.ticker}
        />
      </Grid>
      <Grid item margin="auto">
        <Button
          color="primary"
          variant="contained"
          onClick={handleAnalyzePress}
        >
          Analyze
        </Button>
      </Grid>
    </Grid>
  );
}
