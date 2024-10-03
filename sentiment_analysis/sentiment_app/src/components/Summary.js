import React from "react";
import CircularProgress from "@mui/material/CircularProgress";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import { Gauge, gaugeClasses } from "@mui/x-charts";
import LinearProgress from "@mui/material/LinearProgress";
import { green, red, grey } from "@mui/material/colors";

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
  return (
    <Box position="absolute" height="100%" width="22.5%" left="2.5%">
      <Box
        position="absolute"
        height="30%"
        width="100%"
        alignContent="center"
        textAlign="center"
      >
        <Typography variant="h5" height="30%">
          Today: {props.circle_ratings[0]}
        </Typography>
        <LinearProgress
          variant="determinate"
          value={props.circle_ratings[0]}
          sx={{
            height: 1 / 3,
            backgroundColor: "white",
            "& .MuiLinearProgress-bar": {
              backgroundColor: colors[0],
            },
          }}
        ></LinearProgress>
      </Box>
      <Box
        position="absolute"
        top="30%"
        height="30%"
        width="100%"
        alignContent="center"
        textAlign="center"
      >
        <Typography variant="h5" height="30%">
          Past 3 Days: {props.circle_ratings[1]}
        </Typography>
        <LinearProgress
          variant="determinate"
          value={props.circle_ratings[1]}
          sx={{
            height: 1 / 3,
            backgroundColor: "white",
            "& .MuiLinearProgress-bar": {
              backgroundColor: colors[1],
            },
          }}
        ></LinearProgress>
      </Box>
      <Box
        position="absolute"
        top="60%"
        height="30%"
        width="100%"
        alignContent="center"
        textAlign="center"
      >
        <Typography variant="h5" height="30%">
          Past 7 Days: {props.circle_ratings[2]}
        </Typography>
        <LinearProgress
          variant="determinate"
          value={props.circle_ratings[2]}
          sx={{
            height: 1 / 3,
            backgroundColor: "white",
            "& .MuiLinearProgress-bar": {
              backgroundColor: colors[2],
            },
          }}
        ></LinearProgress>
      </Box>
    </Box>
  );

  {
    /* <CircularProgress
        value={props.circle_ratings[1]}
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
        <Typography variant="h3">{props.circle_ratings[1]}</Typography>
      </Box> */
  }
  // );
}
