import React from "react";
import Grid from "@mui/material/Grid2";
import { Button, TextField } from "@mui/material";

export default function SearchBar(props) {
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
        <Button color="primary" variant="contained" onClick={props.onClick}>
          Analyze
        </Button>
      </Grid>
    </Grid>
  );
}
