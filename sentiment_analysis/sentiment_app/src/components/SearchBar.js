import React from "react";
import Grid from "@mui/material/Grid2";
import { Button, TextField } from "@mui/material";
import CircularProgress from "@mui/material/CircularProgress";
import { green } from "@mui/material/colors";
import LoadingButton from "@mui/lab/LoadingButton";

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
        <LoadingButton
          color="primary"
          variant="contained"
          onClick={props.onClick}
          loading={props.loading}
          loadingIndicator="Analyzing..."
          size="large"
        >
          Analyze
        </LoadingButton>
      </Grid>
    </Grid>
  );
}
