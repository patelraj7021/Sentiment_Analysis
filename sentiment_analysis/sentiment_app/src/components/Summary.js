import React, { Component } from "react";
import Grid from "@mui/material/Grid2";
import CircularProgress from "@mui/material/CircularProgress";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";

export default class Summary extends Component {
  constructor(props) {
    super(props);
  }

  updateSummary() {
    fetch("/sentiment-app/update-summary")
      .then((response) => response.json())
      .then((data) => this.setState({ rating: data.overall_rating }));
  }

  render() {
    return (
      <Box sx={{ position: "relative", display: "inline-flex" }}>
        <CircularProgress
          value={this.state.rating}
          variant="determinate"
          size="16rem"
        />
        <Box
          sx={{
            top: 0,
            left: 0,
            bottom: 0,
            right: 0,
            position: "absolute",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <Typography variant="h3">{this.state.rating}</Typography>
        </Box>
      </Box>
    );
  }
}
