import React, { Component } from "react";
import Grid from "@mui/material/Grid2";
import CircularProgress from "@mui/material/CircularProgress";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";

export default function Summary(props) {
  return (
    <Box sx={{ position: "relative", display: "inline-flex" }}>
      <CircularProgress
        value={props.overall_rating}
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
        <Typography variant="h3">{props.overall_rating}</Typography>
      </Box>
    </Box>
  );
}
