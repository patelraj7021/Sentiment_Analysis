import React, { Component } from "react";
import Grid from "@mui/material/Grid2";
import { Button, TextField } from "@mui/material";

export default class SearchBar extends Component {
  defaultTicker = "NVDA";
  constructor(props) {
    super(props);
    this.state = {
      ticker: this.defaultTicker,
    };
    this.handleAnalyzePress = this.handleAnalyzePress.bind(this);
    this.handleTickerChange = this.handleTickerChange.bind(this);
  }

  handleTickerChange(e) {
    this.setState({
      ticker: e.target.value,
    });
  }

  handleAnalyzePress() {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ticker: this.state.ticker,
      }),
    };
    fetch("/sentiment_app/analyze-request", requestOptions);
    // .then((response) => response.json())
    // .then((data) => console.log(data));
  }

  render() {
    return (
      <Grid container spacing={2}>
        <Grid item margin="auto">
          <TextField
            id="search-input"
            label="Enter Stock Ticker"
            variant="outlined"
            onChange={this.handleTickerChange}
            defaultValue={this.defaultTicker}
          />
        </Grid>
        <Grid item margin="auto">
          <Button
            color="primary"
            variant="contained"
            onClick={this.handleAnalyzePress}
          >
            Analyze
          </Button>
        </Grid>
      </Grid>
    );
  }
}
