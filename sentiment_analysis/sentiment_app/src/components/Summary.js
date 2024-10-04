import React from "react";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import LinearProgress from "@mui/material/LinearProgress";
import { green, red, grey } from "@mui/material/colors";
import Grid from "@mui/material/Grid2";

export default function Summary(props) {
  var colors = props.circle_ratings.map((rating) => {
    if (rating <= 40) {
      return red[700];
    } else if (rating >= 60) {
      return green[700];
    } else {
      return grey[700];
    }
  });
  const rating_header_variant = "h5";
  const bar_height = "1.5rem";
  return (
    <Grid item size={4} sx={{ textAlign: "center" }}>
      <Grid container spacing={2} direction="column">
        <Grid item>
          <Typography variant={rating_header_variant}>
            Today: {props.circle_ratings[0]}
          </Typography>
        </Grid>
        <Grid item>
          <LinearProgress
            variant="determinate"
            value={props.circle_ratings[0]}
            sx={{
              height: bar_height,
              backgroundColor: "white",
              "& .MuiLinearProgress-bar": {
                backgroundColor: colors[0],
              },
            }}
          ></LinearProgress>
        </Grid>
        <Grid item>
          <Typography variant={rating_header_variant}>
            Past 3 Days: {props.circle_ratings[1]}
          </Typography>
        </Grid>
        <Grid item>
          <LinearProgress
            variant="determinate"
            value={props.circle_ratings[1]}
            sx={{
              height: bar_height,
              backgroundColor: "white",
              "& .MuiLinearProgress-bar": {
                backgroundColor: colors[1],
              },
            }}
          ></LinearProgress>
        </Grid>
        <Grid item>
          <Typography variant={rating_header_variant}>
            Past 7 Days: {props.circle_ratings[2]}
          </Typography>
        </Grid>
        <Grid item>
          <LinearProgress
            variant="determinate"
            value={props.circle_ratings[2]}
            sx={{
              height: bar_height,
              backgroundColor: "white",
              "& .MuiLinearProgress-bar": {
                backgroundColor: colors[2],
              },
            }}
          ></LinearProgress>
        </Grid>
      </Grid>
    </Grid>
  );
}
