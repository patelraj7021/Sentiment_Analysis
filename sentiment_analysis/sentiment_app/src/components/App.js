import React, { Component, useState } from "react";
import Summary from "./Summary";
import SearchBar from "./SearchBar";
import Grid from "@mui/material/Grid2";
import Typography from "@mui/material/Typography";
import { Button, TextField } from "@mui/material";

export default function App() {
  const [ticker, setTicker] = useState("NVDA");

  const handleTickerChange = (e) => {
    setTicker(e.target.value);
  };

  return (
    <Grid container spacing={2} display="flex" margin="auto" direction="column">
      <SearchBar ticker={ticker} onChange={handleTickerChange} />
      <Grid container spacing={2}>
        {/* <Summary /> */}
        <Grid item margin="auto">
          <Button color="primary" variant="contained">
            Search
          </Button>
        </Grid>
      </Grid>
    </Grid>
  );
}
