import React, { Component } from "react";
import { render } from "react-dom";
import Summary from "./Summary";
import SearchBar from "./SearchBar";
import Grid from "@mui/material/Grid2";
import Typography from "@mui/material/Typography";
import { Button, TextField } from "@mui/material";

export default class App extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <Grid
        container
        spacing={2}
        display="flex"
        margin="auto"
        direction="column"
      >
        <SearchBar />
        <Grid container spacing={2}>
          <Grid item margin="auto">
            <TextField
              id="search-input"
              label="Enter Stock Ticker"
              variant="outlined"
            />
          </Grid>
          <Grid item margin="auto">
            <Button color="primary" variant="contained">
              Search
            </Button>
          </Grid>
        </Grid>
      </Grid>
    );
  }
}

const appDiv = document.getElementById("app");
render(<App />, appDiv);
